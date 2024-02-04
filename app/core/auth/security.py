from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.core import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """
    Проверяет соответствие обычного пароля и хэшированного пароля.

    Args:
        plain_password (str): Обычный пароль в виде строки.
        hashed_password (str): Хэшированный пароль в виде строки.

    Returns:
        bool: True, если пароли совпадают, иначе False.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Получает хэш пароля.

    Args:
        password (str): Пароль в виде строки.

    Returns:
        str: Хэшированный пароль в виде строки.
    """
    return pwd_context.hash(password)


def create_access_token(username: str):
    """
    Создает токен доступа на основе имени пользователя.

    Args:
        username (str): Имя пользователя в виде строки.

    Returns:
        str: Закодированный JWT токен в виде строки.
    """
    data = dict(
        username=username,
        exp=datetime.utcnow() + timedelta(minutes=120)
    )
    encoded_jwt = jwt.encode(data, settings.APP_AUTH_SECRET, algorithm="HS256")
    return encoded_jwt
