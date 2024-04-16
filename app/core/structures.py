"""
Structures
"""

from enum import IntEnum, Enum


class TokenType(IntEnum):
    AUTH = 0
    LONG = 1
    SHORT = 2


class Tags(Enum):
    users = "users"
    tokens = "tokens"
    staff = "staff"
