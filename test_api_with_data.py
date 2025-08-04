import pytest
from fastapi.testclient import TestClient
from main import app


def test_get_organizations_with_real_data():
    """Тест получения организаций с реальными данными"""
    client = TestClient(app)
    response = client.get("/api/v1/organizations/search?name=Рога", headers={"X-API-Key": "your-secret-api-key-here"})
    assert response.status_code == 200
    
    data = response.json()
    assert data["total"] >= 1
    assert any("Рога и Копыта" in org["name"] for org in data["organizations"])


def test_get_buildings_with_real_data():
    """Тест получения зданий с реальными данными"""
    client = TestClient(app)
    response = client.get("/api/v1/buildings", headers={"X-API-Key": "your-secret-api-key-here"})
    assert response.status_code == 200
    
    data = response.json()
    assert data["total"] >= 5
    assert any("Красная площадь" in building["address"] for building in data["buildings"])


def test_get_activities_with_real_data():
    """Тест получения деятельностей с реальными данными"""
    client = TestClient(app)
    response = client.get("/api/v1/activities", headers={"X-API-Key": "your-secret-api-key-here"})
    assert response.status_code == 200
    
    data = response.json()
    assert data["total"] >= 10
    assert any(activity["name"] == "Еда" for activity in data["activities"])


def test_geo_search_with_real_data():
    """Тест геопоиска с реальными данными"""
    client = TestClient(app)
    
    # Поиск организаций в радиусе от Красной площади
    search_data = {
        "latitude": 55.7539,
        "longitude": 37.6208,
        "radius_km": 1.0
    }
    response = client.post("/api/v1/organizations/geo/radius", json=search_data, headers={"X-API-Key": "your-secret-api-key-here"})
    assert response.status_code == 200
    
    data = response.json()
    assert data["total"] >= 1  # Должна найтись организация на Красной площади


def test_activity_hierarchy_with_real_data():
    """Тест иерархии деятельностей с реальными данными"""
    client = TestClient(app)
    
    # Получаем ID деятельности "Еда"
    response = client.get("/api/v1/activities", headers={"X-API-Key": "your-secret-api-key-here"})
    activities = response.json()["activities"]
    food_activity = next(activity for activity in activities if activity["name"] == "Еда")
    
    # Ищем организации по иерархии "Еда"
    response = client.get(f"/api/v1/activities/{food_activity['id']}/organizations/hierarchy", headers={"X-API-Key": "your-secret-api-key-here"})
    assert response.status_code == 200
    
    data = response.json()
    assert data["total"] >= 3  # Должны найтись организации с мясной и молочной продукцией


def test_organization_details_with_real_data():
    """Тест получения деталей организации с реальными данными"""
    client = TestClient(app)
    
    # Получаем список организаций
    response = client.get("/api/v1/organizations/search?name=Рога", headers={"X-API-Key": "your-secret-api-key-here"})
    organizations = response.json()["organizations"]
    
    if organizations:
        org_id = organizations[0]["id"]
        
        # Получаем детали организации
        response = client.get(f"/api/v1/organizations/{org_id}", headers={"X-API-Key": "your-secret-api-key-here"})
        assert response.status_code == 200
        
        data = response.json()
        assert "name" in data
        assert "building" in data
        assert "phones" in data
        assert "activities" in data
        assert len(data["phones"]) >= 1
        assert len(data["activities"]) >= 1


def test_building_organizations_with_real_data():
    """Тест получения организаций в здании с реальными данными"""
    client = TestClient(app)
    
    # Получаем список зданий
    response = client.get("/api/v1/buildings", headers={"X-API-Key": "your-secret-api-key-here"})
    buildings = response.json()["buildings"]
    
    if buildings:
        building_id = buildings[0]["id"]
        
        # Получаем организации в здании
        response = client.get(f"/api/v1/buildings/{building_id}/organizations", headers={"X-API-Key": "your-secret-api-key-here"})
        assert response.status_code == 200
        
        data = response.json()
        assert "organizations" in data
        assert "total" in data 