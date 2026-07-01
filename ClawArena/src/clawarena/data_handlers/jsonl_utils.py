"""JSONL shared utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict]:
    """Read a JSONL file and return list of parsed dicts."""
    if not path.exists():
        return []
    entries: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            entries.append(json.loads(line))
    return entries


def trim_llm_log_messages(log: Any) -> Any:
    """Trim llm_log so messages contains only the last user turn onward."""
    if not isinstance(log, dict):
        return log
    messages = log.get("messages")
    if not isinstance(messages, list) or not messages:
        return log
    last_user_idx: int | None = None
    for i in range(len(messages) - 1, -1, -1):
        if messages[i].get("role") == "user":
            last_user_idx = i
            break
    if last_user_idx is None:
        return log
    trimmed = dict(log)
    trimmed["messages"] = messages[last_user_idx:]
    return trimmed
