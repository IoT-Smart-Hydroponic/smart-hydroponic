from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from authlib.jose import jwt
from config.config import settings
from utils.crypto import load_signing_key, load_verification_key
from repositories.user_repo import UserRepository
from schemas.user import UserLogin, Token
import bcrypt

class UserService:
    def __init__(self, session):
        self.repo = UserRepository(session)

    async def authenticate_user(self, user_credentials: UserLogin):
        user = await self.repo.get_user_by_username(user_credentials.username)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        if not bcrypt.checkpw(user_credentials.password.encode('utf-8'), user['password'].encode('utf-8')):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        return user
    
    def create_access_token(self, sub: str):
        now = datetime.now(timezone.utc)
        payload = {
            "sub": sub,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(hours=1)).timestamp())
        }
        key = load_signing_key().decode()
        return jwt.encode({"alg": settings.ALGORITHM}, payload, key).decode('utf-8')
    
    def verify_token(self, token: str):
        key = load_verification_key().decode()
        claims = jwt.decode(token, key)
        claims.validate()
        print(claims)

        return claims