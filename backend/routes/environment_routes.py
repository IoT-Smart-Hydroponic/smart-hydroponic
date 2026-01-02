from fastapi import APIRouter, Depends, WebSocket
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.deps import get_session, get_db_session
from services.environment_service import EnvironmentService
from schemas.environment import EnvironmentIn, EnvironmentOut

router = APIRouter(prefix="/environment", tags=["Environment"])

@router.post("/data", response_model=EnvironmentOut, status_code=201)
async def add_environment_data(env_data: EnvironmentIn, session: AsyncSession = Depends(get_session)):
    service = EnvironmentService(session)
    row = await service.add_data(env_data)
    return row

@router.get("/data", response_model=List[EnvironmentOut], status_code=200)
async def get_environment_data(page: int = 1, limit: int = 25, session: AsyncSession = Depends(get_session)):
    service = EnvironmentService(session)
    return await service.get_all_data(page, limit)

@router.get("/data/{data_type}", response_model=List[EnvironmentOut], status_code=200)
async def get_specific_environment_data(data_type: str, page: int = 1, limit: int = 25, session: AsyncSession = Depends(get_session)):
    service = EnvironmentService(session)
    return await service.get_specific_data(data_type, page, limit)

@router.get("/data/latest", response_model=EnvironmentOut | None, status_code=200)
async def get_latest_environment_data(session: AsyncSession = Depends(get_session)):
    service = EnvironmentService(session)
    return await service.get_latest_data()

@router.websocket("/ws/environment")
async def environment_data_websocket(websocket: WebSocket):
    """WebSocket endpoint untuk menerima data lingkungan secara real-time."""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()

            async with get_db_session() as session:
                service = EnvironmentService(session)
                env_in = EnvironmentIn.model_validate(data)
                row = await service.add_data(env_in)
                await session.commit()
            await websocket.send_json(
                {
                    "message": "Environment data added successfully",
                    "data": row.model_dump(),
                }
            )
    except Exception as e:
        await websocket.close()

@router.get(
        "/ws/environment-info",
        summary="WebSocket Environment Connection",
        description="Use /ws/environment to connect to the WebSocket for real-time environment data.")
def websocket_info():
    pass