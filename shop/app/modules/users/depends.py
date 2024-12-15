import redis.asyncio as redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from modules.users.settings import SETTINGS


REDIS_POOL = redis.ConnectionPool(**SETTINGS.users_redis.model_dump())  # .from_url(SETTINGS.users_redis.dsn)

_ENGINE = create_async_engine(SETTINGS.users_db.dsn)
ASYNC_SESSION_MAKER = async_sessionmaker(_ENGINE, expire_on_commit=False)
