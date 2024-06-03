from fastapi import APIRouter, Depends, Query
from fastapi.responses import PlainTextResponse
from typing_extensions import Annotated

from app.api import deps
from app.core import exps
from app.core.db import Database
from app.core.security import JWTManager

router = APIRouter(prefix='/refresh')


@router.get('/')
async def refresh_access_token(token: Annotated[str, Query(description="refresh-token")],
        db: Annotated[Database, Depends(deps.get_db)],
        jwt_manager: Annotated[JWTManager, Depends(deps.get_jwt_manager)], ):
    """
    Get new access token
    """
    payload = jwt_manager.decode_token(token)
    if payload.get('type') != 'refresh':
        raise exps.TOKEN_INVALID
    if not await db.user.retrieve_one(ident=payload.get('id')):
        raise exps.USER_NOT_FOUND
    payload['type'] = 'access'
    return PlainTextResponse(jwt_manager.encode_token(payload, 120))
