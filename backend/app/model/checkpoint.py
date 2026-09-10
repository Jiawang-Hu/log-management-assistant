from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base


class LogReaderCheckpoint(Base):
    __tablename__ = "log_reader_checkpoint"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("log_service.id", ondelete="CASCADE"), nullable=False, unique=True)
    file_path: Mapped[str] = mapped_column(String(500), default="", nullable=False)
    offset_position: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    update_time: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
    service = relationship("LogService", back_populates="checkpoint")
