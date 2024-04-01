from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from repositories.users_db.users import UserRepository
from schemas.users import UserLogInDTO, UserSignInDTO, ValidUser
from services.users.use_cases import UserController


class UserService:
    def __init__(self, async_session_maker: async_sessionmaker[AsyncSession], user_repository: UserRepository):
        self._user_controller = UserController(
            async_session_maker=async_session_maker,
            user_repository=user_repository,
        )

    async def login_user(self, user: UserLogInDTO) -> ValidUser:
        return await self._user_controller.get_user_by_login_creds(user=user)

    async def signin_user(self, user: UserSignInDTO) -> ValidUser:
        return await self._user_controller.create_user(user=user)
