from pathlib import Path

from pydantic import Field, computed_field, BaseModel
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"


class _BaseRedisConfig(BaseSettings):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT")
    password: str = Field(alias="REDIS_PASSWORD")
    db: int


class UsersRedisConfig(_BaseRedisConfig):
    db: int = Field(alias="USERS_REDIS_DB")


class PGConfig(BaseSettings):
    host: str = Field(alias="POSTGRES_HOST")
    port: int = Field(alias="POSTGRES_PORT")
    user: str = Field(alias="POSTGRES_USER")
    password: str = Field(alias="POSTGRES_PASSWORD")
    database: str = Field(alias="POSTGRES_DB")

    @computed_field
    @property
    def dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
