"""
User API Module
"""

from fastapi import APIRouter

from . import retrieve

router = APIRouter(prefix='/users', tags=['users'])
router.include_router(retrieve.router)
