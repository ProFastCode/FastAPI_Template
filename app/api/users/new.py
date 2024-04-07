"""
User Endpoints Module
"""

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app import schemas
from app.api import depends
from app.database import Database
from app.core import security

router = APIRouter()


@router.post("/", response_model=schemas.users.GetUser)
async def new(user: schemas.users.NewUser, db: Database = Depends(depends.get_db)):
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

    hash_password = security.password_manager.hash_password(user.password)
    user = await db.user.new(user.email, hash_password)
    await db.session.commit()
    return user
