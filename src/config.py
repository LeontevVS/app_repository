from dotenv import load_dotenv
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings

load_dotenv()


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
