def export_lines(entries: list[dict]) -> bytes:
    content = "\n".join(
        entry.get("raw")
        or (
            f"{entry['timestamp']} {entry['level']} [{entry['service']}] "
            f"{entry['message']} traceId={entry['trace_id']}"
        )
        for entry in entries
    )
    return (content + ("\n" if content else "")).encode("utf-8")
