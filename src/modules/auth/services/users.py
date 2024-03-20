import bcrypt
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.modules.auth.enums.user_enums import PrivateUserRoles
from src.modules.auth.repositories.users_db.users import UserRepository
from src.modules.auth.schemas.users import UserSignInDTO, UserLogInDTO, ValidUser, UserToCreate


class UserService:
    def __init__(
        self,
        async_session_maker: async_sessionmaker[AsyncSession],
        user_repository: UserRepository
    ):
        self._async_session_maker = async_session_maker
        self.user_repository = user_repository

    async def get_user_by_login_creds(self, user: UserLogInDTO) -> ValidUser:
        existing_user = await self.user_repository.get_user_by_phone_number(
            async_session_maker=self._async_session_maker,
            phone_number=user.phone_number,
        )
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN
            )
        is_valid_password = self._validate_password(
            password=user.password,
            hashed_password=existing_user.hashed_password,
        )
        if not is_valid_password:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN
            )
        return ValidUser(
            id=existing_user.id,
            role=existing_user.role,
        )

    async def create_user(self, user: UserSignInDTO) -> ValidUser:
        existing_user = await self.user_repository.get_user_by_phone_number(
            async_session_maker=self._async_session_maker,
            phone_number=user.phone_number,
        )
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN
            )

        user_to_create = UserToCreate(
            phone_number=user.phone_number,
            role=PrivateUserRoles(user.role),
            hashed_password=self._hash_password(user.password)
        )
        new_user = await self.user_repository.create_user(
            async_session_maker=self._async_session_maker,
            user_data=user_to_create,
        )
        return ValidUser(
            id=new_user.id,
            role=new_user.role,
        )

    @staticmethod
    def _hash_password(
        password: str,
    ) -> bytes:
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt)

    @staticmethod
    def _validate_password(
        password: str,
        hashed_password: bytes,
    ) -> bool:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password,
        )
