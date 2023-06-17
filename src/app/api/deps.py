from typing import Annotated, AsyncIterator, Generator

import aioredis
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.config import settings
from app.db.session import SessionLocal, async_session


def get_db() -> Generator[SessionLocal, None, None]:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_redis() -> aioredis.Redis:
    redis = await aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
    )
    try:
        yield redis
    finally:
        await redis.close()


async def get_session() -> AsyncIterator[async_sessionmaker]:
    try:
        yield async_session
    except SQLAlchemyError as e:
        print(f"Async Session Exception: {e}")


AsyncSession = Annotated[async_sessionmaker, Depends(get_session)]
