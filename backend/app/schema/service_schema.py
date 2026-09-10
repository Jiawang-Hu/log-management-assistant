from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ServiceBase(BaseModel):
    service_name: str = Field(min_length=1, max_length=100)
    log_path: str = Field(min_length=1, max_length=500)
    source_type: str = Field(default="app", max_length=30)
    enabled: bool = True

    @field_validator("service_name", "log_path", "source_type", mode="before")
    @classmethod
    def strip_text_fields(cls, value: str) -> str:
        return value.strip() if isinstance(value, str) else value


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(ServiceBase):
    pass


class ServiceOut(ServiceBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str
    last_read_at: datetime | None
    create_time: datetime
    update_time: datetime
