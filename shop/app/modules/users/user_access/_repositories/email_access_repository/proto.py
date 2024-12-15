from typing import Protocol

from .table_model import EmailAccessTableModel


class EmailAccessRepositoryP(Protocol):
    async def create_email_access(self, data: EmailAccessTableModel) -> None:
        pass

    async def get_email_access(self, email: str) -> EmailAccessTableModel | None:
        pass
