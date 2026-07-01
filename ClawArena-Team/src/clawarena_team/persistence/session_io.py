"""Session JSONL read/write.

One message per line; the first line is ``system_meta`` (containing metadata
such as owner and system prompt), followed by the three kinds ``user`` /
``assistant`` / ``tool_result`` recorded in time order.

Optional fields per line (non-meta):

- ``context_size_after``: the current total context length after this turn is
  added (computed by the local tokenizer).
- ``input_delta`` / ``output_delta`` / ``cache_read_delta``: filled for assistant
  turns only, corresponding to the three billing segments of this model call
  (local view, comparable across providers).
- ``provider_usage``: filled for assistant turns only, the raw usage returned by
  the provider (arbitrary schema).
- ``usage_normalized``: filled for assistant turns only, the unified view aligned
  across providers (the dict form of
  :class:`clawarena_team.provider.usage.UsageRecord`).
- ``provider_model_id``: filled for assistant turns only, the model id the
  provider actually served the request with (read from the ``model`` field of the
  raw response; may differ from the request-side ``model_id`` — for example,
  after fable triggers a ``refusal`` the answer is actually produced by the
  fallback ``claude-opus-4-8``).
- ``provider_extra``: filled for assistant turns only, an audit dict freely
  attached by the provider (empty by default; for example a fable fallback writes
  fields such as ``fable_refusal_fallback`` / ``fallback_model``).

These fields are **for statistics/reconciliation only**; harness decisions use
local tokenizer counts.
"""
from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Iterable


def write_session_jsonl(
    path: Path, turns: Iterable[Any], *, owner: str
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        meta = {
            "type": "system_meta",
            "owner": owner,
        }
        f.write(json.dumps(meta, ensure_ascii=False) + "\n")
        for t in turns:
            row: dict[str, Any] = {
                "uuid": uuid.uuid4().hex,
                "role": t.role,
                "content": t.content,
                "timestamp": getattr(t, "timestamp", 0.0),
                "context_size_after": getattr(t, "context_size_after", 0),
                "is_real_user_question": getattr(t, "is_real_user_question", False),
            }
            if getattr(t, "tool_calls", None):
                row["tool_calls"] = t.tool_calls
            if getattr(t, "tool_call_id", None):
                row["tool_call_id"] = t.tool_call_id
            if t.role == "assistant":
                row["input_delta"] = getattr(t, "input_delta", 0)
                row["output_delta"] = getattr(t, "output_delta", 0)
                row["cache_read_delta"] = getattr(t, "cache_read_delta", 0)
                pu = getattr(t, "provider_usage", None)
                if pu:
                    row["provider_usage"] = pu
                un = getattr(t, "usage_normalized", None)
                if un:
                    row["usage_normalized"] = un
                pmi = getattr(t, "provider_model_id", "") or ""
                if pmi:
                    row["provider_model_id"] = pmi
                pex = getattr(t, "provider_extra", None)
                if pex:
                    row["provider_extra"] = pex
            srs = getattr(t, "system_reminders", None)
            if srs:
                row["system_reminders"] = list(srs)
            tns = getattr(t, "task_notifications", None)
            if tns:
                row["task_notifications"] = list(tns)
            f.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")


def read_session_jsonl(path: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out
