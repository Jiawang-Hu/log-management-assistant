import re

LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}[-/]\d{2}[-/]\d{2}\s+\d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>ERROR|WARN|WARNING|INFO|DEBUG)\s+"
    r"(?:\[(?P<service>[^\]]+)\]\s*)?"
    r"(?P<message>.*?)(?:\s+trace(?:Id|ID|id)=(?P<trace>[A-Za-z0-9_-]+))?$"
)


def parse_log_line(line: str, fallback_service: str) -> dict:
    clean = line.rstrip("\r\n")
    match = LOG_PATTERN.match(clean)
    if not match:
        return {
            "timestamp": "",
            "level": "INFO",
            "service": fallback_service,
            "message": clean,
            "trace_id": "",
            "raw": clean,
        }
    data = match.groupdict()
    return {
        "timestamp": data["timestamp"],
        "level": "WARN" if data["level"] == "WARNING" else data["level"],
        "service": data["service"] or fallback_service,
        "message": data["message"].strip(),
        "trace_id": data["trace"] or "",
        "raw": clean,
    }
