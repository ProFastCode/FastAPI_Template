"""
User Endpoints Module
"""

from fastapi import APIRouter, Depends

from app.api import depends
from app.database import models
from app.schemas.users import GetUser

router = APIRouter()


@router.get("/", response_model=GetUser)
async def get(user: models.User = Depends(depends.get_current_user)):
    """
    Получить информацию о пользователе:

    - **id**: ID-пользователя
    - **role**: Role-Пользователя
    - **email**: Email-Пользователя
    """
    return user
