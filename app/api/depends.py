"""
Dependency Module
"""

from fastapi import Depends, HTTPException, status, Request

from app.core import security
from app.database import Database, new_session, models


async def get_db() -> Database:
    session = await new_session()
    try:
        yield Database(session)
    finally:
        await session.close()


async def get_auth_token(
        request: Request, email: str, password: str,
        db: Database = Depends(get_db)
):
    user_agent = request.headers.get("User-Agent")
    if not (user := await db.user.get_by_email(email, password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A user not yet been registered",
        )
    token_auth = security.create_token_auth({"id": user.id})
    await db.user_activity.new(
        user_id=user.id,
        action="new_auth_token",
        comment="Новый токен аутентификации",
        user_agent=user_agent,
        ip=request.client.host,
    )
    await db.session.commit()
    return token_auth


async def get_pair_tokens(
        request: Request, auth_token: str, db: Database = Depends(get_db)
):
    user_agent = request.headers.get("User-Agent")
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


async def get_current_user(
        token_short: str,
        db: Database = Depends(get_db),
) -> models.User:
    if not token_short:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Short token not transferred",
        )

    if not (token_short_data := security.decode_token(token_short)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your short token have expired",
        )

    if token_short_data.get("action") != "token_short":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You did not transfer a short token",
        )

    if not (user := await db.user.get(token_short_data.get("payload").get("id"))):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return user
