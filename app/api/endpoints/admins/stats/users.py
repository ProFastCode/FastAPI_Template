"""
Stats Users Endpoints Module
"""

from fastapi import APIRouter, Depends

from app import schemas, use_cases

router = APIRouter()


@router.get("/users_count", response_model=schemas.staff.stats.UsersCount)
async def users_count(
    use_case: use_cases.staff.stats.UsersUseCase = Depends(
        use_cases.staff.stats.UsersUseCase
    ),
):
    """
    Получить информацию о количестве пользователей:
    """

    users = await use_case.execute()
    return users
