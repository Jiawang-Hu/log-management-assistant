from sqlalchemy import select
from sqlalchemy.orm import Session
from ..model.checkpoint import LogReaderCheckpoint


class CheckpointRepository:
    @staticmethod
    def get_or_create(db: Session, service_id: int) -> LogReaderCheckpoint:
        item = db.scalar(select(LogReaderCheckpoint).where(LogReaderCheckpoint.service_id == service_id))
        if item is None:
            item = LogReaderCheckpoint(service_id=service_id)
            db.add(item)
            db.commit()
            db.refresh(item)
        return item
