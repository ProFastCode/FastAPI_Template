from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(username: str):
    data = dict(
        username=username,
        exp=datetime.utcnow() + timedelta(minutes=120)
    )
    encoded_jwt = jwt.encode(data, settings.APP_AUTH_SECRET, algorithm="HS256")
    return encoded_jwt
