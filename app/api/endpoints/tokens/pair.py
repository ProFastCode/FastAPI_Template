from fastapi import APIRouter, Depends
from typing_extensions import Annotated

from app import models
from app.api import deps
from app.core import exps
from app.core.security import JWTManager

router = APIRouter()


@router.post('/pair/', response_model=models.PairTokens)
async def new_pair_tokens(
    data: models.AuthToken,
    jwt_manager: Annotated[JWTManager, Depends(deps.get_jwt_manager)],
):
    """
    Get pair tokens
    """

    payload = jwt_manager.decode_token(data.auth_token)
    if payload.get('type') != 'auth':
        raise exps.TOKEN_INVALID
    payload['type'] = 'access'
    access_token = models.AccessToken(token=jwt_manager.encode_token(payload, 120))
    payload['type'] = 'refresh'
    refresh_token = models.RefreshToken(token=jwt_manager.encode_token(payload, 1440))
    tokens = models.PairTokens(access=access_token, refresh=refresh_token)
    return tokens
