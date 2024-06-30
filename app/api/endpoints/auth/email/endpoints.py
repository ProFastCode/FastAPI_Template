from fastapi import APIRouter, Depends
from typing_extensions import Annotated

from app.api import deps
from app.core import exps
from app.core.db import Database
from app.core.security import JWTManager
from app.models.token import AccessToken
from app.models.user import User, UserCreate, UserRead

router = APIRouter(prefix="/email")


@router.post("/registration", response_model=UserRead)
async def registration(
    data: UserCreate,
    db: Annotated[Database, Depends(deps.get_db)],
):
    """
    Create user
    """
    if await db.user.retrieve_by_email(data.email):
        raise exps.USER_EXISTS

    password_hash = deps.pwd_context.hash(data.password)
    user = User(email=data.email, password=password_hash)
    await db.user.create(user)
    return user


@router.post("/token", response_model=AccessToken)
async def token(
    data: UserCreate,
    db: Annotated[Database, Depends(deps.get_db)],
    jwt_manager: Annotated[JWTManager, Depends(deps.get_jwt_manager)],
):
    """
    Retrieve new access token
    """
    if user := await db.user.retrieve_by_email(data.email):
        if not deps.pwd_context.verify(data.password, user.password):
            raise exps.USER_IS_CORRECT

        return AccessToken(token=jwt_manager.encode_token({"id": user.id}, 1440))
