from fastapi import HTTPException, status

USER_EXISTS = HTTPException(status.HTTP_409_CONFLICT, "User is already taken.")
USER_NOT_FOUND = HTTPException(status.HTTP_404_NOT_FOUND, "User not found.")
USER_NOT_REGISTERED = HTTPException(
    status.HTTP_401_UNAUTHORIZED, "A user not yet been registered"
)
USER_INCORRECT_PASSWORD = HTTPException(
    status.HTTP_401_UNAUTHORIZED, "Incorrect password"
)
