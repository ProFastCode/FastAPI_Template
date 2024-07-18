from fastapi import APIRouter

from app.api import anotations
from app.models.token import AccessToken
from app.models.user import UserCreate

router = APIRouter(prefix="/token")


@router.post("/", response_model=AccessToken)
async def token(data: UserCreate, logic: anotations.Logic):
    """
    Retrieve new access token
    """
    return await logic.users.generate_token(**data.model_dump())


__all__ = ["router"]
