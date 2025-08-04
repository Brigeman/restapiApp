import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from database import Base, get_db
from main import app


# Создаем тестовую базу данных в памяти
from config import settings

engine = create_engine(
    settings.TEST_DATABASE_URL,
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


def test_create_organization_with_activities(client):
    """Тест создания организации с деятельностями"""
    # Создаем здание
    building_data = {
        "name": "Тестовое здание 1",
        "address": "г. Москва, ул. Ленина 1",
        "latitude": 55.7558,
        "longitude": 37.6176
    }
    response = client.post("/api/v1/buildings", json=building_data, headers={"X-API-Key": "your-secret-api-key-here"})
    assert response.status_code == 201
    building_id = response.json()["id"]
    
    # Создаем деятельность
    activity_data = {
        "name": "Молочная продукция",
        "level": 2,
        "parent_id": None
    }
    response = client.post("/api/v1/activities", json=activity_data, headers={"X-API-Key": "your-secret-api-key-here"})
    assert response.status_code == 201
    activity_id = response.json()["id"]
    
    # Создаем организацию
    org_data = {
        "name": "ООО 'Молоко'",
        "building_id": building_id,
        "phones": [{"number": "2-222-222", "type": "mobile"}, {"number": "3-333-333", "type": "mobile"}],
        "activity_ids": [activity_id]
    }
    response = client.post("/api/v1/organizations", json=org_data, headers={"X-API-Key": "your-secret-api-key-here"})
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == "ООО 'Молоко'"
    assert len(data["phones"]) == 2
    assert len(data["activities"]) == 1
    assert data["activities"][0]["name"] == "Молочная продукция"


def test_activity_hierarchy_validation(client):
    """Тест валидации уровня вложенности деятельностей"""
    # Пытаемся создать деятельность с уровнем > 3
    activity_data = {
        "name": "Слишком глубокий уровень",
        "level": 4,
        "parent_id": None
    }
    response = client.post("/api/v1/activities", json=activity_data, headers={"X-API-Key": "your-secret-api-key-here"})
    assert response.status_code == 422  # Pydantic валидация отклоняет уровень > 3
    assert "level" in response.json()["detail"][0]["loc"]


def test_geo_search_functionality(client):
    """Тест функциональности геопоиска"""
    # Создаем здание
    building_data = {
        "name": "Тестовое здание 2",
        "address": "г. Москва, Красная площадь",
        "latitude": 55.7539,
        "longitude": 37.6208
    }
    response = client.post("/api/v1/buildings", json=building_data, headers={"X-API-Key": "your-secret-api-key-here"})
    assert response.status_code == 201
    building_id = response.json()["id"]
    
    # Создаем организацию
    org_data = {
        "name": "ООО 'Красная площадь'",
        "description": "Организация на Красной площади",
        "address": "г. Москва, Красная площадь",
        "latitude": 55.7539,
        "longitude": 37.6208,
        "building_id": building_id,
        "phones": [{"number": "2-222-222", "type": "mobile"}],
        "activity_ids": []
    }
    response = client.post("/api/v1/organizations", json=org_data, headers={"X-API-Key": "your-secret-api-key-here"})
    assert response.status_code == 201
    
    # Тестируем поиск по радиусу
    search_data = {
        "latitude": 55.7539,
        "longitude": 37.6208,
        "radius_km": 1.0
    }
    response = client.post("/api/v1/organizations/geo/radius", json=search_data, headers={"X-API-Key": "your-secret-api-key-here"})
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["organizations"]) == 1
    assert data["organizations"][0]["name"] == "ООО 'Красная площадь'"


def test_activity_hierarchy_search(client):
    """Тест поиска по иерархии деятельностей"""
    # Создаем родительскую деятельность
    parent_activity = {
        "name": "Еда",
        "level": 1,
        "parent_id": None
    }
    response = client.post("/api/v1/activities", json=parent_activity, headers={"X-API-Key": "your-secret-api-key-here"})
    assert response.status_code == 201
    parent_id = response.json()["id"]
    
    # Создаем дочернюю деятельность
    child_activity = {
        "name": "Молочная продукция",
        "level": 2,
        "parent_id": parent_id
    }
    response = client.post("/api/v1/activities", json=child_activity, headers={"X-API-Key": "your-secret-api-key-here"})
    assert response.status_code == 201
    child_id = response.json()["id"]
    
    # Создаем здание и организацию
    building_data = {
        "name": "Тестовое здание 3",
        "address": "г. Москва, ул. Ленина 1",
        "latitude": 55.7558,
        "longitude": 37.6176
    }
    response = client.post("/api/v1/buildings", json=building_data, headers={"X-API-Key": "your-secret-api-key-here"})
    building_id = response.json()["id"]
    
    org_data = {
        "name": "ООО 'Молоко'",
        "building_id": building_id,
        "phones": [{"number": "2-222-222", "type": "mobile"}],
        "activity_ids": [child_id]
    }
    response = client.post("/api/v1/organizations", json=org_data, headers={"X-API-Key": "your-secret-api-key-here"})
    assert response.status_code == 201
    
    # Тестируем поиск по иерархии (должна найтись организация с дочерней деятельностью)
    response = client.get(f"/api/v1/activities/{parent_id}/organizations/hierarchy?level=3", headers={"X-API-Key": "your-secret-api-key-here"})
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["organizations"]) == 1
    assert data["organizations"][0]["name"] == "ООО 'Молоко'" 