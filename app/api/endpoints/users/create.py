from fastapi import APIRouter

from app.api import anotations
from app.models.user import UserCreate, UserRead

router = APIRouter(prefix='/create')


@router.post('/', response_model=UserRead)
async def create(data: UserCreate, logic: anotations.Logic):
    """
    Create user
    """
    return await logic.users.create(**data.model_dump())
