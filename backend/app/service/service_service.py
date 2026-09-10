from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from ..config import get_settings
from ..model.service import LogService
from ..utils.file_utils import resolve_log_files


class ServiceManager:
    @staticmethod
    def _base_path(configured_path: str) -> Path:
        path = Path(configured_path).expanduser()
        return path.parent if any(char in path.name for char in "*?[") else path

    @staticmethod
    def ensure_path_allowed(configured_path: str) -> None:
        allowed_root = Path(get_settings().allowed_log_root).expanduser().resolve()
        candidate = ServiceManager._base_path(configured_path).resolve()
        try:
            candidate.relative_to(allowed_root)
        except ValueError as error:
            raise ValueError(f"日志路径必须位于允许目录 {allowed_root} 内") from error

    @staticmethod
    def refresh_status(db: Session, item: LogService) -> LogService:
        if not item.enabled:
            status = "disabled"
        else:
            base = ServiceManager._base_path(item.log_path)
            status = "collecting" if base.is_file() or base.is_dir() else "error"

        item.status = status
        now = datetime.now()
        if status == "collecting" and resolve_log_files(item.log_path, now.date()):
            item.last_read_at = now

        db.commit()
        db.refresh(item)
        return item
