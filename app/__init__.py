"""
Init App Module
"""

from fastapi import FastAPI

from app import api
from app.core import settings

app = FastAPI(
    title=settings.APP_TITLE,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url=f'{settings.APP_API_PREFIX}/docs',
    openapi_url=f'{settings.APP_API_PREFIX}/openapi.json',
    swagger_ui_oauth2_redirect_url=f'{settings.APP_API_PREFIX}/docs/oauth2-redirect',
)

app.include_router(api.api_router, prefix=settings.APP_API_PREFIX)
