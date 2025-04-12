import json
from typing import Any, Optional, Union
import redis
from fastapi import Depends
from core.config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD

class RedisClient:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            password=REDIS_PASSWORD,
            decode_responses=True
        )
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from Redis"""
        value = self.redis_client.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None
    
    def set(self, key: str, value: Any, expiry: Optional[int] = None) -> bool:
        """Set a value in Redis with optional expiry in seconds"""
        if not isinstance(value, str):
            value = json.dumps(value)
        
        if expiry:
            return self.redis_client.setex(key, expiry, value)
        return self.redis_client.set(key, value)
    
    def delete(self, key: str) -> bool:
        """Delete a key from Redis"""
        return bool(self.redis_client.delete(key))
    
    def exists(self, key: str) -> bool:
        """Check if a key exists in Redis"""
        return bool(self.redis_client.exists(key))
    
    def hash_get(self, hash_key: str, field: str) -> Optional[Any]:
        """Get a field from a hash in Redis"""
        value = self.redis_client.hget(hash_key, field)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return None
    
    def hash_set(self, hash_key: str, field: str, value: Any) -> bool:
        """Set a field in a hash in Redis"""
        if not isinstance(value, str):
            value = json.dumps(value)
        return bool(self.redis_client.hset(hash_key, field, value))
    
    def flush(self) -> bool:
        """Clear the entire Redis database"""
        return self.redis_client.flushdb()

# Singleton instance
_redis_client = None

def get_redis_client() -> RedisClient:
    """Dependency to get Redis client instance"""
    global _redis_client
    if _redis_client is None:
        _redis_client = RedisClient()
    return _redis_client 