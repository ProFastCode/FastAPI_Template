"""
Stats Endpoints Module
"""

from fastapi import APIRouter

from . import users

router = APIRouter(prefix="/stats")
router.include_router(users.router)
