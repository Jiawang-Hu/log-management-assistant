from datetime import date
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from ..model.statistics import LogStatistics


class StatisticsRepository:
    @staticmethod
    def totals(db: Session, day: date) -> tuple[int, int]:
        statement = select(
            func.coalesce(func.sum(LogStatistics.error_count), 0),
            func.coalesce(func.sum(LogStatistics.warn_count), 0),
        ).where(LogStatistics.stat_date == day)
        row = db.execute(statement).one()
        return int(row[0]), int(row[1])

    @staticmethod
    def upsert(db: Session, service_id: int, day: date, errors: int, warnings: int) -> LogStatistics:
        item = db.scalar(select(LogStatistics).where(LogStatistics.service_id == service_id, LogStatistics.stat_date == day))
        if item is None:
            item = LogStatistics(service_id=service_id, stat_date=day)
            db.add(item)
        item.error_count = errors
        item.warn_count = warnings
        db.commit()
        db.refresh(item)
        return item
