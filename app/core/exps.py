"""
Exceptions
"""


class CustomException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


# Users
class UserExistsException(CustomException):
    def __init__(self):
        super().__init__('User is already taken.', status_code=409)


class UserNotFoundException(CustomException):
    def __init__(self):
        super().__init__('User not found.', status_code=404)


class UserIsCorrectException(CustomException):
    def __init__(self):
        super().__init__('User is correct.', status_code=401)


# Tokens
class TokenInvalidException(CustomException):
    def __init__(self):
        super().__init__('Invalid token.', status_code=401)


class TokenExpiredException(CustomException):
    def __init__(self):
        super().__init__('Token expired.', status_code=401)
