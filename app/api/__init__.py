"""
App API Module
"""

from fastapi import APIRouter

from . import users, tokens, staff

api_router = APIRouter()
api_router.include_router(staff.router)
api_router.include_router(users.router)
api_router.include_router(tokens.router)
