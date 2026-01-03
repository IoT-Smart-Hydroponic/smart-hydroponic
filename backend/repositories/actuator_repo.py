from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from models.actuator_data import ActuatorData


class ActuatorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session  # db session

    async def add_actuator_data(self, data: ActuatorData):
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)
        return data

    async def get_all_actuator_data(self, page: int = 1, limit: int = 25):
        stmt = text(
            """
            SELECT * FROM actuator_data ORDER BY "timestamp" DESC LIMIT :limit OFFSET :offset
            """
        )
        result = await self.session.execute(
            stmt, {"limit": limit, "offset": (page - 1) * limit}
        )
        return list(result.mappings())

    async def get_specific_actuator_data(
        self, actuator_type: str, page: int = 1, limit: int = 25
    ):
        stmt = text(
            """
            SELECT :actuator_type, "timestamp" FROM actuator_data
            ORDER BY "timestamp" DESC LIMIT :limit OFFSET :offset
            """
        )
        result = await self.session.execute(
            stmt,
            {
                "actuator_type": actuator_type,
                "limit": limit,
                "offset": (page - 1) * limit,
            },
        )
        return list(result.mappings())

    async def get_latest_actuator_data(self):
        stmt = text(
            """
            SELECT * FROM actuator_data ORDER BY "timestamp" DESC LIMIT 1
            """
        )
        result = await self.session.execute(stmt)
        return result.mappings().first()
