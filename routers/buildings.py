from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Building, Organization
from schemas import (
    Building as BuildingSchema,
    BuildingCreate,
    BuildingsResponse,
    OrganizationsResponse
)
from dependencies import verify_api_key

router = APIRouter(prefix="/api/v1/buildings", tags=["buildings"])


@router.get("/", response_model=BuildingsResponse)
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


@router.get("/{building_id}", response_model=BuildingSchema)
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


@router.get("/{building_id}/organizations", response_model=OrganizationsResponse)
async def get_organizations_by_building(
    building_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Получить список организаций в здании"""
    # Проверяем существование здания
    building = db.query(Building).filter(Building.id == building_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    
    # Получаем организации в здании
    organizations = db.query(Organization).filter(Organization.building_id == building_id).all()
    
    return OrganizationsResponse(
        organizations=organizations,
        total=len(organizations)
    )


@router.post("/", response_model=BuildingSchema, status_code=201)
async def create_building(
    building_data: BuildingCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Создать новое здание"""
    building = Building(
        name=building_data.name,
        address=building_data.address,
        latitude=building_data.latitude,
        longitude=building_data.longitude
    )
    
    db.add(building)
    db.commit()
    db.refresh(building)
    
    return building 