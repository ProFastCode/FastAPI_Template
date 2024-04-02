"""
User Endpoints Module
"""

from fastapi import APIRouter, Depends

from app import schemas
from app.api import depends
from app.database import models

router = APIRouter()


@router.get("/", response_model=schemas.GetUser)
async def get(user: models.User = Depends(depends.get_current_user)):
    """
    Получить информацию о пользователе:

    - **id**: ID-пользователя
    - **username**: Username-Пользователя
    """
    return user
