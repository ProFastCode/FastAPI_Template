from fastapi import APIRouter, Depends

from app import models
from app.api import deps
from app.core import exps
from app.core.db import Database
from app.core.security import tkn_manager, pwd_manager

router = APIRouter()


@router.post("/auth/", response_model=models.AuthToken)
async def new_auth_token(data: models.UserCreate, db: Database = Depends(deps.get_db)):
    """
    Получить токен аутентификации:

    - **email**: Email-пользователя
    - **password**: Password-Пользователя
    """
    if not (user := await db.user.get_by_email(data.email)):
        raise exps.USER_NOT_REGISTERED

    if not pwd_manager.verify_password(data.password, user.password):
        raise exps.USER_INCORRECT_PASSWORD

    auth_token = tkn_manager.create_auth_token({"id": user.id})
    return models.AuthToken(auth_token=auth_token)
