from fastapi import APIRouter

from . import token

router = APIRouter(prefix="/auth", tags=["auth"])
router.include_router(token.router)

__all__ = ["router"]
