import json
from typing import Any, Optional, TypeVar, Type, Callable
from functools import wraps
from app.config.redis import redis_client
from app.config import settings

T = TypeVar('T')

def cache_key(prefix: str, *args, **kwargs) -> str:
    """Generate a cache key from prefix and arguments."""
    key_parts = [prefix]
    key_parts.extend(str(arg) for arg in args)
    key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
    return ":".join(key_parts)

def get_cached(key: str, model: Type[T]) -> Optional[T]:
    """Get a cached value by key and deserialize it to the specified model."""
    cached = redis_client.get(key)
    if cached is None:
        return None
    try:
        return model(**json.loads(cached))
    except (json.JSONDecodeError, TypeError):
        return None

def set_cached(key: str, value: Any, ttl: Optional[int] = None) -> bool:
    """Cache a value with an optional TTL (in seconds)."""
    if ttl is None:
        ttl = settings.CACHE_TTL
    try:
        serialized = json.dumps(value.dict() if hasattr(value, 'dict') else value)
        return redis_client.setex(key, ttl, serialized)
    except (TypeError, ValueError):
        return False

def delete_cached(key: str) -> bool:
    """Delete a cached value by key."""
    return bool(redis_client.delete(key))

def cached(prefix: str, ttl: Optional[int] = None):
    """Decorator to cache function results in Redis."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            # Skip caching if Redis is not available
            if not redis_client.ping():
                return func(*args, **kwargs)
                
            key = cache_key(prefix, *args, **{k: v for k, v in kwargs.items() if k != 'self'})
            
            # Try to get from cache
            if hasattr(func, '__annotations__') and 'return' in func.__annotations__:
                model = func.__annotations__['return']
                cached_result = get_cached(key, model)
                if cached_result is not None:
                    return cached_result
            
            # If not in cache, call the function and cache the result
            result = func(*args, **kwargs)
            if result is not None:
                set_cached(key, result, ttl)
            return result
        return wrapper
    return decorator
