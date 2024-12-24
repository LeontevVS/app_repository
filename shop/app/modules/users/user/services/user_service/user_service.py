from uuid import UUID

from .models import CreationUserDTO, UserInfoDTO, UserInfoDTO
from .proto import UserServiceP
from modules.users.user._repositories.user_repository import UserRepositoryP, get_user_repository


class UserService(UserServiceP):
    def __init__(self, user_repo: UserRepositoryP):
        self._user_repo = user_repo

    async def create_user(self, creation_data: CreationUserDTO) -> UUID:
        async with self._user_repo:
            return await self._user_repo.create_user(role=creation_data.role)

    async def get_user(self, user_id: UUID) -> UserInfoDTO:
        async with self._user_repo:
            user_model = await self._user_repo.get_by_id(user_id=user_id)
            return UserInfoDTO(
                user_id=user_model.user_id,
                role=user_model.role,
                deleted=user_model.deleted,
                created_at=user_model.created_at,
                deleted_at=user_model.deleted_at,
            )

    async def get_users(self, limit: int, offset: int) -> list[UserInfoDTO]:
        async with self._user_repo:
            user_models = await self._user_repo.get_users(
                limit=limit,
                offset=offset,
            )
            return [
                UserInfoDTO(
                    user_id=user_model.user_id,
                    role=user_model.role,
                    deleted=user_model.deleted,
                    created_at=user_model.created_at,
                    deleted_at=user_model.deleted_at,
                )
                for user_model in user_models
            ]


def get_user_service() -> UserServiceP:
    return UserService(user_repo=get_user_repository())
