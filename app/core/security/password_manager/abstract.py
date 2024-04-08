import abc
from abc import ABC


class AbstractPasswordManager(ABC):
    @classmethod
    @abc.abstractmethod
    def hash_password(cls, password: str) -> str: ...

    @classmethod
    @abc.abstractmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool: ...
