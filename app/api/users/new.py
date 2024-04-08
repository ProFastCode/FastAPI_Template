"""
User Endpoints Module
"""

from fastapi import APIRouter, Depends

from app import schemas, use_cases

router = APIRouter()


@router.post("/", response_model=schemas.users.GetUser)
async def new(
    data: schemas.users.NewUser,
    use_case: use_cases.users.NewUseCase = Depends(use_cases.users.NewUseCase),
):
    """
    Создать нового пользователя:

    - **id**: ID-пользователя
    - **email**: Email-Пользователя
    - **password**: Password-Пользователя
    """

    user = await use_case.execute(data)
    return user
