from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Organization, Building, Activity, Phone
from schemas import (
    Organization as OrganizationSchema,
    OrganizationCreate,
    OrganizationsResponse,
    GeoSearchRequest,
    RectangleSearchRequest
)
from utils import calculate_distance, get_organizations_by_activity_hierarchy
from dependencies import verify_api_key

router = APIRouter(prefix="/api/v1/organizations", tags=["organizations"])


@router.get("/search", response_model=OrganizationsResponse)
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


@router.get("/{organization_id}", response_model=OrganizationSchema)
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


@router.post("/", response_model=OrganizationSchema, status_code=201)
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
        description=organization_data.description,
        address=organization_data.address,
        latitude=organization_data.latitude,
        longitude=organization_data.longitude,
        building_id=organization_data.building_id
    )
    
    # Добавляем телефоны
    for phone_data in organization_data.phones:
        phone = Phone(
            number=phone_data.number,
            type=phone_data.type
        )
        organization.phones.append(phone)
    
    # Добавляем деятельности
    organization.activities = activities
    
    db.add(organization)
    db.commit()
    db.refresh(organization)
    
    return organization


@router.post("/geo/radius", response_model=OrganizationsResponse)
async def search_organizations_by_radius(
    search_data: GeoSearchRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Поиск организаций в радиусе от заданной точки"""
    organizations = db.query(Organization).all()
    
    # Фильтруем организации по радиусу
    filtered_organizations = []
    for org in organizations:
        if org.latitude and org.longitude:
            distance = calculate_distance(
                search_data.latitude, search_data.longitude,
                org.latitude, org.longitude
            )
            if distance <= search_data.radius_km:
                filtered_organizations.append(org)
    
    return OrganizationsResponse(
        organizations=filtered_organizations,
        total=len(filtered_organizations)
    )


@router.post("/geo/rectangle", response_model=OrganizationsResponse)
async def search_organizations_by_rectangle(
    search_data: RectangleSearchRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Поиск организаций в прямоугольной области"""
    organizations = db.query(Organization).all()
    
    # Фильтруем организации по прямоугольной области
    filtered_organizations = []
    for org in organizations:
        if org.latitude and org.longitude:
            if (search_data.min_lat <= org.latitude <= search_data.max_lat and
                search_data.min_lon <= org.longitude <= search_data.max_lon):
                filtered_organizations.append(org)
    
    return OrganizationsResponse(
        organizations=filtered_organizations,
        total=len(filtered_organizations)
    ) 