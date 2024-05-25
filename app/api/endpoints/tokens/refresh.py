from fastapi import APIRouter, Depends
from typing_extensions import Annotated

from app import models
from app.api import deps
from app.core import exps
from app.core.db import Database
from app.core.security import JWTManager

router = APIRouter()


@router.post('/refresh/', response_model=models.AccessToken)
async def refresh_access_token(
    data: models.RefreshToken,
    db: Annotated[Database, Depends(deps.get_db)],
    jwt_manager: Annotated[JWTManager, Depends(deps.get_jwt_manager)],
):
    """
    Get new access token
    """
    payload = jwt_manager.decode_token(data.refresh_token)
    if payload.get('type') != 'refresh':
        raise exps.TOKEN_INVALID
    if not await db.user.read(payload.get('id')):
        raise exps.USER_NOT_FOUND
    return models.AccessToken(token=jwt_manager.encode_token(payload, 120))
