from fastapi import HTTPException, Header
from typing import Optional
from config import settings

# API ключ из настроек
API_KEY = settings.API_KEY


def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """Проверка API ключа"""
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )
    return x_api_key 