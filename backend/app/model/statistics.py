from datetime import date, datetime
from sqlalchemy import Date, DateTime, ForeignKey, Index, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base


class LogStatistics(Base):
    __tablename__ = "log_statistics"
    __table_args__ = (UniqueConstraint("service_id", "stat_date"), Index("ix_statistics_service_date", "service_id", "stat_date"))

    id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("log_service.id", ondelete="CASCADE"), nullable=False)
    stat_date: Mapped[date] = mapped_column(Date, nullable=False)
    error_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    warn_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    create_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    update_time: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now, nullable=False
    )
    service = relationship("LogService", back_populates="statistics")
