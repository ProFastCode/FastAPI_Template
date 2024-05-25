import hashlib
import hmac

from app.core import settings


class TelegramAuth:
    def __init__(
        self,
        token: str = settings.TELEGRAM_BOT_TOKEN,
        username: str = settings.TELEGRAM_BOT_USERNAME,
    ):
        self.token = token
        self.username = username

    @property
    def hash(self) -> bytes:
        return hashlib.sha256(self.token.encode()).digest()

    def generate_hash(self, user: dict) -> str:
        user.pop('hash')
        string = '\n'.join(f'{x}={y}' for x, y in sorted(user.items()))
        computed_hash = hmac.new(
            self.hash,
            string.encode(),
            hashlib.sha256,
        ).hexdigest()
        return computed_hash

    @classmethod
    def is_correct(cls, computed_hash: str, user_hash: str) -> bool:
        return hmac.compare_digest(computed_hash, user_hash)
