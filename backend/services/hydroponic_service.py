from sqlalchemy.ext.asyncio import AsyncSession
from repositories.hydroponic_repo import HydroponicRepository
from schemas.hydroponic import HydroponicIn, HydroponicOut
from models.hydroponic import HydroponicData

class HydroponicService:
    def __init__(self, session: AsyncSession):
        self.repo = HydroponicRepository(session)

    async def add_data(self, hydroponic_data: HydroponicIn) -> HydroponicOut:
        # Create ORM entity from the incoming validated Pydantic data
        entity = HydroponicData(**hydroponic_data.model_dump())
        added_record = await self.repo.add_hydroponic_data(entity)
        # Convert ORM object (or refreshed instance) back to response schema
        return HydroponicOut.model_validate(added_record)
    
    async def get_all_data(self, page: int = 1, limit: int = 25) -> list[HydroponicOut]:
        records = await self.repo.get_all_hydroponic_data(page, limit)
        return [HydroponicOut.model_validate(record) for record in records]
    
    async def get_specific_data(self, parameter: str, page: int = 1, limit: int = 25, start_date: str | None = None, end_date: str | None = None) -> list[HydroponicOut]:
        records = await self.repo.get_specific_hydroponic_data(parameter, page, limit, start_date, end_date)
        return [HydroponicOut.model_validate(record) for record in records]
    
    async def get_latest_data(self) -> HydroponicOut | None:
        record = await self.repo.get_latest_hydroponic_data()
        if record:
            return HydroponicOut.model_validate(record)
        return None