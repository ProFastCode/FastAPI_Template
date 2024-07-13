"""
Dependencies
"""

from typing import Annotated

from app.core import deps

Database = Annotated[deps.Database, deps.Depends(deps.get_db)]

Security = Annotated[deps.Security, deps.Depends(deps.get_security)]

Logic = Annotated[deps.Logic, deps.Depends(deps.get_logic)]

CurrentUser = Annotated[deps.User, deps.Depends(deps.get_current_user)]
