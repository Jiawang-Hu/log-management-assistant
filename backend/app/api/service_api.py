from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ..database import get_db
from ..repository.service_repository import ServiceRepository
from ..schema.service_schema import ServiceCreate, ServiceOut, ServiceUpdate
from ..service.service_service import ServiceManager

router = APIRouter(prefix="/services", tags=["服务管理"])


def require_service(db: Session, service_id: int):
    item = ServiceRepository.get(db, service_id)
    if item is None:
        raise HTTPException(404, "服务不存在")
    return item


def require_allowed_log_path(log_path: str) -> None:
    try:
        ServiceManager.ensure_path_allowed(log_path)
    except ValueError as error:
        raise HTTPException(400, str(error)) from error


@router.get("")
def list_services(keyword: str | None = None, status_: str | None = Query(None, alias="status"), enabled: bool | None = None, db: Session = Depends(get_db)):
    items = ServiceRepository.list(db)
    if keyword:
        items = [item for item in items if keyword.lower() in item.service_name.lower()]
    if status_:
        items = [item for item in items if item.status == status_]
    if enabled is not None:
        items = [item for item in items if item.enabled == enabled]
    return {"items": [ServiceOut.model_validate(x) for x in items], "total": len(items)}


@router.get("/{service_id}", response_model=ServiceOut)
def get_service(service_id: int, db: Session = Depends(get_db)):
    return require_service(db, service_id)


@router.post("", response_model=ServiceOut, status_code=status.HTTP_201_CREATED)
def create_service(payload: ServiceCreate, db: Session = Depends(get_db)):
    require_allowed_log_path(payload.log_path)
    try:
        item = ServiceRepository.create(db, **payload.model_dump(), status="error")
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(409, "服务名称已存在") from error
    return ServiceManager.refresh_status(db, item)


@router.put("/{service_id}", response_model=ServiceOut)
def update_service(service_id: int, payload: ServiceUpdate, db: Session = Depends(get_db)):
    item = require_service(db, service_id)
    require_allowed_log_path(payload.log_path)
    try:
        item = ServiceRepository.update(db, item, **payload.model_dump())
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(409, "服务名称已存在") from error
    return ServiceManager.refresh_status(db, item)


@router.patch("/{service_id}/toggle", response_model=ServiceOut)
def toggle_service(service_id: int, db: Session = Depends(get_db)):
    item = require_service(db, service_id)
    item = ServiceRepository.update(db, item, enabled=not item.enabled)
    return ServiceManager.refresh_status(db, item)


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(service_id: int, db: Session = Depends(get_db)):
    ServiceRepository.delete(db, require_service(db, service_id))
    return Response(status_code=204)
