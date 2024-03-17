from redis.asyncio import Redis, ConnectionPool


class RedisConnection:
    def __init__(self, redis_pool: ConnectionPool):
        self._redis_pool = redis_pool

    async def __aenter__(self):
        self._client = Redis.from_pool(self._redis_pool)
        return self._client

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.close()


class AuthRepository:
    def __init__(self, redis_pool: ConnectionPool):
        self._redis_pool = redis_pool

    async def some(self):
        async with RedisConnection(self._redis_pool) as connection:
            pass
