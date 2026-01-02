from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from models.hydroponic import HydroponicData
from schemas.hydroponic import (
    HydroponicDataSensor, 
    HydroponicDataEnvironment,
    HydroponicDataActuator
)
import datetime
from uuid import UUID

SENSOR_FIELDS = set(HydroponicDataSensor.model_fields.keys())
ENVIRONMENT_FIELDS = set(HydroponicDataEnvironment.model_fields.keys())
ACTUATOR_FIELDS = set(HydroponicDataActuator.model_fields.keys())

GROUPS = {
    "sensor": SENSOR_FIELDS,
    "environment": ENVIRONMENT_FIELDS,
    "actuator": ACTUATOR_FIELDS,
}

def get_uuidv7_from_timestamp(time : datetime.datetime, is_end=False) -> UUID:
    timestamp_ms = int(time.timestamp() * 1000)

    uuid_int = (timestamp_ms & 0xFFFFFFFFFFFF) << 80

    uuid_int |= (0x7 << 76) # Set version to 7

    uuid_int |= (0x2 << 62) # Set variant to RFC 4122

    if is_end:
        uuid_int |= 0x000000000FFF3FFFFFFFFFFFFFFF
    else:
        pass
    return UUID(int=uuid_int)

class HydroponicRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_hydroponic_data(self, data: HydroponicData):
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)
        return data

    async def get_all_hydroponic_data(self, page: int = 1, limit: int = 25):
        stmt = text(
            """
            SELECT * FROM hydroponic_data ORDER BY "dataid" DESC LIMIT :limit OFFSET :offset
            """
        )
        result = await self.session.execute(stmt, {"limit": limit, "offset": (page - 1) * limit})
        return list(result.mappings())

    async def get_specific_hydroponic_data(self, parameter: str, page: int = 1, limit: int = 25, start_date: str | None = None, end_date: str | None = None):
        if parameter in GROUPS:
            _fields = GROUPS[parameter]

        elif parameter in SENSOR_FIELDS | ENVIRONMENT_FIELDS | ACTUATOR_FIELDS:
            _fields = {parameter}

        else:
            raise ValueError(f"Invalid parameter: {parameter}")
        
        columns = ", ".join(f'"{field}"' for field in _fields)

        # Process date conversion to UUID v7
        if start_date:
            # Check if contains time component
            if " " in start_date:
                dt_start = datetime.datetime.fromisoformat(start_date).replace(tzinfo=datetime.timezone.utc)
            else:
                dt_start = datetime.datetime.combine(datetime.datetime.fromisoformat(start_date), datetime.time.min, tzinfo=datetime.timezone.utc)
            start_date = str(get_uuidv7_from_timestamp(dt_start))
        
        if end_date:
            if " " in end_date:
                dt_end = datetime.datetime.fromisoformat(end_date).replace(tzinfo=datetime.timezone.utc)
            else:
                dt_end = datetime.datetime.combine(datetime.datetime.fromisoformat(end_date), datetime.time.max, tzinfo=datetime.timezone.utc)
            end_date = str(get_uuidv7_from_timestamp(dt_end, is_end=True))
        stmt = text(
            f"""
            SELECT "dataid", {columns} FROM hydroponic_data
            WHERE "dataid" >= :start_date AND "dataid" <= :end_date ORDER BY "dataid" DESC LIMIT :limit OFFSET :offset
            """
        )
        result = await self.session.execute(stmt, { "limit": limit, "offset": (page - 1) * limit, "start_date": start_date, "end_date": end_date})
        return list(result.mappings())
    
    async def get_latest_hydroponic_data(self):
        stmt = text(
            """
            SELECT * FROM hydroponic_data ORDER BY "dataid" DESC LIMIT 1
            """
        )
        result = await self.session.execute(stmt)
        return result.mappings().first()