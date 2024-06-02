from src.api.v1.schamas import TodoTaskCreate, TodoTaskUpdate
from src.core.service import CRUDService
from src.database import TodoTask


class TodoTasksService(CRUDService[TodoTask, TodoTaskCreate, TodoTaskUpdate]):
    CREATE_MODEL = TodoTaskCreate
    UPDATE_MODEL = TodoTaskUpdate

    DB_MODEL = TodoTask
