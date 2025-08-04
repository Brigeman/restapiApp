from fastapi import FastAPI, Depends, HTTPException, Header, Query
from typing import Optional

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
@app.get("/api/v1/organizations/search")
async def search_organizations_by_name(
    name: str = Query(..., description="Название организации для поиска"),
    api_key: str = Depends(verify_api_key)
):
    """Поиск организаций по названию"""
    # Пока что возвращаем пустой список
    return {
        "organizations": [],
        "total": 0
    }


@app.get("/api/v1/organizations/{organization_id}")
async def get_organization(
    organization_id: int,
    api_key: str = Depends(verify_api_key)
):
    """Получить информацию об организации по ID"""
    # Пока что возвращаем 404, так как база данных не настроена
    raise HTTPException(status_code=404, detail="Organization not found")


# Роутеры для зданий
@app.get("/api/v1/buildings")
async def get_buildings(api_key: str = Depends(verify_api_key)):
    """Получить список всех зданий"""
    return {
        "buildings": [],
        "total": 0
    }


@app.get("/api/v1/buildings/{building_id}")
async def get_building(
    building_id: int,
    api_key: str = Depends(verify_api_key)
):
    """Получить информацию о здании по ID"""
    # Пока что возвращаем 404, так как база данных не настроена
    raise HTTPException(status_code=404, detail="Building not found")


@app.get("/api/v1/buildings/{building_id}/organizations")
async def get_organizations_by_building(
    building_id: int,
    api_key: str = Depends(verify_api_key)
):
    """Получить список всех организаций в конкретном здании"""
    # Пока что возвращаем 404, так как база данных не настроена
    raise HTTPException(status_code=404, detail="Building not found")


@app.post("/api/v1/buildings")
async def create_building(
    building_data: dict,
    api_key: str = Depends(verify_api_key)
):
    """Создать новое здание"""
    # Пока что возвращаем 404, так как база данных не настроена
    raise HTTPException(status_code=404, detail="Database not configured")


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