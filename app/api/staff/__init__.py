"""
Staff API Module
"""

from fastapi import APIRouter
from fastapi.params import Depends

from . import stats
from .. import depends
from ..tags import Tags

router = APIRouter(
    prefix="/staff", tags=[Tags.staff], dependencies=[Depends(depends.only_staff)]
)
router.include_router(stats.router)
