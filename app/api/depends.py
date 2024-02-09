"""
Модуль с зависимостями для FastAPI.
"""

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import settings, auth
from app.database import Database, engine

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.APP_API_PREFIX}/users/token")


async def get_db() -> Database:
    async with AsyncSession(bind=engine, expire_on_commit=False) as session:
        try:
            yield Database(session)
        finally:
            await session.close()


async def get_current_user(token: str = Depends(oauth2_scheme), db: Database = Depends(get_db)):
    return await auth.authorization(token, db)
