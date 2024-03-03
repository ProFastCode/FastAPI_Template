"""
Init App Module
"""

from fastapi import FastAPI

from app import api
from app.core import settings

app = FastAPI(openapi_url=f"{settings.APP_API_PREFIX}/openapi.json")

app.include_router(api.api_router, prefix=settings.APP_API_PREFIX)
