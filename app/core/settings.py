from sqlalchemy import URL
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True
    )

    # App-related environment variables
    app_path: str = Field(alias="APP_PATH")
    app_title: str = Field(alias="APP_TITLE")
    app_secret: str = Field(alias="APP_SECRET")
    app_version: str = Field(alias="APP_VERSION")

    # Postgres-related environment variables
    postgres_db: str = Field(alias="POSTGRES_DB")
    postgres_host: str = Field(alias="POSTGRES_HOST")
    postgres_port: int = Field(alias="POSTGRES_PORT")
    postgres_user: str = Field(alias="POSTGRES_USER")
    postgres_password: str = Field(alias="POSTGRES_PASSWORD")
    postgres_drivername: str = Field(alias="POSTGRES_DRIVERNAME")

    @property
    def postgres_dsn(self) -> str:
        return URL.create(
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
            username=self.postgres_user,
            password=self.postgres_password,
            drivername=self.postgres_drivername,
        ).render_as_string(hide_password=False)


settings = Settings()
