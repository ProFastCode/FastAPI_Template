"""
App API Module
"""

from fastapi import APIRouter

from .endpoints import users, tokens, admins

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(tokens.router)
api_router.include_router(admins.router)
