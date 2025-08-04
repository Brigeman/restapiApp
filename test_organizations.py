import pytest
from fastapi.testclient import TestClient
from main import app


def test_get_organization_without_api_key():
    """Тест получения организации без API ключа - должен вернуть 401"""
    client = TestClient(app)
    response = client.get("/api/v1/organizations/1")
    assert response.status_code == 401


def test_get_organization_with_invalid_api_key():
    """Тест получения организации с неверным API ключом - должен вернуть 401"""
    client = TestClient(app)
    response = client.get("/api/v1/organizations/1", headers={"X-API-Key": "invalid-key"})
    assert response.status_code == 401


def test_get_organization_with_valid_api_key():
    """Тест получения организации с правильным API ключом"""
    client = TestClient(app)
    response = client.get("/api/v1/organizations/999", headers={"X-API-Key": "your-secret-api-key-here"})
    # Должно вернуть 404, так как организация с ID 999 не существует
    assert response.status_code == 404


def test_search_organizations_by_name():
    """Тест поиска организаций по названию"""
    client = TestClient(app)
    response = client.get("/api/v1/organizations/search?name=test", headers={"X-API-Key": "your-secret-api-key-here"})
    assert response.status_code == 200
    data = response.json()
    assert "organizations" in data
    assert "total" in data 