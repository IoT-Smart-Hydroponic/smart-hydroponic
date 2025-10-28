from pydantic import BaseModel, Field
from datetime import datetime

class EnvironmentIn(BaseModel):
    deviceid: str = Field(..., max_length=50)
    timestamp: datetime = Field(default_factory=datetime.now)
    temperature_atas: float = Field(0.0)
    temperature_bawah: float = Field(0.0)
    humidity_atas: float = Field(0.0)
    humidity_bawah: float = Field(0.0)
    avg_temperature: float = Field(0.0)
    avg_humidity: float = Field(0.0)
    light_intensity_atas: int = Field(0, ge=0)
    light_intensity_bawah: int = Field(0, ge=0)
    avg_light_intensity: float = Field(0.0)

class EnvironmentOut(EnvironmentIn):
    class Config:
        from_attributes = True