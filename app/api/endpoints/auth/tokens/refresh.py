from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader
from typing_extensions import Annotated

from app.api import deps
from app.core import exps
from app.core.db import Database
from app.core.security import JWTManager
from app.models.token import PairTokens

router = APIRouter(prefix='/refresh')


@router.get('/', response_model=PairTokens, response_model_exclude_none=True)
async def refresh_access_token(
    token: Annotated[str, APIKeyHeader(name='refresh-token')],
    db: Annotated[Database, Depends(deps.get_db)],
    jwt_manager: Annotated[JWTManager, Depends(deps.get_jwt_manager)],
):
    """
    Retrieve new access token
    """
    payload = jwt_manager.decode_token(token)
    if payload.get('type') != 'refresh':
        raise exps.TOKEN_INVALID
    if not await db.user.retrieve_one(ident=payload.get('id')):
        raise exps.USER_NOT_FOUND
    payload['type'] = 'access'
    return PairTokens(access=jwt_manager.encode_token(payload, 120))
