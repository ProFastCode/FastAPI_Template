from fastapi import APIRouter

from app.api import anotations
from app.core import deps, exps
from app.models.user import User, UserCreate, UserRead

router = APIRouter(prefix="/create")


@router.post("/", response_model=UserRead)
async def registration(
    data: UserCreate,
    db: anotations.Database,
):
    """
    Create user
    """
    if await db.user.retrieve_by_email(data.email):
        raise exps.USER_EXISTS

    password_hash = deps.pwd_context.hash(data.password)
    model = User(email=data.email, password=password_hash)
    user = await db.user.create(model)
    return user
