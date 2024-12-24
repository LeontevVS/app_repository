from typing import Protocol
from uuid import UUID

from .models import CreationUserDTO, UserInfoDTO, UserInfoDTO


class UserServiceP(Protocol):
    async def create_user(self, creation_data: CreationUserDTO) -> UUID:
        pass

    async def get_user(self, user_id: UUID) -> UserInfoDTO:
        pass

    async def get_users(self, limit: int, offset: int) -> list[UserInfoDTO]:
        pass
