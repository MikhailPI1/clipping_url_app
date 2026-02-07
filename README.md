# URL Shortener API
FastAPI-приложение для сокращения URL-адресов с отслеживанием статистики переходов.

## Настройка окружения
```bash
python3.13 -m venv venv

venv\Scripts\activate

pip install .

python -m uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8000
```
Доступ к документации
После запуска откройте:

Swagger UI: http://localhost:8000/docs

## API Endpoints
1. Создание короткой ссылки
POST /shorten

Request Body:

```bash
{
  "url": "https://example.com/very-long-url",
  "custom_code": "mycode123"
}
```
Response:
```bash
{
  "short_code": "abc123",
  "short_url": "http://localhost:8000/abc123",
  "original_url": "https://example.com/very-long-url",
  "created_at": "2024-01-15T12:00:00"
}
```
2. Переход по короткой ссылке
GET /{short_code}
Редирект на оригинальный URL со статусом 302.

3. Получение информации о ссылке
GET /urls/{short_code}/info

Response:

```bash
{
  "short_code": "abc123",
  "original_url": "https://example.com",
  "clicks": 42,
  "created_at": "2024-01-15T12:00:00",
  "short_url": "http://localhost:8000/abc123"
}
```

4. Получение всех ссылок (отладка)
GET /urls/all
Возвращает список всех сокращенных URL в системе.

## Структура проекта
```text
cut_url_app/
├── src/
│   ├── app/
│   │   ├── main.py
│   │   └── routers/
│   │       └── url.py
│   ├── db/
│   │   ├── db_con.py
│   │   └── db_func.py
│   ├── logs/
│   │   └── logger.py
│   └── utils/
│       └── utils.py
└── README.md
```
### Технологии
FastAPI - асинхронный веб-фреймворк

SQLite - база данных

Uvicorn - ASGI-сервер

Pydantic - валидация данных

### Логирование
Приложение логирует все запросы к API через декоратор @log_endpoint.

## Рекомендации по улучшению
1. Понижение версии Python
Текущая: Python 3.13
Рекомендуемая: Python 3.11
Причина: Большая стабильность, лучшая поддержка библиотек

2. Миграция на асинхронную БД
Текущая: SQLite (синхронная)
Рекомендуемая: PostgreSQL + asyncpg
Причина: Лучшая синергия с FastAPI, настоящая асинхронность

3. Усовершенствовать логгер
Заменить декораторы на middleware

Добавить структурированное логирование (JSON)

Логирование в файл + консоль

4. Добавить тесты
bash
tests/
├── test_api.py
├── test_db.py
└── test_utils.py

# Запуск тестов
pytest tests/ -v
