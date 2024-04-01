from fastapi import APIRouter, Depends, Request

from app import schemas
from app.api import depends

router = APIRouter()


@router.post("/auth/", response_model=schemas.TokenAuth)
async def new_auth_token(
    request: Request, token_auth: schemas.TokenAuth = Depends(depends.get_auth_token)
):
    return token_auth
