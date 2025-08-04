from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Building, Activity, Organization, Phone
from utils import get_child_activity_ids


def create_test_data():
    """Создает тестовые данные для базы данных"""
    db = SessionLocal()
    
    try:
        # Создаем таблицы
        Base.metadata.create_all(bind=engine)
        
        print("🌱 Создание тестовых данных...")
        
        # 1. Создаем здания
        buildings_data = [
            {
                "name": "Торговый центр 'Красная площадь'",
                "address": "г. Москва, Красная площадь, 1",
                "latitude": 55.7539,
                "longitude": 37.6208
            },
            {
                "name": "Бизнес-центр 'Тверская'",
                "address": "г. Москва, ул. Тверская, 1",
                "latitude": 55.7575,
                "longitude": 37.6136
            },
            {
                "name": "Торговый центр 'Арбат'",
                "address": "г. Москва, ул. Арбат, 1",
                "latitude": 55.7494,
                "longitude": 37.5931
            },
            {
                "name": "Бизнес-центр 'Ленинский'",
                "address": "г. Москва, ул. Ленина, 10",
                "latitude": 55.7558,
                "longitude": 37.6176
            },
            {
                "name": "Торговый центр 'Пушкинский'",
                "address": "г. Москва, ул. Пушкина, 15",
                "latitude": 55.7558,
                "longitude": 37.6176
            }
        ]
        
        buildings = []
        for building_data in buildings_data:
            building = Building(**building_data)
            db.add(building)
            buildings.append(building)
        
        db.commit()
        print(f"✅ Создано {len(buildings)} зданий")
        
        # 2. Создаем иерархию деятельностей
        activities_data = [
            # Уровень 1
            {"name": "Еда", "level": 1, "parent_id": None},
            {"name": "Автомобили", "level": 1, "parent_id": None},
            {"name": "Услуги", "level": 1, "parent_id": None},
            
            # Уровень 2 - Еда
            {"name": "Мясная продукция", "level": 2, "parent_id": None},
            {"name": "Молочная продукция", "level": 2, "parent_id": None},
            {"name": "Хлебобулочные изделия", "level": 2, "parent_id": None},
            
            # Уровень 2 - Автомобили
            {"name": "Грузовые автомобили", "level": 2, "parent_id": None},
            {"name": "Легковые автомобили", "level": 2, "parent_id": None},
            
            # Уровень 3 - Автомобили
            {"name": "Запчасти", "level": 3, "parent_id": None},
            {"name": "Аксессуары", "level": 3, "parent_id": None},
        ]
        
        activities = []
        for activity_data in activities_data:
            activity = Activity(**activity_data)
            db.add(activity)
            activities.append(activity)
        
        db.commit()
        
        # Устанавливаем связи parent-child
        food_activity = db.query(Activity).filter(Activity.name == "Еда").first()
        cars_activity = db.query(Activity).filter(Activity.name == "Автомобили").first()
        
        # Еда -> Мясная продукция, Молочная продукция, Хлебобулочные изделия
        meat_activity = db.query(Activity).filter(Activity.name == "Мясная продукция").first()
        milk_activity = db.query(Activity).filter(Activity.name == "Молочная продукция").first()
        bread_activity = db.query(Activity).filter(Activity.name == "Хлебобулочные изделия").first()
        
        meat_activity.parent_id = food_activity.id
        milk_activity.parent_id = food_activity.id
        bread_activity.parent_id = food_activity.id
        
        # Автомобили -> Грузовые, Легковые
        truck_activity = db.query(Activity).filter(Activity.name == "Грузовые автомобили").first()
        car_activity = db.query(Activity).filter(Activity.name == "Легковые автомобили").first()
        
        truck_activity.parent_id = cars_activity.id
        car_activity.parent_id = cars_activity.id
        
        # Легковые автомобили -> Запчасти, Аксессуары
        parts_activity = db.query(Activity).filter(Activity.name == "Запчасти").first()
        accessories_activity = db.query(Activity).filter(Activity.name == "Аксессуары").first()
        
        parts_activity.parent_id = car_activity.id
        accessories_activity.parent_id = car_activity.id
        
        db.commit()
        print(f"✅ Создано {len(activities)} деятельностей с иерархией")
        
        # 3. Создаем организации
        organizations_data = [
            {
                "name": "ООО 'Рога и Копыта'",
                "building_id": buildings[0].id,
                "phones": ["2-222-222", "3-333-333"],
                "activities": [meat_activity, milk_activity]
            },
            {
                "name": "ИП 'Мясо и Молоко'",
                "building_id": buildings[1].id,
                "phones": ["4-444-444"],
                "activities": [meat_activity]
            },
            {
                "name": "ООО 'АвтоСервис'",
                "building_id": buildings[2].id,
                "phones": ["5-555-555", "6-666-666"],
                "activities": [parts_activity, accessories_activity]
            },
            {
                "name": "ИП 'Хлеб и Булочки'",
                "building_id": buildings[3].id,
                "phones": ["7-777-777"],
                "activities": [bread_activity]
            },
            {
                "name": "ООО 'Грузовики России'",
                "building_id": buildings[4].id,
                "phones": ["8-888-888"],
                "activities": [truck_activity]
            }
        ]
        
        for org_data in organizations_data:
            # Создаем организацию
            organization = Organization(
                name=org_data["name"],
                description=f"Описание {org_data['name']}",
                address=f"Адрес {org_data['name']}",
                latitude=55.7558,  # Координаты Москвы
                longitude=37.6176,
                building_id=org_data["building_id"]
            )
            db.add(organization)
            db.commit()
            db.refresh(organization)
            
            # Добавляем телефоны
            for phone_number in org_data["phones"]:
                phone = Phone(number=phone_number, type="mobile", organization_id=organization.id)
                db.add(phone)
            
            # Добавляем связи с деятельностями
            organization.activities = org_data["activities"]
            
            db.commit()
        
        print(f"✅ Создано {len(organizations_data)} организаций")
        
        # 4. Выводим статистику
        total_buildings = db.query(Building).count()
        total_activities = db.query(Activity).count()
        total_organizations = db.query(Organization).count()
        total_phones = db.query(Phone).count()
        
        print("\n📊 Статистика базы данных:")
        print(f"   Здания: {total_buildings}")
        print(f"   Деятельности: {total_activities}")
        print(f"   Организации: {total_organizations}")
        print(f"   Телефоны: {total_phones}")
        
        # 5. Тестируем иерархию
        print("\n🔍 Тестирование иерархии деятельностей:")
        
        # Тест 1: Поиск организаций по "Еда" (должны найтись все организации с едой)
        food_orgs = db.query(Organization).join(Organization.activities).filter(
            Activity.id.in_([food_activity.id] + get_child_activity_ids(db, food_activity.id, 3))
        ).distinct().all()
        print(f"   Организации в категории 'Еда': {len(food_orgs)}")
        
        # Тест 2: Поиск организаций по "Автомобили" (должны найтись организации с автозапчастями)
        cars_orgs = db.query(Organization).join(Organization.activities).filter(
            Activity.id.in_([cars_activity.id] + get_child_activity_ids(db, cars_activity.id, 3))
        ).distinct().all()
        print(f"   Организации в категории 'Автомобили': {len(cars_orgs)}")
        
        print("\n✅ Тестовые данные успешно созданы!")
        
    except Exception as e:
        print(f"❌ Ошибка при создании тестовых данных: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    create_test_data() 