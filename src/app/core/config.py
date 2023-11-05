from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    APP_DIR: str = str(Path(__file__).resolve(strict=True).parent.parent)
    PROJECT_NAME: str = "Demo"
    DEBUG_MODE: bool = False

    # Database
    POSTGRES_SERVER: str = "localhost:5432"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "app"
    DB_URI: Optional[PostgresDsn] = None
    DB_ASYNC_URI: Optional[PostgresDsn] = None

    # Cache
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_TTL: int = 60
    REDIS_URI: Optional[str] = None

    # pylint: disable=no-self-argument
    @validator("DB_ASYNC_URI", pre=True)
    def assemble_db_async_uri(
        cls, value: Optional[str], values: Dict[str, Any]
    ) -> PostgresDsn:
        """
        Assemble the asynchronous PostgreSQL database URI.

        Args:
            cls: The class.
            value (Optional[str]): The value of the DB_ASYNC_URI setting.
            values (Dict[str, Any]): The values of all the settings.

        Returns:
            PostgresDsn: The assembled PostgreSQL DSN.

        """
        if isinstance(value, str):
            return value

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            host=values.get("POSTGRES_SERVER"),
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            path=f'/{values.get("POSTGRES_DB", "")}',
        )

    # pylint: disable=no-self-argument
    @validator("DB_URI", pre=True)
    def assemble_db_sync_uri(
        cls, value: Optional[str], values: Dict[str, Any]
    ) -> PostgresDsn:
        """
        Assemble the synchronous PostgreSQL database URI.

        Args:
            cls: The class.
            value (Optional[str]): The value of the DB_URI setting.
            values (Dict[str, Any]): The values of all the settings.

        Returns:
            PostgresDsn: The assembled PostgreSQL DSN.

        """
        if isinstance(value, str):
            return value

        return PostgresDsn.build(
            scheme="postgresql",
            host=values.get("POSTGRES_SERVER"),
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            path=f'/{values.get("POSTGRES_DB", "")}',
        )

    @validator('REDIS_URI', pre=True)
    def assemble_redis_uri(cls, value: Optional[str], values: Dict[str, Any]) -> str:
        """
        Assemble the Redis URI.

        Args:
            cls: The class.
            value (Optional[str]): The value of the REDIS_URI setting.
            values (Dict[str, Any]): The values of all the settings.

        Returns:
            str: The assembled Redis URI.

        """
        if isinstance(value, str):
            return value
        return (
            f"redis://{values['REDIS_HOST']}:{values['REDIS_PORT']}/{values['REDIS_DB']}"
        )


settings = Settings()
