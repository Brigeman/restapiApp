import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models import Organization, Building, Activity, Phone


class TestOrganizationsAPI:
    """Тесты для API организаций"""
    
    def test_get_organization_by_id_success(self, client: TestClient, headers: dict, db_session: Session):
        """Тест получения организации по ID - успешный случай"""
        # Создаем тестовые данные
        building = Building(
            address="г. Москва, ул. Ленина 1, офис 3",
            latitude=55.7558,
            longitude=37.6176
        )
        db_session.add(building)
        db_session.commit()
        
        activity = Activity(name="Молочная продукция", level=2)
        db_session.add(activity)
        db_session.commit()
        
        org = Organization(
            name="ООО 'Рога и Копыта'",
            building_id=building.id
        )
        db_session.add(org)
        db_session.commit()
        
        # Добавляем связи
        org.activities.append(activity)
        phone = Phone(phone_number="2-222-222", organization_id=org.id)
        db_session.add(phone)
        db_session.commit()
        
        # Тестируем API
        response = client.get(f"/api/v1/organizations/{org.id}", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "ООО 'Рога и Копыта'"
        assert data["building"]["address"] == "г. Москва, ул. Ленина 1, офис 3"
        assert len(data["phones"]) == 1
        assert data["phones"][0]["phone_number"] == "2-222-222"
        assert len(data["activities"]) == 1
        assert data["activities"][0]["name"] == "Молочная продукция"
    
    def test_get_organization_by_id_not_found(self, client: TestClient, headers: dict):
        """Тест получения организации по ID - не найдена"""
        response = client.get("/api/v1/organizations/999", headers=headers)
        assert response.status_code == 404
    
    def test_search_organizations_by_name(self, client: TestClient, headers: dict, db_session: Session):
        """Тест поиска организаций по названию"""
        # Создаем тестовые данные
        building = Building(
            address="г. Москва, ул. Пушкина 10",
            latitude=55.7558,
            longitude=37.6176
        )
        db_session.add(building)
        db_session.commit()
        
        org1 = Organization(name="ООО 'Рога и Копыта'", building_id=building.id)
        org2 = Organization(name="ИП 'Копыта и Рога'", building_id=building.id)
        db_session.add_all([org1, org2])
        db_session.commit()
        
        # Тестируем поиск
        response = client.get("/api/v1/organizations/search?name=Рога", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["organizations"]) == 2
        assert any(org["name"] == "ООО 'Рога и Копыта'" for org in data["organizations"])
        assert any(org["name"] == "ИП 'Копыта и Рога'" for org in data["organizations"])
    
    def test_get_organizations_by_building(self, client: TestClient, headers: dict, db_session: Session):
        """Тест получения организаций по зданию"""
        # Создаем тестовые данные
        building1 = Building(
            address="г. Москва, ул. Ленина 1",
            latitude=55.7558,
            longitude=37.6176
        )
        building2 = Building(
            address="г. Москва, ул. Пушкина 10",
            latitude=55.7558,
            longitude=37.6176
        )
        db_session.add_all([building1, building2])
        db_session.commit()
        
        org1 = Organization(name="ООО 'Рога и Копыта'", building_id=building1.id)
        org2 = Organization(name="ИП 'Копыта и Рога'", building_id=building1.id)
        org3 = Organization(name="ООО 'Другая компания'", building_id=building2.id)
        db_session.add_all([org1, org2, org3])
        db_session.commit()
        
        # Тестируем API
        response = client.get(f"/api/v1/buildings/{building1.id}/organizations", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["organizations"]) == 2
        assert any(org["name"] == "ООО 'Рога и Копыта'" for org in data["organizations"])
        assert any(org["name"] == "ИП 'Копыта и Рога'" for org in data["organizations"])
    
    def test_get_organizations_by_activity(self, client: TestClient, headers: dict, db_session: Session):
        """Тест получения организаций по деятельности"""
        # Создаем тестовые данные
        building = Building(
            address="г. Москва, ул. Ленина 1",
            latitude=55.7558,
            longitude=37.6176
        )
        db_session.add(building)
        db_session.commit()
        
        activity1 = Activity(name="Молочная продукция", level=2)
        activity2 = Activity(name="Мясная продукция", level=2)
        db_session.add_all([activity1, activity2])
        db_session.commit()
        
        org1 = Organization(name="ООО 'Молоко'", building_id=building.id)
        org2 = Organization(name="ИП 'Мясо'", building_id=building.id)
        org3 = Organization(name="ООО 'Другая компания'", building_id=building.id)
        db_session.add_all([org1, org2, org3])
        db_session.commit()
        
        # Добавляем связи
        org1.activities.append(activity1)
        org2.activities.append(activity2)
        db_session.commit()
        
        # Тестируем API
        response = client.get(f"/api/v1/activities/{activity1.id}/organizations", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["organizations"]) == 1
        assert data["organizations"][0]["name"] == "ООО 'Молоко'"
    
    def test_create_organization(self, client: TestClient, headers: dict, db_session: Session):
        """Тест создания организации"""
        # Создаем тестовые данные
        building = Building(
            address="г. Москва, ул. Ленина 1",
            latitude=55.7558,
            longitude=37.6176
        )
        activity = Activity(name="Молочная продукция", level=2)
        db_session.add_all([building, activity])
        db_session.commit()
        
        # Тестируем создание
        org_data = {
            "name": "ООО 'Новая компания'",
            "building_id": building.id,
            "phones": ["2-222-222", "3-333-333"],
            "activity_ids": [activity.id]
        }
        
        response = client.post("/api/v1/organizations", json=org_data, headers=headers)
        assert response.status_code == 201
        
        data = response.json()
        assert data["name"] == "ООО 'Новая компания'"
        assert len(data["phones"]) == 2
        assert len(data["activities"]) == 1 