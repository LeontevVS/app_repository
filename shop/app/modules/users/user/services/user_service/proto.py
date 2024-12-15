from typing import Protocol
from uuid import UUID

from .models import CreationUserDTO, UserInfoDTO


class UserServiceP(Protocol):
    async def create_user(self, creation_data: CreationUserDTO) -> UUID:
        pass

    async def get_user(self, user_id: UUID) -> UserInfoDTO | None:
        pass
