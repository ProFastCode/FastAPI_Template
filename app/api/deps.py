"""
Dependencies
"""

from fastapi import Depends, Header
from typing_extensions import Annotated

from app import models
from app.core import exps, settings
from app.core.db import Database, SessionLocal
from app.core.security import JWTManager, TelegramAuth


async def get_db() -> Database:
    async with SessionLocal() as session:
        yield Database(session)


async def get_jwt_manager() -> JWTManager:
    return JWTManager(settings.APP_SECRET_KEY)


async def get_telegram_auth() -> TelegramAuth:
    return TelegramAuth(
        settings.TELEGRAM_BOT_TOKEN, settings.TELEGRAM_BOT_USERNAME
    )


async def get_current_user(
        access_token: Annotated[str, Header()],
        db: Annotated[Database, Depends(get_db)],
        jwt_manager: Annotated[JWTManager, Depends(get_jwt_manager)],
) -> models.User:
    payload = jwt_manager.decode_token(access_token)
    if payload.get('type') != 'access':
        raise exps.TOKEN_INVALID
    if not (user := await db.user.read(payload.get('id'))):
        raise exps.USER_NOT_FOUND
    return user
