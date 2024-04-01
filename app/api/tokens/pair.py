from fastapi import APIRouter, Depends

from app import schemas
from app.api import depends

router = APIRouter()


@router.get("/pair/", response_model=schemas.TokenPair)
async def new_pair_tokens(
    pair_tokens: schemas.TokenPair = Depends(depends.get_pair_tokens),
):
    return pair_tokens
