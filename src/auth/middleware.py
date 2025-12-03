from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request, HTTPException
from src.auth import utils

PUBLIC_PATHS = {
    "/docs",
    "/openapi.json",
}

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if path.startswith("/auth/") or path in PUBLIC_PATHS:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse(
                {"detail": "Authorization header is missing"}, status_code=401
            )

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return JSONResponse(
                {"detail": "Invalid authorization header"}, status_code=401
            )

        token = parts[1]

        try:
            token_data = utils.verify_access_token(token)
            request.state.user = token_data
        except HTTPException as e:
            return JSONResponse({"detail": e.detail}, status_code=e.status_code)

        return await call_next(request)
