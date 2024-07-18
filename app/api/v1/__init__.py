"""
Endpoints API Module
"""

from pathlib import Path
from fastapi import APIRouter

from . import users

FOLDER_NAME = f"{Path(__file__).parent.name}"

router = APIRouter(prefix=f"/{FOLDER_NAME}", tags=[FOLDER_NAME])
router.include_router(users.router)

__all__ = ["router"]
