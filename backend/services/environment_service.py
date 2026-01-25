from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from schemas.environment import EnvironmentIn, EnvironmentOut
from models.environment_data import EnvironmentData


class EnvironmentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_data(self, env_data: EnvironmentIn) -> EnvironmentOut:
        row = EnvironmentData(**env_data.model_dump())

        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)

        return EnvironmentOut.model_validate(row)

    async def get_all_data(
        self, page: int = 1, limit: int = 25
    ) -> list[EnvironmentOut]:
        stmt = text(
            """
            SELECT * FROM environment_data ORDER BY "timestamp" DESC LIMIT :limit OFFSET :offset
            """
        )
        result = await self.session.execute(
            stmt, {"limit": limit, "offset": (page - 1) * limit}
        )
        return [EnvironmentOut.model_validate(record) for record in result.mappings()]

    async def get_specific_data(
        self, data_type: str, page: int = 1, limit: int = 25
    ) -> list[EnvironmentOut]:
        stmt = text(
            """
            SELECT :data_type, "timestamp" FROM environment_data
            ORDER BY "timestamp" DESC LIMIT :limit OFFSET :offset
            """
        )
        result = await self.session.execute(
            stmt, {"data_type": data_type, "limit": limit, "offset": (page - 1) * limit}
        )
        return [EnvironmentOut.model_validate(record) for record in result.mappings()]

    async def get_latest_data(self) -> EnvironmentOut | None:
        stmt = text(
            """
            SELECT * FROM environment_data ORDER BY "timestamp" DESC LIMIT 1
            """
        )
        record = await self.session.execute(stmt)
        record = record.mappings().first()
        if record:
            return EnvironmentOut.model_validate(record)
        return None
