from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import DBConfig


engine = create_async_engine(DBConfig().dsn)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
