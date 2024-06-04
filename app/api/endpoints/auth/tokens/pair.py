from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader
from typing_extensions import Annotated

from app.api import deps
from app.core import exps
from app.core.security import JWTManager
from app.models.token import PairTokens

router = APIRouter(prefix='/pair')


@router.get('/', response_model=PairTokens)
async def new_pair_tokens(
    token: Annotated[str, APIKeyHeader(name='auth-token')],
    jwt_manager: Annotated[JWTManager, Depends(deps.get_jwt_manager)],
):
    """
    Retrieve new pair tokens
    """
    payload = jwt_manager.decode_token(token)
    if payload.get('type') != 'auth':
        raise exps.TOKEN_INVALID
    payload['type'] = 'access'
    access_token = jwt_manager.encode_token(payload, 120)
    payload['type'] = 'refresh'
    refresh_token = jwt_manager.encode_token(payload, 1440)
    tokens = PairTokens(access=access_token, refresh=refresh_token)
    return tokens
