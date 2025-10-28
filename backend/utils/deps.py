from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import Session
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from services.user_service import UserService

bearer_scheme = HTTPBearer()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a SQLAlchemy async session (expire_on_commit=False)"""
    async with Session() as session:
        yield session

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), session: AsyncSession = Depends(get_session)):
    service = UserService(session)
    try:
        token = credentials.credentials
        payload = service.verify_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token") from e
    return {
        "sub": payload.get("sub"),
        "payload": dict(payload)
    }