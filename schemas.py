from pydantic import BaseModel, Field
from typing import List, Optional


# Схемы для Building
class BuildingBase(BaseModel):
    name: str = Field(..., description="Название здания")
    address: str = Field(..., description="Адрес здания")
    latitude: float = Field(..., ge=-90, le=90, description="Широта")
    longitude: float = Field(..., ge=-180, le=180, description="Долгота")


class BuildingCreate(BuildingBase):
    pass


class Building(BuildingBase):
    id: int
    
    model_config = {"from_attributes": True}


# Схемы для Activity
class ActivityBase(BaseModel):
    name: str = Field(..., description="Название деятельности")
    description: Optional[str] = Field(None, description="Описание деятельности")
    parent_id: Optional[int] = Field(None, description="ID родительской деятельности")
    level: int = Field(1, ge=1, le=3, description="Уровень вложенности")


class ActivityCreate(ActivityBase):
    pass


class Activity(ActivityBase):
    id: int
    children: List['Activity'] = []
    
    model_config = {"from_attributes": True}


# Схемы для Phone
class PhoneBase(BaseModel):
    number: str = Field(..., description="Номер телефона")
    type: str = Field("mobile", description="Тип телефона")


class PhoneCreate(PhoneBase):
    pass


class Phone(PhoneBase):
    id: int
    organization_id: int
    
    model_config = {"from_attributes": True}


# Схема для создания телефона
class PhoneCreate(BaseModel):
    number: str = Field(..., description="Номер телефона")
    type: str = Field("mobile", description="Тип телефона")


# Схемы для Organization
class OrganizationBase(BaseModel):
    name: str = Field(..., description="Название организации")
    description: Optional[str] = Field(None, description="Описание организации")
    address: Optional[str] = Field(None, description="Адрес организации")
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="Широта")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="Долгота")
    building_id: int = Field(..., description="ID здания")


class OrganizationCreate(OrganizationBase):
    phones: List[PhoneCreate] = Field(..., description="Список телефонов")
    activity_ids: List[int] = Field(..., description="Список ID деятельностей")


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    building_id: Optional[int] = None
    phones: Optional[List[str]] = None
    activity_ids: Optional[List[int]] = None


class Organization(OrganizationBase):
    id: int
    building: Building
    phones: List[Phone]
    activities: List[Activity]
    
    model_config = {"from_attributes": True}


# Схемы для геопоиска
class GeoSearchRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Широта центра поиска")
    longitude: float = Field(..., ge=-180, le=180, description="Долгота центра поиска")
    radius_km: float = Field(10.0, gt=0, description="Радиус поиска в километрах")


class RectangleSearchRequest(BaseModel):
    min_lat: float = Field(..., ge=-90, le=90, description="Минимальная широта")
    max_lat: float = Field(..., ge=-90, le=90, description="Максимальная широта")
    min_lon: float = Field(..., ge=-180, le=180, description="Минимальная долгота")
    max_lon: float = Field(..., ge=-180, le=180, description="Максимальная долгота")


# Схемы для ответов
class OrganizationsResponse(BaseModel):
    organizations: List[Organization]
    total: int


class BuildingsResponse(BaseModel):
    buildings: List[Building]
    total: int


class ActivitiesResponse(BaseModel):
    activities: List[Activity]
    total: int


# Обновляем forward references
Activity.model_rebuild() 