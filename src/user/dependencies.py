from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.user.service import UserService

async def get_user_service(db: AsyncSession = Depends(get_db)):
    return UserService(db)
