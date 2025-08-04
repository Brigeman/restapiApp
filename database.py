from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Настройки базы данных
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./organizations.db")

# Создание движка базы данных
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()


def get_db():
    """Dependency для получения сессии базы данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 