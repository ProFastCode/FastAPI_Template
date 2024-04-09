from fastapi import APIRouter, Depends, Request

from app.api import depends
from app.core import exps
from app.core.security import tkn_manager
from app.database import Database
from app.schemas.tokens import LongToken, ShortToken

router = APIRouter()


@router.post("/refresh/", response_model=ShortToken)
async def refresh_short_token(
    data: LongToken, request: Request, db: Database = Depends(depends.get_db)
):
    """
    Обновить короткий токен:

    - **long_token**: Длинный токен
    """
    payload = tkn_manager.decode_long_token(data.long_token)
    if not (user := await db.user.get(payload.get("id"))):
        raise exps.USER_NOT_FOUND
    short_token = tkn_manager.create_short_token(payload)
    await db.user_activity.new(
        user.id,
        "refresh_short_token",
        "Обновлён короткий токен",
        user_agent=request.headers.get("User-Agent"),
        ip=request.client.host,
    )
    await db.session.commit()
    return ShortToken(short_token=short_token)
