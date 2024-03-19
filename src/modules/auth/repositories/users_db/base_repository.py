from typing import Protocol, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.base_model import ORMBaseModel


class IRepository(Protocol):
    async def _raw_get_all(self, session: AsyncSession) -> List[ORMBaseModel]:
        pass

    async def _create_one(
        self,
        session: AsyncSession,
        model: ORMBaseModel,
    ):
        pass

    # async def raw_get_one_by_id(self, id: int) -> ORMBaseModel:
    #     pass


class ORMRepository(IRepository):
    model: ORMBaseModel

    async def _raw_get_all(self, session: AsyncSession) -> List[ORMBaseModel]:
        stmt = select(self.model)
        result = await session.execute(stmt)
        return list(result.scalars().all())

    async def _create_one(
        self,
        session: AsyncSession,
        model: ORMBaseModel,
    ):
        async with session.begin():
            session.add(model)
