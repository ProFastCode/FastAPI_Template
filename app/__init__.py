import os

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app import api
from app.core import exps
from app.core.settings import settings

os.environ["TZ"] = "UTC"

app = FastAPI(
    title=settings.app_title,
    root_path=settings.app_path,
    version=settings.app_version,
    contact={
        "name": "Fast Code",
        "url": "https://fast-code.pro/",
        "email": "fast.code.auth@gmail.com",
    },
)

app.include_router(api.api_router)


@app.exception_handler(exps.CustomException)
async def exception_handler(request, exc: exps.CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )
