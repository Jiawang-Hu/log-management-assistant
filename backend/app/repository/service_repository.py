from sqlalchemy import select
from sqlalchemy.orm import Session
from ..model.service import LogService


class ServiceRepository:
    @staticmethod
    def list(db: Session) -> list[LogService]:
        return list(db.scalars(select(LogService).order_by(LogService.id)))

    @staticmethod
    def get(db: Session, service_id: int) -> LogService | None:
        return db.get(LogService, service_id)

    @staticmethod
    def create(db: Session, **values) -> LogService:
        item = LogService(**values)
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def update(db: Session, item: LogService, **values) -> LogService:
        for key, value in values.items(): setattr(item, key, value)
        db.commit(); db.refresh(item)
        return item

    @staticmethod
    def delete(db: Session, item: LogService) -> None:
        db.delete(item)
        db.commit()
