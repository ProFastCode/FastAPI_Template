"""
Schemas Stats
"""

from pydantic import ConfigDict, BaseModel


class BaseStats(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UsersCount(BaseStats):
    quantity_for_today: int
    quantity_per_week: int
    quantity_per_month: int
    quantity_for_all_time: int
