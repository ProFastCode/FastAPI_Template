"""
User Endpoints Module
"""

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app import schemas
from app.api import depends
from app.database import Database

router = APIRouter()


@router.post("/")
async def new(user: schemas.UserNew, db: Database = Depends(depends.get_db)) -> schemas.UserGet:
    """
    Создать нового пользователя:

    - **id**: ID-пользователя
    - **username**: Username-Пользователя
    - **password**: Password-Пользователя
    """

    if await db.user.get_by_username(user.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Такой пользователь существует.",
        )

    user = await db.user.new(user.username, user.password)
    await db.session.commit()
    return schemas.UserGet(**user.__dict__)
