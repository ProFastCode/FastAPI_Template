"""
Endpoints API Module
"""

from pathlib import Path

from fastapi import APIRouter

from . import auth, user

FOLDER_NAME = f"{Path(__file__).parent.name}"

router = APIRouter(prefix=f"/{FOLDER_NAME}", tags=[FOLDER_NAME])
router.include_router(auth.router)
router.include_router(user.router)

__all__ = ["router"]
