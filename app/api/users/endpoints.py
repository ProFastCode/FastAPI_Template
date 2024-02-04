"""
Endpoints user
"""

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.api import depends
from app.core import auth
from app.database import Database
from app.schemas import UserScheme
from app.schemas import UserSchemeAdd, UserTokenScheme

router = APIRouter()


@router.get("/", response_model=UserScheme)
async def get(current_user=Depends(depends.get_current_user)):
    """
    Получение информации о текущем пользователе.
    """
    return UserScheme(**current_user.__dict__)


@router.post("/", response_model=UserTokenScheme)
async def new(user: UserSchemeAdd, db: Database = Depends(depends.get_db)):
    """
    Регистрация нового пользователя.
    """
    user_exists = await db.user.get_by_username(user.username)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Такой пользователь уже зарегистрирован.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    hash_password = auth.get_password_hash(user.password)
    await db.user.new(user.username, hash_password)
    await db.session.commit()
    access_token = auth.create_access_token(user.username)
    return UserTokenScheme(access_token=access_token)


@router.post("/token", response_model=UserTokenScheme)
async def token(form_data: auth.OAuth2PasswordRequestForm = Depends(), db: Database = Depends(depends.get_db)):
    """
    Получение токена доступа для пользователя.
    """
    user = await db.user.get_by_username(form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth.create_access_token(user.username)
    return UserTokenScheme(access_token=access_token)
