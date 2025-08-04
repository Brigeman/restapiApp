import pytest
from fastapi.testclient import TestClient
from main import app


def test_health_check():
    """Тест проверки здоровья приложения"""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint():
    """Тест корневого эндпоинта"""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data 