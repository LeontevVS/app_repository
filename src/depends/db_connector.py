from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import DBConfig


engine = create_async_engine(DBConfig().dsn)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    async with async_session_maker() as session:
        yield session
