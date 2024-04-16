"""
User API Module
"""

from fastapi import APIRouter

from app.core.structures import Tags
from . import create, read

router = APIRouter(prefix="/users", tags=[Tags.users])
router.include_router(create.router)
router.include_router(read.router)
