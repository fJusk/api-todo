import logging
from typing import Generic, Sequence, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import RecordNotFoundError
from src.core.repo.generic import M, Repository

from .base import BaseSessionService

log = logging.getLogger(__name__)


C = TypeVar("C", bound=BaseModel)
U = TypeVar("U", bound=BaseModel)

"""
GENERIC CRUD SERVICE

M - MODEL TYPE bound to SQLAlchemy model
C - CREATE MODEL TYPE bound to BaseModel from pydantic
U - UPDATE MODEL TYPE bound to BaseModel from pydantic
"""


class CRUDService(BaseSessionService, Generic[M, C, U]):
    DB_MODEL: Type[M]
    CREATE_MODE: Type[C]
    UPDATE_MODEL: Type[U]

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

        self._repo = Repository(self.DB_MODEL, session)

    def _raise_not_found(self, _id: int) -> None:
        """Raise not found exception"""
        raise RecordNotFoundError(f"Record {self.DB_MODEL.__name__} with id={_id} not found")

    async def _create(self, data: C) -> M:
        """
        Create new record

        :param data: pydantic model

        :return: created model
        """
        log.debug(f"Creating {self.DB_MODEL.__name__} with data: {data}")
        return await self._repo.create(self.DB_MODEL(**data.model_dump()))

    async def _update(self, _id: int, data: U) -> M:
        """
        Update existing record

        :param _id: record id
        :param data: pydantic model

        :return: updated model
        """
        record = await self._repo.get_by_pk(_id)

        if not record:
            self._raise_not_found(_id)

        for field, value in data.model_dump().items():
            setattr(record, field, value)

        log.debug(f"Updating {self.DB_MODEL.__name__} with data: {data}")

        # FIXME: mypy doesn't understand that result is not None
        return await self._repo.update(record)  # type: ignore

    async def _delete(self, _id: int) -> bool:
        """
        Delete existing record

        :param _id: record id

        :return: bool
        """
        record = await self._repo.get_by_pk(_id)

        if not record:
            self._raise_not_found(_id)

        try:
            # FIXME: mypy doesn't understand
            await self._repo.delete(record)  # type: ignore

        except IntegrityError as e:
            log.error(f"Failed to delete {self.DB_MODEL.__name__} with id={_id} due to IntegrityError - {e}")
            return False

        except Exception as e:
            log.error(f"Failed to delete {self.DB_MODEL.__name__} with id={_id} due to unknown Exception - {e}")
            return False

        else:
            log.debug(f"Deleted {self.DB_MODEL.__name__} with id={_id}")

        return True

    async def _get_by_id(self, _id: int) -> M:
        """
        Get record by id

        :param _id: record id

        :return: model
        """
        res = await self._repo.get_by_pk(_id)

        if res is None:
            self._raise_not_found(_id)

        # FIXME: mypy doesn't understand that res is not None
        return res  # type: ignore

    async def create(self, data: C) -> M:
        """
        Create new record

        :param data: pydantic model
        :return: created model

        ## You can override create method like this:

        .. code-block:: python
            class MyAwesomeCRUDService(CRUDService[MyAwesomeModel, MyAwesomeCreate, MyAwesomeUpdate]):

                CREATE_MODEL = MyAwesomeCreate
                UPDATE_MODEL = MyAwesomeUpdate

                DB_MODEL = MyAwesomeModel

                async def create(self, data: MyAwesomeCreate) -> MyAwesomeModel:
                    # do something before create
                    result = await super().create(data)
                    # do something after create
                    return result
        """
        return await self._create(data)

    async def update(self, _id: int, data: U) -> M:
        """
        Update existing record

        :param _id: record id
        :param data: pydantic model

        :return: updated model

        ## You can override update method like this:

        .. code-block:: python
            class MyAwesomeCRUDService(CRUDService[MyAwesomeModel, MyAwesomeCreate, MyAwesomeUpdate]):

                CREATE_MODEL = MyAwesomeCreate
                UPDATE_MODEL = MyAwesomeUpdate

                DB_MODEL = MyAwesomeModel

                async def update(self, _id: int, data: MyAwesomeUpdate) -> MyAwesomeModel:
                    # do something before update
                    result = await super().update(_id, data)
                    # do something after update
                    return result
        """
        return await self._update(_id, data)

    async def delete(self, _id: int) -> bool:
        """
        Delete existing record

        :param _id: record id

        :return: bool

        ## You can override delete method like this:

        .. code-block:: python
            class MyAwesomeCRUDService(CRUDService[MyAwesomeModel, MyAwesomeCreate, MyAwesomeUpdate]):

                CREATE_MODEL = MyAwesomeCreate
                UPDATE_MODEL = MyAwesomeUpdate

                DB_MODEL = MyAwesomeModel

                async def delete(self, _id: int) -> bool:
                    # do something before delete
                    result = await super().delete(_id)
                    # do something after delete
                    return result
        """
        return await self._delete(_id)

    async def get_by_id(self, task_id: int) -> M:
        """Get record by id"""
        return await self._get_by_id(task_id)

    async def get_all(self) -> Sequence[M]:
        """Get all records"""
        return await self._repo.all()
