# 🧪 Простое руководство по тестированию

## 🚀 Шаг 1: Запуск сервера

```bash
# Остановите все процессы на порту 8000
pkill -f uvicorn

# Запустите сервер
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

## 🔍 Шаг 2: Тестирование через браузер

Откройте в браузере:
- **Документация**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/health

## 🔧 Шаг 3: Тестирование через curl

### Поиск организаций
```bash
curl -X GET "http://localhost:8000/api/v1/organizations/search?name=Рога" \
  -H "X-API-Key: your-secret-api-key-here"
```

### Список зданий
```bash
curl -X GET "http://localhost:8000/api/v1/buildings" \
  -H "X-API-Key: your-secret-api-key-here"
```

### Геопоиск
```bash
curl -X POST "http://localhost:8000/api/v1/organizations/geo/radius" \
  -H "X-API-Key: your-secret-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{"latitude": 55.7539, "longitude": 37.6208, "radius_km": 1.0}'
```

## 🐍 Шаг 4: Тестирование через Python

```bash
# Простое тестирование (без внешних зависимостей)
python simple_test.py

# Полное тестирование (требует requests)
pip install requests
python test_manual.py
```

## 📊 Шаг 5: Проверка данных

```bash
# Статистика базы данных
sqlite3 organizations.db "SELECT COUNT(*) as total FROM organizations;"
sqlite3 organizations.db "SELECT COUNT(*) as total FROM buildings;"
sqlite3 organizations.db "SELECT COUNT(*) as total FROM activities;"
```

## 🎯 Что должно работать:

1. **Поиск организаций** - должна найтись "ООО 'Рога и Копыта'"
2. **Список зданий** - должно быть 10 зданий
3. **Геопоиск** - должны найтись организации в радиусе от Красной площади
4. **Иерархия деятельностей** - поиск по "Еда" должен найти организации с продуктами

## 🚨 Если что-то не работает:

1. **Сервер не запускается**: `pkill -f uvicorn` затем перезапустите
2. **Ошибки в БД**: `rm organizations.db && python seed_data.py`
3. **Проблемы с зависимостями**: `pip install -r requirements.txt`

## 💡 Полезные команды:

```bash
# Проверка порта
lsof -i :8000

# Остановка сервера
pkill -f uvicorn

# Перезапуск с логами
uvicorn main:app --reload --port 8000 --log-level debug
``` 