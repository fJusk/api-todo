# api-todo

## О проекте

api-todo - простой набор CRUD операций для управления сущностью "Задача"

### Основные технологии
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- pytests
- sqlite (for tests)
- pre-commit (hooks, mypy, ruff)
- docker

### Решения
- дженерик репо на CRUD операции
- дженерик сервис на CRUD операции (изначально идея была получить аналог GenericView из DRF, но до конкретной реализации еще далеко)
- ответственность за валидацию полностью на pydantic
- стандартное версионирование api

## Запуск проекта

### From Docker
1. Определить .env переменные проекта (для разработки можно просто скопировать из .env)
2. Выполнить комманду
```bash
docker-compose up -d
```

- автоматически поднимется база PostgreSQL
- автоматически выполнятся миграции Alembic
- запустится приложение на порте 8000

### Without Docker
1. Установка зависимостей

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Миграции Alembic

```bash
alembic upgrade head
```

3. Запуск приложения
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
