from fastapi import APIRouter, Depends

from app import schemas, use_cases

router = APIRouter()


@router.post("/auth/", response_model=schemas.tokens.AuthToken)
async def new_auth_token(
    data: schemas.users.AuthUser,
    use_case: use_cases.tokens.AuthUseCase = Depends(use_cases.tokens.AuthUseCase),
):
    """
    Получить токен аутентификации:

    - **email**: Email-пользователя
    - **password**: Password-Пользователя
    """
    auth_token = await use_case.execute(data)
    return auth_token
