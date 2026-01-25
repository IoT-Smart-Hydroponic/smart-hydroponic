from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from schemas.plant import SensorIn, SensorOut
from models.plant_data import SensorData


class SensorService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_data(self, sensor_data: SensorIn) -> SensorOut:
        # Create ORM entity from the incoming validated Pydantic data
        row = SensorData(**sensor_data.model_dump())
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        # Convert ORM object (or refreshed instance) back to response schema
        return SensorOut.model_validate(row)

    async def get_all_data(self, page: int = 1, limit: int = 25) -> list[SensorOut]:
        stmt = text(
            """
            SELECT * FROM sensor_data ORDER BY "timestamp" DESC LIMIT :limit OFFSET :offset
            """
        )
        result = await self.session.execute(
            stmt, {"limit": limit, "offset": (page - 1) * limit}
        )
        return [SensorOut.model_validate(record) for record in result.mappings()]

    async def get_specific_data(
        self, sensor_type: str, page: int = 1, limit: int = 25
    ) -> list[SensorOut]:
        stmt = text(
            """
            SELECT :sensor_type, "timestamp" FROM sensor_data
            ORDER BY "timestamp" DESC LIMIT :limit OFFSET :offset
            """
        )
        result = await self.session.execute(
            stmt,
            {"sensor_type": sensor_type, "limit": limit, "offset": (page - 1) * limit},
        )
        return [SensorOut.model_validate(record) for record in result.mappings()]

    async def get_latest_data(self) -> SensorOut | None:
        stmt = text(
            """
            SELECT * FROM sensor_data ORDER BY "timestamp" DESC LIMIT 1
            """
        )
        record = await self.session.execute(stmt)
        record = record.mappings().first()
        if record:
            return SensorOut.model_validate(record)
        return None
