from datetime import timedelta
from typing import Protocol

from modules.users.auth._repositories.models.token_payload import TokenPayloadDTO
from utils_backend.redis.base_redis_repo import BaseRedisRepo


class TokenRepositoryP(Protocol):
    def get_connection(self) -> BaseRedisRepo:
        pass

    async def get_refresh_token_info(self, token: str) -> TokenPayloadDTO | None:
        pass

    async def set_cache_token(self, token: str, token_payload: TokenPayloadDTO, exp: timedelta) -> None:
        pass

    async def remove_token(self, token: str) -> None:
        pass

    async def add_client_session(self, user_id: str, token: str) -> None:
        pass

    async def remove_client_session(self, user_id: str, token: str) -> None:
        pass

    async def get_client_sessions(self, user_id: str) -> list[str] | None:
        pass
