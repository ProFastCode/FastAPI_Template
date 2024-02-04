"""
Модуль где подключаются endpoints user
"""

from fastapi import APIRouter

from . import endpoints

router = APIRouter(prefix="/users", tags=["users"])
router.include_router(endpoints.router)
