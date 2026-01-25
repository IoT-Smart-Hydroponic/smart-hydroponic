from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from models.hydroponic import HydroponicData
from schemas.hydroponic import (
    HydroponicDataSensor,
    HydroponicDataEnvironment,
    HydroponicDataActuator,
    HydroponicInternalResult,
    HydroponicOut,
)
from utils.converter import get_uuidv7_from_timestamp

SENSOR_FIELDS = set(HydroponicDataSensor.model_fields.keys())
ENVIRONMENT_FIELDS = set(HydroponicDataEnvironment.model_fields.keys())
ACTUATOR_FIELDS = set(HydroponicDataActuator.model_fields.keys())

GROUPS = {
    "sensor": SENSOR_FIELDS,
    "environment": ENVIRONMENT_FIELDS,
    "actuator": ACTUATOR_FIELDS,
}


class HydroponicRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_hydroponic_data(self, data: HydroponicData):
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)
        return data

    async def get_all_hydroponic_data(
        self,
        page: int = 1,
        limit: int = 25,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> HydroponicInternalResult:
        filters = []
        params = {"limit": limit, "offset": (page - 1) * limit}

        _start_date = get_uuidv7_from_timestamp(start_date) if start_date else None
        _end_date = (
            get_uuidv7_from_timestamp(end_date, is_end=True) if end_date else None
        )

        if _start_date and _end_date:
            filters.append('"dataid" >= :start_date')
            filters.append('"dataid" <= :end_date')
            params["start_date"] = _start_date
            params["end_date"] = _end_date

        where_clause = ""
        if filters:
            where_clause = " WHERE " + " AND ".join(filters)

        query_data = f"""
            SELECT * FROM hydroponic_data
            {where_clause}
            ORDER BY "dataid" DESC
            LIMIT :limit OFFSET :offset
        """

        query_count = f"""
            SELECT COUNT(*) FROM hydroponic_data
            {where_clause}
        """

        data_result = await self.session.execute(
            text(query_data),
            params,
        )
        count_result = await self.session.execute(
            text(query_count),
            {k: v for k, v in params.items() if k in ["start_date", "end_date"]},
        )
        return HydroponicInternalResult(
            data=list(
                HydroponicOut.model_validate(record)
                for record in data_result.mappings()
            ),
            total=count_result.scalar_one(),
        )

    async def get_specific_hydroponic_data(
        self,
        parameter: str,
        page: int = 1,
        limit: int = 25,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> HydroponicInternalResult:
        if parameter in GROUPS:
            _fields = GROUPS[parameter]

        elif parameter in SENSOR_FIELDS | ENVIRONMENT_FIELDS | ACTUATOR_FIELDS:
            _fields = {parameter}

        else:
            raise ValueError(f"Invalid parameter: {parameter}")

        columns = ", ".join(f'"{field}"' for field in _fields)

        filters = []
        params = {"limit": limit, "offset": (page - 1) * limit}

        # Process date conversion to UUID v7
        _start_date = get_uuidv7_from_timestamp(start_date) if start_date else None
        _end_date = (
            get_uuidv7_from_timestamp(end_date, is_end=True) if end_date else None
        )

        if _start_date and _end_date:
            filters.append('"dataid" >= :start_date')
            filters.append('"dataid" <= :end_date')
            params["start_date"] = _start_date
            params["end_date"] = _end_date

        where_clause = ""
        if filters:
            where_clause = " WHERE " + " AND ".join(filters)

        query_data = f"""
            SELECT "dataid", {columns} FROM hydroponic_data
            {where_clause}
            ORDER BY "dataid" DESC
            LIMIT :limit OFFSET :offset
        """

        query_count = f"""
            SELECT COUNT(*) FROM hydroponic_data
            {where_clause}
        """

        data_result = await self.session.execute(
            text(query_data),
            params,
        )
        count_result = await self.session.execute(
            text(query_count),
            {k: v for k, v in params.items() if k in ["start_date", "end_date"]},
        )

        return HydroponicInternalResult(
            data=list(
                HydroponicOut.model_validate(record)
                for record in data_result.mappings()
            ),
            total=count_result.scalar() or 0,
        )

    async def get_latest_hydroponic_data(self):
        stmt = text(
            """
            SELECT * FROM hydroponic_data ORDER BY "dataid" DESC LIMIT 1
            """
        )
        result = await self.session.execute(stmt)
        return result.mappings().first()
