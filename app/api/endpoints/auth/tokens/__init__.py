"""
Token API Module
"""

from fastapi import APIRouter

from . import pair, refresh

router = APIRouter(prefix='/tokens')
router.include_router(pair.router)
router.include_router(refresh.router)

__all__ = ['router']
