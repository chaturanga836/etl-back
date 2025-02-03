from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import create_engine  # Synchronous engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:2324@localhost/etldb"

async_engine = create_async_engine(DATABASE_URL, echo=True)
sync_engine = create_engine(DATABASE_URL.replace('postgresql+asyncpg', 'postgresql+psycopg2'), echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)
Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session
