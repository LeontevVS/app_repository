from modules.users.auth.services.token_service import TokenServiceP, get_token_service
from .proto import LogoutUserServiceP


class LogoutUserService(LogoutUserServiceP):
    def __init__(self, token_service: TokenServiceP):
        self._token_service = token_service

    async def logout(self, refresh_token: str) -> None:
        await self._token_service.remove_refresh_token(refresh_token=refresh_token)


def get_logout_service() -> LogoutUserService:
    return LogoutUserService(token_service=get_token_service())
