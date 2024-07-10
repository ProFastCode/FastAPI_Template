"""
Dependencies
"""

from fastapi import Depends
from typing_extensions import Annotated

from app.core import deps

Database = Annotated[deps.Database, Depends(deps.get_db)]

Security = Annotated[deps.Security, Depends(deps.get_security)]

Logic = Annotated[deps.Logic, Depends(deps.get_logic)]

CurrentUser = Annotated[deps.User, Depends(deps.get_current_user)]
