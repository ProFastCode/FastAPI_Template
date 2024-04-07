class InvalidToken(Exception):
    def __init__(self, msg: str = "Invalid token") -> None:
        self.msg = msg


class TokenExpired(Exception):
    def __init__(self, msg: str = "Token expired") -> None:
        self.msg = msg


class InvalidTokenType(Exception):
    def __init__(self, msg: str = "Invalid token type") -> None:
        self.msg = msg
