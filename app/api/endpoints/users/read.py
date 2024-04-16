"""
User Endpoints Module
"""

from fastapi import APIRouter, Depends

from app import models
from app.api import deps

router = APIRouter()


@router.get("/", response_model=models.UserRead)
async def read(user: models.User = Depends(deps.get_current_user)):
    """
    Получить информацию о пользователе:

    - **id**: ID-пользователя
    - **staff**: Персонал ли
    - **email**: Email-Пользователя
    """
    return user
