
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import async_sessionmaker

async def get_async_db():
    async with async_sessionmaker() as session:
        yield session
