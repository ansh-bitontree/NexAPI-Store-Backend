from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
from app.core.config import settings


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        public_paths = [
            "/", "/favicon.ico",
            "/login", "/signup", "/forgot-password", "/reset-password"
        ]

        if request.method == "OPTIONS" or any(
            request.url.path.startswith(path) for path in public_paths
        ):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, 
                                detail="Authorization header missing")

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, 
                                 algorithms=[settings.ALGORITHM])
            request.state.user = payload  
        except JWTError:
            raise HTTPException(status_code=401, 
                                detail="Invalid or expired token")

        return await call_next(request)
