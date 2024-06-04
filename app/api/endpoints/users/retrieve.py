"""
User Endpoints Module
"""

from fastapi import APIRouter, Depends
from typing_extensions import Annotated

from app.api import deps
from app.models.user import User, UserRead

router = APIRouter()


@router.get('/', response_model=UserRead)
async def retrieve(user: Annotated[User, Depends(deps.get_current_user)]):
    """
    Retrieve user
    """
    return user
