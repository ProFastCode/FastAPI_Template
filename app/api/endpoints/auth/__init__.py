from fastapi import APIRouter

from . import oauth2, tokens

router = APIRouter(prefix='/auth', tags=['auth'])
router.include_router(tokens.router)
router.include_router(oauth2.router)

__all__ = ['router']
