from enum import IntEnum, Enum


class Role(IntEnum):
    USER = 0
    ADMIN = 1


class TokenType(IntEnum):
    AUTH = 0
    LONG = 1
    SHORT = 2


class Tags(Enum):
    users = "users"
    tokens = "tokens"
    admins = "admins"
