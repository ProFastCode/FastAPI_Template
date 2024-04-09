from enum import IntEnum


class Role(IntEnum):
    USER = 0
    ADMIN = 1


class TokenType(IntEnum):
    AUTH = 0
    LONG = 1
    SHORT = 2
