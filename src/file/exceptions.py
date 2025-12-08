from fastapi import HTTPException
from starlette import status

FileNotFoundError = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="File not found"
)