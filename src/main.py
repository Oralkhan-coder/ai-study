from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.core.database import init_db
from src.core.config import init_middleware, init_routers
from src.core.openapi import add_jwt_openapi

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="My API",
        version="1.0.0",
        lifespan=lifespan,
    )

    init_middleware(app)
    init_routers(app)
    add_jwt_openapi(app)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", reload=True)
