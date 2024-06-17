from fastapi import APIRouter

from . import email

router = APIRouter(prefix='/auth', tags=['auth'])
router.include_router(email.router)

__all__ = ['router']
