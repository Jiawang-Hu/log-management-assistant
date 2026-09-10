from datetime import date
from sqlalchemy.orm import Session
from ..reader.log_reader import log_reader
from ..repository.service_repository import ServiceRepository
from .service_service import ServiceManager


class LogQueryService:
    @staticmethod
    def query(db: Session, day: date, service_id: int | None = None, **filters) -> list[dict]:
        services = [ServiceRepository.get(db, service_id)] if service_id else ServiceRepository.list(db)
        entries: list[dict] = []
        for service in services:
            if not service or not service.enabled:
                continue
            try:
                ServiceManager.ensure_path_allowed(service.log_path)
            except ValueError:
                continue
            entries.extend(log_reader.read(service, day, **filters))
        entries.sort(key=lambda item: item["timestamp"], reverse=True)
        return entries
