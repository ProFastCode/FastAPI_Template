from fastapi import APIRouter

from app import models
from app.core.security import tkn_manager

router = APIRouter()


@router.post("/pair/", response_model=models.PairTokens)
async def new_pair_tokens(data: models.AuthToken):
    """
    Получить парные токены
    """
    payload = tkn_manager.decode_auth_token(data.auth_token)
    long_token = tkn_manager.create_long_token(payload)
    short_token = tkn_manager.create_short_token(payload)
    return models.PairTokens(long_token=long_token, short_token=short_token)
