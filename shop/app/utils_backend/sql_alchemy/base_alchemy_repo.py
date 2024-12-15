from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class BaseORMRepo:
    _session: AsyncSession | None
    _session_maker: async_sessionmaker[AsyncSession]

    def __init__(self: Self, session_maker: async_sessionmaker[AsyncSession]):
        self._session_maker = session_maker
        self._session = None

    async def __aenter__(self) -> AsyncSession:
        self._session = self._session_maker()
        return self._session

    async def __aexit__(
        self: Self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._session:
            await self._session.rollback()
            await self._session.close()
            self._session = None

    async def commit(self) -> None:
        await self._session.commit()
