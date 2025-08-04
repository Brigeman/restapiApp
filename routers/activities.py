from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Activity, Organization
from schemas import (
    Activity as ActivitySchema,
    ActivityCreate,
    ActivitiesResponse,
    OrganizationsResponse
)
from utils import get_organizations_by_activity_hierarchy, get_child_activity_ids
from dependencies import verify_api_key

router = APIRouter(prefix="/api/v1/activities", tags=["activities"])


@router.get("/", response_model=ActivitiesResponse)
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


@router.get("/{activity_id}", response_model=ActivitySchema)
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


@router.post("/", response_model=ActivitySchema, status_code=201)
async def create_activity(
    activity_data: ActivityCreate,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Создать новую деятельность"""
    # Проверяем родительскую деятельность, если указана
    if activity_data.parent_id:
        parent_activity = db.query(Activity).filter(Activity.id == activity_data.parent_id).first()
        if not parent_activity:
            raise HTTPException(status_code=404, detail="Parent activity not found")
    
    activity = Activity(
        name=activity_data.name,
        description=activity_data.description,
        parent_id=activity_data.parent_id
    )
    
    db.add(activity)
    db.commit()
    db.refresh(activity)
    
    return activity


@router.get("/{activity_id}/organizations", response_model=OrganizationsResponse)
async def get_organizations_by_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Получить список организаций по деятельности"""
    # Проверяем существование деятельности
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Получаем организации с этой деятельностью
    organizations = db.query(Organization).join(Organization.activities).filter(Activity.id == activity_id).all()
    
    return OrganizationsResponse(
        organizations=organizations,
        total=len(organizations)
    )


@router.get("/{activity_id}/organizations/hierarchy", response_model=OrganizationsResponse)
async def get_organizations_by_activity_hierarchy(
    activity_id: int,
    level: int = Query(..., ge=1, le=3, description="Уровень иерархии (1-3)"),
    db: Session = Depends(get_db),
    api_key: str = Depends(verify_api_key)
):
    """Получить список организаций по иерархии деятельностей"""
    # Проверяем существование деятельности
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Получаем ID всех дочерних деятельностей
    child_activity_ids = get_child_activity_ids(db, activity_id, level)
    
    # Получаем организации с этими деятельностями
    organizations = db.query(Organization).join(Organization.activities).filter(
        Activity.id.in_(child_activity_ids)
    ).all()
    
    return OrganizationsResponse(
        organizations=organizations,
        total=len(organizations)
    ) 