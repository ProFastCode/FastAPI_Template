from fastapi import APIRouter

from app.api import deps
from app.models import auth as auth_models
from app.models import user as user_models

router = APIRouter(prefix="/auth")


@router.post("/token", response_model=auth_models.AccessToken)
async def token(data: user_models.UserCreate, logic: deps.Logic):
    """
    Retrieve new access token
    """
    return await logic.auth.generate_token(data)
