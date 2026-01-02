from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, text, DOUBLE_PRECISION, Computed
from config.db import Base
from datetime import datetime


class SensorData(Base):
    __tablename__ = "sensor_data"

    deviceid: Mapped[str] = mapped_column(String(50), primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=text("CURRENT_TIMESTAMP"),
        primary_key=True,
        nullable=False,
    )

    moisture1: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    moisture2: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    moisture3: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    moisture4: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    moisture5: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    moisture6: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    moisture_avg: Mapped[float] = mapped_column(
        DOUBLE_PRECISION,
        Computed(
            "((moisture1 + moisture2 + moisture3 + moisture4 + moisture5 + moisture6) / 6.0)", 
            persisted=True),
        )
    flowrate: Mapped[float] = mapped_column(DOUBLE_PRECISION, nullable=False, default=0.0)
    total_litres: Mapped[float] = mapped_column(DOUBLE_PRECISION, nullable=False, default=0.0)
    distance_cm: Mapped[float] = mapped_column(DOUBLE_PRECISION, nullable=False, default=0.0)
    ph: Mapped[float] = mapped_column(DOUBLE_PRECISION, nullable=False, default=0.0)
    tds: Mapped[float] = mapped_column(DOUBLE_PRECISION, nullable=False, default=0.0)
