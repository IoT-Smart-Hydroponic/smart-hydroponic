from sqlalchemy.ext.asyncio import AsyncSession
from repositories.environment_repo import EnvironmentRepository
from schemas.environment import EnvironmentIn, EnvironmentOut
from models.environment_data import EnvironmentData


class EnvironmentService:
    def __init__(self, session: AsyncSession):
        self.repo = EnvironmentRepository(session)

    async def add_data(self, env_data: EnvironmentIn) -> EnvironmentOut:
        entity = EnvironmentData(**env_data.model_dump())
        added_record = await self.repo.add_environment_data(entity)
        return EnvironmentOut.model_validate(added_record)

    async def get_all_data(
        self, page: int = 1, limit: int = 25
    ) -> list[EnvironmentOut]:
        records = await self.repo.get_all_environment_data(page, limit)
        return [EnvironmentOut.model_validate(record) for record in records]

    async def get_specific_data(
        self, data_type: str, page: int = 1, limit: int = 25
    ) -> list[EnvironmentOut]:
        records = await self.repo.get_specific_environment_data(data_type, page, limit)
        return [EnvironmentOut.model_validate(record) for record in records]

    async def get_latest_data(self) -> EnvironmentOut | None:
        record = await self.repo.get_latest_environment_data()
        if record:
            return EnvironmentOut.model_validate(record)
        return None
