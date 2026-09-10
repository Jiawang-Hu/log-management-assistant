from datetime import date, timedelta
from ..database import SessionLocal
from ..service.statistics_service import StatisticsService


def calculate_yesterday_statistics():
    with SessionLocal() as db:
        StatisticsService.calculate_day(db, date.today() - timedelta(days=1))
