from pydantic import BaseModel


class LogEntry(BaseModel):
    timestamp: str
    level: str
    service: str
    message: str
    trace_id: str = ""
    raw: str


class LogPage(BaseModel):
    items: list[LogEntry]
    total: int
    limit: int
    offset: int
