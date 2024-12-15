from datetime import timedelta

import orjson

from modules.users.depends import REDIS_POOL
from utils_backend.redis.base_redis_repo import BaseRedisRepo
from .proto import TokenRepositoryP
from modules.users.auth._repositories.models.token_payload import TokenPayloadDTO


class TokenRepository(BaseRedisRepo, TokenRepositoryP):
    async def get_refresh_token_info(self, token: str) -> TokenPayloadDTO | None:
        cache_token_info = await self._client.get(token)
        if cache_token_info:
            return TokenPayloadDTO.model_validate(
                obj=orjson.loads(cache_token_info),
                from_attributes=True,
            )

    async def set_cache_token(self, token: str, token_payload: TokenPayloadDTO, exp: timedelta) -> None:
        await self._client.set(
            name=token,
            value=orjson.dumps(token_payload.model_dump()),
            ex=exp,
        )

    async def remove_token(self, token: str) -> None:
        await self._client.delete(token)

    async def add_client_session(self, user_id: str, token: str) -> None:
        await self._client.lpush(user_id, token)

    async def remove_client_session(self, user_id: str, token: str) -> None:
        await self._client.lrem(name=user_id, count=1, value=token)


def get_token_repository() -> TokenRepository:
    return TokenRepository(redis_pool=REDIS_POOL)
