"""
User Repository
"""

from datetime import date
from datetime import datetime as dt
from datetime import timedelta as td
from typing import Literal

from sqlalchemy.ext.asyncio import AsyncSession

from .abstract import Repository
from .. import models


class UserRepo(Repository[models.User]):
    type_model: type[models.User]

    def __init__(self, session: AsyncSession):
        super().__init__(type_model=models.User, session=session)

    async def new(
            self,
            email: str,
            password: str,
    ) -> models.User:
        model = models.User()
        model.email = email
        model.password = password

        new_entry = await self.session.merge(model)
        await self.session.flush()
        return new_entry

    async def get_by_email(self, email: str) -> models.User | None:
        where_clauses = [self.type_model.email == email]
        entry = await self.get(where_clauses=where_clauses)
        return entry

    async def get_count_users(self, period: Literal["today", "week", "month"] = None) -> int | None:
        where_clauses = None
        match period:
            case "today":
                today = dt.combine(date.today(), dt.min.time())
                where_clauses = [self.type_model.create_at >= today, self.type_model.create_at < today + td(days=1)]
            case "week":
                start_of_week = dt.now() - td(days=dt.now().weekday() + 1)
                where_clauses = [self.type_model.create_at >= start_of_week, self.type_model.create_at < dt.now()]
            case "month":
                start_of_month = dt.now().replace(day=1)
                end_of_month = start_of_month.replace(month=start_of_month.month + 1) - td(days=1)
                where_clauses = [self.type_model.create_at >= start_of_month, self.type_model.create_at <= end_of_month]
        entry = await self.count(where_clauses)
        return entry
