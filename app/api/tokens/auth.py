from fastapi import APIRouter, Depends, HTTPException, status, Request, Header

from app import schemas
from app.api import depends
from app.core import security
from app.database import Database

router = APIRouter()


@router.get("/auth/", response_model=schemas.TokenAuth)
async def new_auth_token(
    request: Request,
    email: str,
    password: str,
    user_agent: str = Header(),
    db: Database = Depends(depends.get_db),
):
    if not (user := await db.user.get_by_email(email, password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A user not yet been registered",
        )
    token_auth = security.create_token_auth({"id": user.id})

    await db.user_activity.new(
        user_id=user.id,
        action="new_auth_token",
        comment="Новый токен аутентификации",
        user_agent=user_agent,
        ip=request.client.host,
    )
    await db.session.commit()

    return token_auth
