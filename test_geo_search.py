import pytest
from fastapi.testclient import TestClient
from main import app


def test_search_organizations_by_radius():
    """Тест поиска организаций в радиусе"""
    client = TestClient(app)
    search_data = {
        "latitude": 55.7558,
        "longitude": 37.6176,
        "radius_km": 1.0
    }
    response = client.post("/api/v1/organizations/geo/radius", json=search_data, headers={"X-API-Key": "your-secret-api-key-here"})
    assert response.status_code == 200
    data = response.json()
    assert "organizations" in data
    assert "total" in data


def test_search_organizations_by_rectangle():
    """Тест поиска организаций в прямоугольной области"""
    client = TestClient(app)
    search_data = {
        "min_lat": 55.7500,
        "max_lat": 55.7600,
        "min_lon": 37.6000,
        "max_lon": 37.6200
    }
    response = client.post("/api/v1/organizations/geo/rectangle", json=search_data, headers={"X-API-Key": "your-secret-api-key-here"})
    assert response.status_code == 200
    data = response.json()
    assert "organizations" in data
    assert "total" in data


def test_search_organizations_by_activity_hierarchy():
    """Тест поиска организаций по иерархии деятельности"""
    client = TestClient(app)
    response = client.get("/api/v1/activities/1/organizations/hierarchy", headers={"X-API-Key": "your-secret-api-key-here"})
    # Пока что должно вернуть 404, так как деятельность не существует
    assert response.status_code == 404 