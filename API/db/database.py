
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession

DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'

async_engine = create_async_engine(DATABASE_URL, echo=True)
async_sessionmaker = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()
