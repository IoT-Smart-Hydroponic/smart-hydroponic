from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from models.user import User

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