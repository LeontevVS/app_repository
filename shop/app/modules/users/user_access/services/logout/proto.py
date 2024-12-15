from typing import Protocol

from modules.users.auth.services.token_service import TokenServiceP


class LogoutUserServiceP(Protocol):
    _auth_service: TokenServiceP

    async def logout(self, refresh_token: str) -> None:
        pass
