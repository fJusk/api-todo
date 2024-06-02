from enum import StrEnum

from pydantic_settings import BaseSettings


class PostgresEngineType(StrEnum):
    asyncpg = "asyncpg"
    psycopg2 = "psycopg2"


class Config(BaseSettings):
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


config = Config()

ALLOWED_ORIGINS = [
    # TODO: Add allowed origins, only for development
    "*",
]


def get_postgres_uri(engine_type: PostgresEngineType) -> str:
    return f"postgresql+{engine_type}://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
