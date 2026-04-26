## Архитектура

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Web Server**: Nginx (reverse proxy)
- **Container Orchestration**: Docker Compose


## Получить все задачи
curl -X 'GET' 'http://localhost:8000/tasks/?skip=0&limit=100' -H 'accept: application/json'

## Получить задачу по ID
curl -X 'GET' 'http://localhost:8000/tasks/1' -H 'accept: application/json'

## Создать задачу
curl -X 'POST' 'http://localhost:8000/tasks/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Купить продукты",
    "description": "Молоко, хлеб, яйца",
    "priority": "high",
    "due_date": "2026-03-15T18:00:00"
  }'

## Обновить задачу
curl -X 'PUT' 'http://localhost:8000/tasks/1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "completed": true
  }'

## Удалить задачу
curl -X 'DELETE' 'http://localhost:8000/tasks/2' -H 'accept: application/json'

## Установка и запуск
1. Клонировать репозиторий:
```bash
git clone <repository-url>
cd todo-app

## Локальный запуск
```bash
docker-compose up -d --build
curl http://localhost:8000/health/
