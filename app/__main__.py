import uvicorn
from fastapi import FastAPI

from app import api
from app.core.settings import settings

app = FastAPI(openapi_url=f"{settings.APP_API_PREFIX}/openapi.json")

app.include_router(api.api_router, prefix=settings.APP_API_PREFIX)


# TEST ACTIONS

list_one = [
    "das"
]

list_two = ["asda"]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
