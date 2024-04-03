"""
Stats Users Endpoints Module
"""

from fastapi import APIRouter, Depends

from app import schemas
from app.api import depends
from app.database import Database

router = APIRouter()


@router.get("/users_count", response_model=schemas.staff.stats.UsersCount)
async def users_count(db: Database = Depends(depends.get_db)):
    """
    Получить информацию о количестве пользователей:
    """

    quantity_for_today = await db.user.get_count_users("today")
    quantity_per_week = await db.user.get_count_users("week")
    quantity_per_month = await db.user.get_count_users("month")
    quantity_for_all_time = await db.user.get_count_users()

    return schemas.staff.stats.UsersCount(
        quantity_for_today=quantity_for_today,
        quantity_per_week=quantity_per_week,
        quantity_per_month=quantity_per_month,
        quantity_for_all_time=quantity_for_all_time,
    )
