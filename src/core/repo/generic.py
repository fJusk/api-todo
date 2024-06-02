from typing import Any, Generic, Sequence, Type, TypeVar

from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from .base import ABCRepo

M = TypeVar("M", bound=DeclarativeBase)


class Repository(ABCRepo, Generic[M]):
    def __init__(self, model: Type[M], session: AsyncSession) -> None:
        """
        Generic repository class for CRUD operations

        :param model: SQLAlchemy model class
        :param session: SQLAlchemy session
        """
        self._model: Type[M] = model
        self._session: AsyncSession = session

    async def get_by_pk(self, pk: int | str | Any) -> M | None:
        """
        Get model by primary key

        :param pk: primary key

        :return: model or None
        """
        return await self._session.get(self._model, pk)

    async def all(self) -> Sequence[M] | M:
        """
        Get all models

        :return: list of models
        """
        result = await self._session.execute(select(self._model))
        return result.scalars().all()

    async def filter(self, **kwargs) -> ScalarResult[M] | M:
        """
        Get models by filter parameters (synonyms: filter_by in SQLAlchemy)

        :param kwargs: filter parameters

        :return: list of models
        """
        result = await self._session.execute(select(self._model).filter_by(**kwargs))
        return result.scalars()

    async def create(self, model: M) -> M:
        """
        Create new model

        :param model: new model

        :return: created model
        """
        self._session.add(model)
        await self._session.flush()
        return model

    async def update(self, model: M) -> M:
        """
        Update model

        :param model: model to update

        :return: updated model
        """
        self._session.add(model)
        await self._session.flush()
        return model

    async def delete(self, model: M) -> None:
        """
        Delete model

        :param model: model to delete

        :return: None
        """
        await self._session.delete(model)

    async def commit(self) -> None:
        """Commit changes (synonyms: session.commit() in SQLAlchemy)"""
        await self._session.commit()

    async def rollback(self) -> None:
        """Rollback changes (synonyms: session.rollback() in SQLAlchemy)"""
        await self._session.rollback()
