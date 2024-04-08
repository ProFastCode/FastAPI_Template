from fastapi import APIRouter, Depends

from app import schemas, use_cases

router = APIRouter()


@router.post("/pair/", response_model=schemas.tokens.PairTokens)
async def new_pair_tokens(
    data: schemas.tokens.AuthToken,
    use_case: use_cases.tokens.PairUseCase = Depends(use_cases.tokens.PairUseCase),
):
    """
    Получить парные токены:

    - **auth_token**: Токен аутентификации
    """
    pair_tokens = await use_case.execute(data)
    return pair_tokens
