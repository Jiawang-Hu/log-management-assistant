from datetime import date, timedelta
from sqlalchemy.orm import Session
from .log_service import LogQueryService
from ..repository.service_repository import ServiceRepository
from ..repository.statistics_repository import StatisticsRepository


class StatisticsService:
    @staticmethod
    def calculate_day(db: Session, day: date) -> None:
        for service in ServiceRepository.list(db):
            if not service.enabled: continue
            entries = LogQueryService.query(db, day, service_id=service.id)
            StatisticsRepository.upsert(db, service.id, day, sum(x["level"] == "ERROR" for x in entries), sum(x["level"] == "WARN" for x in entries))

    @staticmethod
    def summary(db: Session, day: date) -> dict:
        StatisticsService.calculate_day(db, day)
        StatisticsService.calculate_day(db, day - timedelta(days=1))
        current = StatisticsRepository.totals(db, day)
        previous = StatisticsRepository.totals(db, day - timedelta(days=1))
        return {"date": day, "error_count": current[0], "warn_count": current[1], "yesterday_error_count": previous[0], "yesterday_warn_count": previous[1], "error_delta": current[0]-previous[0], "warn_delta": current[1]-previous[1]}
