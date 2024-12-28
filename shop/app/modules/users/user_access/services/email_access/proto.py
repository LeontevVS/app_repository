from typing import Protocol

from modules.users.auth.services.token_service import CoupleTokensDTO, TokenServiceP
from modules.users.consts import PublicUserRoles
from modules.users.user.services.user_service import UserServiceP


class EmailUserAccessServiceP(Protocol):
    _user_service: UserServiceP
    _auth_service: TokenServiceP

    async def login_with_password(self, email: str, password: bytes) -> CoupleTokensDTO | None:
        pass

    async def signin_with_password(self, email: str, password: bytes, role: PublicUserRoles) -> int:
        pass

    async def confirm_email(self, email: str, code: str) -> CoupleTokensDTO:
        pass
