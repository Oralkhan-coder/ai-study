from fastapi import HTTPException
import httpx
from jose import jwt
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

    async def google_auth(self, token: str):
        payload = jwt.get_unverified_claims(token)
        utils.check_google_aud(payload.get('aud'))

        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token}")
            info = response.json()
            utils.check_google_aud(info.get('aud'))

        user = await self.db.scalar(
            select(User).where(User.email == payload.get("email"))
        )
        if not user:
            user = User(
                username=payload.get("email"),
                email=payload.get("email"),
                full_name=payload.get("name"),
                role="user",
                is_verified=True
            )
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)

        return TokenResponse(access_token=utils.create_access_token(data=
                                schemas.TokenData(email=user.email).model_dump()))

    async def github_auth(self, code: str):
        if not code:
            return utils.get_github_auth_url()

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://github.com/login/oauth/access_token",
                headers={"Accept": "application/json"},
                data=utils.get_github_client_data(code),
            )
            token_json = response.json()

        if "access_token" not in token_json:
            raise HTTPException(status_code=400, detail="Token exchange failed")

        token = token_json["access_token"]

        async with httpx.AsyncClient() as client:
            user_response = await client.get(
                "https://api.github.com/user",
                headers={"Authorization": f"Bearer {token}"}
            )
            info = user_response.json()

        username = info.get("login")
        full_name = info.get("name") or username
        email = info.get("email")
        if not email:
            email = f"{username}@github.local"

        user = await self.db.scalar(
            select(User).where(User.email == email)
        )

        if not user:
            user = User(
                username=username,
                email=email,
                full_name=full_name,
                role="user",
                is_verified=True
            )
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)

        return TokenResponse(
            access_token=utils.create_access_token(
                data=schemas.TokenData(email=user.email).model_dump()
            )
        )
