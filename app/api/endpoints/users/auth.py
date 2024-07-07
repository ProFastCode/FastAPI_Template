from fastapi import APIRouter

from app.api import anotations
from app.core import exps
from app.models.token import AccessToken
from app.models.user import UserCreate

router = APIRouter(prefix='/auth')


@router.post('/token/', response_model=AccessToken)
async def token(
    data: UserCreate, db: anotations.Database, security: anotations.Security
):
    """
    Retrieve new access token
    """
    if user := await db.user.retrieve_by_email(data.email):
        if not security.pwd.checkpwd(data.password, user.password):
            raise exps.USER_IS_CORRECT
        access_token = security.jwt.encode_token({'id': user.id}, 1440)
        return AccessToken(token=access_token)

    raise exps.USER_NOT_FOUND
