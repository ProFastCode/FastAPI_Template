"""
Dependencies
"""

from typing import Annotated, AsyncGenerator

from fastapi import Depends
from fastapi.security import APIKeyHeader

from app.logic import Logic as _Logic
from app.models.users.user import User as _User


async def get_logic() -> AsyncGenerator[_Logic, None]:
    async with _Logic.create() as logic:
        yield logic


Logic = Annotated[_Logic, Depends(get_logic)]


async def get_user(
    token: Annotated[str, Depends(APIKeyHeader(name="access-token"))],
    logic: Logic,
) -> _User | None:
    return await logic.users.retrieve_by_token(token)


User = Annotated[_User, Depends(get_user)]
