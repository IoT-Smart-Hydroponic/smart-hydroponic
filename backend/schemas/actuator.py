from pydantic import BaseModel, Field
from datetime import datetime

class ActuatorIn(BaseModel):
    deviceid: str = Field(..., max_length=50)
    timestamp: datetime = Field(default_factory=datetime.now)
    pump_status: int = Field(0, ge=0)
    light_status: int = Field(0, ge=0)
    automation_status: int = Field(0, ge=0)

class ActuatorOut(ActuatorIn):
    class Config:
        from_attributes = True