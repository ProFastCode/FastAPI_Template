"""
User Endpoints Module
"""
import hmac

from fastapi import APIRouter, Depends
from typing_extensions import Annotated

from app import models
from app.api import deps
from app.core import exps, settings
from app.core.db import Database
from app.core.security import JWTTokenManager

router = APIRouter()


@router.post('/auth/', response_model=models.AuthToken)
async def auth(
        user: models.UserCreate,
        db: Annotated[Database, Depends(deps.get_db)],
        tkn_manager: Annotated[JWTTokenManager, Depends(deps.get_tkn_manager)],
):
    """
    Get auth token
    """
    data_check_string = '\n'.join(
        sorted(
            f'{x}={y}'
            for x, y in user.model_dump().items()
            if x not in 'hash' and y is not None
        )
    )
    computed_hash = hmac.new(
        settings.telegram_bot_token_hash.digest(),
        data_check_string.encode(),
        'sha256',
    ).hexdigest()
    is_correct = hmac.compare_digest(computed_hash, user.hash)
    if not is_correct:
        raise exps.USER_IS_CORRECT

    model_user = models.User(**user.model_dump())
    if cur_user := await db.user.retrieve(user.id):
        await db.user.update(cur_user.id, **model_user.model_dump())
    else:
        await db.user.create(model_user)
    await db.session.commit()
    auth_token = tkn_manager.encode_token({'id': user.id, 'type': 'auth'}, 15)
    return models.AuthToken(auth_token=auth_token)
