"""
User Endpoints Module
"""

from fastapi import APIRouter, Depends
from typing_extensions import Annotated

from app import models
from app.api import deps

router = APIRouter()


@router.get('/', response_model=models.UserRead)
async def retrieve(
    user: Annotated[models.User, Depends(deps.get_current_user)]
):
    """
    Get user
    """
    return user
