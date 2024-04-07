from fastapi import APIRouter, Depends, Request, HTTPException, status

from app import schemas
from app.api import depends
from app.core import security
from app.database import Database

router = APIRouter()


@router.post("/pair/", response_model=schemas.tokens.PairTokens)
async def new_pair_tokens(
    request: Request,
    data: schemas.tokens.AuthToken,
    db: Database = Depends(depends.get_db),
):
    """
    Получить парные токены:

    - **auth_token**: Токен аутентификации
    """
    user_agent = request.headers.get("User-Agent")
    payload = security.token_manager.decode_auth_token(data.auth_token)
    if not (user := await db.user.get(payload.get("id"))):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    long_token = security.token_manager.create_long_token(payload)
    short_token = security.token_manager.create_short_token(payload)
    await db.user_activity.new(
        user_id=user.id,
        action="new_pair_tokens",
        comment="Новая пара токенов",
        user_agent=user_agent,
        ip=request.client.host,
    )
    await db.session.commit()
    return schemas.tokens.PairTokens(long_token=long_token, short_token=short_token)
