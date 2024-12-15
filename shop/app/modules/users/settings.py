from pydantic_settings import BaseSettings

from config import PGConfig, AuthJWT, UsersRedisConfig


class Settings(BaseSettings):
    users_db: PGConfig = PGConfig()
    auth_jwt: AuthJWT = AuthJWT()
    users_redis: UsersRedisConfig = UsersRedisConfig()


SETTINGS = Settings()
