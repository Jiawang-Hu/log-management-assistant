from datetime import date
from pathlib import Path


def resolve_log_files(configured_path: str, day: date) -> list[Path]:
    raw = Path(configured_path).expanduser()
    base = raw.parent if any(ch in raw.name for ch in "*?[") else raw
    if base.is_file(): return [base]
    if not base.exists() or not base.is_dir(): return []
    patterns = [
        f"*{day.isoformat()}*.log.gz", f"*{day.strftime('%Y%m%d')}*.log.gz",
        f"*{day.isoformat()}*.log", f"*{day.strftime('%Y%m%d')}*.log",
    ]
    found: dict[str, Path] = {}
    for pattern in patterns:
        for path in base.glob(pattern):
            if path.is_file(): found[str(path.resolve())] = path
    # 兜底，可能今日日志还没有带日期文件名
    if not found and day == date.today():
        for path in base.glob("*.log"):
            if path.is_file(): found[str(path.resolve())] = path
    return sorted(found.values())
