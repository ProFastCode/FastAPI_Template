from fastapi import APIRouter, Depends, HTTPException, status, Request

from app import schemas
from app.api import depends
from app.core import security
from app.database import Database

router = APIRouter()


@router.post("/refresh/", response_model=schemas.tokens.ShortToken)
async def refresh_short_token(
    request: Request,
    data: schemas.tokens.LongToken,
    db: Database = Depends(depends.get_db),
):
    """
    Обновить короткий токен:

    - **long_token**: Длинный токен
    """
    user_agent = request.headers.get("User-Agent")
    payload = security.decode_long_token(data.long_token)
    if not (user := await db.user.get(payload.get("id"))):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    short_token = security.create_short_token(payload)
    await db.user_activity.new(
        user.id,
        "refresh_short_token",
        "Обновлён короткий токен",
        user_agent=user_agent,
        ip=request.client.host,
    )
    await db.session.commit()
    return short_token
