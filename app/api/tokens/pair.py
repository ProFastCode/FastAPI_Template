from fastapi import APIRouter, Depends, HTTPException, status, Response, Request

from app import schemas
from app.api import depends
from app.core import security
from app.database import Database

router = APIRouter()


@router.get("/pair/")
async def get_token_pair(
    request: Request,
    response: Response,
    token: str,
    db: Database = Depends(depends.get_db),
) -> schemas.TokenPair:
    data = security.decode_token(token)
    payload = data.get("payload")

    if data.get("action") not in ["token_auth", "token_long"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This must be an authorization token or a long token",
        )

    if user := await db.user.get(payload.get("id")):
        token_pair = security.create_token_pair(payload)
        if data.get("action") != "token_long":
            response.set_cookie(key="_token_long", value=token_pair.token_long)
            response.set_cookie(key="_token_short", value=token_pair.token_short)
        else:
            token_pair.token_long = token
            response.set_cookie(key="_token_short", value=token_pair.token_short)

        if data.get("action") == "token_auth":
            ip = request.client.host
            user_agent = request.headers.get("User-Agent")
            await db.user_activity.new(
                user.id, "new_auth", "Новая авторизация", user_agent, ip
            )
            await db.session.commit()

        return token_pair
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
