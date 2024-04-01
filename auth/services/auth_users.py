from schemas.auth import AuthDTO, UserTokenInfoDTO
from schemas.users import UserLogInDTO, UserSignInDTO
from services.auth import AuthService
from services.users.users import UserService


class AuthUserService:
    def __init__(self, user_service: UserService, auth_service: AuthService):
        self._auth_service = auth_service
        self._user_service = user_service

    async def login_user(self, user: UserLogInDTO) -> AuthDTO:
        authenticated_user = await self._user_service.login_user(user=user)
        couple_token = await self._auth_service.get_couple_tokens_for_user(
            UserTokenInfoDTO(
                id=authenticated_user.id,
                role=authenticated_user.role,
            )
        )
        return couple_token

    async def signin_user(self, user: UserSignInDTO) -> AuthDTO:
        authenticated_user = await self._user_service.signin_user(user=user)
        couple_token = await self._auth_service.get_couple_tokens_for_user(
            UserTokenInfoDTO(
                id=authenticated_user.id,
                role=authenticated_user.role,
            )
        )
        return couple_token

    async def logout_user(self, refresh_token: str) -> None:
        await self._auth_service.remove_refresh_token(refresh_token)
