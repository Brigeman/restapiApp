# 🧪 Ручное тестирование проекта

## 🚀 Быстрый старт

### 1. Запуск сервера
```bash
# Вариант 1: Через скрипт (рекомендуется)
./start_server.sh

# Вариант 2: Вручную
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

### 2. Быстрое тестирование
```bash
# Автоматическое тестирование основных эндпоинтов
./quick_test.sh

# Или через Python скрипт
python test_manual.py
```

## 🌐 Веб-интерфейс

После запуска сервера откройте в браузере:

- **📚 Swagger UI**: http://localhost:8000/docs
- **🔍 ReDoc**: http://localhost:8000/redoc
- **🏥 Health Check**: http://localhost:8000/health

## 🔍 Тестирование через браузер

### Базовые эндпоинты
- `GET /` - Главная страница
- `GET /health` - Проверка состояния сервера

### Организации
- `GET /api/v1/organizations/search?name=Рога` - Поиск организаций
- `GET /api/v1/organizations/1` - Получить организацию по ID

### Здания
- `GET /api/v1/buildings` - Список всех зданий
- `GET /api/v1/buildings/1` - Получить здание по ID
- `GET /api/v1/buildings/1/organizations` - Организации в здании

### Деятельности
- `GET /api/v1/activities` - Список всех деятельностей
- `GET /api/v1/activities/1` - Получить деятельность по ID
- `GET /api/v1/activities/1/organizations` - Организации по деятельности
- `GET /api/v1/activities/1/organizations/hierarchy?level=3` - По иерархии

## 🔧 Тестирование через curl

### Поиск организаций
```bash
curl -X GET "http://localhost:8000/api/v1/organizations/search?name=Рога" \
  -H "X-API-Key: your-secret-api-key-here"
```

### Получение зданий
```bash
curl -X GET "http://localhost:8000/api/v1/buildings" \
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

### Геопоиск в прямоугольнике
```bash
curl -X POST "http://localhost:8000/api/v1/organizations/geo/rectangle" \
  -H "X-API-Key: your-secret-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "min_lat": 55.75,
    "max_lat": 55.76,
    "min_lon": 37.61,
    "max_lon": 37.62
  }'
```

### Создание нового здания
```bash
curl -X POST "http://localhost:8000/api/v1/buildings" \
  -H "X-API-Key: your-secret-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Новое здание",
    "address": "г. Москва, ул. Тестовая, 123",
    "latitude": 55.7558,
    "longitude": 37.6176
  }'
```

### Поиск по иерархии деятельностей
```bash
curl -X GET "http://localhost:8000/api/v1/activities/1/organizations/hierarchy?level=3" \
  -H "X-API-Key: your-secret-api-key-here"
```

## 🐍 Тестирование через Python

### Простое тестирование (без внешних зависимостей)
```bash
python simple_test.py
```

### Полное тестирование (требует requests)
```bash
pip install requests
python test_manual.py
```

## 📊 Проверка данных

### Статистика базы данных
```bash
# Количество организаций
sqlite3 organizations.db "SELECT COUNT(*) as organizations FROM organizations;"

# Количество зданий
sqlite3 organizations.db "SELECT COUNT(*) as buildings FROM buildings;"

# Количество деятельностей
sqlite3 organizations.db "SELECT COUNT(*) as activities FROM activities;"

# Количество телефонов
sqlite3 organizations.db "SELECT COUNT(*) as phones FROM phones;"
```

### Детальная информация
```bash
# Организации с телефонами
sqlite3 organizations.db "SELECT o.name, COUNT(p.id) as phone_count FROM organizations o LEFT JOIN phones p ON o.id = p.organization_id GROUP BY o.id;"

# Здания с координатами
sqlite3 organizations.db "SELECT name, address, latitude, longitude FROM buildings;"

# Иерархия деятельностей
sqlite3 organizations.db "SELECT name, level, parent_id FROM activities ORDER BY level, name;"
```

## 🎯 Ожидаемые результаты

### Поиск организаций
- Поиск "Рога" должен найти "ООО 'Рога и Копыта'"
- Поиск "Мясо" должен найти "ИП 'Мясо и Молоко'"

### Геопоиск
- Радиус 1 км от Красной площади должен найти 10 организаций
- Прямоугольник должен найти организации в заданной области

### Иерархия деятельностей
- Поиск по "Еда" (ID=1) с level=3 должен найти организации с продуктами
- Поиск по "Автомобили" (ID=2) с level=3 должен найти организации с запчастями

### Создание записей
- Создание здания должно вернуть 201 статус
- Создание деятельности должно вернуть 201 статус
- Создание организации должно вернуть 201 статус

## 🚨 Устранение проблем

### Сервер не запускается
```bash
# Остановка всех процессов на порту 8000
pkill -f uvicorn

# Проверка порта
lsof -i :8000

# Перезапуск
uvicorn main:app --reload --port 8000
```

### Ошибки в базе данных
```bash
# Удаление старой базы
rm organizations.db

# Создание новой базы с тестовыми данными
python seed_data.py
```

### Проблемы с зависимостями
```bash
# Переустановка зависимостей
pip install -r requirements.txt

# Активация виртуального окружения
source venv/bin/activate
```

### Проблемы с Docker
```bash
# Остановка контейнеров
docker-compose down

# Пересборка
docker-compose up --build

# Просмотр логов
docker-compose logs
```

## 💡 Полезные команды

### Мониторинг
```bash
# Проверка здоровья
curl http://localhost:8000/health

# Проверка корневого эндпоинта
curl http://localhost:8000/

# Просмотр логов сервера
tail -f logs/app.log
```

### Отладка
```bash
# Запуск с отладкой
uvicorn main:app --reload --port 8000 --log-level debug

# Проверка переменных окружения
echo $DATABASE_URL
echo $API_KEY

# Проверка версий
python --version
pip list | grep fastapi
```

### Очистка
```bash
# Очистка кэша Python
find . -type d -name "__pycache__" -exec rm -r {} +
find . -name "*.pyc" -delete

# Очистка тестовых файлов
rm -rf .pytest_cache
rm -rf htmlcov
rm .coverage
```

## 📈 Метрики успешного тестирования

- ✅ Сервер запускается без ошибок
- ✅ Health check возвращает 200
- ✅ Swagger UI доступен
- ✅ Поиск организаций работает
- ✅ Геопоиск находит организации
- ✅ Иерархия деятельностей работает
- ✅ Создание записей работает
- ✅ Все эндпоинты отвечают корректно 