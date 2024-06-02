from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, Text
from sqlalchemy.dialects.sqlite import INTEGER
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)
from sqlalchemy.sql import func

from src.enums import TodoStatus


class BaseModel(AsyncAttrs, DeclarativeBase):
    """Base Model with id field"""

    # NOTE: SQLite doesn't love BigIntegers as primary keys with autoincrement
    id: Mapped[int] = mapped_column(
        BigInteger().with_variant(
            INTEGER(),
            "sqlite",
            "aiosqlite",
            "sqlite+aiosqlite",
        ),
        primary_key=True,
        autoincrement=True,
    )


class CreateUpdateMixin:
    """Create and Update mixin for common fields"""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
    )


class TodoTask(CreateUpdateMixin, BaseModel):
    """Model for todo tasks"""

    __tablename__ = "todo_tasks"

    title: Mapped[str] = mapped_column(Text, comment="Title of the task")
    description: Mapped[str] = mapped_column(Text, comment="Description of the task")

    status: Mapped[TodoStatus] = mapped_column(
        Enum(TodoStatus),
        default=TodoStatus.PENDING,
        server_default=TodoStatus.PENDING,
        comment="Status of the task",
    )
