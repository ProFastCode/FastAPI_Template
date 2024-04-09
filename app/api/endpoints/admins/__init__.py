"""
Admins API Module
"""

from fastapi import APIRouter
from fastapi.params import Depends

from . import stats
from app.api import depends
from app.core.structures import Tags

router = APIRouter(
    prefix="/admins",
    tags=[Tags.admins],
    dependencies=[Depends(depends.admins_access)],
)
router.include_router(stats.router)
