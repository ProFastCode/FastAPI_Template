"""
Репозитории базы данных.
"""

from .abstract import Repository
from .user import UserRepo

__all__ = (
    'UserRepo',
    'Repository',
)
