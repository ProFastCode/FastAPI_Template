"""
User API Module
"""

from fastapi import APIRouter

from . import auth, create, retrieve

router = APIRouter(prefix='/users', tags=['users'])
router.include_router(auth.router)
router.include_router(create.router)
router.include_router(retrieve.router)

__all__ = ['router']
