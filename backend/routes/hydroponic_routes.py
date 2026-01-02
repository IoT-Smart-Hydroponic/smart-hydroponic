from fastapi import APIRouter, Depends, Request, WebSocket, WebSocketDisconnect
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from utils.deps import get_session, get_db_session
from services.hydroponic_service import HydroponicService
from schemas.hydroponic import (
    HydroponicIn, 
    HydroponicOut, 
    HydroponicDataSensor, 
    HydroponicDataEnvironment, 
    HydroponicDataActuator, 
    HydroponicAggregate
)
from uuid import UUID, uuid7, uuid4
from utils.manager import manager
from utils.aggregator import aggregator
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/hydroponics", tags=["Hydroponics"])

templates = Jinja2Templates(directory="./templates")

DEVICE_CONFIG = {
    "sensor-data": {
        "role": "sensor",
        "room": "hydroponics",
        "model": HydroponicDataSensor,
    },
    "environment-data": {
        "role": "environment",
        "room": "hydroponics",
        "model": HydroponicDataEnvironment,
    },
    "actuator-data": {
        "role": "actuator",
        "room": "hydroponics",
        "model": HydroponicDataActuator,
    },
    "web-client": {
        "role": "web-client",
        "room": "hydroponics",
        "model": None,
    },
}

@router.get("/data/latest", response_model=HydroponicOut | None, status_code=200)
async def get_latest_hydroponic_data(session: AsyncSession = Depends(get_session)):
    service = HydroponicService(session)
    return await service.get_latest_data()

@router.get("/data/{parameter}", response_model=List[HydroponicOut], response_model_exclude_none=True, status_code=200)
async def get_specific_hydroponic_data(parameter: str, page: int = 1, limit: int = 25, start_date: str | None = None, end_date: str | None = None, session: AsyncSession = Depends(get_session)):
    service = HydroponicService(session)
    return await service.get_specific_data(parameter, page, limit, start_date, end_date)

@router.post("/data", response_model=HydroponicOut, status_code=201)
async def add_hydroponic_data(hydroponic_data: HydroponicIn, session: AsyncSession = Depends(get_session)):
    """Endpoint untuk menambahkan data hidroponik baru."""
    service = HydroponicService(session)
    row = await service.add_data(hydroponic_data)
    return row

@router.get("/data", response_model=List[HydroponicOut], status_code=200)
async def get_hydroponic_data(page: int = 1, limit: int = 25, session: AsyncSession = Depends(get_session)):
    service = HydroponicService(session)
    return await service.get_all_data(page, limit)

@router.websocket("/ws/{device_type}")
async def hydroponic_data_websocket(device_type: str, websocket: WebSocket):
    """WebSocket endpoint untuk menerima data hidroponik secara real-time."""
    config = DEVICE_CONFIG.get(device_type)
    if not config:
        await websocket.close(code=4000, reason="Unknown device type")
        return
    
    session_id = str(uuid4())
    await websocket.accept()

    try:
        register = await websocket.receive_json()
        physical_id = register.get("physical_id", "unknown_device")
    except Exception:
        await websocket.close(code=4001, reason="Invalid registration data")
        return
    
    role = config["role"]
    room = config["room"]
    validator_model = config["model"]

    await manager.connect(
        room=room,
        role=role,
        client_id=session_id,
        websocket=websocket
    )

    print(f"{role.capitalize()}: {physical_id} connected with session ID: {session_id}")
    
    try:
        while True:
            data = await websocket.receive_json()

            if validator_model:
                validated_data = validator_model.model_validate(data)

                snapshot = await aggregator.gather_data(
                    source=role,
                    data=validated_data.model_dump(),
                )

                if snapshot:
                    async with get_db_session() as session:
                        service = HydroponicService(session)
                        saved_data = HydroponicIn.model_validate(snapshot)
                        new_data =await service.add_data(saved_data)

                    data_out = HydroponicOut.model_validate(new_data)
                    print(f"Snapshot created: {data_out.model_dump()}")

                    actuator_fields = {'moisture_avg', 'temperature_avg', 'pump_status', 'light_status', 'automation_status'}

                    await manager.send_to_room(
                        room=room,
                        role="web-client",
                        message=data_out.model_dump()
                    )

                    await manager.send_to_room(
                        room=room,
                        role="actuator",
                        message=data_out.model_dump(include=actuator_fields)
                    )
                    print(f"Snapshot created and sent to actuator clients: {data_out.model_dump(include=actuator_fields)}")
            else:
                # Directly forward commands from dashboard to actuators
                await manager.send_to_room(
                    room=room,
                    role="actuator",
                    message={
                        "type": "command",
                        "payload": data
                    }
                )

    except WebSocketDisconnect:
        await manager.disconnect(
            room="hydroponics",
            role="sensor",
            client_id=session_id
        )
        print(f"Client {session_id} disconnected")

    except Exception as e:
        await manager.disconnect(
            room="hydroponics",
            role="sensor",
            client_id=session_id
        )
        await websocket.close(code=1011)
        print(f"Error: {e}")

@router.get("/test-sensor-data", response_class=HTMLResponse)
async def test_sensor_data(request: Request):
    """Endpoint untuk menguji WebSocket sensor data hidroponik."""
    return templates.TemplateResponse("test_ws_sensor_data.html", {"request": request})

@router.get(
        "/ws/sensor-data",
        summary="WebSocket Hydroponic Connection",
        description="Use /ws/sensor-data to connect to the WebSocket for real-time hydroponic data.")
def websocket_info():
    pass
