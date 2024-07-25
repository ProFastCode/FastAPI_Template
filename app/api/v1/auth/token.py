from fastapi import APIRouter

from app.api import deps
from app.models.auth import AccessToken
from app.models.users.user import UserCreate

router = APIRouter(prefix='/token')


@router.post('/', response_model=AccessToken)
async def token(data: UserCreate, logic: deps.Logic):
    """
    Retrieve new access token
    """
    return await logic.auth.generate_token(data)


__all__ = ['router']
