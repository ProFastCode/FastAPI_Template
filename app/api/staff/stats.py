"""
Stats Endpoints Module
"""

from fastapi import APIRouter, Depends

from app import schemas
from app.api import depends
from app.database import Database

router = APIRouter(prefix="/stats")


@router.get("/users", response_model=schemas.StatsUsers)
async def stats_users(db: Database = Depends(depends.get_db)):
    """
    Получить информацию о пользователе:

    - **id**: ID-пользователя
    - **username**: Username-Пользователя
    """

    users = await db.user.get_many()
    return schemas.StatsUsers(count=len(users))
