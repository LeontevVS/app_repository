from typing import Protocol
from uuid import UUID

from .table_models import UserTableModel
from modules.users.consts import PrivateUserRoles


class UserRepositoryP(Protocol):
    async def get_by_id(self, user_id: UUID) -> UserTableModel | None:
        pass

    async def create_user(self, role: PrivateUserRoles) -> UUID:
        pass
