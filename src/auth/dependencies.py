from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.service import AuthService
from src.core.database import get_db
from src.shared.email_service import EmailService, get_email_service


async def get_auth_service(
    db: AsyncSession = Depends(get_db),
    email_service: EmailService = Depends(get_email_service)
):
    return AuthService(db, email_service)
