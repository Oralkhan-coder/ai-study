from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from starlette import status

from src.auth.dependencies import get_auth_service
from src.auth.schemas import TokenResponse
from src.auth import schemas
from src.auth.service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login", response_model=TokenResponse)
async def login(data: schemas.LoginRequest, service: AuthService = Depends(get_auth_service)):
    return await service.authenticate(data.email, data.password)


@router.post("/sign-up", status_code=status.HTTP_201_CREATED)
async def sign_up(data: schemas.SignUpRequest, service: AuthService = Depends(get_auth_service)):
    return await service.register(data)


@router.get("/verify-email")
async def verify_email(token: str, request: Request, service: AuthService = Depends(get_auth_service)):
    template = Jinja2Templates(directory="src/resources/templates/")

    user = await service.verify_email(token)
    return template.TemplateResponse(
        "email_verified.html",
        {"request": request, "user": user}
    )

@router.get("/google", response_model=TokenResponse)
async def google_auth(request: schemas.GoogleTokenRequest, service: AuthService = Depends(get_auth_service)):
    return await service.google_auth(request.id_token)

@router.get("/github")
async def login_with_github(code: str = None, service: AuthService = Depends(get_auth_service)):
    return await service.github_auth(code)