from datetime import datetime
from pydantic import BaseModel

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

class PoolMetricSynapse(BaseModel):
    class_name: str = 'PoolMetricSynapse'

class PoolMetricResponse(BaseModel):
    class_name: str = 'PoolMetricResponse'

class TokenMetricSynapse(BaseModel):
    class_name: str = 'TokenMetricSynapse'

class TokenMetricResponse(BaseModel):
    class_name: str = 'TokenMetricResponse'

class CurrentPoolMetric(BaseModel):
    pool_address: str
    liquidity_token0: float
    liquidity_token1: float
    volume_token0: float
    volume_token1: float
    token0_symbol: str
    token1_symbol: str
    fee: int
    
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

class_dict = {
    'HealthCheckSynapse': HealthCheckSynapse,
    'HealthCheckResponse': HealthCheckResponse,
    'PoolEventSynapse': PoolEventSynapse,
    'PoolEventResponse': PoolEventResponse,
    'PoolMetricSynapse': PoolMetricSynapse,
    'PoolMetricResponse' : PoolMetricResponse,
    'TokenMetricSynapse': TokenMetricSynapse,
    'TokenMetricResponse' : TokenMetricResponse,
    'CurrentPoolMetricSynapse': CurrentPoolMetricSynapse,
    'CurrentPoolMetricResponse' : CurrentPoolMetricResponse,
    'CurrentTokenMetricSynapse': CurrentTokenMetricSynapse,
    'CurrentTokenMetricResponse' : CurrentTokenMetricResponse,
    'PredictionSynapse': PredictionSynapse,
    'PredictionResponse': PredictionResponse,
    'RecentPoolEventSynapse': RecentPoolEventSynapse,
    'RecentPoolEventResponse': RecentPoolEventResponse
}