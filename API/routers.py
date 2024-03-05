from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
import subprocess
import os

from db.models import User, Model
from db.security import get_current_user

from db.models import ModelResponse, ModelCreate
from db.dependencies import get_async_db


router = APIRouter()

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register/")
async def register(username: str, password: str, db: Session = Depends(get_async_db)):
    # Хэш пароля
    hashed_password = password_context.hash(password)

    new_user = User(username=username, hashed_password=hashed_password)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message": "Успешная регистрация"}

@router.post("/login/")
async def login(username: str, password: str, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(User).filter(User.username == username))
    user = result.scalar()

    if not user or not password_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Шел бы отсюда")

    return {"message": "Повезло повезло..."}

@router.get("/users/")
async def get_users(db: AsyncSession = Depends(get_async_db)):
    users = await db.execute(select(User))
    return {"users": [dict(user) for user in users]}

@router.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    user = await db.execute(select(User).filter(User.id == user_id))
    user_data = user.scalar()
    if not user_data:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return {"user": dict(user_data)}

@router.post("/models/", response_model=ModelResponse)
async def models(model: ModelCreate, user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    db_model = Model(**model.dict(), user_id=user["id"])
    db.add(db_model)
    await db.commit()
    await db.refresh(db_model)
    return db_model

@router.get("/models/user/{user_id}", response_model=list[ModelResponse])
async def get_user_models(user_id: int, db: AsyncSession = Depends(get_async_db)):
    models = await db.execute(select(Model).filter(Model.user_id == user_id))
    return [ModelResponse(**model.dict()) for model in models]

@router.post("/train")
async def train_model():
    try:
        process = subprocess.run(["python", "training_classif/train.py"], capture_output=True, text=True, check=True)

        return JSONResponse(content={"message": "Скрипт обучения успешно выполнен", "output": process.stdout})
    except subprocess.CalledProcessError as e:
        return JSONResponse(content={"message": "Ошибка при выполнении скрипта обучения", "error": e.stderr})