from fastapi import APIRouter, Depends
from typing_extensions import Annotated

from app import models
from app.api import deps
from app.core import exps
from app.core.security import JWTTokenManager

router = APIRouter()


@router.post('/pair/', response_model=models.PairTokens)
async def new_pair_tokens(
    data: models.AuthToken,
    tkn_manager: Annotated[JWTTokenManager, Depends(deps.get_tkn_manager)],
):
    """
    Get pair tokens
    """

    payload = tkn_manager.decode_token(data.auth_token)
    if payload.get('type') != 'auth':
        raise exps.TOKEN_INVALID
    payload['type'] = 'access'
    access_token = tkn_manager.encode_token(payload, 120)
    payload['type'] = 'refresh'
    refresh_token = tkn_manager.encode_token(payload, 1440)
    return models.PairTokens(
        access_token=access_token, refresh_token=refresh_token
    )
