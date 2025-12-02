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
async def login(data: schemas.LoginRequest, svc: AuthService = Depends(get_auth_service)):
    return await svc.authenticate(data.email, data.password)


@router.post("/sign-up", status_code=status.HTTP_201_CREATED)
async def sign_up(data: schemas.SignUpRequest, svc: AuthService = Depends(get_auth_service)):
    return await svc.register(data)


@router.get("/verify-email")
async def verify_email(token: str, request: Request, auth_service: AuthService = Depends(get_auth_service)):
    template = Jinja2Templates(directory="src/resources/templates/")

    user = await auth_service.verify_email(token)
    return template.TemplateResponse(
        "email_verified.html",
        {"request": request, "user": user}
    )
