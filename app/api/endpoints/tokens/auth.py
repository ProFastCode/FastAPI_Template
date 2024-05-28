"""
User Endpoints Module
"""

from fastapi import APIRouter, Depends
from typing_extensions import Annotated

from app import models
from app.api import deps
from app.core import exps
from app.core.db import Database
from app.core.security import JWTManager, oauth

router = APIRouter(prefix='/auth')


@router.post('/telegram/', response_model=models.AuthToken)
async def telegram(
    user: models.UserCreate,
    db: Annotated[Database, Depends(deps.get_db)],
    jwt_manager: Annotated[JWTManager, Depends(deps.get_jwt_manager)],
    oauth_telegram: Annotated[oauth, Depends(deps.get_oauth_telegram)],
):
    """
    Get auth token
    """
    user_dict = user.model_dump()
    computed_hash = oauth_telegram.generate_hash(user_dict)
    if not oauth_telegram.is_correct(computed_hash, user.hash):
        raise exps.USER_IS_CORRECT

    model_user = models.User(**user.model_dump())
    if cur_user := await db.user.retrieve_one(ident=user.id):
        await db.user.update(cur_user.id, **model_user.model_dump())
    else:
        await db.user.create(model_user)
    await db.session.commit()
    token = models.AuthToken(
        token=jwt_manager.encode_token({'id': user.id, 'type': 'auth'}, 15)
    )
    return token
