from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.deps import get_session
from services.sensor_service import SensorService
from schemas.plant import SensorIn, SensorOut

router = APIRouter(prefix="/plants", tags=["Plants"])

@router.post("/data", response_model=SensorOut, status_code=201)
async def add_sensor_data(sensor_data: SensorIn, session: AsyncSession = Depends(get_session)):
    """Endpoint untuk menambahkan data sensor baru."""
    service = SensorService(session)
    row = await service.add_data(sensor_data)
    return row

@router.get("/data", response_model=List[SensorOut], status_code=200)
async def get_sensor_data(page: int = 1, limit: int = 25, session: AsyncSession = Depends(get_session)):
    service = SensorService(session)
    return await service.get_all_data(page, limit)

@router.get("/data/{sensor_type}", response_model=List[SensorOut], status_code=200)
async def get_specific_sensor_data(sensor_type: str, page: int = 1, limit: int = 25, session: AsyncSession = Depends(get_session)):
    service = SensorService(session)
    return await service.get_specific_data(sensor_type, page, limit)

@router.get("/data/latest", response_model=SensorOut | None, status_code=200)
async def get_latest_sensor_data(session: AsyncSession = Depends(get_session)):
    service = SensorService(session)
    return await service.get_latest_data()