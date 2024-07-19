"""
Init App Module
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app import api
from app.core import exps
from app.core.settings import settings

app = FastAPI(
    title=settings.APP_TITLE,
    root_path=settings.APP_PATH,
    version=settings.APP_VERSION,
    contact={
        "name": "Fast Code",
        "url": "https://fast-code.pro/",
        "email": "fast.code.auth@gmail.com",
    },
)

app.include_router(api.api_router)


@app.exception_handler(exps.BaseException)
async def exception_handler(request, exc: exps.BaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )
