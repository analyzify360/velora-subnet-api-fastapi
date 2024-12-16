from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class HealthCheckSynapse(BaseModel):
    class_name: str = 'HealthCheckSynapse'

class HealthCheckResponse(BaseModel):
    class_name: str = 'HealthCheckResponse'
    time_completed: int
    pool_addresses: list[str]
    
class PoolEventSynapse(BaseModel):
    class_name: str = 'PoolEventSynapse'
    pool_address: str
    start_datetime: int
    end_datetime: int

class PoolEventResponse(BaseModel):
    class_name: str = 'PoolEventResponse'
    data: list[dict]
    overall_data_hash: str

class PoolMetricAPISynapse(BaseModel):
    class_name: str = 'PoolMetricAPISynapse'
    pool_address: str
    interval: str
    period: str
    start_timestamp: Optional[int]
    end_timestamp: Optional[int]
    page_limit: int
    page_number: int
    
class PoolMetricAPI(BaseModel):
    timestamp: int
    price: float
    liquidity_token0: float
    liquidity_token1: float
    volume_token0: float
    volume_token1: float

class TokenPairData(BaseModel):
    token0_price: float
    token1_price: float
    token0_symbol: str
    token1_symbol: str
    token0_address: str
    token1_address: str
    fee: int
    pool_address: str   


class PoolMetricAPIResponse(BaseModel):
    class_name: str = 'PoolMetricAPIResponse'
    data: list[PoolMetricAPI]
    token_pair_data: TokenPairData
    total_pool_count: int
    
class TokenMetricSynapse(BaseModel):
    class_name: str = 'TokenMetricSynapse'
class TokenMetricResponse(BaseModel):
    class_name: str = 'TokenMetricResponse'

class TokenMetricAPISynapse(BaseModel):
    class_name: str = 'TokenMetricAPISynapse'
    token_address: str
    interval: str
    period: str
    start_timestamp: Optional[int]
    end_timestamp: Optional[int]
    page_limit: int
    page_number: int

class TokenMetricAPI(BaseModel):
    timestamp: int
    close_price: float
    high_price: float
    low_price: float
    total_volume: float
    total_liquidity: float
    
class TokenData(BaseModel):
    token_address: str
    symbol: str
    decimals: int
class TokenMetricAPIResponse(BaseModel):
    class_name: str = 'TokenMetricAPIResponse'
    data: list[TokenMetricAPI]
    token_data: TokenData
    total_token_count: int

class CurrentPoolMetric(BaseModel):
    pool_address: str
    liquidity_token0: float
    liquidity_token1: float
    total_volume_token0: float
    total_volume_token1: float
    volume_token0_1day: float
    volume_token1_1day: float
    token0_symbol: str
    token1_symbol: str
    fee: int
    token0_price: float
    token1_price: float
    
class CurrentPoolMetricSynapse(BaseModel):
    class_name: str = 'CurrentPoolMetricSynapse'
    page_limit: int
    page_number: int
    fee_tier: int
    liquidity_threshold: float
    volume_threshold: float
    search_query: str
    sort_by: str
    sort_order: str

class CurrentPoolMetricResponse(BaseModel):
    class_name: str = 'CurrentPoolMetricResponse'
    data: list[CurrentPoolMetric]
    overall_data_hash: str
    total_pool_count: int

class PoolEvent(BaseModel):
    timestamp: int
    pool_address: str
    token0_symbol: str
    token1_symbol: str
    amount0: float
    amount1: float
    event_type: str
    transaction_hash: str
    
class RecentPoolEventSynapse(BaseModel):
    class_name: str = 'RecentPoolEventSynapse'
    page_limit: int = 10
    filter_by: str = 'all'
    
class RecentPoolEventResponse(BaseModel):
    class_name: str = 'RecentPoolEventResponse'
    data: list[PoolEvent]
    overall_data_hash: str

class CurrentTokenMetricSynapse(BaseModel):
    class_name: str = 'CurrentTokenMetricSynapse'
    page_limit: int
    page_number: int
    search_query: str
    sort_by: str

class CurrentTokenMetric(BaseModel):
    token_address: str
    symbol: str
    price: float
    total_volume: float
    total_liquidity: float
    
class CurrentTokenMetricResponse(BaseModel):
    class_name: str = 'CurrentTokenMetricResponse'
    data: list[CurrentTokenMetric]
    total_token_count: int

class PredictionSynapse(BaseModel):
    class_name: str = 'PredictionSynapse'
    timestamp: int
    
class PredictionResponse(BaseModel):
    class_name: str = 'PredictionResponse'
    prices: list[float]

class SwapEventAPISynapse(BaseModel):
    class_name: str = 'SwapEventAPISynapse'
    pool_address: str
    start_timestamp: int
    end_timestamp: int
    page_limit: Optional[int]
    page_number: Optional[int]

class SwapEventAPIResponse(BaseModel):
    class_name: str = 'SwapEventAPIResponse'
    data: list[dict]
    total_event_count: int

class MintEventAPISynapse(BaseModel):
    class_name: str = 'MintEventAPISynapse'
    pool_address: str
    start_timestamp: int
    end_timestamp: int
    page_limit: Optional[int]
    page_number: Optional[int]

class MintEventAPIResponse(BaseModel):
    class_name: str = 'MintEventAPIResponse'
    data: list[dict]
    total_event_count: int

class BurnEventAPISynapse(BaseModel):
    class_name: str = 'BurnEventAPISynapse'
    pool_address: str
    start_timestamp: int
    end_timestamp: int
    page_limit: Optional[int]
    page_number: Optional[int]

class BurnEventAPIResponse(BaseModel):
    class_name: str = 'BurnEventAPIResponse'
    data: list[dict]
    total_event_count: int


class_dict = {
    'HealthCheckSynapse': HealthCheckSynapse,
    'HealthCheckResponse': HealthCheckResponse,
    'PoolEventSynapse': PoolEventSynapse,
    'PoolEventResponse': PoolEventResponse,
    'SwapEventAPISynapse': SwapEventAPISynapse,
    'SwapEventAPIResponse': SwapEventAPIResponse,
    'MintEventAPISynapse': MintEventAPISynapse,
    'MintEventAPIResponse': MintEventAPIResponse,
    'BurnEventAPISynapse': BurnEventAPISynapse,
    'BurnEventAPIResponse': BurnEventAPIResponse,
    'PoolMetricAPISynapse': PoolMetricAPISynapse,
    'PoolMetricAPIResponse' : PoolMetricAPIResponse,
    'TokenMetricSynapse': TokenMetricSynapse,
    'TokenMetricResponse' : TokenMetricResponse,
    'TokenMetricAPISynapse': TokenMetricAPISynapse,
    'TokenMetricAPIResponse' : TokenMetricAPIResponse,
    'CurrentPoolMetricSynapse': CurrentPoolMetricSynapse,
    'CurrentPoolMetricResponse' : CurrentPoolMetricResponse,
    'CurrentTokenMetricSynapse': CurrentTokenMetricSynapse,
    'CurrentTokenMetricResponse' : CurrentTokenMetricResponse,
    'PredictionSynapse': PredictionSynapse,
    'PredictionResponse': PredictionResponse,
    'RecentPoolEventSynapse': RecentPoolEventSynapse,
    'RecentPoolEventResponse': RecentPoolEventResponse
}