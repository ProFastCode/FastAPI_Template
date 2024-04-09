from fastapi import HTTPException, status


class InvalidToken(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: str = "Invalid token",
    ) -> None:
        self.status_code = status_code
        self.detail = detail


class TokenExpired(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: str = "Token expired",
    ) -> None:
        self.status_code = status_code
        self.detail = detail


class InvalidTokenType(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: str = "Invalid token type",
    ) -> None:
        self.status_code = status_code
        self.detail = detail
