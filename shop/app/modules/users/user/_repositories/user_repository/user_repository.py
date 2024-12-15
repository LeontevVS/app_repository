from uuid import UUID

from sqlalchemy import select

from modules.users.depends import ASYNC_SESSION_MAKER
from utils_backend.sql_alchemy.base_alchemy_repo import BaseORMRepo
from .table_models import UserTableModel
from .proto import UserRepositoryP
from modules.users.consts import PrivateUserRoles


class UserRepository(BaseORMRepo, UserRepositoryP):
    async def get_by_id(self, user_id: UUID) -> UserTableModel | None:
        stmt = select(UserTableModel).where(UserTableModel.user_id == user_id)
        result = await self._session.execute(stmt)
        return result.scalars().one_or_none()

    async def create_user(self, role: PrivateUserRoles) -> UUID:
        new_user = UserTableModel(role=role)
        self._session.add(new_user)
        await self.commit()
        return new_user.user_id


def get_user_repository() -> UserRepository:
    return UserRepository(session_maker=ASYNC_SESSION_MAKER)
