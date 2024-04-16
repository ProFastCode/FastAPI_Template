"""
User Endpoints Module
"""

from fastapi import APIRouter, Depends

from app import models
from app.api import deps
from app.core import exps
from app.core.db import Database
from app.core.security import pwd_manager

router = APIRouter()


@router.post("/", response_model=models.UserRead)
async def create(data: models.UserCreate, db: Database = Depends(deps.get_db)):
    """
    Создать нового пользователя:

    - **id**: ID-пользователя
    - **role**: Role-Пользователя
    - **email**: Email-Пользователя
    """

    if await db.user.get_by_email(data.email):
        raise exps.USER_EXISTS

    hash_password = pwd_manager.hash_password(data.password)
    user = await db.user.new(data.email, hash_password)
    await db.session.commit()
    return user
