from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from models.user import User
from schemas.user import UserUpdate
import bcrypt


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

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

    async def get_user_by_id(self, user_id: str):
        stmt = text(
            """
            SELECT * FROM user_data WHERE id = :user_id
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
