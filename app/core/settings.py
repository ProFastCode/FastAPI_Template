"""
App Settings Module
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )

    # APP
    APP_AUTH_KEY: str
    APP_API_PREFIX: str

    # DATABASE
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DATABASE: str

    @property
    def pg_url(self) -> URL:
        url = URL.create(
            "postgresql+asyncpg",
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_HOST,
            self.POSTGRES_PORT,
            self.POSTGRES_DATABASE,
        )
        return url


settings = Settings()
