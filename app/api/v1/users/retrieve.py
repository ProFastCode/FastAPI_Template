"""
User Endpoints Module
"""

from fastapi import APIRouter

from app.api import anotations
from app.models.user import UserRead

router = APIRouter()


@router.get("/", response_model=UserRead)
async def retrieve(user: anotations.CurrentUser):
    """
    Retrieve user
    """
    return user


__all__ = ["router"]
