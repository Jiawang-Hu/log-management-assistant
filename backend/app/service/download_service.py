from datetime import date
from sqlalchemy.orm import Session
from .log_service import LogQueryService
from ..utils.export_utils import export_lines


class DownloadService:
    @staticmethod
    def build(db: Session, day: date, **filters) -> bytes:
        return export_lines(LogQueryService.query(db, day, **filters))
