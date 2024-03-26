from typing import Annotated

from fastapi import HTTPException, status, Header
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from enums.user_enums import PrivateUserRoles
from schemas.auth import UserTokenInfoDTO, AuthDTO, AuthenticatedUserDTO
from schemas.users import UserSignInDTO, UserLogInDTO
from services.auth.auth import AuthService
from services.users import UserService


class AuthUserService:
    def __init__(
        self,
        async_session_maker: async_sessionmaker[AsyncSession],
        user_service: UserService,
        auth_service: AuthService,
    ):
        self._async_session_maker = async_session_maker
        self.user_service = user_service
        self.auth_service = auth_service

    async def login_user(self, user: UserLogInDTO) -> AuthDTO:
        authenticated_user = await self.user_service.get_user_by_login_creds(user=user)
        couple_token = await self.auth_service.get_couple_tokens_for_user(
            UserTokenInfoDTO(
                id=authenticated_user.id,
                role=authenticated_user.role,
            )
        )
        return couple_token

    async def signin_user(self, user: UserSignInDTO) -> AuthDTO:
        authenticated_user = await self.user_service.create_user(user=user)
        couple_token = await self.auth_service.get_couple_tokens_for_user(
            UserTokenInfoDTO(
                id=authenticated_user.id,
                role=authenticated_user.role,
            )
        )
        return couple_token

    async def auth_user(self, access_token: str, roles: list[PrivateUserRoles]) -> AuthenticatedUserDTO:
        token_user_info = await self.auth_service.get_token_info(access_token)
        authenticated_user = AuthenticatedUserDTO(
            id=token_user_info.id,
            role=token_user_info.role,
        )
        if authenticated_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
            )
        return authenticated_user


class UserPermission:
    def __init__(self, auth_user_service: AuthUserService):
        self.auth_user_service = auth_user_service

    async def auth_seller_permissions(self, access_token: Annotated[str | None, Header()]) -> AuthenticatedUserDTO:
        return await self.auth_user_service.auth_user(
            access_token=access_token,
            roles=[PrivateUserRoles.SELLER, PrivateUserRoles.ADMIN]
        )

    async def auth_buyer_permissions(self, access_token: Annotated[str | None, Header()]) -> AuthenticatedUserDTO:
        return await self.auth_user_service.auth_user(
            access_token=access_token,
            roles=[PrivateUserRoles.BUYER, PrivateUserRoles.ADMIN]
        )

    async def auth_admin_permissions(self, access_token: Annotated[str | None, Header()]) -> AuthenticatedUserDTO:
        return await self.auth_user_service.auth_user(
            access_token=access_token,
            roles=[PrivateUserRoles.ADMIN]
        )

    async def auth_all_permissions(self, access_token: Annotated[str | None, Header()]) -> AuthenticatedUserDTO:
        return await self.auth_user_service.auth_user(
            access_token=access_token,
            roles=[PrivateUserRoles.ADMIN, PrivateUserRoles.BUYER, PrivateUserRoles.SELLER]
        )
