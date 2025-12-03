import os
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv

from src.core.model import BaseModel

load_dotenv()
DATABASE = os.getenv("DB")

engine = create_async_engine(
    DATABASE,
    echo=False,
    future=True,
    pool_size=10,
    max_overflow=20
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_db() -> AsyncGenerator[AsyncSession | Any, Any]:
    async with async_session() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)