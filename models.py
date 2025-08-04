from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, Text
from sqlalchemy.orm import relationship
from database import Base


# Связующая таблица для связи многие-ко-многим между организациями и деятельностями
organization_activity = Table(
    'organization_activity',
    Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id'), primary_key=True),
    Column('activity_id', Integer, ForeignKey('activities.id'), primary_key=True)
)


class Organization(Base):
    """Модель организации"""
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    address = Column(Text, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)
    
    # Связи
    building = relationship("Building", back_populates="organizations")
    activities = relationship("Activity", secondary=organization_activity, back_populates="organizations")
    phones = relationship("Phone", back_populates="organization")


class Phone(Base):
    """Модель телефона организации"""
    __tablename__ = "phones"
    
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(20), nullable=False)
    type = Column(String(20), nullable=False, default="mobile")
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    
    # Связи
    organization = relationship("Organization", back_populates="phones")


class Building(Base):
    """Модель здания"""
    __tablename__ = "buildings"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Связи
    organizations = relationship("Organization", back_populates="building")


class Activity(Base):
    """Модель деятельности (иерархическая структура)"""
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    parent_id = Column(Integer, ForeignKey("activities.id"), nullable=True)
    level = Column(Integer, default=1)  # Уровень вложенности (1-3)
    
    # Связи
    parent = relationship("Activity", remote_side=[id], back_populates="children")
    children = relationship("Activity", back_populates="parent")
    organizations = relationship("Organization", secondary=organization_activity, back_populates="activities") 