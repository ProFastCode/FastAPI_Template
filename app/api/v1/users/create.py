from fastapi import APIRouter

from app.api import deps
from app.models.user import UserCreate, UserRead

router = APIRouter(prefix="/create")


@router.post("/", response_model=UserRead)
async def create(data: UserCreate, logic: deps.Logic):
    """
    Create user
    """
    return await logic.users.create(**data.model_dump())


__all__ = ["router"]
