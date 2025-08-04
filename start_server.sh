#!/bin/bash

# Скрипт для запуска сервера
echo "🚀 Запуск REST API сервера..."

# Проверяем, запущен ли уже сервер
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Сервер уже запущен на порту 8000"
    echo "Остановка предыдущего процесса..."
    pkill -f uvicorn
    sleep 2
fi

# Активируем виртуальное окружение
source venv/bin/activate

# Проверяем, есть ли тестовые данные
if [ ! -f "organizations.db" ]; then
    echo "📊 Создание тестовых данных..."
    python seed_data.py
fi

# Запускаем сервер
echo "🌐 Запуск сервера на http://localhost:8000"
echo "📚 Документация: http://localhost:8000/docs"
echo "🔍 ReDoc: http://localhost:8000/redoc"
echo "🏥 Health check: http://localhost:8000/health"
echo ""
echo "Для остановки сервера нажмите Ctrl+C"
echo ""

uvicorn main:app --reload --port 8000 --host 0.0.0.0 