from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from authlib.jose import jwt
from config.config import settings
from utils.crypto import load_signing_key, load_verification_key
from schemas.user import UserLogin, UserUpdate, UserOut, TokenPayload
import bcrypt

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from models.user import User


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def authenticate_user(self, user_credentials: UserLogin):
        user = None
        
        if user_credentials.username:
            user = await self.get_user_by_username(user_credentials.username)
        elif user_credentials.email:
            user = await self.get_user_by_email(user_credentials.email)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        if not bcrypt.checkpw(
            user_credentials.password.encode("utf-8"), user["password"].encode("utf-8")
        ):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        return UserOut.model_validate(user)

    def create_access_token(self, data: dict):
        now = datetime.now(timezone.utc)
        payload = TokenPayload(
            **data,
            iat=int(now.timestamp()),
            exp=int((now + timedelta(hours=1)).timestamp()),
        )
        key = load_signing_key().decode()
        return jwt.encode(
            {"alg": settings.ALGORITHM}, payload.model_dump(), key
        ).decode("utf-8")

    def verify_token(self, token: str):
        key = load_verification_key().decode()
        claims = jwt.decode(token, key)
        claims.validate()

        return claims

    async def add_user(self, user: User):
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_user_by_username(self, username: str):
        stmt = text(
            """
            SELECT * FROM user_data WHERE username = :username
            """
        )
        result = await self.session.execute(stmt, {"username": username})
        return result.mappings().first()
    
    async def get_user_by_email(self, email: str):
        stmt = text(
            """
            SELECT * FROM user_data WHERE email = :email
            """
        )
        result = await self.session.execute(stmt, {"email": email})
        return result.mappings().first()

    async def get_user_by_id(self, user_id: str):
        stmt = text(
            """
            SELECT * FROM user_data WHERE userid = :user_id
            """
        )

        result = await self.session.execute(stmt, {"user_id": user_id})

        return result.mappings().first()

    async def get_all_users(self):
        stmt = text(
            """
            SELECT * FROM user_data
            """
        )
        result = await self.session.execute(stmt)
        return result.mappings().all()

    async def update_user(self, user_id: str, user_update: UserUpdate):
        user = await self.get_user_by_id(user_id)
        if not user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)

        if "password" in update_data:
            hashed = bcrypt.hashpw(
                update_data["password"].encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            update_data["password"] = hashed

        for key, value in update_data.items():
            setattr(user, key, value)

        try:
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except IntegrityError:
            await self.session.rollback()
            raise ValueError("Username already registered")

    async def delete_user(self, user: User):
        await self.session.delete(user)
        await self.session.commit()
        return
