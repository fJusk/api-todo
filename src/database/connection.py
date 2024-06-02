from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import PostgresEngineType, get_postgres_uri

postgres_uri = get_postgres_uri(PostgresEngineType.asyncpg)

engine = create_async_engine(postgres_uri, pool_pre_ping=True)
SessionMaker = sessionmaker(engine, autoflush=False, class_=AsyncSession, expire_on_commit=False)
