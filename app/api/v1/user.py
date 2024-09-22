from fastapi import APIRouter

from app.api import deps
from app.models import user as user_models

router = APIRouter(prefix="/users")


@router.post("", response_model=user_models.UserRetrieve)
async def create(data: user_models.UserCreate, logic: deps.Logic):
    """
    Create user
    """
    return await logic.user.create(data)


@router.get("", response_model=user_models.UserRetrieve)
async def retrieve(user: deps.User):
    """
    Retrieve user
    """
    return user
