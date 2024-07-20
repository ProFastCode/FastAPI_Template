from fastapi import APIRouter

from app.api import deps
from app.models.token import AccessToken
from app.models.user import UserCreate

router = APIRouter(prefix="/token")


@router.post("/", response_model=AccessToken)
async def token(data: UserCreate, logic: deps.Logic):
    """
    Retrieve new access token
    """
    return await logic.users.auth.generate_token(**data.model_dump())


__all__ = ["router"]
