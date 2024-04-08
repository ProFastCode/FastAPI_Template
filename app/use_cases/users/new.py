from fastapi import status

from app import schemas
from app.core import security
from ..abstract import AbstractUseCase


class NewUseCase(AbstractUseCase):
    async def execute(self, data: schemas.users.NewUser):
        if await self.db.user.get_by_email(data.email):
            self.exp(status.HTTP_409_CONFLICT, "User is already taken.")

        hash_password = security.password_manager.hash_password(data.password)
        user = await self.db.user.new(data.email, hash_password)
        await self.db.session.commit()
        return user
