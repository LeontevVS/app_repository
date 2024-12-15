from types import TracebackType
from typing import Self

from redis.asyncio import Redis, ConnectionPool


class BaseRedisRepo:
    _client: Redis | None
    _redis_pool: ConnectionPool

    def __init__(self: Self, redis_pool: ConnectionPool):
        self._redis_pool = redis_pool
        self._client = None

    async def __aenter__(self) -> Redis:
        self._client = Redis.from_pool(self._redis_pool)
        return self._client

    async def __aexit__(
        self: Self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._client:
            await self._client.close()
            self._client = None
