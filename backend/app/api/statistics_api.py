from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..schema.statistics_schema import StatisticsSummary
from ..service.statistics_service import StatisticsService

router = APIRouter(prefix="/statistics", tags=["日志统计"])


@router.get("/summary", response_model=StatisticsSummary)
def statistics_summary(
    date_: date = Query(alias="date"), db: Session = Depends(get_db)
):
    return StatisticsService.summary(db, date_)
