from fastapi import APIRouter, Depends, HTTPException, status, Request, Header

from app import schemas
from app.api import depends
from app.core import security
from app.database import Database

router = APIRouter()


@router.get("/refresh/", response_model=schemas.TokenShort)
async def refresh_short_token(
    request: Request,
    long_token: str,
    user_agent: str = Header(),
    db: Database = Depends(depends.get_db),
):
    long_token_data = security.decode_token(long_token)
    payload = long_token_data.get("payload")

    if long_token_data.get("action") != "token_long":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This must be an long token",
        )

    if not (user := await db.user.get(payload.get("id"))):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    token_short = security.create_token_short(payload)
    await db.user_activity.new(
        user.id,
        "refresh_short_token",
        "Обновлён короткий токен",
        user_agent=user_agent,
        ip=request.client.host,
    )
    await db.session.commit()

    return token_short
