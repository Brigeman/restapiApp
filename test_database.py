import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base, get_db
from main import app


# Создаем тестовую базу данных в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Переопределяем зависимость для тестов"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client():
    """Фикстура для тестового клиента с тестовой БД"""
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    
    # Переопределяем зависимость
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Очищаем
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def test_create_and_get_building(client):
    """Тест создания и получения здания"""
    # Создаем здание
    building_data = {
        "name": "Тестовое здание БД 1",
        "address": "г. Москва, ул. Ленина 1, офис 3",
        "latitude": 55.7558,
        "longitude": 37.6176
    }
    
    response = client.post("/api/v1/buildings", json=building_data, headers={"X-API-Key": "your-secret-api-key-here"})
    assert response.status_code == 201
    
    data = response.json()
    building_id = data["id"]
    assert data["address"] == "г. Москва, ул. Ленина 1, офис 3"
    assert data["latitude"] == 55.7558
    assert data["longitude"] == 37.6176
    
    # Получаем здание
    response = client.get(f"/api/v1/buildings/{building_id}", headers={"X-API-Key": "your-secret-api-key-here"})
    assert response.status_code == 200
    
    data = response.json()
    assert data["address"] == "г. Москва, ул. Ленина 1, офис 3"


def test_get_buildings_list(client):
    """Тест получения списка зданий"""
    # Создаем несколько зданий
    buildings_data = [
        {
            "name": "Тестовое здание БД 2",
            "address": "г. Москва, ул. Ленина 1",
            "latitude": 55.7558,
            "longitude": 37.6176
        },
        {
            "name": "Тестовое здание БД 3",
            "address": "г. Москва, ул. Пушкина 10",
            "latitude": 55.7558,
            "longitude": 37.6176
        }
    ]
    
    for building_data in buildings_data:
        response = client.post("/api/v1/buildings", json=building_data, headers={"X-API-Key": "your-secret-api-key-here"})
        assert response.status_code == 201
    
    # Получаем список зданий
    response = client.get("/api/v1/buildings", headers={"X-API-Key": "your-secret-api-key-here"})
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["buildings"]) == 2
    assert data["total"] == 2 