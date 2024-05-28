"""
App API Module
"""

from fastapi import APIRouter

from . import endpoints

api_router = APIRouter()
api_router.include_router(endpoints.router)
