from fastapi import APIRouter, Depends, Request

from app.api import depends, exps
from app.core.security import tkn_manager
from app.database import Database
from app.schemas.tokens import PairTokens, AuthToken

router = APIRouter()


@router.post("/pair/", response_model=PairTokens)
async def new_pair_tokens(
    data: AuthToken, request: Request, db: Database = Depends(depends.get_db)
):
    """
    Получить парные токены:

    - **auth_token**: Токен аутентификации
    """
    payload = tkn_manager.decode_auth_token(data.auth_token)
    if not (user := await db.user.get(payload.get("id"))):
        raise exps.USER_NOT_FOUND
    long_token = tkn_manager.create_long_token(payload)
    short_token = tkn_manager.create_short_token(payload)
    await db.user_activity.new(
        user_id=user.id,
        action="new_pair_tokens",
        comment="Новая пара токенов",
        user_agent=request.headers.get("User-Agent"),
        ip=request.client.host,
    )
    await db.session.commit()
    return PairTokens(long_token=long_token, short_token=short_token)
