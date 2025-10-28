from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from models.environment_data import EnvironmentData

class EnvironmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session  # db session

    async def add_environment_data(self, data: EnvironmentData):
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)
        return data

    async def get_all_environment_data(self, page: int = 1, limit: int = 25):
        stmt = text(
            """
            SELECT * FROM environment_data ORDER BY "timestamp" DESC LIMIT :limit OFFSET :offset
            """
        )
        result = await self.session.execute(stmt, {"limit": limit, "offset": (page - 1) * limit})
        return list(result.mappings())
    
    async def get_specific_environment_data(self, data_type: str, page: int = 1, limit: int = 25):
        stmt = text(
            """
            SELECT :data_type, "timestamp" FROM environment_data
            ORDER BY "timestamp" DESC LIMIT :limit OFFSET :offset
            """
        )
        result = await self.session.execute(stmt, {"data_type": data_type, "limit": limit, "offset": (page - 1) * limit})
        return list(result.mappings())
    
    async def get_latest_environment_data(self):
        stmt = text(
            """
            SELECT * FROM environment_data ORDER BY "timestamp" DESC LIMIT 1
            """
        )
        result = await self.session.execute(stmt)
        return result.mappings().first()
    
