import redis.asyncio as redis

from src.config import RedisAuthConfig


redis_pool = redis.ConnectionPool.from_url(RedisAuthConfig().dsn)
