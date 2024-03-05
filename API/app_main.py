from fastapi import FastAPI, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy import select
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from passlib.context import CryptContext
import asyncio

from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

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


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict):
    to_encode = data.copy()
    expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiration})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return {"id": user_id}
    except JWTError:
        raise credentials_exception



async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.create_task(create_tables())

app = FastAPI()

# Хеши паролей
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_async_db():
    async with async_sessionmaker() as session:
        yield session

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

# @app.post("/login")
# async def login(username: str = Form(...), password: str = Form(...), db: AsyncSession = Depends(get_async_db)):
#     result = await db.execute(select(User).filter(User.username == username))
#     user = result.scalar()

#     if not user or not password_context.verify(password, user.hashed_password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     access_token = create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}

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



@app.post("/models/", response_model=ModelResponse)
async def models(model: ModelCreate, user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_async_db)):
    db_model = Model(**model.dict(), user_id=user["id"])
    db.add(db_model)
    await db.commit()
    await db.refresh(db_model)
    return db_model

@app.get("/models/user/{user_id}", response_model=list[ModelResponse])
async def get_user_models(user_id: int, db: AsyncSession = Depends(get_async_db)):
    models = await db.execute(select(Model).filter(Model.user_id == user_id))
    return [ModelResponse(**model.dict()) for model in models]
