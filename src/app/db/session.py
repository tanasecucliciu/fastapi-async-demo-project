from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.DB_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async_engine = create_async_engine(
    settings.DB_ASYNC_URI,
    pool_pre_ping=True,
    echo=True,
)

async_session = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    future=True,
)
