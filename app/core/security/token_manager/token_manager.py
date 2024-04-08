from datetime import datetime, timedelta

from jose import jwt, JWTError

from app.core import settings
from .abstract import AbstractTokenManager
from .structures import TokenType
from .exceptions import TokenExpired, InvalidTokenType, InvalidToken

ALGORITHM = "HS256"


class JWTTokenManager(AbstractTokenManager):
    def _decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, settings.APP_SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise InvalidToken
        return payload

    def _create_token(self, payload: dict) -> str:
        token = jwt.encode(payload, settings.APP_SECRET_KEY, algorithm=ALGORITHM)
        return token

    @classmethod
    def expand_payload(cls, token_type: TokenType, payload: dict, minutes: int) -> dict:
        new_payload = dict(
            token_type=token_type.value,
            payload=payload,
            exp=datetime.now() + timedelta(minutes=minutes),
        )
        return new_payload

    @classmethod
    def validate_payload(cls, token_type: TokenType, payload: dict) -> None:
        exp: float = payload.get("exp")
        if not (datetime.fromtimestamp(exp) > datetime.now()):
            raise TokenExpired
        if payload.get("token_type") != token_type.value:
            raise InvalidTokenType


class TokenManager(JWTTokenManager):
    def decode_auth_token(self, token: str) -> dict:
        payload = self._decode_token(token)
        self.validate_payload(TokenType.AUTH, payload)
        return payload.get("payload")

    def create_auth_token(self, payload: dict) -> str:
        payload = self.expand_payload(TokenType.AUTH, payload, 15)
        token = self._create_token(payload)
        return token

    def decode_long_token(self, token: str) -> dict:
        payload = self._decode_token(token)
        self.validate_payload(TokenType.LONG, payload)
        return payload.get("payload")

    def create_long_token(self, payload: dict) -> str:
        payload = self.expand_payload(TokenType.LONG, payload, 52560)
        token = self._create_token(payload)
        return token

    def decode_short_token(self, token: str) -> dict:
        payload = self._decode_token(token)
        self.validate_payload(TokenType.SHORT, payload)
        return payload.get("payload")

    def create_short_token(self, payload: dict) -> str:
        payload = self.expand_payload(TokenType.SHORT, payload, 120)
        token = self._create_token(payload)
        return token
