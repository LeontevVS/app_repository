from uuid import UUID

from .models import CreationUserDTO, UserInfoDTO
from .proto import UserServiceP
from modules.users.user._repositories.user_repository import UserRepositoryP, get_user_repository


class UserService(UserServiceP):
    def __init__(self, user_repo: UserRepositoryP):
        self._user_repo = user_repo

    async def create_user(self, creation_data: CreationUserDTO) -> UUID:
        async with self._user_repo:
            return await self._user_repo.create_user(role=creation_data.role)

    async def get_user(self, user_id: UUID) -> UserInfoDTO | None:
        async with self._user_repo:
            user_model = await self._user_repo.get_by_id(user_id=user_id)
            return UserInfoDTO(
                user_id=user_model.user_id,
                role=user_model.role,
                deleted=user_model.deleted,
            ) if user_model else None


def get_user_service() -> UserService:
    return UserService(user_repo=get_user_repository())
