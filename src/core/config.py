from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.auth.middleware import JWTAuthMiddleware
from src.auth.router import router as auth_router
from src.user.router import router as user_router

def init_middleware(app: FastAPI):
    origins = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(JWTAuthMiddleware)


def init_routers(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(user_router)
