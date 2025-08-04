from fastapi import FastAPI, Depends, HTTPException, Header, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import Organization, Building, Activity, Phone
from schemas import (
    Organization as OrganizationSchema,
    OrganizationCreate,
    Building as BuildingSchema,
    BuildingCreate,
    Activity as ActivitySchema,
    ActivityCreate,
    OrganizationsResponse,
    BuildingsResponse,
    ActivitiesResponse,
    GeoSearchRequest,
    RectangleSearchRequest
)
from utils import calculate_distance, get_organizations_by_activity_hierarchy

app = FastAPI(
    title="REST API Organizations Directory",
    description="REST API для справочника организаций, зданий и деятельностей",
    version="1.0.0"
)

# API ключ (в реальном проекте должен быть в переменных окружения)
API_KEY = "your-secret-api-key-here"


def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """Проверка API ключа"""
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return x_api_key


@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": "REST API Organizations Directory",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Проверка здоровья приложения"""
    return {"status": "healthy"}


# Роутеры для организаций
@app.get("/api/v1/organizations/search", response_model=OrganizationsResponse)
async def search_organizations_by_name(
    name: str = Query(..., description="Название организации для поиска"),
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Поиск организаций по названию"""
    organizations = db.query(Organization).filter(
        Organization.name.ilike(f"%{name}%")
    ).all()
    
    return OrganizationsResponse(
        organizations=organizations,
        total=len(organizations)
    )


@app.get("/api/v1/organizations/{organization_id}", response_model=OrganizationSchema)
async def get_organization(
    organization_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Получить информацию об организации по ID"""
    organization = db.query(Organization).filter(Organization.id == organization_id).first()
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization


@app.post("/api/v1/organizations", response_model=OrganizationSchema, status_code=201)
async def create_organization(
    organization_data: OrganizationCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Создать новую организацию"""
    # Проверяем существование здания
    building = db.query(Building).filter(Building.id == organization_data.building_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    # Проверяем существование деятельностей
    activities = db.query(Activity).filter(Activity.id.in_(organization_data.activity_ids)).all()
    if len(activities) != len(organization_data.activity_ids):
        raise HTTPException(status_code=404, detail="Some activities not found")
    
    # Создаем организацию
    organization = Organization(
        name=organization_data.name,
        building_id=organization_data.building_id
    )
    db.add(organization)
    db.commit()
    db.refresh(organization)
    
    # Добавляем телефоны
    for phone_number in organization_data.phones:
        phone = Phone(phone_number=phone_number, organization_id=organization.id)
        db.add(phone)
    
    # Добавляем связи с деятельностями
    organization.activities = activities
    
    db.commit()
    db.refresh(organization)
    return organization


# Роутеры для зданий
@app.get("/api/v1/buildings", response_model=BuildingsResponse)
async def get_buildings(
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Получить список всех зданий"""
    buildings = db.query(Building).all()
    return BuildingsResponse(
        buildings=buildings,
        total=len(buildings)
    )


@app.get("/api/v1/buildings/{building_id}", response_model=BuildingSchema)
async def get_building(
    building_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Получить информацию о здании по ID"""
    building = db.query(Building).filter(Building.id == building_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building


@app.get("/api/v1/buildings/{building_id}/organizations", response_model=OrganizationsResponse)
async def get_organizations_by_building(
    building_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Получить список всех организаций в конкретном здании"""
    # Проверяем существование здания
    building = db.query(Building).filter(Building.id == building_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    organizations = db.query(Organization).filter(Organization.building_id == building_id).all()
    
    return OrganizationsResponse(
        organizations=organizations,
        total=len(organizations)
    )


@app.post("/api/v1/buildings", response_model=BuildingSchema, status_code=201)
async def create_building(
    building_data: BuildingCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Создать новое здание"""
    building = Building(**building_data.model_dump())
    db.add(building)
    db.commit()
    db.refresh(building)
    return building


# Роутеры для геопоиска
@app.post("/api/v1/organizations/geo/radius", response_model=OrganizationsResponse)
async def search_organizations_by_radius(
    search_data: GeoSearchRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Поиск организаций в радиусе от указанной точки"""
    organizations = []
    
    # Получаем все организации с их зданиями
    orgs_with_buildings = db.query(Organization).join(Building).all()
    
    for org in orgs_with_buildings:
        distance = calculate_distance(
            search_data.latitude, search_data.longitude,
            org.building.latitude, org.building.longitude
        )
        
        if distance <= search_data.radius_km:
            organizations.append(org)
    
    return OrganizationsResponse(
        organizations=organizations,
        total=len(organizations)
    )


@app.post("/api/v1/organizations/geo/rectangle", response_model=OrganizationsResponse)
async def search_organizations_by_rectangle(
    search_data: RectangleSearchRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Поиск организаций в прямоугольной области"""
    organizations = db.query(Organization).join(Building).filter(
        Building.latitude >= search_data.min_lat,
        Building.latitude <= search_data.max_lat,
        Building.longitude >= search_data.min_lon,
        Building.longitude <= search_data.max_lon
    ).all()
    
    return OrganizationsResponse(
        organizations=organizations,
        total=len(organizations)
    )


# Роутеры для деятельностей
@app.get("/api/v1/activities", response_model=ActivitiesResponse)
async def get_activities(
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Получить список всех деятельностей"""
    activities = db.query(Activity).all()
    return ActivitiesResponse(
        activities=activities,
        total=len(activities)
    )


@app.get("/api/v1/activities/{activity_id}", response_model=ActivitySchema)
async def get_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Получить информацию о деятельности по ID"""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@app.post("/api/v1/activities", response_model=ActivitySchema, status_code=201)
async def create_activity(
    activity_data: ActivityCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Создать новую деятельность"""
    # Проверяем уровень вложенности
    if activity_data.level > 3:
        raise HTTPException(status_code=400, detail="Activity level cannot exceed 3")
    
    # Проверяем родительскую деятельность
    if activity_data.parent_id:
        parent = db.query(Activity).filter(Activity.id == activity_data.parent_id).first()
        if not parent:
            raise HTTPException(status_code=404, detail="Parent activity not found")
        if parent.level >= 3:
            raise HTTPException(status_code=400, detail="Cannot create activity with level > 3")
    
    activity = Activity(**activity_data.model_dump())
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


@app.get("/api/v1/activities/{activity_id}/organizations", response_model=OrganizationsResponse)
async def get_organizations_by_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Получить организации по конкретной деятельности"""
    # Проверяем существование деятельности
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    organizations = db.query(Organization).join(
        Organization.activities
    ).filter(Activity.id == activity_id).all()
    
    return OrganizationsResponse(
        organizations=organizations,
        total=len(organizations)
    )


@app.get("/api/v1/activities/{activity_id}/organizations/hierarchy", response_model=OrganizationsResponse)
async def get_organizations_by_activity_hierarchy(
    activity_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Получить организации по иерархии деятельности"""
    from utils import get_organizations_by_activity_hierarchy as get_orgs_by_hierarchy
    organizations = get_orgs_by_hierarchy(db, activity_id)
    
    return OrganizationsResponse(
        organizations=organizations,
        total=len(organizations)
    ) 