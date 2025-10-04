import redis
import json
from typing import Optional, Any
from datetime import timedelta

class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        try:
            self.client = redis.Redis(
                host=host,
                port=port,
                db=db,
                decode_responses=True,
                socket_connect_timeout=2
            )
            self.client.ping()
        except redis.ConnectionError:
            self.client = None
    
    def is_connected(self) -> bool:
        return self.client is not None
    
    @property
    def redis(self):
        return self.client
    
    def set(self, key: str, value: Any, expiry: Optional[int] = None) -> bool:
        if not self.is_connected():
            return False
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            if expiry:
                return self.client.setex(key, expiry, value)
            return self.client.set(key, value)
        except Exception:
            return False
    
    def get(self, key: str) -> Optional[Any]:
        if not self.is_connected():
            return None
        try:
            value = self.client.get(key)
            if value:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            return None
        except Exception:
            return None
    
    def delete(self, key: str) -> bool:
        if not self.is_connected():
            return False
        try:
            return bool(self.client.delete(key))
        except Exception:
            return False
    
    def exists(self, key: str) -> bool:
        if not self.is_connected():
            return False
        try:
            return bool(self.client.exists(key))
        except Exception:
            return False
    
    def incr(self, key: str) -> Optional[int]:
        if not self.is_connected():
            return None
        try:
            return self.client.incr(key)
        except Exception:
            return None
    
    def expire(self, key: str, seconds: int) -> bool:
        if not self.is_connected():
            return False
        try:
            return bool(self.client.expire(key, seconds))
        except Exception:
            return False
    
    def ttl(self, key: str) -> int:
        if not self.is_connected():
            return -1
        try:
            return self.client.ttl(key)
        except Exception:
            return -1
    
    def keys(self, pattern: str = '*') -> list:
        if not self.is_connected():
            return []
        try:
            return self.client.keys(pattern)
        except Exception:
            return []
    
    def get_all_keys(self) -> list:
        return self.keys('*')
    
    def flush_db(self) -> bool:
        if not self.is_connected():
            return False
        try:
            return self.client.flushdb()
        except Exception:
            return False

redis_client = RedisClient()
