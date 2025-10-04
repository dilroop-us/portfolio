from fastapi import APIRouter
import time

from backend.schemas import (
    CacheSetRequest, CacheSetResponse, CacheGetResponse,
    CacheOperationResponse, MultiLevelCacheStats
)
from backend.redis_client import redis_client

router = APIRouter(prefix="/api/cache", tags=["cache"])

l1_cache = None
l1_stats = None
l2_stats = None

def set_cache_references(cache, stats1, stats2):
    global l1_cache, l1_stats, l2_stats
    l1_cache = cache
    l1_stats = stats1
    l2_stats = stats2

@router.get("/stats", response_model=MultiLevelCacheStats)
async def get_cache_stats():
    l2_keys_count = 0
    if redis_client.is_connected():
        try:
            l2_keys_count = len(redis_client.get_all_keys())
        except:
            l2_keys_count = 0
    
    total_requests = l1_stats["hits"] + l1_stats["misses"]
    total_hits = l1_stats["hits"] + l2_stats["hits"]
    hit_rate = (total_hits / total_requests * 100) if total_requests > 0 else 0
    
    return MultiLevelCacheStats(
        l1_hits=l1_stats["hits"],
        l1_misses=l1_stats["misses"],
        l2_hits=l2_stats["hits"],
        l2_misses=l2_stats["misses"],
        l1_size=len(l1_cache),
        l2_keys=l2_keys_count,
        hit_rate=round(hit_rate, 2)
    )

@router.post("/set", response_model=CacheSetResponse)
async def cache_set(request: CacheSetRequest):
    cache_key = f"playground:{request.key}"
    
    expire_at = None
    if request.ttl:
        expire_at = time.time() + request.ttl
    
    l1_cache[cache_key] = (request.value, expire_at)
    
    if redis_client.is_connected():
        redis_client.set(cache_key, request.value, request.ttl)
    
    message = f"Set '{request.key}' in L1 cache"
    if redis_client.is_connected():
        message += " and L2 (Redis) cache"
        if request.ttl:
            message += f" with TTL of {request.ttl} seconds"
    
    return CacheSetResponse(
        success=True,
        key=request.key,
        message=message,
        ttl=request.ttl
    )

@router.get("/get/{key}", response_model=CacheGetResponse)
async def cache_get(key: str):
    cache_key = f"playground:{key}"
    
    if cache_key in l1_cache:
        cached_data = l1_cache[cache_key]
        value, expire_at = cached_data
        
        if expire_at is not None and time.time() > expire_at:
            del l1_cache[cache_key]
        else:
            l1_stats["hits"] += 1
            
            ttl_remaining = None
            if expire_at is not None:
                ttl_remaining = int(expire_at - time.time())
            elif redis_client.is_connected():
                ttl_remaining = redis_client.ttl(cache_key)
                if ttl_remaining == -1:
                    ttl_remaining = None
            
            return CacheGetResponse(
                success=True,
                key=key,
                value=value,
                source="L1 (in-memory)",
                ttl=ttl_remaining,
                message="Cache hit from L1"
            )
    
    l1_stats["misses"] += 1
    
    if redis_client.is_connected():
        value = redis_client.get(cache_key)
        if value:
            l2_stats["hits"] += 1
            
            ttl_remaining = redis_client.ttl(cache_key)
            expire_at = None
            if ttl_remaining and ttl_remaining > 0:
                expire_at = time.time() + ttl_remaining
            elif ttl_remaining == -1:
                ttl_remaining = None
            
            l1_cache[cache_key] = (value, expire_at)
            
            return CacheGetResponse(
                success=True,
                key=key,
                value=value,
                source="L2 (Redis)",
                ttl=ttl_remaining,
                message="Cache hit from L2, promoted to L1"
            )
        else:
            l2_stats["misses"] += 1
    else:
        l2_stats["misses"] += 1
    
    return CacheGetResponse(
        success=False,
        key=key,
        value=None,
        source="miss",
        message="Cache miss - key not found in L1 or L2"
    )

@router.delete("/delete/{key}", response_model=CacheOperationResponse)
async def cache_delete(key: str):
    cache_key = f"playground:{key}"
    affected = 0
    
    if cache_key in l1_cache:
        del l1_cache[cache_key]
        affected += 1
    
    if redis_client.is_connected() and redis_client.exists(cache_key):
        redis_client.delete(cache_key)
        affected += 1
    
    if affected > 0:
        return CacheOperationResponse(
            success=True,
            message=f"Deleted '{key}' from cache",
            affected_keys=affected
        )
    else:
        return CacheOperationResponse(
            success=False,
            message=f"Key '{key}' not found in cache",
            affected_keys=0
        )

@router.post("/clear", response_model=CacheOperationResponse)
async def cache_clear():
    l1_count = len([k for k in list(l1_cache.keys()) if k.startswith("playground:")])
    
    for key in list(l1_cache.keys()):
        if key.startswith("playground:"):
            del l1_cache[key]
    
    l2_count = 0
    if redis_client.is_connected():
        all_keys = redis_client.get_all_keys()
        playground_keys = [k for k in all_keys if k.startswith("playground:")]
        for key in playground_keys:
            redis_client.delete(key)
        l2_count = len(playground_keys)
    
    total_cleared = l1_count + l2_count
    
    return CacheOperationResponse(
        success=True,
        message=f"Cleared {total_cleared} playground cache entries",
        affected_keys=total_cleared
    )
