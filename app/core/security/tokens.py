from datetime import datetime, timedelta
from enum import Enum

from fastapi import HTTPException, status
from jose import jwt, JWTError

from app import schemas
from app.core import settings

ALGORITHM = "HS256"


class TokenType(Enum):
    AUTH = (0, "This must be an authorization token")
    LONG = (1, "This must be an long token")
    SHORT = (2, "You did not transfer a short token")


def create_token(token_type: TokenType, payload: dict, minutes: int) -> str:
    data = dict(
        token_type=token_type.value[0],
        payload=payload,
        exp=datetime.now() + timedelta(minutes=minutes),
    )
    encoded_jwt = jwt.encode(data, settings.APP_AUTH_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token_type: TokenType, token: str) -> dict:
    try:
        data = jwt.decode(token, settings.APP_AUTH_KEY, algorithms=[ALGORITHM])
        exp: float = data.get("exp")
        if not (datetime.fromtimestamp(exp) > datetime.now()):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Your short token have expired",
            )
        if data.get("token_type") != token_type.value[0]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=token_type.value[1],
            )
        return data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Failed to parse token"
        )


def create_auth_token(payload: dict) -> schemas.tokens.AuthToken:
    auth_token = create_token(TokenType.AUTH, payload, 15)
    return schemas.tokens.AuthToken(auth_token=auth_token)


def decode_auth_token(token: str) -> dict:
    token_dict = decode_token(TokenType.AUTH, token)
    payload = token_dict.get("payload")
    return payload


def create_long_token(payload: dict) -> schemas.tokens.LongToken:
    long_token = create_token(TokenType.LONG, payload, minutes=52560)
    return schemas.tokens.LongToken(long_token=long_token)


def decode_long_token(token: str) -> dict:
    token_dict = decode_token(TokenType.LONG, token)
    payload = token_dict.get("payload")
    return payload


def create_short_token(payload: dict) -> schemas.tokens.ShortToken:
    short_token = create_token(TokenType.SHORT, payload, minutes=120)
    return schemas.tokens.ShortToken(short_token=short_token)


def decode_short_token(token: str) -> dict:
    token_dict = decode_token(TokenType.SHORT, token)
    payload = token_dict.get("payload")
    return payload


def create_token_pair(payload: dict) -> schemas.tokens.PairTokens:
    long_token = create_long_token(payload)
    short_token = create_short_token(payload)
    return schemas.tokens.PairTokens(
        long_token=long_token.long_token, short_token=short_token.short_token
    )
