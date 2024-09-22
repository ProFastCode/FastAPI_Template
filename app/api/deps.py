"""
Dependencies
"""

from typing import Annotated, AsyncGenerator

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.logic import Logic as _Logic
from app.models.user import User as _User


security = HTTPBearer()


async def get_logic() -> AsyncGenerator[_Logic, None]:
    async with _Logic.create() as logic:
        yield logic


Logic = Annotated[_Logic, Depends(get_logic)]


async def get_user(
    creds: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    logic: Logic,
) -> _User | None:
    return await logic.user.retrieve_by_token(creds.credentials)


User = Annotated[_User, Depends(get_user)]
