"""
User Endpoints Module
"""

from fastapi import APIRouter, Depends

from app import schemas
from app.api import depends
from app.database import models

router = APIRouter()


@router.get("/")
async def get(user: models.User = Depends(depends.get_current_user)) -> schemas.UserGet:
    """
    Получить информацию о пользователе:

    - **id**: ID-пользователя
    - **username**: Username-Пользователя
    """
    return schemas.UserGet(**user.__dict__)
