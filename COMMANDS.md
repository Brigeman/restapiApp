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
# Сборка образа
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
curl -X GET "http://localhost:8000/api/v1/activities/1/organizations/hierarchy" \
  -H "X-API-Key: your-secret-api-key-here"
```

## 📚 Документация

```bash
# Swagger UI
open http://localhost:8000/docs

# ReDoc
open http://localhost:8000/redoc

# Health check
curl http://localhost:8000/health
```

## 🛠 Разработка

```bash
# Проверка синтаксиса
python -m py_compile main.py

# Проверка импортов
python -c "import main; print('✅ Импорты корректны')"

# Очистка кэша
find . -type d -name "__pycache__" -exec rm -r {} +
find . -name "*.pyc" -delete

# Перезапуск сервера
pkill -f uvicorn
uvicorn main:app --reload --port 8000
```

## 📊 Мониторинг

```bash
# Проверка процессов
ps aux | grep uvicorn

# Проверка портов
lsof -i :8000

# Проверка размера базы данных
ls -lh organizations.db

# Статистика базы данных
sqlite3 organizations.db "SELECT COUNT(*) as total_organizations FROM organizations;"
```

## 🔧 Отладка

```bash
# Запуск с отладкой
uvicorn main:app --reload --port 8000 --log-level debug

# Проверка переменных окружения
echo $DATABASE_URL

# Проверка зависимостей
pip list

# Проверка версии Python
python --version
```

## 🚀 Продакшн

```bash
# Сборка для продакшна
docker build -t organizations-api:prod .

# Запуск в продакшне
docker run -d -p 8000:8000 --name organizations-api organizations-api:prod

# Проверка статуса
docker ps

# Просмотр логов
docker logs organizations-api
```

## 📝 Git команды

```bash
# Проверка статуса
git status

# Добавление файлов
git add .

# Создание коммита
git commit -m "feat: add Docker containerization and documentation"

# Отправка в репозиторий
git push origin main

# Просмотр истории
git log --oneline
``` 