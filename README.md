# MKLuna - REST API для справочника организаций

REST API приложение для управления справочником организаций, зданий и видов деятельности.

## Стек

- FastAPI
- SQLAlchemy + Alembic
- PostgreSQL + PostGIS
- Docker

## Архитектура

- Clean Architecture
- DDD (Domain-Driven Design)
- Repository pattern
- Dependency Injection (Dishka)

## Запуск

```bash
docker-compose up --build
```

API доступно на `http://localhost:8000`

Swagger документация: `http://localhost:8000/docs`

## Endpoints

### Organizations
- `GET /organizations/{id}` - информация об организации
- `GET /organizations/?building_id={id}` - организации в здании
- `GET /organizations/?latitude=0&longitude=0&radius=50000` - организации в радиусе
- `GET /organizations/search?name={name}` - поиск по названию
- `GET /organizations/search/by-activity/{activity_id}` - поиск по виду деятельности (с учётом дерева)

### Buildings
- `GET /buildings/?page=1&size=10` - список зданий

### Activities
- `GET /activities/?page=1&size=10` - список видов деятельности

## База данных

При первом запуске:
1. Применяются миграции Alembic
2. Автоматически заполняются тестовые данные
3. Создаётся структура с 5 зданиями, 8 видами деятельности и 7 организациями


## Запуск

1. Создать .env и настроить переменные окружения (пример в .env_example)
2. Запуск: docker compose up --build
