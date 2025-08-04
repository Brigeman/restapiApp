import pytest
from fastapi.testclient import TestClient
from main import app


def test_get_buildings_without_api_key():
    """Тест получения списка зданий без API ключа - должен вернуть 401"""
    client = TestClient(app)
    response = client.get("/api/v1/buildings")
    assert response.status_code == 401


def test_get_buildings_with_valid_api_key():
    """Тест получения списка зданий с правильным API ключом"""
    client = TestClient(app)
    response = client.get("/api/v1/buildings", headers={"X-API-Key": "your-secret-api-key-here"})
    assert response.status_code == 200
    data = response.json()
    assert "buildings" in data
    assert "total" in data


def test_get_building_by_id():
    """Тест получения здания по ID"""
    client = TestClient(app)
    response = client.get("/api/v1/buildings/1", headers={"X-API-Key": "your-secret-api-key-here"})
    # Пока что должно вернуть 404, так как здание не существует
    assert response.status_code == 404


def test_get_organizations_by_building():
    """Тест получения организаций в конкретном здании"""
    client = TestClient(app)
    response = client.get("/api/v1/buildings/1/organizations", headers={"X-API-Key": "your-secret-api-key-here"})
    # Пока что должно вернуть 404, так как здание не существует
    assert response.status_code == 404


def test_create_building():
    """Тест создания здания"""
    client = TestClient(app)
    building_data = {
        "address": "г. Москва, ул. Ленина 1, офис 3",
        "latitude": 55.7558,
        "longitude": 37.6176
    }
    response = client.post("/api/v1/buildings", json=building_data, headers={"X-API-Key": "your-secret-api-key-here"})
    # Пока что должно вернуть 404, так как база данных не настроена
    assert response.status_code == 404 