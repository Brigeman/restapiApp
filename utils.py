import math
from typing import List
from sqlalchemy.orm import Session
from models import Organization, Building, Activity


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Вычисляет расстояние между двумя точками на Земле в километрах
    используя формулу гаверсинуса
    """
    # Радиус Земли в километрах
    R = 6371.0
    
    # Переводим координаты в радианы
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Разности координат
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Формула гаверсинуса
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c


def get_organizations_by_activity_hierarchy(db: Session, activity_id: int) -> List[Organization]:
    """
    Получает все организации, связанные с деятельностью и её дочерними деятельностями
    """
    # Получаем деятельность и все её дочерние деятельности
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        return []
    
    # Получаем все дочерние деятельности (рекурсивно)
    child_activity_ids = get_child_activity_ids(db, activity_id)
    all_activity_ids = [activity_id] + child_activity_ids
    
    # Получаем организации, связанные с этими деятельностями
    organizations = db.query(Organization).join(
        Organization.activities
    ).filter(Activity.id.in_(all_activity_ids)).distinct().all()
    
    return organizations


def get_child_activity_ids(db: Session, parent_id: int) -> List[int]:
    """
    Рекурсивно получает ID всех дочерних деятельностей
    """
    children = db.query(Activity).filter(Activity.parent_id == parent_id).all()
    child_ids = [child.id for child in children]
    
    # Рекурсивно получаем дочерние элементы дочерних элементов
    for child_id in child_ids:
        child_ids.extend(get_child_activity_ids(db, child_id))
    
    return child_ids 