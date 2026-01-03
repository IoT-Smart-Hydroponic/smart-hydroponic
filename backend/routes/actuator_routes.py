from fastapi import APIRouter, Depends, WebSocket
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.deps import get_session, get_db_session
from services.actuator_service import ActuatorService
from schemas.actuator import ActuatorIn, ActuatorOut

router = APIRouter(prefix="/actuators", tags=["Actuators"])


@router.post("/control", response_model=ActuatorOut, status_code=201)
async def control_actuator(
    actuator_data: ActuatorIn, session: AsyncSession = Depends(get_session)
):
    service = ActuatorService(session)
    row = await service.add_data(actuator_data)
    return row


@router.get("/status", response_model=List[ActuatorOut], status_code=200)
async def get_actuator_status(
    page: int = 1, limit: int = 25, session: AsyncSession = Depends(get_session)
):
    service = ActuatorService(session)
    return await service.get_all_data(page, limit)


@router.get(
    "/status/{actuator_type}", response_model=List[ActuatorOut], status_code=200
)
async def get_specific_actuator_status(
    actuator_type: str,
    page: int = 1,
    limit: int = 25,
    session: AsyncSession = Depends(get_session),
):
    service = ActuatorService(session)
    return await service.get_specific_data(actuator_type, page, limit)


@router.get("/status/latest", response_model=ActuatorOut | None, status_code=200)
async def get_latest_actuator_status(session: AsyncSession = Depends(get_session)):
    service = ActuatorService(session)
    return await service.get_latest_data()


@router.websocket("/ws/actuator")
async def actuator_data_websocket(websocket: WebSocket):
    """WebSocket endpoint untuk menerima data aktuator secara real-time."""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()

            async with get_db_session() as session:
                service = ActuatorService(session)
                actuator_in = ActuatorIn.model_validate(data)
                row = await service.add_data(actuator_in)
                await session.commit()
            await websocket.send_json(
                {
                    "message": "Actuator data added successfully",
                    "data": row.model_dump(),
                }
            )
    except Exception:
        await websocket.close()


@router.get(
    "/ws/actuator-info",
    summary="WebSocket Actuator Connection",
    description="Use /ws/actuator to connect to the WebSocket for real-time actuator data.",
)
def websocket_info():
    pass
