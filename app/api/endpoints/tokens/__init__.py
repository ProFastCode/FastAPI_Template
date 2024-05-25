"""
Token API Module
"""

from fastapi import APIRouter

from . import auth, pair, refresh

router = APIRouter(prefix='/tokens', tags=['tokens'])
router.include_router(auth.router)
router.include_router(pair.router)
router.include_router(refresh.router)
