from datetime import date
from pathlib import Path
from types import SimpleNamespace
from app.reader.log_reader import LogReader


def test_reader_filters_level_and_keyword_in_trace_id(tmp_path: Path):
    (tmp_path / "app-2026-09-07.log").write_text(
        "2026-09-07 10:00:00 ERROR [orders] failed traceId=abc123\n"
        "2026-09-07 10:00:01 INFO [orders] ok traceId=def456\n", encoding="utf-8")
    service = SimpleNamespace(log_path=str(tmp_path), service_name="orders")
    result = LogReader().read(service, date(2026, 9, 7), level="ERROR", keyword="abc")
    assert len(result) == 1
    assert result[0]["message"] == "failed"
