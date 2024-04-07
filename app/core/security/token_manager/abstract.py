import abc
from abc import ABC


class AbstractTokenManager(ABC):
    @abc.abstractmethod
    def _decode_token(self, token) -> dict: ...

    @abc.abstractmethod
    def _create_token(self, payload) -> str: ...
