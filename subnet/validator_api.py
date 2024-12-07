import asyncio
import concurrent.futures
import json
import re
import time
import random
from functools import partial
from datetime import timedelta, datetime, date
from collections import defaultdict

from communex.client import CommuneClient  # type: ignore
from communex.module.client import ModuleClient  # type: ignore
from communex.module.module import Module  # type: ignore
from communex.types import Ss58Address  # type: ignore
from substrateinterface import Keypair  # type: ignore

from utils.log import log, Logger
from utils.protocols import (
    class_dict, 
    CurrentPoolMetricSynapse, 
    CurrentTokenMetricSynapse,
    TokenMetricSynapse,
    PoolMetricAPISynapse,
    RecentPoolEventSynapse
)
from utils.get_ip_port import get_ip_port

class VeloraValidatorAPI(Module):
    def __init__(
        self,
        key: Keypair,
        netuid: int,
        client: CommuneClient,
        call_timeout: int = 60,
    ) -> None:
        super().__init__()
        self.client = client
        self.key = key
        self.netuid = netuid
        self.val_model = "foo"
        self.call_timeout = call_timeout
        self.logger = Logger("VeloraValidatorAPI")
        
    def get_addresses(self, client: CommuneClient, netuid: int) -> dict[int, str]:
        """
        Retrieve all module addresses from the subnet.

        Args:
            client: The CommuneClient instance used to query the subnet.
            netuid: The unique identifier of the subnet.

        Returns:
            A dictionary mapping module IDs to their addresses.
        """

        # Makes a blockchain query for the miner addresses
        module_addreses = client.query_map_address(netuid)
        return module_addreses
    
    def retrieve_miner_information(self, velora_netuid):
        modules_adresses = self.get_addresses(self.client, velora_netuid)
        modules_keys = self.client.query_map_key(velora_netuid)
        val_ss58 = self.key.ss58_address
        if val_ss58 not in modules_keys.values():
            raise RuntimeError(f"validator key {val_ss58} is not registered in subnet")

        modules_info: dict[int, tuple[list[str], Ss58Address]] = {}

        modules_filtered_address = get_ip_port(modules_adresses)
        for module_id in modules_keys.keys():
            module_addr = modules_filtered_address.get(module_id, None)
            if not module_addr:
                continue
            modules_info[module_id] = (module_addr, modules_keys[module_id])
        return modules_info
    
    def _get_miner_prediction(
        self,
        synapse,
        miner_info: tuple[list[str], Ss58Address],
    ) -> str | None:
        """
        Prompt a miner module to generate an answer to the given question.

        Args:
            question: The question to ask the miner module.
            miner_info: A tuple containing the miner's connection information and key.

        Returns:
            The generated answer from the miner module, or None if the miner fails to generate an answer.
        """
        connection, miner_key = miner_info
        module_ip, module_port = connection
        client = ModuleClient(module_ip, int(module_port), self.key)
        try:
            # handles the communication with the miner
            current_time = datetime.now()
            miner_answer = dict()
            response = asyncio.run(
                client.call(
                    f'forward{synapse.class_name}',
                    miner_key,
                    {"synapse": synapse.dict()},
                    timeout=self.call_timeout,  #  type: ignore
                )
            )
            response = json.loads(response)
            # print(f'Response from miner: {response}')
            miner_answer['data'] = class_dict[response['class_name']](**response)
            process_time = datetime.now() - current_time
            miner_answer["process_time"] = process_time

        except Exception as e:
            log(f"Miner {module_ip}:{module_port} failed to generate an answer")
            print(e)
            miner_answer = None
        return miner_answer
    
    def get_miner_answer(self, modules_info, synapses):
        if not isinstance(synapses, list):
            synapses = [synapses] * len(modules_info)
        log(f"Selected the following miners: {modules_info.keys()}")

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            it = executor.map(lambda x: self._get_miner_prediction(x[0], x[1]), list(zip(synapses, modules_info.values())))
            answers = [*it]
            
        if not answers:
            log("No miner managed to give an answer")
            return None
        
        # print(f'miner answers: {answers}')
        
        return answers
    
    def get_top_miners(self, k = 5) -> dict[int, tuple[list[str], Ss58Address]]:
        miner_weights = self.client.query_map_weights(netuid=self.netuid)
        
        # Dictionary to store the sum of weights for each miner_uid
        miner_weight_sums = defaultdict(int)
        
        # Sum weights for each miner_uid
        for validator_uid, miner_data in miner_weights.items():
            for miner_uid, miner_weight in miner_data:
                miner_weight_sums[miner_uid] += miner_weight

        # Sort miners by total weight in descending order and pick top k
        top_k_miners = sorted(miner_weight_sums.items(), key=lambda x: x[1], reverse=True)[:k]
        
        miner_uids = [miner_uid for miner_uid, _ in top_k_miners]
        module_infos = self.retrieve_miner_information(self.netuid)
        top_miners = {miner_uid: module_infos[miner_uid] for miner_uid in miner_uids if miner_uid in module_infos}
        return top_miners
    
    def getCurrentPoolMetric(self, req):
        modules_info = self.get_top_miners()
        page_limit = req.query_params.get('page_limit', 10) if int(req.query_params.get('page_limit', '10')) < 100 else 100
        page_number = req.query_params.get('page_number', 1)
        search_query = req.query_params.get('search_query', '')
        sort_by = req.query_params.get('sort_by', '')
        fee_tier = req.query_params.get('fee_tier', 0)
        liquidity_threshold = req.query_params.get('liquidity_threshold', 0.0)
        volume_threshold = req.query_params.get('volume_threshold', 0.0)
        sort_order = req.query_params.get('sort_order', 'desc')
        synapse = CurrentPoolMetricSynapse(page_limit=page_limit, page_number=page_number, search_query=search_query, fee_tier=fee_tier, liquidity_threshold=liquidity_threshold, volume_threshold=volume_threshold, sort_by=sort_by, sort_order=sort_order)
        miner_answers = self.get_miner_answer(modules_info, synapse)
        miner_answers = [answer for answer in miner_answers if answer is not None]
        if not miner_answers:
            self.logger.log_info("No miner managed to give an answer")
            return None
        response = random.choice(miner_answers)
        if not response:
            self.logger.log_info("No miner managed to give an answer")
            return None
        self.logger.log_info(f"Current pool metric response: {response['data'].dict().get('data')}")
        return {"pools": response['data'].dict().get('data'), "total_pool_count": response['data'].dict().get('total_pool_count')}
        
        
    
    def getCurrentTokenMetric(self, req):
        modules_info = self.get_top_miners()
        
        page_limit = req.query_params.get('page_limit', 10) if int(req.query_params.get('page_limit', '10')) < 100 else 100
        page_number = req.query_params.get('page_number', 1)
        search_query = req.query_params.get('search_query', '')
        sort_by = req.query_params.get('sort_by', 'volume')
        
        synapse = CurrentTokenMetricSynapse(page_limit=page_limit, page_number=page_number, search_query=search_query, sort_by=sort_by)
        miner_answers = self.get_miner_answer(modules_info, synapse)
        miner_answers = [answer for answer in miner_answers if answer is not None]
        if not miner_answers:
            self.logger.log_info("No miner managed to give an answer")
            return None
        response = random.choice(miner_answers)
        if not response:
            self.logger.log_info("No miner managed to give an answer")
            return None
        return {"tokens": response['data'].dict().get('data'), "total_token_count": response['data'].dict().get('total_token_count')}
    
    def getTokenMetric(self):
        modules_info = self.get_top_miners()
        synapse = TokenMetricSynapse()
        miner_answers = self.get_miner_answer(modules_info, synapse)
        return random.choice(miner_answers)
    
    def getPoolMetric(self, req):
        modules_info = self.get_top_miners()
        
        page_limit = req.query_params.get('page_limit', 10) if int(req.query_params.get('page_limit', '10')) < 100 else 100
        page_number = req.query_params.get('page_number', 1)
        pool_address = req.query_params.get('pool_address', '')
        start_timestamp = req.query_params.get('start_timestamp', int(time.time()) - 86400)
        end_timestamp = req.query_params.get('end_timestamp', int(time.time()))
        
        synapse = PoolMetricAPISynapse(page_limit=page_limit, page_number=page_number, pool_address=pool_address, start_timestamp=start_timestamp, end_timestamp=end_timestamp)
        
        miner_answers = self.get_miner_answer(modules_info, synapse)
        miner_answers = [answer for answer in miner_answers if answer is not None]
        
        if not miner_answers:
            self.logger.log_info("No miner managed to give an answer")
            return None
        response = random.choice(miner_answers)
        if not response:
            self.logger.log_info("No miner managed to give an answer")
            return None
        return {"pools": response['data'].dict().get('data'), "token_pair_data": response['data'].dict().get('token_pair_data'), "total_pool_count": response['data'].dict().get('total_pool_count')}
    
    def getRecentPoolEvent(self, req):
        page_limit = req.query_params.get('page_limit', 10) if int(req.query_params.get('page_limit', '10')) < 100 else 100
        filter_by = req.query_params.get('filter_by', 'all')
        modules_info = self.get_top_miners()
        synapse = RecentPoolEventSynapse(filter_by=filter_by)
        miner_answers = self.get_miner_answer(modules_info, synapse)
        miner_answers = [answer for answer in miner_answers if answer is not None]
        response = random.choice(miner_answers)
        if not response:
            return None
        return response["data"].dict().get("data")
