from datetime import date
from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from ..database import get_db
from ..schema.log_schema import LogPage
from ..service.download_service import DownloadService
from ..service.log_service import LogQueryService

router = APIRouter(prefix="/logs", tags=["日志"])


@router.get("", response_model=LogPage)
def query_logs(date_: date = Query(alias="date"), level: str | None = None, keyword: str | None = None, service_id: int | None = None, limit: int = Query(200, ge=1, le=5000), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    entries = LogQueryService.query(db, date_, service_id=service_id, level=level, keyword=keyword)
    return {"items": entries[offset:offset+limit], "total": len(entries), "limit": limit, "offset": offset}


@router.get("/download")
def download_logs(date_: date = Query(alias="date"), level: str | None = None, keyword: str | None = None, service_id: int | None = None, db: Session = Depends(get_db)):
    content = DownloadService.build(db, date_, service_id=service_id, level=level, keyword=keyword)
    filename = f"logs-{date_.isoformat()}.log"
    return Response(content, media_type="text/plain; charset=utf-8", headers={"Content-Disposition": f'attachment; filename="{filename}"'})
