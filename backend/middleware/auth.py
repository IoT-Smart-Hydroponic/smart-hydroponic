from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from services.user_service import UserService
from utils.deps import get_session
from authlib.jose.errors import JoseError


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return await call_next(
                request
            )  # Allow unauthenticated access for certain routes if needed

        token = auth_header.split(" ")[1]
        async for session in get_session():
            user_service = UserService(session)
            try:
                claims = user_service.verify_token(token)
                request.state.user = claims.get("sub")
            except JoseError:
                request.state.user = None
                raise HTTPException(status_code=401, detail="Invalid or expired token")
            break

        return await call_next(request)
