# REST API Organizations Directory

REST API приложение для справочника организаций, зданий и деятельностей.

## 🚀 Быстрый старт с Docker

### Вариант 1: Docker Compose (рекомендуется)

```bash
# Клонируйте репозиторий
git clone <repository-url>
cd restapiApp

# Запустите приложение
docker-compose up --build
```

Приложение будет доступно по адресу: http://localhost:8000

### Вариант 2: Docker без Docker Compose

```bash
# Соберите образ (SQLite версия)
docker build -f Dockerfile.sqlite -t organizations-api .

# Запустите контейнер
docker run -p 8000:8000 organizations-api
```

## 🛠 Локальная разработка

### Требования

- Python 3.11+
- pip

### Установка

```bash
# Клонируйте репозиторий
git clone <repository-url>
cd restapiApp

# Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установите зависимости
pip install -r requirements.txt

# Создайте базу данных и заполните тестовыми данными
python seed_data.py

# Запустите приложение
uvicorn main:app --reload
```

## 📚 API Документация

После запуска приложения документация доступна по адресам:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 Аутентификация

Все API запросы требуют API ключ в заголовке:

```
X-API-Key: your-secret-api-key-here
```

## 📋 Основные эндпоинты

### Организации
- `GET /api/v1/organizations/{id}` - Получить организацию по ID
- `GET /api/v1/organizations/search?name={name}` - Поиск организаций по названию
- `POST /api/v1/organizations` - Создать новую организацию

### Здания
- `GET /api/v1/buildings` - Список всех зданий
- `GET /api/v1/buildings/{id}` - Получить здание по ID
- `GET /api/v1/buildings/{id}/organizations` - Организации в здании
- `POST /api/v1/buildings` - Создать новое здание

### Деятельности
- `GET /api/v1/activities` - Список всех деятельностей
- `GET /api/v1/activities/{id}` - Получить деятельность по ID
- `GET /api/v1/activities/{id}/organizations` - Организации по деятельности
- `GET /api/v1/activities/{id}/organizations/hierarchy?level={level}` - Организации по иерархии
- `POST /api/v1/activities` - Создать новую деятельность

### Геопоиск
- `POST /api/v1/organizations/geo/radius` - Поиск организаций в радиусе
- `POST /api/v1/organizations/geo/rectangle` - Поиск организаций в прямоугольной области

## 🧪 Тестирование

```bash
# Запуск всех тестов
pytest test_*.py -v

# Запуск конкретного теста
pytest test_business_logic.py -v

# Запуск тестов с покрытием
pytest --cov=. test_*.py
```

## 🗄 База данных

Приложение использует SQLite для разработки. Для продакшена рекомендуется PostgreSQL.

### Миграции

```bash
# Создать новую миграцию
alembic revision --autogenerate -m "Description"

# Применить миграции
alembic upgrade head

# Откатить миграцию
alembic downgrade -1
```

## 📊 Тестовые данные

Приложение поставляется с тестовыми данными:

- **5 зданий** в разных районах Москвы
- **10 деятельностей** с иерархической структурой
- **5 организаций** с телефонами и связями с деятельностями

Для создания тестовых данных:

```bash
python seed_data.py
```

## 🔧 Конфигурация

Основные настройки в `config.py`:

- `DATABASE_URL` - URL базы данных
- `API_KEY` - Ключ для аутентификации
- `APP_NAME` - Название приложения
- `APP_VERSION` - Версия приложения

## 🐳 Docker команды

```bash
# Сборка образа (SQLite)
docker build -f Dockerfile.sqlite -t organizations-api .

# Сборка образа (PostgreSQL)
docker build -t organizations-api .

# Запуск контейнера
docker run -p 8000:8000 organizations-api

# Просмотр логов
docker logs <container-id>

# Остановка контейнера
docker stop <container-id>
```

## 📝 Примеры запросов

### Поиск организаций по названию
```bash
curl -X GET "http://localhost:8000/api/v1/organizations/search?name=Рога" \
  -H "X-API-Key: your-secret-api-key-here"
```

### Геопоиск в радиусе
```bash
curl -X POST "http://localhost:8000/api/v1/organizations/geo/radius" \
  -H "X-API-Key: your-secret-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 55.7539,
    "longitude": 37.6208,
    "radius_km": 1.0
  }'
```

### Поиск по иерархии деятельностей
```bash
curl -X GET "http://localhost:8000/api/v1/activities/1/organizations/hierarchy?level=3" \
  -H "X-API-Key: your-secret-api-key-here"
```

### Создание нового здания
```bash
curl -X POST "http://localhost:8000/api/v1/buildings" \
  -H "X-API-Key: your-secret-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Новое здание",
    "address": "г. Москва, ул. Новая, 123",
    "latitude": 55.7558,
    "longitude": 37.6176
  }'
```

## 🏗 Архитектура

- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM
- **Alembic** - миграции БД
- **Pydantic** - валидация данных
- **SQLite** - база данных (разработка)
- **Docker** - контейнеризация

## 📈 Мониторинг

- **Health check**: `GET /health`
- **Корневой эндпоинт**: `GET /`

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request

## 📄 Лицензия

MIT License 