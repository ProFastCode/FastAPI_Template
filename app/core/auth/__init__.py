"""
Модуль авторизации
"""

from .oauth2 import authorization, OAuth2PasswordRequestForm
from .security import verify_password, get_password_hash, create_access_token

__all__ = (
    "authorization",
    "OAuth2PasswordRequestForm",
    "verify_password",
    "get_password_hash",
    "create_access_token",
)
