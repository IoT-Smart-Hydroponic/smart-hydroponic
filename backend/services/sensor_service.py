from sqlalchemy.ext.asyncio import AsyncSession
from repositories.plant_repo import PlantRepository
from schemas.plant import SensorIn, SensorOut
from models.plant_data import SensorData


class SensorService:
    def __init__(self, session: AsyncSession):
        self.repo = PlantRepository(session)

    async def add_data(self, sensor_data: SensorIn) -> SensorOut:
        # Create ORM entity from the incoming validated Pydantic data
        entity = SensorData(**sensor_data.model_dump())
        added_record = await self.repo.add_sensor_data(entity)
        # Convert ORM object (or refreshed instance) back to response schema
        return SensorOut.model_validate(added_record)

    async def get_all_data(self, page: int = 1, limit: int = 25) -> list[SensorOut]:
        records = await self.repo.get_all_sensor_data(page, limit)
        return [SensorOut.model_validate(record) for record in records]

    async def get_specific_data(
        self, sensor_type: str, page: int = 1, limit: int = 25
    ) -> list[SensorOut]:
        records = await self.repo.get_specific_sensor_data(sensor_type, page, limit)
        return [SensorOut.model_validate(record) for record in records]

    async def get_latest_data(self) -> SensorOut | None:
        record = await self.repo.get_latest_sensor_data()
        if record:
            return SensorOut.model_validate(record)
        return None
