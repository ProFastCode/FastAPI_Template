from fastapi import APIRouter, Depends, HTTPException, status, Request, Header

from app import schemas
from app.api import depends
from app.core import security
from app.database import Database

router = APIRouter()


@router.get("/pair/", response_model=schemas.TokenPair)
async def new_pair_tokens(
    request: Request,
    auth_token: str,
    user_agent: str = Header(),
    db: Database = Depends(depends.get_db),
):
    token_dict = security.decode_token(auth_token)
    payload = token_dict.get("payload")

    if token_dict.get("action") != "token_auth":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This must be an authorization token",
        )

    if not (user := await db.user.get(payload.get("id"))):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    token_pair = security.create_token_pair(payload)
    await db.user_activity.new(
        user_id=user.id,
        action="new_pair_tokens",
        comment="Новая пара токенов",
        user_agent=user_agent,
        ip=request.client.host,
    )
    await db.session.commit()
    return token_pair
