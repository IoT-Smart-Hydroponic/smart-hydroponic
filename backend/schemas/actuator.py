from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class ActuatorBase(BaseModel):
    deviceid: str = Field(..., max_length=50)
    pump_status: int = Field(0, ge=0)
    light_status: int = Field(0, ge=0)
    automation_status: int = Field(0, ge=0)


class ActuatorIn(ActuatorBase):
    timestamp: Optional[datetime] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "deviceid": "actuator_001",
                "pump_status": 1,
                "light_status": 1,
                "automation_status": 1,
            }
        }
    )


class ActuatorOut(ActuatorBase):
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)
