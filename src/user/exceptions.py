from fastapi import HTTPException, status

UserNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found"
)

UserAlreadyExists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User already exists"
)
