
from sqlalchemy import Column, Integer, String, DateTime, Text, func, ForeignKey
from sqlalchemy.orm import relationship

from pydantic import BaseModel

from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=func.now())

    models = relationship('Model', back_populates='owner')

class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    model_link = Column(String)

    user_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', back_populates='models')

class ModelCreate(BaseModel):
    name: str
    description: str
    model_link: str

class ModelResponse(BaseModel):
    id: int
    name: str
    description: str
    model_link: str