from sqlalchemy import select

from modules.users.depends import ASYNC_SESSION_MAKER
from utils_backend.sql_alchemy.base_alchemy_repo import BaseORMRepo
from .proto import EmailAccessRepositoryP
from .table_model import EmailAccessTableModel


class EmailAccessRepository(BaseORMRepo, EmailAccessRepositoryP):
    async def create_email_access(self, data: EmailAccessTableModel) -> None:
        self._session.add(data)
        await self.commit()

    async def get_email_access(self, email: str) -> EmailAccessTableModel | None:
        stmt = select(EmailAccessTableModel).where(EmailAccessTableModel.email == email)
        result = await self._session.execute(stmt)
        return result.scalars().one_or_none()


def get_email_access_repository() -> EmailAccessRepositoryP:
    return EmailAccessRepository(session_maker=ASYNC_SESSION_MAKER)
