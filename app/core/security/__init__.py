from app.core.settings import settings

from .jwt import JWT


class Security:
    def __init__(self):
        self.jwt = JWT(settings.APP_SECRET_KEY)


__all__ = ["Security"]
