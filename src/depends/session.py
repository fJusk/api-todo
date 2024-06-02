from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connection import SessionMaker


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get an async session
    """
    async with SessionMaker() as session, session.begin():
        yield session
