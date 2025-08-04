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
    OrganizationsResponse,
    BuildingsResponse,
    GeoSearchRequest,
    RectangleSearchRequest
)

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
@app.post("/api/v1/organizations/geo/radius")
async def search_organizations_by_radius(
    search_data: dict,
    api_key: str = Depends(verify_api_key)
):
    """Поиск организаций в радиусе от указанной точки"""
    return {
        "organizations": [],
        "total": 0
    }


@app.post("/api/v1/organizations/geo/rectangle")
async def search_organizations_by_rectangle(
    search_data: dict,
    api_key: str = Depends(verify_api_key)
):
    """Поиск организаций в прямоугольной области"""
    return {
        "organizations": [],
        "total": 0
    }


# Роутеры для деятельностей
@app.get("/api/v1/activities/{activity_id}/organizations/hierarchy")
async def get_organizations_by_activity_hierarchy(
    activity_id: int,
    api_key: str = Depends(verify_api_key)
):
    """Получить организации по иерархии деятельности"""
    # Пока что возвращаем 404, так как база данных не настроена
    raise HTTPException(status_code=404, detail="Activity not found") 