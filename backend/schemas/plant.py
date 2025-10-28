from pydantic import BaseModel, Field
from datetime import datetime

class SensorIn(BaseModel):
    deviceid: str = Field(..., max_length=50)
    timestamp: datetime = Field(default_factory=datetime.now)
    moisture1: int = Field(0, ge=0)
    moisture2: int = Field(0, ge=0)
    moisture3: int = Field(0, ge=0)
    moisture4: int = Field(0, ge=0)
    moisture5: int = Field(0, ge=0)
    moisture6: int = Field(0, ge=0)
    moistureavg: float = Field(0.0, ge=0.0)
    flowrate: float = Field(0.0)
    total_litres: float = Field(0.0)
    distance_cm: float = Field(0.0)
    ph: float = Field(0.0, ge=0.0, le=14.0)
    tds: float = Field(0.0)


class SensorOut(SensorIn):
    class Config:
        from_attributes = True