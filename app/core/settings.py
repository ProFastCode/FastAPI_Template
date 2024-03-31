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
    APP_AUTH_KEY: str = "app_auth_key"
    APP_API_PREFIX: str = "/api"

    # DATABASE
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DATABASE: str = "postgres"

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
