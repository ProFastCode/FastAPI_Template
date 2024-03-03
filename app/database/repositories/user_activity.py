"""
User Activity Repository
"""

from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import Repository
from .. import models


class UserActivityRepo(Repository[models.UserActivity]):
    type_model: type[models.UserActivity]

    def __init__(self, session: AsyncSession):
        super().__init__(type_model=models.UserActivity, session=session)

    async def new(
        self,
        user_id: int,
        action: str,
        comment: str | None = None,
        user_agent: str | None = None,
        ip: str | None = None,
    ) -> models.UserActivity:
        model = models.UserActivity()
        model.user_id = user_id
        model.action = action
        model.comment = comment
        model.user_agent = user_agent
        model.ip = ip

        new_entry = await self.session.merge(model)
        await self.session.flush()
        return new_entry

    async def get_many_by_action(
        self, action: str, user_id: int | None = None
    ) -> list[models.UserActivity] | None:
        where_clause = [self.type_model.action == action]
        if user_id:
            where_clause.append(self.type_model.user_id == user_id)
        entries = await self.get_many(where_clause)
        return entries
