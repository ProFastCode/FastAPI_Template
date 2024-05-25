"""
Endpoints API Module
"""

from fastapi import APIRouter

from . import tokens, users

router = APIRouter()
router.include_router(users.router)
router.include_router(tokens.router)
