import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repo import Repository
from src.database.models import TodoTask
from src.enums import TodoStatus


@pytest.mark.asyncio
async def test_create_todo(test_client: TestClient, sqlite_session: AsyncSession):
    response = test_client.post("/api/v1/tasks", json={"title": "test_title", "description": "test_description"})
    assert response.status_code == 201

    data = await Repository(TodoTask, sqlite_session).all()

    # NOTE: проверяем кол-во созданных записей
    assert len(data) == 1

    record = data[0]

    assert record.title == "test_title"
    assert record.description == "test_description"

    # NOTE: проверяем, что по-умолчанию статус задачи - PENDING
    assert record.status == TodoStatus.PENDING


@pytest.mark.asyncio
async def test_get_all_todos(test_client: TestClient, sqlite_session: AsyncSession):
    records = [
        TodoTask(title="test_title_1", description="test_description_1"),
        TodoTask(title="test_title_2", description="test_description_2"),
        TodoTask(title="test_title_3", description="test_description_3"),
    ]

    repo = Repository(TodoTask, sqlite_session)

    for record in records:
        await repo.create(record)

    await repo.commit()

    response = test_client.get("/api/v1/tasks")
    assert response.status_code == 200

    data = response.json()

    # NOTE: проверяем кол-во созданных записей
    assert len(data) == 3

    # NOTE: проверяем, что возвращаются все записи которые были созданы
    response_titles = {record["title"] for record in data}
    test_titles = {record.title for record in records}

    assert response_titles == test_titles

    response_descriptions = {record["description"] for record in data}
    test_descriptions = {record.description for record in records}

    assert response_descriptions == test_descriptions


@pytest.mark.asyncio
async def test_get_todo_by_id(test_client: TestClient, sqlite_session: AsyncSession):
    records = [
        TodoTask(title="test_title_1", description="test_description_1"),
        TodoTask(title="test_title_2", description="test_description_2"),
        TodoTask(title="test_title_3", description="test_description_3"),
    ]

    repo = Repository(TodoTask, sqlite_session)

    for record in records:
        await repo.create(record)

    await repo.commit()

    # NOTE: проверяем, что возвращаются все записи которые были созданы
    response = test_client.get("/api/v1/tasks/1")
    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "test_title_1"
    assert data["description"] == "test_description_1"

    # NOTE: проверяем, что возвращается 404 если задачи с таким id не существует
    response = test_client.get("/api/v1/tasks/4")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_todo(test_client: TestClient, sqlite_session: AsyncSession):
    records = [
        TodoTask(title="test_title_1", description="test_description_1"),
        TodoTask(title="test_title_2", description="test_description_2"),
        TodoTask(title="test_title_3", description="test_description_3"),
    ]

    repo = Repository(TodoTask, sqlite_session)

    for record in records:
        await repo.create(record)

    await repo.commit()

    # NOTE: проверяем обновление записи
    response = test_client.put(
        "/api/v1/tasks/1",
        json={
            "title": "test_title_1",
            "description": "test_description_1",
            "status": "in_progress",
        },
    )
    assert response.status_code == 200

    data = response.json()

    # NOTE: проверяем что запись обновилась в ответе
    assert data["status"] == TodoStatus.IN_PROGRESS

    sqlite_session.expire_all()

    record_db = await repo.get_by_pk(1)

    assert record_db is not None

    # NOTE: проверяем что запись обновилась в базе
    assert record_db.title == "test_title_1"
    assert record_db.description == "test_description_1"
    assert record_db.status == TodoStatus.IN_PROGRESS


@pytest.mark.asyncio
async def test_delete_todo(test_client: TestClient, sqlite_session: AsyncSession):
    records = [
        TodoTask(title="test_title_1", description="test_description_1"),
        TodoTask(title="test_title_2", description="test_description_2"),
        TodoTask(title="test_title_3", description="test_description_3"),
    ]

    repo = Repository(TodoTask, sqlite_session)

    for record in records:
        await repo.create(record)

    await repo.commit()

    # NOTE: проверяем удаление записи
    response = test_client.delete("/api/v1/tasks/1")
    assert response.status_code == 200

    sqlite_session.expire_all()

    # NOTE: проверяем что запись удалена
    record_db = await repo.get_by_pk(1)

    assert record_db is None


@pytest.mark.asyncio
async def test_bad_create_request(test_client: TestClient, sqlite_session: AsyncSession):
    record = TodoTask(title="test_title", description="test_description")

    repo = Repository(TodoTask, sqlite_session)
    await repo.create(record)
    await repo.commit()

    # NOTE: пробуем обновить с пользовательским статусом
    response = test_client.put(
        "/api/v1/tasks/1",
        json={
            "title": "test_title",
            "description": "test_description",
            "status": "bad_status",
        },
    )
    assert response.status_code == 422
