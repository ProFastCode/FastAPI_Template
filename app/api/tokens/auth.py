from fastapi import APIRouter, Depends, HTTPException, status

from app import schemas
from app.api import depends
from app.api.tags import Tags
from app.core import security
from app.database import Database

router = APIRouter(dependencies=[Depends(depends.service)], tags=[Tags.services])


@router.get("/auth/")
async def get_token_auth(
        username: str,
        db: Database = Depends(depends.get_db),
) -> schemas.TokenAuth:
    if not (user := await db.user.get_by_username(username)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="A user not yet been registered"
        )
    token_auth = security.create_token_auth({"id": user.id})
    return token_auth
