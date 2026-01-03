from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


class SensorBase(BaseModel):
    deviceid: str = Field(..., max_length=50)
    moisture1: int = Field(0, ge=0)
    moisture2: int = Field(0, ge=0)
    moisture3: int = Field(0, ge=0)
    moisture4: int = Field(0, ge=0)
    moisture5: int = Field(0, ge=0)
    moisture6: int = Field(0, ge=0)

    flowrate: float = Field(0.0)
    total_litres: float = Field(0.0)
    distance_cm: float = Field(0.0)
    ph: float = Field(0.0, ge=0.0, le=14.0)
    tds: float = Field(0.0)


class SensorIn(SensorBase):
    timestamp: Optional[datetime] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "deviceid": "sensor_001",
                "moisture1": 450,
                "moisture2": 460,
                "moisture3": 470,
                "moisture4": 480,
                "moisture5": 490,
                "moisture6": 500,
                "flowrate": 1.5,
                "total_litres": 10.0,
                "distance_cm": 15.0,
                "ph": 6.5,
                "tds": 300.0,
            }
        }
    )


class SensorOut(SensorBase):
    timestamp: datetime
    moisture_avg: float
    model_config = ConfigDict(from_attributes=True)
