from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.file.service import FileService


async def get_file_service(
        db: AsyncSession = Depends(get_db),
):
    return FileService(db)