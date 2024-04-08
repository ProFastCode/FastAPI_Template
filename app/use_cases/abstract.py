from fastapi import Request, HTTPException, Depends

from app.api import depends
from app.database import Database


class AbstractUseCase:
    def __init__(
        self, request: Request, db: Database = Depends(depends.get_db)
    ) -> None:
        self.db = db
        self.request = request

    @property
    def host(self):
        return self.request.client.host

    @property
    def user_agent(self):
        return self.request.headers.get("User-Agent")

    def exp(self, status_code: int, detail: str) -> None:
        raise HTTPException(status_code=status_code, detail=detail)
