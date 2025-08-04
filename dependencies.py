from fastapi import HTTPException, Header
from typing import Optional

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