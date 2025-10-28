from sqlalchemy.ext.asyncio import AsyncSession
from repositories.actuator_repo import ActuatorRepository
from schemas.actuator import ActuatorIn, ActuatorOut
from models.actuator_data import ActuatorData

class ActuatorService:
    def __init__(self, session: AsyncSession):
        self.repo = ActuatorRepository(session)

    async def add_data(self, actuator_data: ActuatorIn) -> ActuatorOut:
        entity = ActuatorData(**actuator_data.model_dump())
        added_record = await self.repo.add_actuator_data(entity)
        return ActuatorOut.model_validate(added_record)

    async def get_all_data(self, page: int = 1, limit: int = 25) -> list[ActuatorOut]:
        records = await self.repo.get_all_actuator_data(page, limit)
        return [ActuatorOut.model_validate(record) for record in records]

    async def get_specific_data(self, actuator_type: str, page: int = 1, limit: int = 25) -> list[ActuatorOut]:
        records = await self.repo.get_specific_actuator_data(actuator_type, page, limit)
        return [ActuatorOut.model_validate(record) for record in records]
    
    async def get_latest_data(self) -> ActuatorOut | None:
        record = await self.repo.get_latest_actuator_data()
        if record:
            return ActuatorOut.model_validate(record)
        return None