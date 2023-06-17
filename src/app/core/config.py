from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    APP_DIR: str = str(Path(__file__).resolve(strict=True).parent.parent)
    PROJECT_NAME: str = "Demo"
    DEBUG_MODE: bool = False

    # Database
    DB_HOST: str = "localhost:5432"
    DB_USER: str = "postgres"
    DB_PASS: str = ""
    DB_NAME: str = "app"
    DB_URI: Optional[PostgresDsn] = None
    DB_ASYNC_URI: Optional[PostgresDsn] = None

    # Cache
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_TTL: int = 60

    # pylint: disable=no-self-argument
    @validator("DB_ASYNC_URI", pre=True)
    def assemble_db_async_uri(
        cls, value: Optional[str], values: Dict[str, Any]
    ) -> PostgresDsn:
        if isinstance(value, str):
            return value

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            host=values.get("DB_HOST"),
            user=values.get("DB_USER"),
            password=values.get("DB_PASS"),
            path=f'/{values.get("DB_NAME", "")}',
        )


settings = Settings()
