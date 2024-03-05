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


from db.database import async_engine, async_sessionmaker, Base
from db.models import User, Model, ModelCreate, ModelResponse
from db.security import get_current_user
from routers import router

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.create_task(create_tables())

app = FastAPI()

app.include_router(router, prefix="/api")
