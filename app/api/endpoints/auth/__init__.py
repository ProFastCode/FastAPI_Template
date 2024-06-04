from fastapi import APIRouter

from . import email, tokens

router = APIRouter(prefix='/auth', tags=['auth'])
router.include_router(tokens.router)
router.include_router(email.router)

__all__ = ['router']
