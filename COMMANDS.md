# 🚀 Основные команды проекта

## 📦 Установка и настройка

```bash
# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements.txt

# Создание базы данных и тестовых данных
python seed_data.py
```

## 🏃‍♂️ Запуск приложения

```bash
# Локальный запуск
uvicorn main:app --reload --port 8000

# Запуск в фоновом режиме
uvicorn main:app --reload --port 8000 &
```

## 🧪 Тестирование

```bash
# Запуск всех тестов
pytest test_*.py -v

# Запуск конкретного теста
pytest test_business_logic.py -v

# Запуск тестов с покрытием
pytest --cov=. test_*.py

# Запуск тестов с реальными данными
pytest test_api_with_data.py -v
```

## 🗄 База данных

```bash
# Создание новой миграции
alembic revision --autogenerate -m "Описание изменений"

# Применение миграций
alembic upgrade head

# Откат миграции
alembic downgrade -1

# Просмотр истории миграций
alembic history
```

## 🐳 Docker команды

```bash
# Сборка образа (SQLite версия)
docker build -f Dockerfile.sqlite -t organizations-api .

# Сборка образа (PostgreSQL версия)
docker build -t organizations-api .

# Запуск контейнера
docker run -p 8000:8000 organizations-api

# Запуск с Docker Compose
docker-compose up --build

# Остановка Docker Compose
docker-compose down

# Просмотр логов
docker logs <container-id>

# Остановка контейнера
docker stop <container-id>
```

## 🔍 API тестирование

```bash
# Поиск организаций
curl -X GET "http://localhost:8000/api/v1/organizations/search?name=Рога" \
  -H "X-API-Key: your-secret-api-key-here"

# Получение зданий
curl -X GET "http://localhost:8000/api/v1/buildings" \
  -H "X-API-Key: your-secret-api-key-here"

# Геопоиск в радиусе
curl -X POST "http://localhost:8000/api/v1/organizations/geo/radius" \
  -H "X-API-Key: your-secret-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 55.7539,
    "longitude": 37.6208,
    "radius_km": 1.0
  }'

# Поиск по иерархии деятельностей
curl -X GET "http://localhost:8000/api/v1/activities/1/organizations/hierarchy?level=3" \
  -H "X-API-Key: your-secret-api-key-here"

# Создание нового здания
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

## 📊 Покрытие кода

```bash
# Запуск тестов с покрытием
pytest --cov=. test_*.py

# Генерация HTML отчета
pytest --cov=. --cov-report=html test_*.py

# Просмотр отчета
open htmlcov/index.html  # Mac
# или
start htmlcov/index.html  # Windows
```

## 🔧 Разработка

```bash
# Запуск сервера разработки
uvicorn main:app --reload --port 8000

# Запуск с отладкой
uvicorn main:app --reload --port 8000 --log-level debug

# Проверка синтаксиса
python -m py_compile *.py

# Проверка импортов
python -c "import main; import routers; import models; import schemas"
```

## 📝 Документация

```bash
# Генерация документации API
# (автоматически доступна по адресу http://localhost:8000/docs)

# Просмотр документации
open http://localhost:8000/docs  # Mac
# или
start http://localhost:8000/docs  # Windows
```

## 🐛 Отладка

```bash
# Просмотр логов сервера
tail -f logs/app.log

# Проверка портов
lsof -i :8000

# Остановка всех процессов на порту
pkill -f uvicorn
```

## 📈 Мониторинг

```bash
# Проверка здоровья приложения
curl http://localhost:8000/health

# Статистика базы данных
sqlite3 organizations.db "SELECT COUNT(*) as organizations FROM organizations;"
sqlite3 organizations.db "SELECT COUNT(*) as buildings FROM buildings;"
sqlite3 organizations.db "SELECT COUNT(*) as activities FROM activities;"
```

## 🚀 Продакшн

```bash
# Сборка продакшн образа
docker build -f Dockerfile.sqlite -t organizations-api:prod .

# Запуск в продакшне
docker run -d -p 8000:8000 --name organizations-api organizations-api:prod

# Просмотр логов продакшн
docker logs organizations-api
``` 