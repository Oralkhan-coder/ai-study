from fastapi import HTTPException
from sqlalchemy import select
from jinja2 import Template
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.auth import schemas, utils
from src.auth.schemas import TokenResponse
from src.shared.email_service import EmailService
from src.user.model import User

class AuthService:
    def __init__(self, db: AsyncSession, email_service=EmailService):
        self.db = db
        self.email_service = email_service

    async def authenticate(self, email: str, password: str) -> TokenResponse:
        user = await self.db.scalar(
            select(User).where(User.email == email)
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email"
            )

        if not utils.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect password"
            )

        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email not verified"
            )

        token = utils.create_access_token(data=schemas.TokenData(email=user.email).model_dump())

        return TokenResponse(access_token=token)

    async def register(self, data: schemas.SignUpRequest):
        user = await self.db.scalar(
            select(User).where(User.email == data.email)
        )
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        new_user = User(
            username=data.email,
            email=data.email,
            full_name=data.full_name,
            password=utils.hash_password(data.password),
            role="user"
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)

        token = utils.create_email_verification_token(new_user.email)
        verify_url = f"http://localhost:8000/auth/verify-email?token={token}"

        template_path = Path("src/resources/templates/email_verification.html")
        html = Template(template_path.read_text()).render(verify_url=verify_url)

        await self.email_service.send_email(
            to_email=new_user.email,
            subject="Email Verification",
            html_content=html
        )

        return "Verification email sent."


    async def verify_email(self, token: str) -> User:
        try:
            email = utils.verify_email_verification_token(token)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid or expired token")

        user = await self.db.scalar(select(User).where(User.email == email))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.is_verified = True
        await self.db.commit()
        return user