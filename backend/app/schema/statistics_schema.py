from datetime import date
from pydantic import BaseModel


class StatisticsSummary(BaseModel):
    date: date
    error_count: int
    warn_count: int
    yesterday_error_count: int
    yesterday_warn_count: int
    error_delta: int
    warn_delta: int
