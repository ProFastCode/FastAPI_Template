from typing import TYPE_CHECKING

from app.core import exps
from app.models.auth import AccessToken
from app.models.users.user import UserCreate

if TYPE_CHECKING:
    from app.logic import Logic


class Auth:
    def __init__(self, logic: 'Logic'):
        self.logic = logic

    async def generate_token(self, data: UserCreate) -> AccessToken | None:
        if (
            user := await self.logic.db.user.retrieve_by_email(data.email)
        ) is None:
            raise exps.UserNotFoundException()
        if not self.logic.security.pwd.checkpwd(data.password, user.password):
            raise exps.UserIsCorrectException()
        access_token = self.logic.security.jwt.encode_token(
            {'id': user.id}, 1440
        )
        return AccessToken(token=access_token)
