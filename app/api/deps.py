"""
Dependencies
"""

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, OAuth2AuthorizationCodeBearer
from typing_extensions import Annotated

from app import models
from app.core import exps, settings
from app.core.db import Database, SessionLocal
from app.core.security import JWTManager

oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl="/api/auth/oauth2/telegram/login/",
                                              tokenUrl="/api/auth/tokens/pair/", refreshUrl="/api/auth/tokens/refresh/")


async def get_db() -> Database:
    async with SessionLocal() as session:
        yield Database(session)


async def get_jwt_manager() -> JWTManager:
    return JWTManager(settings.APP_SECRET_KEY)


async def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
                           jwt_manager: Annotated[JWTManager, Depends(get_jwt_manager)],
                           db: Annotated[Database, Depends(get_db)], ) -> models.User:
    payload = jwt_manager.decode_token(credentials.credentials)
    if payload.get('type') != 'access':
        raise exps.TOKEN_INVALID
    if not (user := await db.user.retrieve_one(ident=payload.get('id'))):
        raise exps.USER_NOT_FOUND
    return user
