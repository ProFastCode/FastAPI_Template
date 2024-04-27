from fastapi import APIRouter, Depends

from app import models
from app.api import deps
from app.core import exps
from app.core.db import Database
from app.core.security import tkn_manager

router = APIRouter()


@router.post("/refresh/", response_model=models.ShortToken)
async def refresh_short_token(
    data: models.LongToken, db: Database = Depends(deps.get_db)
):
    """
    Обновить короткий токен
    """
    payload = tkn_manager.decode_long_token(data.long_token)
    if not await db.user.read(payload.get("id")):
        raise exps.USER_NOT_FOUND
    short_token = tkn_manager.create_short_token(payload)
    return models.ShortToken(short_token=short_token)
