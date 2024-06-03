import pathlib

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing_extensions import Annotated

from app import models
from app.api import deps
from app.core import exps, settings
from app.core.db import Database
from app.core.security import JWTManager
from .oauth2 import OAuth2

router = APIRouter(prefix='/telegram')
templates = Jinja2Templates(
    directory=str(pathlib.Path(__file__).parent.resolve())
)
oauth2 = OAuth2(settings.TELEGRAM_BOT_TOKEN, settings.TELEGRAM_BOT_USERNAME)


@router.get('/login/')
async def login(request: Request):
    """
    Login page telegram
    """
    callback_path = request.url.path.replace('login', 'callback')
    return templates.TemplateResponse(
        request=request,
        name='login.html',
        context={
            'username': settings.TELEGRAM_BOT_USERNAME,
            'callback': callback_path,
        },
    )


@router.get('/callback/')
async def callback(
        request: Request,
        db: Annotated[Database, Depends(deps.get_db)],
        jwt_manager: Annotated[JWTManager, Depends(deps.get_jwt_manager)],
):
    """
    Endpoint callback telegram
    """
    data = dict(**{str(k): str(v) for k, v in request.query_params.items()})
    computed_hash = oauth2.generate_hash(data)
    if not oauth2.is_correct(computed_hash, data.get('hash')):
        raise exps.USER_IS_CORRECT

    if not (user := await db.user.retrieve_by_telegram_id(int(data['id']))):
        user = models.User(telegram_id=int(data['id']), full_name='', photo_url='')
        await db.user.create(user)

    user.photo_url = data['photo_url']
    user.full_name = f"{data['first_name']} {data['last_name']}"
    await db.session.commit()

    token = jwt_manager.encode_token({'id': user.id, 'type': 'auth'}, 15)
    return RedirectResponse(url=f'/api/auth/tokens/pair/?token={token}')
