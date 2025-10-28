from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from models.plant_data import SensorData

class PlantRepository:
    def __init__(self, session: AsyncSession):
        self.session = session # db session

    async def add_sensor_data(self, data: SensorData):
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)
        return data

    async def get_all_sensor_data(self, page: int = 1, limit: int = 25):
        stmt = text(
            """
            SELECT * FROM sensor_data ORDER BY "timestamp" DESC LIMIT :limit OFFSET :offset
            """
        )
        result = await self.session.execute(stmt, {"limit": limit, "offset": (page - 1) * limit})
        return list(result.mappings())

    async def get_specific_sensor_data(self, sensor_type: str, page: int = 1, limit: int = 25):
        stmt = text(
            """
            SELECT :sensor_type, "timestamp" FROM sensor_data
            ORDER BY "timestamp" DESC LIMIT :limit OFFSET :offset
            """
        )
        result = await self.session.execute(stmt, {"sensor_type": sensor_type, "limit": limit, "offset": (page - 1) * limit})
        return list(result.mappings())
    
    async def get_latest_sensor_data(self):
        stmt = text(
            """
            SELECT * FROM sensor_data ORDER BY "timestamp" DESC LIMIT 1
            """
        )
        result = await self.session.execute(stmt)
        return result.mappings().first()
