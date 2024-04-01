from fastapi import APIRouter, Depends, Request, HTTPException, status

from app import schemas
from app.api import depends
from app.core import security
from app.database import Database

router = APIRouter()


@router.post("/auth/", response_model=schemas.AuthToken)
async def new_auth_token(
    request: Request, data: schemas.UserNew, db: Database = Depends(depends.get_db)
):
    """
    Получить токен аутентификации:

    - **email**: Email-пользователя
    - **password**: Password-Пользователя
    """
    user_agent = request.headers.get("User-Agent")
    if not (user := await db.user.get_by_email(data.email, data.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A user not yet been registered",
        )
    auth_token = security.create_auth_token({"id": user.id})
    await db.user_activity.new(
        user_id=user.id,
        action="new_auth_token",
        comment="Новый токен аутентификации",
        user_agent=user_agent,
        ip=request.client.host,
    )
    await db.session.commit()
    return auth_token
