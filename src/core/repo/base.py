from abc import ABC, abstractmethod
from typing import Any, Sequence


class ABCRepo(ABC):
    @abstractmethod
    async def get_by_pk(self, pk: Any) -> Any:
        """Get model by primary key"""
        ...

    @abstractmethod
    async def all(self) -> Sequence[Any] | Any:
        """Get all models"""
        ...

    @abstractmethod
    async def create(self, model: Any) -> Any:
        """Create new model"""
        ...

    @abstractmethod
    async def update(self, model: Any) -> Any:
        """Update model"""
        ...

    @abstractmethod
    async def delete(self, model: Any) -> Any:
        """Delete model"""
        ...
