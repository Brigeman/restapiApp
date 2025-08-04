from fastapi import FastAPI
from routers import organizations, buildings, activities
from config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="REST API для справочника организаций, зданий и деятельностей",
    version=settings.APP_VERSION
)

# Подключаем роутеры
app.include_router(organizations.router)
app.include_router(buildings.router)
app.include_router(activities.router)


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