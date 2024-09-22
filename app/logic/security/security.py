from app.core.settings import settings

from .jwt import JWT
from .pwd import PWD


class Security:
    def __init__(self):
        self.jwt = JWT(settings.app_secret)
        self.pwd = PWD()
