from fastapi import APIRouter, Depends, Request

from app.api import depends, exps
from app.core.security import tkn_manager, pswd_manager
from app.database import Database
from app.schemas.tokens import AuthToken
from app.schemas.users import AuthUser

router = APIRouter()


@router.post("/auth/", response_model=AuthToken)
async def new_auth_token(
    data: AuthUser, request: Request, db: Database = Depends(depends.get_db)
):
    """
    Получить токен аутентификации:

    - **email**: Email-пользователя
    - **password**: Password-Пользователя
    """
    if not (user := await db.user.get_by_email(data.email)):
        raise exps.USER_NOT_REGISTERED

    if not pswd_manager.verify_password(data.password, user.password):
        raise exps.USER_INCORRECT_PASSWORD

    auth_token = tkn_manager.create_auth_token({"id": user.id})
    await db.user_activity.new(
        user_id=user.id,
        action="new_auth_token",
        comment="Новый токен аутентификации",
        user_agent=request.headers.get("User-Agent"),
        ip=request.client.host,
    )
    await db.session.commit()
    return AuthToken(auth_token=auth_token)
