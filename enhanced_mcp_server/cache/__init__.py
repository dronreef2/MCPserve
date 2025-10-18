"""Sistema de cache inteligente com Redis fallback."""

import json
import time
from typing import Any, Optional, Callable, Dict
import redis
from functools import wraps
import threading
from enhanced_mcp_server.config import settings
from enhanced_mcp_server.utils.logging import get_logger

logger = get_logger(__name__)


class Cache:
    """Sistema de cache inteligente com Redis (conexão preguiçosa) e fallback para memória."""

    def __init__(self):
        self._redis_client: Optional[redis.Redis] = None
        self._redis_checked = False  # Flag para verificar a conexão apenas uma vez
        self._memory_cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def get_redis_client(self) -> Optional[redis.Redis]:
        """
        Retorna o cliente Redis, inicializando a conexão na primeira chamada.
        Isso é chamado de "lazy connection".
        """
        with self._lock:
            if not self._redis_checked:
                self._redis_checked = True
                if settings.redis_url:
                    try:
                        client = redis.from_url(settings.redis_url, socket_connect_timeout=2)
                        client.ping()
                        self._redis_client = client
                        logger.info("Redis cache connected successfully.")
                    except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
                        logger.warning(f"Failed to connect to Redis: {e}. Using memory cache.")
                        self._redis_client = None
                else:
                    logger.info("Redis not configured. Using memory cache.")
        return self._redis_client

    def _init_redis(self) -> None:
        """Método legado - agora usa get_redis_client()."""
        self.get_redis_client()

    def _get_cache_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Gera chave de cache baseada na função e argumentos."""
        key_parts = [func_name]
        key_parts.extend(str(arg) for arg in args)
        key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
        return ":".join(key_parts)

    def get(self, key: str) -> Optional[Any]:
        """Recupera valor do cache."""
        try:
            redis_client = self.get_redis_client()
            if redis_client:
                data = redis_client.get(key)
                if data:
                    cached_data = json.loads(data)
                    if time.time() < cached_data["expires_at"]:
                        logger.debug(f"Cache hit for key: {key}")
                        return cached_data["value"]
                    else:
                        redis_client.delete(key)
            else:
                with self._lock:
                    if key in self._memory_cache:
                        cached_data = self._memory_cache[key]
                        if time.time() < cached_data["expires_at"]:
                            logger.debug(f"Memory cache hit for key: {key}")
                            return cached_data["value"]
                        else:
                            del self._memory_cache[key]
        except Exception as e:
            logger.error(f"Cache get error: {e}")

        logger.debug(f"Cache miss for key: {key}")
        return None

    def set(self, key: str, value: Any, ttl: int = None) -> None:
        """Armazena valor no cache."""
        if ttl is None:
            ttl = settings.cache_ttl

        expires_at = time.time() + ttl
        cached_data = {
            "value": value,
            "expires_at": expires_at,
            "created_at": time.time()
        }

        try:
            redis_client = self.get_redis_client()
            if redis_client:
                redis_client.setex(key, ttl, json.dumps(cached_data))
                logger.debug(f"Stored in Redis cache: {key}")
            else:
                with self._lock:
                    self._memory_cache[key] = cached_data
                    logger.debug(f"Stored in memory cache: {key}")
        except Exception as e:
            logger.error(f"Cache set error: {e}")

    def delete(self, key: str) -> None:
        """Remove valor do cache."""
        try:
            redis_client = self.get_redis_client()
            if redis_client:
                redis_client.delete(key)
            else:
                with self._lock:
                    self._memory_cache.pop(key, None)
            logger.debug(f"Deleted from cache: {key}")
        except Exception as e:
            logger.error(f"Cache delete error: {e}")

    def clear(self) -> None:
        """Limpa todo o cache."""
        try:
            redis_client = self.get_redis_client()
            if redis_client:
                redis_client.flushdb()
            else:
                with self._lock:
                    self._memory_cache.clear()
            logger.info("Cache cleared")
        except Exception as e:
            logger.error(f"Cache clear error: {e}")


# Instância global do cache
cache = Cache()


def cached(ttl: int = None):
    """Decorador para cache de funções (suporta sync e async)."""
    def decorator(func: Callable) -> Callable:
        import asyncio
        import inspect
        
        is_async = asyncio.iscoroutinefunction(func)
        
        if is_async:
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                if not settings.redis_url and not cache._memory_cache:
                    # Se não há cache configurado, executa diretamente
                    return await func(*args, **kwargs)

                cache_key = cache._get_cache_key(func.__name__, args, kwargs)
                cached_result = cache.get(cache_key)

                if cached_result is not None:
                    return cached_result

                result = await func(*args, **kwargs)
                cache.set(cache_key, result, ttl)
                return result
            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                if not settings.redis_url and not cache._memory_cache:
                    # Se não há cache configurado, executa diretamente
                    return func(*args, **kwargs)

                cache_key = cache._get_cache_key(func.__name__, args, kwargs)
                cached_result = cache.get(cache_key)

                if cached_result is not None:
                    return cached_result

                result = func(*args, **kwargs)
                cache.set(cache_key, result, ttl)
                return result
            return sync_wrapper

    return decorator