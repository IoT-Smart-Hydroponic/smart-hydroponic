from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, text, DOUBLE_PRECISION
from config.db import Base
from datetime import datetime

class EnvironmentData(Base):
    __tablename__ = "environment_data"

    deviceid: Mapped[str] = mapped_column(String(50), primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=text("CURRENT_TIMESTAMP"),
        primary_key=True,
        nullable=False,
    )

    temperature_atas: Mapped[float] = mapped_column(DOUBLE_PRECISION, nullable=False, default=0.0)
    temperature_bawah: Mapped[float] = mapped_column(DOUBLE_PRECISION, nullable=False, default=0.0)
    humidity_atas: Mapped[float] = mapped_column(DOUBLE_PRECISION, nullable=False, default=0.0)
    humidity_bawah: Mapped[float] = mapped_column(DOUBLE_PRECISION, nullable=False, default=0.0)
    avg_temperature: Mapped[float] = mapped_column(DOUBLE_PRECISION, nullable=False, default=0.0)
    avg_humidity: Mapped[float] = mapped_column(DOUBLE_PRECISION, nullable=False, default=0.0)
    light_intensity_atas: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    light_intensity_bawah: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    avg_light_intensity: Mapped[float] = mapped_column(DOUBLE_PRECISION, nullable=False, default=0.0, server_default="0.0")