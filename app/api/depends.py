"""
Dependency Module
"""

from typing import AsyncGenerator

from fastapi import Depends, HTTPException, status, Cookie

from app.core import security
from app.database import Database, new_session, models


async def get_db() -> AsyncGenerator[Database]:
    session = await new_session()
    try:
        yield Database(session)
    finally:
        await session.close()


async def get_current_user(
    token_short: str = Cookie(), db: Database = Depends(get_db)
) -> models.User:
    if not token_short:
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
