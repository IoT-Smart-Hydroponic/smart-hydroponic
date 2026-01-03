from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class EnvironmentBase(BaseModel):
    deviceid: str = Field(..., max_length=50)
    temperature_atas: float = Field(0.0)
    temperature_bawah: float = Field(0.0)
    humidity_atas: float = Field(0.0)
    humidity_bawah: float = Field(0.0)
    light_intensity_atas: int = Field(0, ge=0)
    light_intensity_bawah: int = Field(0, ge=0)


class EnvironmentIn(EnvironmentBase):
    timestamp: Optional[datetime] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "deviceid": "env_sensor_001",
                "temperature_atas": 25.5,
                "temperature_bawah": 24.0,
                "humidity_atas": 60.0,
                "humidity_bawah": 58.0,
                "light_intensity_atas": 800,
                "light_intensity_bawah": 750,
            }
        }
    )


class EnvironmentOut(EnvironmentBase):
    timestamp: datetime
    temperature_avg: float
    humidity_avg: float
    light_intensity_avg: float

    model_config = ConfigDict(from_attributes=True)
