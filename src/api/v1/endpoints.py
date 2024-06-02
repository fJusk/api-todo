from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.depends.session import get_session
from src.services import TodoTasksService

from ..schemas import DefaultResponse
from .schamas import TodoTaskCreate, TodoTaskResponse, TodoTaskUpdate

router = APIRouter(
    prefix="/api/v1",
    tags=[
        "todos",
        "v1",
    ],
)


@router.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def get_task_by_id(task_id: int, session: Annotated[AsyncSession, Depends(get_session)]) -> TodoTaskResponse:
    """
    Get task by id and return task
    """
    return await TodoTasksService(session).get_by_id(task_id)


@router.get("/tasks", status_code=status.HTTP_200_OK)
async def get_tasks(session: Annotated[AsyncSession, Depends(get_session)]) -> Sequence[TodoTaskResponse]:
    """
    Get all tasks
    """
    return await TodoTasksService(session).get_all()


@router.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(data: TodoTaskCreate, session: Annotated[AsyncSession, Depends(get_session)]) -> TodoTaskResponse:
    """
    Create new task and return created task

    :param data: task data

    :return: created task
    """
    return await TodoTasksService(session).create(data)


@router.put("/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def update_task(task_id: int, data: TodoTaskUpdate, session: Annotated[AsyncSession, Depends(get_session)]) -> TodoTaskResponse:
    """
    Update task by id and return updated task

    :param task_id: task id
    :param data: task data

    :return: updated task
    """
    return await TodoTasksService(session).update(task_id, data)


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, session: Annotated[AsyncSession, Depends(get_session)]) -> DefaultResponse:
    """
    Delete task by id and return success status

    :param task_id: task id
    :param session: database session

    :return: success status
    """
    res = await TodoTasksService(session).delete(task_id)

    return DefaultResponse(
        success=res,
        message="Task deleted successfully" if res else "Task deletion failed",
    )
