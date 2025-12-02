from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.database import init_db
from src.user.router import router as user_router
from src.auth.router import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",  # frontend URL
    "http://localhost:3000",  # add more if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # allowed frontend origins
    allow_credentials=True,
    allow_methods=["*"],         # allow all HTTP methods
    allow_headers=["*"],         # allow all headers
)
app.include_router(auth_router)
app.include_router(user_router)
