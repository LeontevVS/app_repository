from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field, computed_field, BaseModel
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent
load_dotenv()


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / 'certs' / 'private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'public.pem'
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 15


class DBConfig(BaseSettings):
    host: str = Field(alias='DB_HOST')
    port: int = Field(alias='DB_PORT')
    user: str = Field(alias='DB_USER')
    password: str = Field(alias='DB_PASSWORD')
    database: str = Field(alias='DB_DATABASE')

    @computed_field
    @property
    def dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class RedisAuthConfig(BaseSettings):
    host: str = Field(alias='REDIS_AUTH_HOST')
    port: int = Field(alias='REDIS_AUTH_PORT')
    password: str = Field(alias='REDIS_AUTH_PASSWORD')

    @computed_field
    @property
    def dsn(self) -> str:
        return f"redis://app:{self.password}@{self.host}:{self.port}"


class Settings(BaseSettings):
    db: DBConfig = DBConfig()
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
