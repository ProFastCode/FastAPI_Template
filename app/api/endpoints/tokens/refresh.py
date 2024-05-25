from fastapi import APIRouter, Depends
from typing_extensions import Annotated

from app import models
from app.api import deps
from app.core import exps
from app.core.db import Database
from app.core.security import JWTTokenManager

router = APIRouter()


@router.post('/refresh/', response_model=models.AccessToken)
async def refresh_access_token(
    data: models.RefreshToken,
    db: Annotated[Database, Depends(deps.get_db)],
    tkn_manager: Annotated[JWTTokenManager, Depends(deps.get_tkn_manager)],
):
    """
    Get new access token
    """
    payload = tkn_manager.decode_token(data.refresh_token)
    if payload.get('type') != 'refresh':
        raise exps.TOKEN_INVALID
    if not await db.user.read(payload.get('id')):
        raise exps.USER_NOT_FOUND
    access_token = tkn_manager.encode_token(payload, 120)
    return models.AccessToken(access_token=access_token)
