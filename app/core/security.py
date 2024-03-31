from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext

from app import schemas
from app.core import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_token(action: str, payload: dict, minutes: int) -> str:
    data = dict(
        action=action, payload=payload, exp=datetime.now() + timedelta(minutes=minutes)
    )
    encoded_jwt = jwt.encode(data, settings.APP_AUTH_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    try:
        data = jwt.decode(token, settings.APP_AUTH_KEY, algorithms=[ALGORITHM])
        exp: float = data.get("exp")

        if datetime.fromtimestamp(exp) > datetime.now():
            return data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Failed to parse token"
        )


def create_token_auth(payload: dict) -> schemas.TokenAuth:
    token_auth = create_token("token_auth", payload, 15)
    return schemas.TokenAuth(token_auth=token_auth)


def create_token_long(payload: dict) -> schemas.TokenLong:
    token_long = create_token("token_long", payload, minutes=52560)
    return schemas.TokenLong(token_long=token_long)


def create_token_short(payload: dict) -> schemas.TokenShort:
    token_short = create_token("token_short", payload, minutes=120)
    return schemas.TokenShort(token_short=token_short)


def create_token_pair(payload: dict) -> schemas.TokenPair:
    token_long = create_token_long(payload)
    token_short = create_token_short(payload)
    return schemas.TokenPair(
        token_long=token_long.token_long, token_short=token_short.token_short
    )
