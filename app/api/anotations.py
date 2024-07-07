"""
Anotations
"""

from fastapi import Depends
from typing_extensions import Annotated

from app.core import deps

Database = Annotated[deps.db.Database, Depends(deps.get_db)]

Security = Annotated[deps.Security, Depends(deps.get_security)]

CurrentUser = Annotated[deps.User, Depends(deps.get_current_user)]
