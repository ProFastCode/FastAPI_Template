"""
Dependencies
"""

from fastapi import Depends
from fastapi.security import APIKeyHeader
from passlib.context import CryptContext
from typing_extensions import Annotated, AsyncGenerator

from app.models.user import User

from . import Security, db, exps

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


async def get_db() -> AsyncGenerator[db.Database]:
    async with db.SessionLocal() as session:
        yield db.Database(session)


async def get_security() -> Security:
    return Security()


async def get_current_user(
    token: Annotated[str, Depends(APIKeyHeader(name='access-token'))],
    security: Annotated[Security, Depends(get_security)],
    db: Annotated[db.Database, Depends(get_db)],
) -> User | None:
    if payload := security.jwt.decode_token(token):
        if not (user := await db.user.retrieve_one(ident=payload.get('id'))):
            raise exps.USER_NOT_FOUND
        else:
            return user
