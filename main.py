from fastapi import FastAPI
from routers import organizations, buildings, activities

app = FastAPI(
    title="REST API Organizations Directory",
    description="REST API для справочника организаций, зданий и деятельностей",
    version="1.0.0"
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