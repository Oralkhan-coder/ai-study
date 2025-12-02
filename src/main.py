from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database import init_db
from src.user.router import router as user_router
from src.auth.router import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(user_router)
