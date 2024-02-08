from typing import Annotated, Union

from fastapi import Form, HTTPException, status
from jose import jwt, JWTError

from app.core import settings
from app.database import Database


class OAuth2PasswordRequestForm:
    def __init__(
            self,
            *,
            grant_type: Annotated[Union[str, None], Form(pattern="password")] = None,
            username: Annotated[str, Form()],
            password: Annotated[str, Form()],
            scope: Annotated[str, Form()] = "",
            client_id: Annotated[Union[str, None], Form()] = None,
            client_secret: Annotated[Union[str, None], Form()] = None,
    ):
        """
        Представляет форму запроса пароля OAuth 2.0.

        Args:
            grant_type (str): Тип предоставления (например, "password").
            username (str): Имя пользователя.
            password (str): Пароль пользователя.
            scope (str): Область запроса.
            client_id (str): Идентификатор клиента.
            client_secret (str): Секрет клиента.
        """
        self.grant_type = grant_type
        self.username = username
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret


async def authorization(token: str, db: Database):
    """
    Авторизует пользователя по токену.

    Args:
        token (str): Токен доступа пользователя.
        db (Database): Объект базы данных.

    Raises:
        HTTPException: Если не удается проверить учетные данные.

    Returns:
        dict: Информация о пользователе.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.APP_AUTH_SECRET, algorithms=["HS256"])
        username: str = payload.get("username")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await db.user.get_by_username(username)
    if not user:
        raise credentials_exception
    return user
