from pydantic import BaseModel

from src.enums import TodoStatus


class BaseTodoTask(BaseModel):
    title: str
    description: str
    status: TodoStatus


class TodoTaskCreate(BaseModel):
    title: str
    description: str


class TodoTaskUpdate(BaseTodoTask):
    pass


class TodoTaskResponse(BaseTodoTask):
    id: int

    class Config:
        from_attributes = True
