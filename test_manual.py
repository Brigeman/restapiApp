#!/usr/bin/env python3
"""
Скрипт для ручного тестирования API
Запуск: python test_manual.py
"""

import requests
import json
from typing import Dict, Any

# Конфигурация
BASE_URL = "http://localhost:8000"
API_KEY = "your-secret-api-key-here"
HEADERS = {"X-API-Key": API_KEY}


def test_endpoint(method: str, endpoint: str, data: Dict[str, Any] = None, params: Dict[str, Any] = None) -> None:
    """Тестирует эндпоинт и выводит результат"""
    url = f"{BASE_URL}{endpoint}"
    
    print(f"\n🔍 Тестируем: {method} {endpoint}")
    print(f"URL: {url}")
    
    if data:
        print(f"Данные: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    if params:
        print(f"Параметры: {params}")
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=HEADERS, params=params)
        elif method.upper() == "POST":
            response = requests.post(url, headers=HEADERS, json=data)
        else:
            print(f"❌ Неподдерживаемый метод: {method}")
            return
        
        print(f"📊 Статус: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Успешно!")
            try:
                result = response.json()
                print(f"📄 Ответ: {json.dumps(result, indent=2, ensure_ascii=False)}")
            except:
                print(f"📄 Ответ: {response.text}")
        else:
            print(f"❌ Ошибка: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Не удалось подключиться к серверу. Убедитесь, что сервер запущен на порту 8000")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


def main():
    """Основная функция тестирования"""
    print("🚀 Начинаем ручное тестирование API")
    print("=" * 50)
    
    # 1. Базовые эндпоинты
    print("\n📋 1. Базовые эндпоинты")
    test_endpoint("GET", "/")
    test_endpoint("GET", "/health")
    
    # 2. Организации
    print("\n📋 2. Тестирование организаций")
    test_endpoint("GET", "/api/v1/organizations/search", params={"name": "Рога"})
    test_endpoint("GET", "/api/v1/organizations/1")
    test_endpoint("GET", "/api/v1/organizations/999")  # Несуществующая организация
    
    # 3. Здания
    print("\n📋 3. Тестирование зданий")
    test_endpoint("GET", "/api/v1/buildings")
    test_endpoint("GET", "/api/v1/buildings/1")
    test_endpoint("GET", "/api/v1/buildings/1/organizations")
    
    # 4. Деятельности
    print("\n📋 4. Тестирование деятельностей")
    test_endpoint("GET", "/api/v1/activities")
    test_endpoint("GET", "/api/v1/activities/1")
    test_endpoint("GET", "/api/v1/activities/1/organizations")
    test_endpoint("GET", "/api/v1/activities/1/organizations/hierarchy")
    
    # 5. Геопоиск
    print("\n📋 5. Тестирование геопоиска")
    radius_data = {
        "latitude": 55.7539,
        "longitude": 37.6208,
        "radius_km": 1.0
    }
    test_endpoint("POST", "/api/v1/organizations/geo/radius", data=radius_data)
    
    rectangle_data = {
        "min_lat": 55.75,
        "max_lat": 55.76,
        "min_lon": 37.61,
        "max_lon": 37.62
    }
    test_endpoint("POST", "/api/v1/organizations/geo/rectangle", data=rectangle_data)
    
    # 6. Создание новых записей
    print("\n📋 6. Тестирование создания записей")
    
    # Создание здания
    building_data = {
        "address": "г. Москва, ул. Тестовая, 123",
        "latitude": 55.7558,
        "longitude": 37.6176
    }
    test_endpoint("POST", "/api/v1/buildings", data=building_data)
    
    # Создание деятельности
    activity_data = {
        "name": "Тестовая деятельность",
        "level": 1,
        "parent_id": None
    }
    test_endpoint("POST", "/api/v1/activities", data=activity_data)
    
    print("\n" + "=" * 50)
    print("✅ Ручное тестирование завершено!")
    print("\n💡 Дополнительные команды для тестирования:")
    print("curl -X GET 'http://localhost:8000/api/v1/buildings' -H 'X-API-Key: your-secret-api-key-here'")
    print("curl -X GET 'http://localhost:8000/docs' # Swagger документация")


if __name__ == "__main__":
    main() 