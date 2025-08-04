import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models import Organization, Building, Activity


class TestGeoSearchAPI:
    """Тесты для геопоиска организаций"""
    
    def test_search_organizations_by_radius(self, client: TestClient, headers: dict, db_session: Session):
        """Тест поиска организаций в радиусе"""
        # Создаем тестовые данные с разными координатами
        building1 = Building(
            name="Красная площадь",
            address="г. Москва, Красная площадь",
            latitude=55.7539,
            longitude=37.6208
        )
        building2 = Building(
            name="Тверская",
            address="г. Москва, ул. Тверская 1",
            latitude=55.7575,
            longitude=37.6136
        )
        building3 = Building(
            name="Арбат",
            address="г. Москва, ул. Арбат 1",
            latitude=55.7494,
            longitude=37.5931
        )
        db_session.add_all([building1, building2, building3])
        db_session.commit()
        
        org1 = Organization(
            name="ООО 'Красная площадь'", 
            building_id=building1.id,
            latitude=55.7539,
            longitude=37.6208
        )
        org2 = Organization(
            name="ИП 'Тверская'", 
            building_id=building2.id,
            latitude=55.7575,
            longitude=37.6136
        )
        org3 = Organization(
            name="ООО 'Арбат'", 
            building_id=building3.id,
            latitude=55.7494,
            longitude=37.5931
        )
        db_session.add_all([org1, org2, org3])
        db_session.commit()
        
        # Тестируем поиск в радиусе от Красной площади
        search_data = {
            "latitude": 55.7539,
            "longitude": 37.6208,
            "radius_km": 1.0
        }
        
        response = client.post("/api/v1/organizations/geo/radius", json=search_data, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        # Должны найтись организации на Красной площади и Тверской
        assert len(data["organizations"]) >= 2
        org_names = [org["name"] for org in data["organizations"]]
        assert "ООО 'Красная площадь'" in org_names
        assert "ИП 'Тверская'" in org_names
    
    def test_search_organizations_by_rectangle(self, client: TestClient, headers: dict, db_session: Session):
        """Тест поиска организаций в прямоугольной области"""
        # Создаем тестовые данные
        building1 = Building(
            name="Ленина",
            address="г. Москва, ул. Ленина 1",
            latitude=55.7558,
            longitude=37.6176
        )
        building2 = Building(
            name="Пушкина",
            address="г. Москва, ул. Пушкина 10",
            latitude=55.7558,
            longitude=37.6176
        )
        building3 = Building(
            name="Гагарина",
            address="г. Москва, ул. Гагарина 20",
            latitude=55.7500,
            longitude=37.6000
        )
        db_session.add_all([building1, building2, building3])
        db_session.commit()
        
        org1 = Organization(
            name="ООО 'Ленина'", 
            building_id=building1.id,
            latitude=55.7558,
            longitude=37.6176
        )
        org2 = Organization(
            name="ИП 'Пушкина'", 
            building_id=building2.id,
            latitude=55.7558,
            longitude=37.6176
        )
        org3 = Organization(
            name="ООО 'Гагарина'", 
            building_id=building3.id,
            latitude=55.7500,
            longitude=37.6000
        )
        db_session.add_all([org1, org2, org3])
        db_session.commit()
        
        # Тестируем поиск в прямоугольной области
        search_data = {
            "min_lat": 55.7500,
            "max_lat": 55.7600,
            "min_lon": 37.6000,
            "max_lon": 37.6200
        }
        
        response = client.post("/api/v1/organizations/geo/rectangle", json=search_data, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        # Должны найтись организации в указанной области
        assert len(data["organizations"]) >= 2
        org_names = [org["name"] for org in data["organizations"]]
        assert "ООО 'Ленина'" in org_names
        assert "ИП 'Пушкина'" in org_names
    
    def test_search_organizations_by_activity_hierarchy(self, client: TestClient, headers: dict, db_session: Session):
        """Тест поиска организаций по иерархии деятельности"""
        # Создаем иерархию деятельностей
        food_activity = Activity(name="Еда", level=1)
        meat_activity = Activity(name="Мясная продукция", level=2, parent_id=None)
        milk_activity = Activity(name="Молочная продукция", level=2, parent_id=None)
        db_session.add_all([food_activity, meat_activity, milk_activity])
        db_session.commit()
        
        # Устанавливаем связи
        meat_activity.parent_id = food_activity.id
        milk_activity.parent_id = food_activity.id
        db_session.commit()
        
        # Создаем здания
        building = Building(
            name="Ленина",
            address="г. Москва, ул. Ленина 1",
            latitude=55.7558,
            longitude=37.6176
        )
        db_session.add(building)
        db_session.commit()
        
        # Создаем организации с разными деятельностями
        org1 = Organization(
            name="ООО 'Мясо'", 
            building_id=building.id,
            latitude=55.7558,
            longitude=37.6176
        )
        org2 = Organization(
            name="ИП 'Молоко'", 
            building_id=building.id,
            latitude=55.7558,
            longitude=37.6176
        )
        org3 = Organization(
            name="ООО 'Другая компания'", 
            building_id=building.id,
            latitude=55.7558,
            longitude=37.6176
        )
        db_session.add_all([org1, org2, org3])
        db_session.commit()
        
        # Добавляем связи
        org1.activities.append(meat_activity)
        org2.activities.append(milk_activity)
        db_session.commit()
        
        # Тестируем поиск по родительской деятельности "Еда"
        response = client.get(f"/api/v1/activities/{food_activity.id}/organizations/hierarchy?level=3", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        # Должны найтись организации с мясной и молочной продукцией
        assert len(data["organizations"]) == 2
        org_names = [org["name"] for org in data["organizations"]]
        assert "ООО 'Мясо'" in org_names
        assert "ИП 'Молоко'" in org_names
    
    def test_activity_level_limit(self, client: TestClient, headers: dict, db_session: Session):
        """Тест ограничения уровня вложенности деятельностей"""
        # Создаем деятельность с уровнем больше 3
        activity_level_4 = Activity(name="Слишком глубокий уровень", level=4)
        db_session.add(activity_level_4)
        db_session.commit()
        
        # Тестируем создание деятельности с превышением лимита
        activity_data = {
            "name": "Новая деятельность",
            "level": 4
        }
        
        response = client.post("/api/v1/activities", json=activity_data, headers=headers)
        assert response.status_code == 422  # Pydantic валидация возвращает 422 