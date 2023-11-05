from typing import Annotated, AsyncGenerator, Generator

from fastapi import Depends
from redis import asyncio as aioredis
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.db.session import (
    async_session_factory,
    get_redis_session,
    sync_session_factory,
)


# Session generators
def get_sync_db_session() -> Generator[Session, None, None]:
    """
    Returns a generator that yields a synchronous SQLAlchemy session.

    Yields:
        Generator[Session, None, None]: A synchronous SQLAlchemy session.

    Raises:
        SQLAlchemyError: If there is an error creating the session.

    """
    try:
        session = sync_session_factory()
        yield session
    except SQLAlchemyError as e:
        print(f"Sync Session Exception: {e}")
    finally:
        session.close()


async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Returns an asynchronous generator that yields an asynchronous SQLAlchemy session.

    Yields:
        AsyncGenerator[AsyncSession, None]: An asynchronous SQLAlchemy session.

    Raises:
        SQLAlchemyError: If there is an error creating the session.

    """
    try:
        session = async_session_factory()
        yield session
    except SQLAlchemyError as e:
        print(f"Async Session Exception: {e}")
    finally:
        await session.close()


async def get_async_redis_session() -> AsyncGenerator[aioredis.Redis, None]:  # type: ignore
    """
    Returns an asynchronous generator that yields an asynchronous Redis session.

    Yields:
        AsyncGenerator[aioredis.Redis, None]: An asynchronous Redis session.

    Raises:
        RedisError: If there is an error creating the session.

    """
    try:
        session = await get_redis_session()
        yield session
    except aioredis.RedisError as e:
        print(f"Redis Session Exception: {e}")
    finally:
        await session.aclose()


# Session dependencies
sync_session = Annotated[Session, Depends(get_sync_db_session)]
async_session = Annotated[AsyncSession, Depends(get_async_db_session)]
redis_async_session = Annotated[aioredis.Redis, Depends(get_async_redis_session)]
