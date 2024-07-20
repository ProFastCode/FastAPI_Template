"""
Exceptions
"""


class BaseException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


# Users
class UserExistsException(BaseException):
    def __init__(self):
        super().__init__('User is already taken.', status_code=409)


class UserNotFoundException(BaseException):
    def __init__(self):
        super().__init__('User not found.', status_code=404)


class UserIsCorrectException(BaseException):
    def __init__(self):
        super().__init__('User is correct.', status_code=401)


# Tokens
class TokenInvalidException(BaseException):
    def __init__(self):
        super().__init__('Invalid token.', status_code=401)


class TokenExpiredException(BaseException):
    def __init__(self):
        super().__init__('Token expired.', status_code=401)
