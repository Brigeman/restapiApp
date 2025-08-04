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
- `GET /api/v1/activities/1/organizations/hierarchy` - По иерархии

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
    "address": "г. Москва, ул. Тестовая, 123",
    "latitude": 55.7558,
    "longitude": 37.6176
  }'
```

### Создание новой деятельности
```bash
curl -X POST "http://localhost:8000/api/v1/activities" \
  -H "X-API-Key: your-secret-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Тестовая деятельность",
    "level": 1,
    "parent_id": null
  }'
```

## 🧪 Тестирование через Python

### Запуск автоматического тестирования
```bash
python test_manual.py
```

### Интерактивное тестирование в Python
```python
import requests

# Конфигурация
BASE_URL = "http://localhost:8000"
API_KEY = "your-secret-api-key-here"
HEADERS = {"X-API-Key": API_KEY}

# Тестирование поиска организаций
response = requests.get(
    f"{BASE_URL}/api/v1/organizations/search?name=Рога",
    headers=HEADERS
)
print(f"Статус: {response.status_code}")
print(f"Ответ: {response.json()}")

# Тестирование геопоиска
geo_data = {
    "latitude": 55.7539,
    "longitude": 37.6208,
    "radius_km": 1.0
}
response = requests.post(
    f"{BASE_URL}/api/v1/organizations/geo/radius",
    headers=HEADERS,
    json=geo_data
)
print(f"Геопоиск статус: {response.status_code}")
print(f"Результат: {response.json()}")
```

## 📊 Проверка данных

### Просмотр базы данных
```bash
# Статистика организаций
sqlite3 organizations.db "SELECT COUNT(*) as total FROM organizations;"

# Статистика зданий
sqlite3 organizations.db "SELECT COUNT(*) as total FROM buildings;"

# Статистика деятельностей
sqlite3 organizations.db "SELECT COUNT(*) as total FROM activities;"

# Просмотр организаций
sqlite3 organizations.db "SELECT id, name FROM organizations LIMIT 5;"

# Просмотр иерархии деятельностей
sqlite3 organizations.db "SELECT id, name, level, parent_id FROM activities ORDER BY level, id;"
```

## 🔍 Отладка

### Проверка логов сервера
```bash
# Запуск с подробными логами
uvicorn main:app --reload --port 8000 --log-level debug
```

### Проверка подключения
```bash
# Проверка, что сервер отвечает
curl -I http://localhost:8000/health

# Проверка порта
lsof -i :8000
```

### Проверка API ключа
```bash
# Без API ключа (должно вернуть 401)
curl -X GET "http://localhost:8000/api/v1/buildings"

# С неправильным API ключом (должно вернуть 401)
curl -X GET "http://localhost:8000/api/v1/buildings" \
  -H "X-API-Key: wrong-key"

# С правильным API ключом (должно вернуть 200)
curl -X GET "http://localhost:8000/api/v1/buildings" \
  -H "X-API-Key: your-secret-api-key-here"
```

## 🎯 Сценарии тестирования

### 1. Поиск организаций
- ✅ Поиск по названию "Рога" → должна найтись "ООО 'Рога и Копыта'"
- ✅ Поиск по названию "Авто" → должны найтись организации с автомобилями
- ✅ Поиск несуществующей организации → пустой список

### 2. Геопоиск
- ✅ Поиск в радиусе 1 км от Красной площади → должны найтись организации
- ✅ Поиск в прямоугольной области → должны найтись организации в области
- ✅ Поиск в пустой области → пустой список

### 3. Иерархия деятельностей
- ✅ Поиск по "Еда" → должны найтись организации с мясной и молочной продукцией
- ✅ Поиск по "Автомобили" → должны найтись организации с автозапчастями
- ✅ Поиск по "Запчасти" → должны найтись организации с запчастями

### 4. Создание записей
- ✅ Создание здания → должен вернуться ID нового здания
- ✅ Создание деятельности → должен вернуться ID новой деятельности
- ✅ Создание организации → должен вернуться ID новой организации

## 🚨 Устранение проблем

### Сервер не запускается
```bash
# Проверка порта
lsof -i :8000

# Остановка процессов на порту
pkill -f uvicorn

# Перезапуск
./start_server.sh
```

### Ошибки в базе данных
```bash
# Пересоздание тестовых данных
rm organizations.db
python seed_data.py
```

### Проблемы с зависимостями
```bash
# Переустановка зависимостей
pip install -r requirements.txt --force-reinstall
```

## 📈 Мониторинг производительности

### Время ответа API
```bash
# Измерение времени ответа
time curl -X GET "http://localhost:8000/api/v1/buildings" \
  -H "X-API-Key: your-secret-api-key-here"
```

### Размер базы данных
```bash
# Проверка размера файла БД
ls -lh organizations.db
```

### Статистика запросов
```bash
# Подсчет записей в таблицах
sqlite3 organizations.db "SELECT 'organizations' as table_name, COUNT(*) as count FROM organizations UNION ALL SELECT 'buildings', COUNT(*) FROM buildings UNION ALL SELECT 'activities', COUNT(*) FROM activities;"
``` 