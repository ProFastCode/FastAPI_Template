"""
Dependencies
"""

from fastapi import Depends, HTTPException, status, Header

from app import models
from app.core import security
from app.core.db import SessionLocal, Database


async def get_db() -> Database:
    async with SessionLocal() as session:
        yield Database(session)


async def get_current_user(
        short_token: str = Header(),
        db: Database = Depends(get_db),
) -> models.User:
    payload = security.tkn_manager.decode_short_token(short_token)
    if not (user := await db.user.read(payload.get("id"))):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user


async def is_superuser(
        user: models.User = Depends(get_current_user),
) -> None:
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this section",
        )
