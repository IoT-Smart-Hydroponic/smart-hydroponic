from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.deps import get_session
from services.actuator_service import ActuatorService
from schemas.actuator import ActuatorIn, ActuatorOut

router = APIRouter(prefix="/actuators", tags=["Actuators"])

@router.post("/control", response_model=ActuatorOut, status_code=201)
async def control_actuator(actuator_data: ActuatorIn, session: AsyncSession = Depends(get_session)):
    service = ActuatorService(session)
    row = await service.add_data(actuator_data)
    return row

@router.get("/status", response_model=List[ActuatorOut], status_code=200)
async def get_actuator_status(page: int = 1, limit: int = 25, session: AsyncSession = Depends(get_session)):
    service = ActuatorService(session)
    return await service.get_all_data(page, limit)

@router.get("/status/{actuator_type}", response_model=List[ActuatorOut], status_code=200)
async def get_specific_actuator_status(actuator_type: str, page: int = 1, limit: int = 25, session: AsyncSession = Depends(get_session)):
    service = ActuatorService(session)
    return await service.get_specific_data(actuator_type, page, limit)

@router.get("/status/latest", response_model=ActuatorOut | None, status_code=200)
async def get_latest_actuator_status(session: AsyncSession = Depends(get_session)):
    service = ActuatorService(session)
    return await service.get_latest_data()