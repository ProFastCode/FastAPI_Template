"""
Settings
"""

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', case_sensitive=True
    )

    # APP
    APP_PATH: str
    APP_TITLE: str
    APP_VERSION: str
    APP_SECRET_KEY: str

    @property
    def app_description(self):
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()

    # DATABASE
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    @property
    def pg_dsn(self) -> PostgresDsn:
        dsn = PostgresDsn.build(
            scheme='postgresql+asyncpg',
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )
        return dsn


settings = Settings()
