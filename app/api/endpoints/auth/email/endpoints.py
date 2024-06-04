from fastapi import APIRouter, Depends
from typing_extensions import Annotated

from app.api import deps
from app.core import exps
from app.core.db import Database
from app.core.security import JWTManager
from app.models.token import AuthToken
from app.models.user import User, UserCreate

router = APIRouter(prefix='/email')


@router.post('/', response_model=AuthToken)
async def token(
    data: UserCreate,
    db: Annotated[Database, Depends(deps.get_db)],
    jwt_manager: Annotated[JWTManager, Depends(deps.get_jwt_manager)],
):
    """
    Create user and/or retrieve new auth token
    """
    if user := await db.user.retrieve_by_email(data.email):
        if not deps.pwd_context.verify(data.password, user.password):
            raise exps.USER_IS_CORRECT
    else:
        password_hash = deps.pwd_context.hash(data.password)
        user = User(email=data.email, password=password_hash)
        await db.user.create(user)

    return AuthToken(
        token=jwt_manager.encode_token({'id': user.id, 'type': 'auth'}, 15)
    )
