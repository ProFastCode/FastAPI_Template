"""
Dependencies
"""

from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader

from app.logic import Logic as _Logic
from app.models.user import User as _User


async def get_logic() -> _Logic:
    return await _Logic.create()


Logic = Annotated[_Logic, Depends(get_logic)]


async def get_user(
    token: Annotated[str, Depends(APIKeyHeader(name="access-token"))],
    logic: Logic,
) -> _User | None:
    return await logic.users.retrieve_by_token(token)


User = Annotated[_User, Depends(get_user)]
