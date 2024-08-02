"""
User Endpoints Module
"""

from fastapi import APIRouter

from app.api import deps
from app.models.users import UserRead

router = APIRouter()


@router.get('/', response_model=UserRead)
async def retrieve(user: deps.User):
    """
    Retrieve user
    """
    return user


__all__ = ['router']
