"""
User API Module
"""

from fastapi import APIRouter

from . import get, new
from app.core.structures import Tags

router = APIRouter(prefix="/users", tags=[Tags.users])
router.include_router(new.router)
router.include_router(get.router)
