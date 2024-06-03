from fastapi import APIRouter

from . import telegram

router = APIRouter(prefix='/oauth2')
router.include_router(telegram.router)
