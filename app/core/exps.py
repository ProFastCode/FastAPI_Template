"""
Exceptions
"""

from fastapi import HTTPException, status

# Users
USER_EXISTS = HTTPException(status.HTTP_409_CONFLICT, 'User is already taken.')
USER_NOT_FOUND = HTTPException(status.HTTP_404_NOT_FOUND, 'User not found.')
USER_IS_CORRECT = HTTPException(
    status.HTTP_401_UNAUTHORIZED, 'User is correct.'
)

# Tokens
TOKEN_INVALID = HTTPException(status.HTTP_401_UNAUTHORIZED, 'Invalid token.')
TOKEN_EXPIRED = HTTPException(status.HTTP_401_UNAUTHORIZED, 'Token expired.')
