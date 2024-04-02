"""
Schemas Stats
"""

from pydantic import ConfigDict, BaseModel, Field


class BaseStats(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class StatsUsers(BaseStats):
    count: int = Field()
