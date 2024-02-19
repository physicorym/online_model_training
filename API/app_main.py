from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy import select

from passlib.context import CryptContext
import asyncio

from pydantic import BaseModel

DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@localhost:5432/postgres'


async_engine = create_async_engine(DATABASE_URL, echo=True)
async_sessionmaker = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=func.now())

class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    model_link = Column(String)

# Асинхронное создание таблиц
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Вызов функции для создания таблиц
asyncio.create_task(create_tables())

app = FastAPI()

# Хеши паролей
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_async_db():
    async with async_sessionmaker() as session:
        yield session

# Регистрация пользователя
@app.post("/register/")
async def register(username: str, password: str, db: Session = Depends(get_async_db)):
    # Хэш пароля
    hashed_password = password_context.hash(password)

    new_user = User(username=username, hashed_password=hashed_password)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message": "Успешная регистрация"}

@app.post("/login/")
async def login(username: str, password: str, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalar()

    if not user or not password_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Шел бы отсюда")

    return {"message": "Повезло повезло..."}

@app.get("/users/")
async def get_users(db: AsyncSession = Depends(get_async_db)):
    users = await db.execute(select(User))
    return {"users": [dict(user) for user in users]}

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    user = await db.execute(select(User).filter(User.id == user_id))
    user_data = user.scalar()
    if not user_data:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return {"user": dict(user_data)}

class ModelCreate(BaseModel):
    name: str
    description: str
    model_link: str

class ModelResponse(BaseModel):
    id: int
    name: str
    description: str
    model_link: str