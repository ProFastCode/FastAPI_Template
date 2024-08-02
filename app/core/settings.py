"""
Settings
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )

    # APP
    APP_PATH: str = "/api"
    APP_TITLE: str = "FastAPI Template"
    APP_VERSION: str = "beta"
    APP_SECRET_KEY: str = "abc"

    # DATABASE
    DB: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_DRIVERNAME: str = "postgresql+asyncpg"

    @property
    def db_dsn(self) -> str:
        return URL.create(
            drivername=self.DB_DRIVERNAME,
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB,
        ).render_as_string(hide_password=False)


settings = Settings()
