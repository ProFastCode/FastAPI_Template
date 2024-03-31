"""
User Endpoints Module
"""

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app import schemas
from app.api import depends
from app.database import Database

router = APIRouter()


@router.post("/", response_model=schemas.UserGet)
async def new(user: schemas.UserNew, db: Database = Depends(depends.get_db)):
    """
    Создать нового пользователя:

    - **id**: ID-пользователя
    - **email**: Email-Пользователя
    - **password**: Password-Пользователя
    """

    if await db.user.get_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already taken.",
        )

    user = await db.user.new(user.email, user.password)
    await db.session.commit()
    return user
