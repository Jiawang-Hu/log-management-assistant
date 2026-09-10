from datetime import datetime
from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base


class LogService(Base):
    __tablename__ = "log_service"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    log_path: Mapped[str] = mapped_column(String(500), nullable=False)
    source_type: Mapped[str] = mapped_column(String(30), default="app")
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="error", nullable=False)
    last_read_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    create_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    update_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    statistics = relationship("LogStatistics", back_populates="service", cascade="all, delete-orphan")
    checkpoint = relationship("LogReaderCheckpoint", back_populates="service", uselist=False, cascade="all, delete-orphan")
