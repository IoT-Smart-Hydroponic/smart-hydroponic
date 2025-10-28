from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, text
from config.db import Base
from datetime import datetime

class ActuatorData(Base):
    __tablename__ = "actuator_data"

    deviceid: Mapped[str] = mapped_column(String(50), primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        primary_key=True,
        nullable=False,
    )

    pump_status: Mapped[int] = mapped_column(Integer, nullable=False)
    light_status: Mapped[int] = mapped_column(Integer, nullable=False)
    automation_status: Mapped[int] = mapped_column(Integer, nullable=False)

