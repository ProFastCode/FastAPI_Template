"""
Token API Module
"""

from fastapi import APIRouter

from . import auth, pair
from ..tags import Tags

router = APIRouter(prefix="/tokens", tags=[Tags.tokens])
router.include_router(auth.router)
router.include_router(pair.router)
