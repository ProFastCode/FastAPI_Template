from typing import Annotated, Union

from fastapi import Form


class OAuth2PasswordRequestForm:
    def __init__(
        self,
        *,
        grant_type: Annotated[Union[str, None], Form(pattern="password")] = None,
        username: Annotated[str, Form()] = None,
        password: Annotated[str, Form()],
        scope: Annotated[str, Form()] = "",
        client_id: Annotated[Union[str, None], Form()] = None,
        client_secret: Annotated[Union[str, None], Form()] = None,
    ):
        self.grant_type = grant_type
        self.username = username
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret
