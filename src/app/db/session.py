from redis import asyncio as aioredis
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

sync_engine = create_engine(settings.DB_URI, pool_pre_ping=True)
sync_session_factory = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

async_engine = create_async_engine(
    settings.DB_ASYNC_URI,
    pool_pre_ping=True,
    echo=True,
)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    future=True,
)


async def get_redis_session() -> aioredis.Redis:  # type: ignore
    """
    Get a Redis session.

    Returns:
        aioredis.Redis: The Redis session.

    """
    return await aioredis.from_url(settings.REDIS_URI)
