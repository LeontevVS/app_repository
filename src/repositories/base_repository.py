from typing import Protocol, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from models.base_model import ORMBaseModel


class IRepository(Protocol):
    async def _raw_get_all(self, async_session_maker: async_sessionmaker) -> List[ORMBaseModel]:
        pass

    async def _create_one(
        self,
        async_session_maker: async_sessionmaker,
        model: ORMBaseModel,
    ):
        pass

    # async def raw_get_one_by_id(self, id: int) -> ORMBaseModel:
    #     pass


class ORMRepository(IRepository):
    model: ORMBaseModel

    async def _raw_get_all(self, async_session_maker: async_sessionmaker) -> List[ORMBaseModel]:
        async with async_session_maker() as session:
            stmt = select(self.model)
            result = await session.execute(stmt)
            return list(result.scalars().all())

    async def _create_one(
        self,
        async_session_maker: async_sessionmaker,
        model: ORMBaseModel,
    ):
        async with async_session_maker() as session:
            async with session.begin():
                session.add(model)
