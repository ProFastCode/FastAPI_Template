"""
Dependencies
"""

from fastapi import Depends
from fastapi.security import APIKeyHeader
from passlib.context import CryptContext
from typing_extensions import Annotated

from app.core import exps, settings
from app.core.db import Database, SessionLocal
from app.core.security import JWTManager
from app.models.user import User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def get_db() -> Database:
    async with SessionLocal() as session:
        yield Database(session)


async def get_jwt_manager() -> JWTManager:
    return JWTManager(settings.APP_SECRET_KEY)


async def get_current_user(
    token: Annotated[str, Depends(APIKeyHeader(name='access-token'))],
    jwt_manager: Annotated[JWTManager, Depends(get_jwt_manager)],
    db: Annotated[Database, Depends(get_db)],
) -> User:
    payload = jwt_manager.decode_token(token)
    if payload.get('type') != 'access':
        raise exps.TOKEN_INVALID
    if not (user := await db.user.retrieve_one(ident=payload.get('id'))):
        raise exps.USER_NOT_FOUND
    return user
