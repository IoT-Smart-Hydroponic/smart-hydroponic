from fastapi import APIRouter, Depends, WebSocket
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.deps import get_session, get_db_session
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

@router.websocket("/ws/sensor")
async def sensor_data_websocket(websocket: WebSocket):
    """WebSocket endpoint untuk menerima data sensor secara real-time."""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()

            async with get_db_session() as session:
                service = SensorService(session)
                sensor_in = SensorIn.model_validate(data)
                row = await service.add_data(sensor_in)
                await session.commit()
            await websocket.send_json(
                {
                    "message": "Sensor data added successfully",
                    "data": row.model_dump(),
                }
            )
    except Exception as e:
        await websocket.close()

@router.get(
        "/ws/sensor-info", 
        summary="WebSocket Sensor Connection",
        description="Use /ws/sensor to connect to the WebSocket for real-time sensor data.")
def websocket_info():
    pass