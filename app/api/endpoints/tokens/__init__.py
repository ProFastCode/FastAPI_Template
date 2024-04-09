"""
Token API Module
"""

from fastapi import APIRouter

from . import auth, pair, refresh
from app.core.structures import Tags

router = APIRouter(prefix="/tokens", tags=[Tags.tokens])
router.include_router(auth.router)
router.include_router(pair.router)
router.include_router(refresh.router)
