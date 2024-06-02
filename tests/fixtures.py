from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from main import app
from src.database.models import BaseModel
from src.depends.session import get_session

ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./test.db"


async_engine = create_async_engine(ASYNC_DATABASE_URL)
SessionMaker = sessionmaker(async_engine, autoflush=False, class_=AsyncSession, expire_on_commit=False)

async_engine.echo = True


async def get_sqlite_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionMaker() as session, session.begin():
        yield session


@pytest.fixture(scope="function")
async def sqlite_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
        async with SessionMaker() as session:
            yield session
        await conn.run_sync(BaseModel.metadata.drop_all)


app.dependency_overrides[get_session] = get_sqlite_session


@pytest.fixture(scope="session")
def test_client():
    return TestClient(app)
