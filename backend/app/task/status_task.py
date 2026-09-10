from ..database import SessionLocal
from ..repository.service_repository import ServiceRepository
from ..service.service_service import ServiceManager


def refresh_all_statuses():
    with SessionLocal() as db:
        for item in ServiceRepository.list(db):
            ServiceManager.refresh_status(db, item)
