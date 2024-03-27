from datetime import timedelta

import orjson
from redis.asyncio import Redis, ConnectionPool

from schemas.auth import TokenPayload


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

    async def get_refresh_token_info(self, token: str) -> TokenPayload | None:
        async with RedisConnection(self._redis_pool) as connection:
            cache_token_info = await connection.get(token)
            if cache_token_info:
                return TokenPayload.model_validate(
                    obj=orjson.loads(cache_token_info),
                    from_attributes=True,
                )

    async def set_cache_token(
        self,
        token: str,
        token_info: TokenPayload,
        exp: timedelta,
    ) -> None:
        async with RedisConnection(self._redis_pool) as connection:
            await connection.set(
                name=token,
                value=orjson.dumps(token_info.model_dump()),
                ex=exp,
            )

    async def remove_token(self, token: str) -> None:
        async with RedisConnection(self._redis_pool) as connection:
            await connection.delete(token)
