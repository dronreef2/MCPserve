"""
Cache system for MCP Server
Supports Redis and in-memory fallback
"""

import json
import time
import logging
from typing import Any, Optional, Dict
import redis
from functools import wraps

logger = logging.getLogger(__name__)

class Cache:
    """Unified cache interface supporting Redis and memory fallback"""

    def __init__(self, redis_url: str = "redis://localhost:6379", default_ttl: int = 3600):
        self.default_ttl = default_ttl
        self.redis_client = None
        self.memory_cache: Dict[str, Dict[str, Any]] = {}

        # Try to connect to Redis
        try:
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            self.redis_client.ping()
            logger.info("Redis cache connected successfully")
        except (redis.ConnectionError, redis.RedisError) as e:
            logger.warning(f"Redis not available, using memory cache: {e}")
            self.redis_client = None

    def _make_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Generate a unique cache key from function name and arguments"""
        # Convert args and kwargs to a stable string representation
        args_str = json.dumps(args, sort_keys=True, default=str)
        kwargs_str = json.dumps(kwargs, sort_keys=True, default=str)
        return f"{func_name}:{args_str}:{kwargs_str}"

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            if self.redis_client:
                value = self.redis_client.get(key)
                if value:
                    return json.loads(value)
            else:
                # Memory cache
                if key in self.memory_cache:
                    entry = self.memory_cache[key]
                    if time.time() < entry['expires']:
                        return entry['value']
                    else:
                        # Expired, remove it
                        del self.memory_cache[key]
        except Exception as e:
            logger.error(f"Cache get error: {e}")

        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache with TTL"""
        try:
            ttl = ttl or self.default_ttl
            expires = time.time() + ttl

            if self.redis_client:
                return self.redis_client.setex(key, ttl, json.dumps(value))
            else:
                # Memory cache
                self.memory_cache[key] = {
                    'value': value,
                    'expires': expires
                }
                return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        try:
            if self.redis_client:
                return bool(self.redis_client.delete(key))
            else:
                if key in self.memory_cache:
                    del self.memory_cache[key]
                    return True
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
        return False

    def clear(self) -> bool:
        """Clear all cache entries"""
        try:
            if self.redis_client:
                return self.redis_client.flushdb()
            else:
                self.memory_cache.clear()
                return True
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return False

    def cached(self, ttl: Optional[int] = None, key_prefix: str = ""):
        """Decorator to cache function results"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Generate cache key
                func_name = f"{key_prefix}:{func.__name__}" if key_prefix else func.__name__
                cache_key = self._make_key(func_name, args, kwargs)

                # Try to get from cache first
                cached_result = self.get(cache_key)
                if cached_result is not None:
                    logger.debug(f"Cache hit for {func_name}")
                    return cached_result

                # Execute function and cache result
                logger.debug(f"Cache miss for {func_name}, executing...")
                result = await func(*args, **kwargs)

                # Cache the result
                if result is not None:
                    self.set(cache_key, result, ttl)

                return result

            return wrapper
        return decorator

# Global cache instance
cache = Cache()

# Cache statistics
class CacheStats:
    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.sets = 0

    def hit(self):
        self.hits += 1

    def miss(self):
        self.misses += 1

    def set(self):
        self.sets += 1

    def get_stats(self):
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            'hits': self.hits,
            'misses': self.misses,
            'sets': self.sets,
            'hit_rate': f"{hit_rate:.1f}%"
        }

stats = CacheStats()