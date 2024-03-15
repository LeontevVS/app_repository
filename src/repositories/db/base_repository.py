from typing import Protocol, List

from sqlalchemy import select

from repositories.db.connector import async_session_maker
from repositories.db.models.base_model import ORMBaseModel


class IRepository(Protocol):
    async def raw_get_all(self) -> List[ORMBaseModel]:
        pass

    async def raw_get_one_by_id(self, id: int) -> ORMBaseModel:
        pass


class ORMRepository(IRepository):
    model: ORMBaseModel

    async def raw_get_all(self) -> List[ORMBaseModel]:
        async with async_session_maker() as session:
            stmt = select(self.model)
            result = await session.execute(stmt)
            return list(result.scalars().all())
