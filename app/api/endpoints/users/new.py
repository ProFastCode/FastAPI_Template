"""
User Endpoints Module
"""

from fastapi import APIRouter, Depends

from app.api import depends
from app.core import exps
from app.core.security import pwd_manager
from app.database import Database
from app.schemas.users import GetUser, NewUser

router = APIRouter()


@router.post("/", response_model=GetUser)
async def new(data: NewUser, db: Database = Depends(depends.get_db)):
    """
    Создать нового пользователя:

    - **id**: ID-пользователя
    - **role**: Role-Пользователя
    - **email**: Email-Пользователя
    """

    if await db.user.get_by_email(data.email):
        raise exps.USER_EXISTS

    hash_password = pwd_manager.hash_password(data.password)
    user = await db.user.new(data.email, hash_password)
    await db.session.commit()
    return user
