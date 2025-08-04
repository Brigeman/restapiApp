#!/bin/bash

# Скрипт для быстрого тестирования API
echo "🧪 Быстрое тестирование API..."

# Проверяем, запущен ли сервер
if ! lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "❌ Сервер не запущен на порту 8000"
    echo "Запустите сначала: ./start_server.sh"
    exit 1
fi

echo "✅ Сервер запущен, начинаем тестирование..."
echo ""

# Тестируем основные эндпоинты
echo "🔍 Тестирование базовых эндпоинтов..."

echo "1. Health check:"
curl -s http://localhost:8000/health | jq '.' 2>/dev/null || curl -s http://localhost:8000/health

echo -e "\n2. Поиск организаций:"
curl -s -X GET "http://localhost:8000/api/v1/organizations/search?name=Рога" \
  -H "X-API-Key: your-secret-api-key-here" | jq '.' 2>/dev/null || \
  curl -s -X GET "http://localhost:8000/api/v1/organizations/search?name=Рога" \
  -H "X-API-Key: your-secret-api-key-here"

echo -e "\n3. Список зданий:"
curl -s -X GET "http://localhost:8000/api/v1/buildings" \
  -H "X-API-Key: your-secret-api-key-here" | jq '.' 2>/dev/null || \
  curl -s -X GET "http://localhost:8000/api/v1/buildings" \
  -H "X-API-Key: your-secret-api-key-here"

echo -e "\n4. Список деятельностей:"
curl -s -X GET "http://localhost:8000/api/v1/activities" \
  -H "X-API-Key: your-secret-api-key-here" | jq '.' 2>/dev/null || \
  curl -s -X GET "http://localhost:8000/api/v1/activities" \
  -H "X-API-Key: your-secret-api-key-here"

echo -e "\n5. Геопоиск в радиусе:"
curl -s -X POST "http://localhost:8000/api/v1/organizations/geo/radius" \
  -H "X-API-Key: your-secret-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{"latitude": 55.7539, "longitude": 37.6208, "radius_km": 1.0}' | jq '.' 2>/dev/null || \
  curl -s -X POST "http://localhost:8000/api/v1/organizations/geo/radius" \
  -H "X-API-Key: your-secret-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{"latitude": 55.7539, "longitude": 37.6208, "radius_km": 1.0}'

echo -e "\n✅ Быстрое тестирование завершено!"
echo ""
echo "💡 Полезные ссылки:"
echo "📚 Swagger UI: http://localhost:8000/docs"
echo "🔍 ReDoc: http://localhost:8000/redoc"
echo "🧪 Полное тестирование: python test_manual.py" 