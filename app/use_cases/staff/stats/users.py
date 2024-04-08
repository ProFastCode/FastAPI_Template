from app import schemas
from app.use_cases.abstract import AbstractUseCase


class UsersUseCase(AbstractUseCase):
    async def execute(self):
        quantity_for_today = await self.db.user.get_count_users("today")
        quantity_per_week = await self.db.user.get_count_users("week")
        quantity_per_month = await self.db.user.get_count_users("month")
        quantity_for_all_time = await self.db.user.get_count_users()

        return schemas.staff.stats.UsersCount(
            quantity_for_today=quantity_for_today,
            quantity_per_week=quantity_per_week,
            quantity_per_month=quantity_per_month,
            quantity_for_all_time=quantity_for_all_time,
        )
