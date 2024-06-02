from sqlalchemy.ext.asyncio import AsyncSession


class BaseSessionService:
    def __init__(self, session: AsyncSession) -> None:
        """
        Base service class for services with async session

        :param session: SQLAlchemy session
        """
        self._session: AsyncSession = session
