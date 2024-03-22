# Описание

## Технологии
1. FastAPI
2. SQLAlchemy + asyncpg
3. Alembic

## Миграции

Для создания миграции (directory: fast_landings):
```bash
alembic revision --autogenerate
```

Для применения всех миграций (directory: fast_landings):
```bash
alembic upgrade head
```

## Локальный запуск

Креды в файле .env

Запуск сервера (ldirectory: fast_landings/app)
```bash
uvicorn app:app --host 0.0.0.0 --port {port}
```