from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ProjectBase(BaseModel):
    title: str
    description: str
    tech_stack: str
    year: str
    status: str
    throughput: Optional[str] = None
    latency: Optional[str] = None
    uptime: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class SkillBase(BaseModel):
    name: str
    category: str
    proficiency: int
    years_experience: int

class SkillResponse(SkillBase):
    id: int
    
    class Config:
        from_attributes = True

class ContactMessageCreate(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = None
    message: str

class ContactMessageResponse(ContactMessageCreate):
    id: int
    created_at: datetime
    read: bool
    
    class Config:
        from_attributes = True

class ContactMessageUpdate(BaseModel):
    read: Optional[bool] = None

class ChallengeBase(BaseModel):
    title: str
    difficulty: str
    description: str
    sql_solution: str
    category: str

class ChallengeResponse(ChallengeBase):
    id: int
    
    class Config:
        from_attributes = True

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    success: bool
    data: Optional[list] = None
    error: Optional[str] = None
    execution_time: float

class AuthDemoRequest(BaseModel):
    username: str
    password: str
    algorithm: str = "HS256"

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    decoded: dict

class TokenPairResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    decoded_access: dict
    decoded_refresh: dict

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class RevokeTokenRequest(BaseModel):
    token: str

class ValidateTokenRequest(BaseModel):
    token: str
    algorithm: str = "HS256"

class ValidateTokenResponse(BaseModel):
    valid: bool
    decoded: Optional[dict] = None
    error: Optional[str] = None

class ExplainQueryRequest(BaseModel):
    query: str

class QueryPlan(BaseModel):
    plan: str
    execution_time_ms: float
    recommendations: list[str]
    complexity_score: int

class CachedQueryRequest(BaseModel):
    query: str
    cache_ttl: int = 300

class CachedQueryResponse(BaseModel):
    success: bool
    data: Optional[list] = None
    cached: bool
    execution_time: float
    error: Optional[str] = None

class RateLimitStatus(BaseModel):
    endpoint: str
    limit: int
    remaining: int
    reset_in: int
    blocked: bool

class ConnectionPoolMetrics(BaseModel):
    pool_size: int
    active_connections: int
    idle_connections: int
    wait_count: int
    overflow_count: int
    healthy: bool

class TransactionRequest(BaseModel):
    operations: list[dict]

class TransactionResponse(BaseModel):
    success: bool
    results: Optional[list] = None
    error: Optional[str] = None
    execution_time: float

class BackgroundTaskRequest(BaseModel):
    task_type: str
    params: dict

class BackgroundTaskResponse(BaseModel):
    task_id: str
    status: str
    message: str

class IndexRecommendation(BaseModel):
    table: str
    columns: list[str]
    reason: str
    impact: str
    sql: str

class EndpointMetrics(BaseModel):
    endpoint: str
    total_requests: int
    avg_response_time: float
    p95_response_time: float
    error_rate: float
    last_accessed: Optional[str] = None

class OAuth2AuthRequest(BaseModel):
    client_id: str
    redirect_uri: str
    scope: str = "read write"
    state: Optional[str] = None

class OAuth2TokenRequest(BaseModel):
    code: str
    code_verifier: str
    client_id: str
    redirect_uri: str

class OAuth2TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str

class RBACPermissionCheck(BaseModel):
    user_id: str
    resource: str
    action: str

class RBACResponse(BaseModel):
    allowed: bool
    user_role: str
    required_permissions: list[str]
    user_permissions: list[str]

class FullTextSearchRequest(BaseModel):
    table: str
    search_term: str
    columns: list[str]

class FullTextSearchResponse(BaseModel):
    results: list[dict]
    total_count: int
    search_term: str
    execution_time: float

class QueryPlanNode(BaseModel):
    node_type: str
    relation_name: Optional[str] = None
    startup_cost: float
    total_cost: float
    plan_rows: int
    plan_width: int
    actual_rows: Optional[int] = None
    actual_time: Optional[list[float]] = None
    children: Optional[list] = None

class QueryPlanVisualization(BaseModel):
    query: str
    plan_tree: dict
    total_cost: float
    execution_time_ms: float
    recommendations: list[str]

class MultiLevelCacheStats(BaseModel):
    l1_hits: int
    l1_misses: int
    l2_hits: int
    l2_misses: int
    l1_size: int
    l2_keys: int
    hit_rate: float

class SQLInjectionDemo(BaseModel):
    query_type: str
    user_input: str
    safe_query: str
    unsafe_query: str
    safe_result: Optional[list] = None
    unsafe_result: Optional[list] = None
    explanation: str

class CircuitBreakerStatus(BaseModel):
    name: str
    state: str
    failure_count: int
    success_count: int
    last_failure_time: Optional[str] = None
    next_retry_time: Optional[str] = None

class CacheSetRequest(BaseModel):
    key: str
    value: str
    ttl: Optional[int] = None

class CacheSetResponse(BaseModel):
    success: bool
    key: str
    message: str
    ttl: Optional[int] = None

class CacheGetResponse(BaseModel):
    success: bool
    key: str
    value: Optional[str] = None
    source: Optional[str] = None
    ttl: Optional[int] = None
    message: Optional[str] = None

class CacheOperationResponse(BaseModel):
    success: bool
    message: str
    affected_keys: int

class ProxyRequest(BaseModel):
    url: str
    method: str = "GET"
    headers: Optional[dict] = None
    body: Optional[str] = None
    query_params: Optional[dict] = None

class ProxyResponse(BaseModel):
    status_code: int
    headers: dict
    body: str
    execution_time: float
    error: Optional[str] = None
