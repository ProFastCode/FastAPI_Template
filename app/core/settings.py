"""
Settings
"""

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )

    # APP
    APP_API_PREFIX: str
    APP_SECRET_KEY: str

    # DATABASE
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DATABASE: str

    @property
    def pg_dns(self) -> PostgresDsn:
        dns = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DATABASE,
        )
        return dns


settings = Settings()
