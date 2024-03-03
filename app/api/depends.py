"""
Dependency Module
"""

from fastapi import Depends, HTTPException, status, Request

from app.core import security, settings
from app.database import Database, new_session, models


async def get_db() -> Database:
    session = await new_session()
    try:
        yield Database(session)
    finally:
        await session.close()


async def service(service_key: str):
    if settings.APP_SERVICE_KEY != service_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid service key"
        )


async def get_current_user(
    request: Request, db: Database = Depends(get_db)
) -> models.User:
    if not (token_short := request.cookies.get("_token_short")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Short token not transferred",
        )

    if not (token_short_data := security.decode_token(token_short)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your short token have expired",
        )

    if token_short_data.get("action") != "token_short":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You did not transfer a short token",
        )

    if not (user := await db.user.get(token_short_data.get("payload").get("id"))):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return user
