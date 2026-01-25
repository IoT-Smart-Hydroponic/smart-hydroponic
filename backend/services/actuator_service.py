from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from schemas.actuator import ActuatorIn, ActuatorOut
from models.actuator_data import ActuatorData


class ActuatorService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_data(self, actuator_data: ActuatorIn) -> ActuatorOut:
        row = ActuatorData(**actuator_data.model_dump())
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)

        return ActuatorOut.model_validate(row)

    async def get_all_data(self, page: int = 1, limit: int = 25) -> list[ActuatorOut]:
        stmt = text(
            """
            SELECT * FROM actuator_data ORDER BY "timestamp" DESC LIMIT :limit OFFSET :offset
            """
        )
        result = await self.session.execute(
            stmt, {"limit": limit, "offset": (page - 1) * limit}
        )
        return [ActuatorOut.model_validate(record) for record in result.mappings()]

    async def get_specific_data(
        self, actuator_type: str, page: int = 1, limit: int = 25
    ) -> list[ActuatorOut]:
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
        return [ActuatorOut.model_validate(record) for record in result.mappings()]

    async def get_latest_data(self) -> ActuatorOut | None:
        stmt = text(
            """
            SELECT * FROM actuator_data ORDER BY "timestamp" DESC LIMIT 1
            """
        )
        record = await self.session.execute(stmt)
        record = record.mappings().first()
        if record:
            return ActuatorOut.model_validate(record)
        return None
