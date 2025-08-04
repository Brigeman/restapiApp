#!/usr/bin/env python3
"""
Простой скрипт для тестирования API без внешних зависимостей
Использует встроенные модули Python
"""

import urllib.request
import urllib.parse
import json
import ssl


def test_endpoint(method: str, endpoint: str, data: dict = None, params: dict = None) -> None:
    """Тестирует эндпоинт и выводит результат"""
    url = f"http://localhost:8000{endpoint}"
    
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    print(f"\n🔍 Тестируем: {method} {endpoint}")
    print(f"URL: {url}")
    
    if data:
        print(f"Данные: {json.dumps(data, indent=2, ensure_ascii=False)}")
    
    try:
        # Создаем запрос
        req = urllib.request.Request(url)
        req.add_header('X-API-Key', 'your-secret-api-key-here')
        req.add_header('Content-Type', 'application/json')
        
        if method.upper() == "POST" and data:
            req.data = json.dumps(data).encode('utf-8')
        
        # Отправляем запрос
        with urllib.request.urlopen(req) as response:
            print(f"📊 Статус: {response.status}")
            print("✅ Успешно!")
            
            # Читаем ответ
            result = response.read().decode('utf-8')
            try:
                json_result = json.loads(result)
                print(f"📄 Ответ: {json.dumps(json_result, indent=2, ensure_ascii=False)}")
            except:
                print(f"📄 Ответ: {result}")
                
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Ошибка: {e.code} - {e.reason}")
        try:
            error_body = e.read().decode('utf-8')
            print(f"Детали ошибки: {error_body}")
        except:
            pass
    except urllib.error.URLError as e:
        print(f"❌ Ошибка подключения: {e.reason}")
        print("Убедитесь, что сервер запущен на порту 8000")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


def main():
    """Основная функция тестирования"""
    print("🚀 Начинаем простое тестирование API")
    print("=" * 50)
    
    # 1. Базовые эндпоинты
    print("\n📋 1. Базовые эндпоинты")
    test_endpoint("GET", "/")
    test_endpoint("GET", "/health")
    
    # 2. Организации
    print("\n📋 2. Тестирование организаций")
    test_endpoint("GET", "/api/v1/organizations/search", params={"name": "Рога"})
    test_endpoint("GET", "/api/v1/organizations/1")
    
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
    
    # 6. Создание новых записей
    print("\n📋 6. Тестирование создания записей")
    
    # Создание здания
    building_data = {
        "address": "г. Москва, ул. Тестовая, 123",
        "latitude": 55.7558,
        "longitude": 37.6176
    }
    test_endpoint("POST", "/api/v1/buildings", data=building_data)
    
    print("\n" + "=" * 50)
    print("✅ Простое тестирование завершено!")
    print("\n💡 Полезные ссылки:")
    print("📚 Swagger UI: http://localhost:8000/docs")
    print("🔍 ReDoc: http://localhost:8000/redoc")


if __name__ == "__main__":
    main() 