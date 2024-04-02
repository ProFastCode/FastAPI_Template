"""
Dependency Module
"""

from fastapi import Depends, HTTPException, status, Header

from app.core import security
from app.database import Database, new_session, models


async def get_db() -> Database:
    session = await new_session()
    try:
        yield Database(session)
    finally:
        await session.close()


async def get_current_user(
    short_token: str = Header(),
    db: Database = Depends(get_db),
) -> models.User:
    payload = security.decode_short_token(short_token)
    if not (user := await db.user.get(payload.get("id"))):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return user
