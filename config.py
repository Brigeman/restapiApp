import os
from typing import Optional


class Settings:
    """Настройки приложения"""
    
    # База данных
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./organizations.db")
    TEST_DATABASE_URL: str = os.getenv("TEST_DATABASE_URL", "sqlite:///./test.db")
    
    # API ключ
    API_KEY: str = os.getenv("API_KEY", "your-secret-api-key-here")
    
    # Настройки приложения
    APP_NAME: str = "REST API Organizations Directory"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"


# Создаем экземпляр настроек
settings = Settings() 