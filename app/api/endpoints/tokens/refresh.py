from fastapi import APIRouter, Depends

from app import schemas, use_cases

router = APIRouter()


@router.post("/refresh/", response_model=schemas.tokens.ShortToken)
async def refresh_short_token(
    data: schemas.tokens.LongToken,
    use_case: use_cases.tokens.RefreshUseCase = Depends(
        use_cases.tokens.RefreshUseCase
    ),
):
    """
    Обновить короткий токен:

    - **long_token**: Длинный токен
    """
    short_token = await use_case.execute(data)
    return short_token
