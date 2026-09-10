from datetime import date
from ..model.service import LogService
from ..utils.compress_utils import open_text
from ..utils.file_utils import resolve_log_files
from ..utils.regex_utils import parse_log_line


class LogReader:
    def read(self, service: LogService, day: date, *, level: str | None = None, keyword: str | None = None) -> list[dict]:
        result: list[dict] = []
        for path in resolve_log_files(service.log_path, day):
            with open_text(path) as stream:
                for line in stream:
                    if not line.strip(): continue
                    item = parse_log_line(line, service.service_name)
                    haystack = f"{item['message']} {item['trace_id']} {item['service']}"
                    if level and item["level"] != level: continue
                    if keyword and keyword.lower() not in haystack.lower(): continue
                    result.append(item)
        return result


log_reader = LogReader()
