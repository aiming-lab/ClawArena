"""q3: analysis/schema_inferred.md exists + >= 4 columns identified
    + time series identified + same session reused (not re-spawned from scratch).

Pass conditions (all required):
  1. analysis/schema_inferred.md exists and is >= 80 chars.
  2. Contains >= 4 distinct column/field names or mentions "4 column" / "schema".
  3. Mentions time series / timestamp / date context.
  4. [致命门控] sessions/main.jsonl 中某非空 session_id 被 RunSubagent 续传 >= 2 次（真实续接信号：
     q2 起头的 session_id 被 q3 再次显式续传）。
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, iter_main_events, passed, workspace_root, _tool_calls


def session_id_counts(ws: Path) -> Counter:
    """统计被 RunSubagent 显式续传的非空 session_id 出现次数。

    真实续接信号：harness 仅当同一 session_id 被再次传入时才视为续接
    （new_session = session_id is None or session_id not in harnesses）。
    复用 subagent_id 并不会续接 session，故只按 session_id 计数。
    """
    counts: Counter[str] = Counter()
    for ev in iter_main_events(ws):
        for tc in _tool_calls(ev):
            name = tc.get("tool") or tc.get("name")
            if name != "RunSubagent":
                continue
            args = tc.get("args") or tc.get("arguments") or {}
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    args = {}
            sid = args.get("session_id")
            if sid:
                counts[str(sid)] += 1
    return counts


def main() -> int:
    ws = workspace_root()
    doc = ws / "analysis" / "schema_inferred.md"
    if not doc.exists():
        fail("missing analysis/schema_inferred.md")
    text = doc.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 80:
        fail("analysis/schema_inferred.md is too short (< 80 chars)")

    # >= 4 columns: look for lines that describe column/field names
    # schema-by-shape: count backtick-wrapped names, or "column", or list items
    col_hits = re.findall(r"`[a-zA-Z_][a-zA-Z0-9_]*`", text)
    if len(col_hits) < 4:
        # fallback: count bullet points that look like column descriptions
        bullets = re.findall(r"^\s*[-*]\s+\S", text, flags=re.MULTILINE)
        if len(bullets) < 4:
            # fallback 2: explicit mention
            if not re.search(r"\b[4-9]\s+col(?:umn)?s?\b", text, re.IGNORECASE):
                fail(
                    f"schema_inferred.md must identify >= 4 columns "
                    f"(found {len(col_hits)} backtick names, {len(bullets)} bullets)"
                )

    # time series check
    if not re.search(
        r"time(?:\s*stamp)?|date|temporal|t[-_]?series|chronolog|datetime",
        text,
        re.IGNORECASE,
    ):
        fail("schema_inferred.md must mention time-series / timestamp dimension")

    # 真实 session 续接（致命门控）
    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    counts = session_id_counts(ws)
    if not counts or max(counts.values()) < 2:
        fail(
            "genuine session reuse not observed — the task asked you to continue the same "
            "subagent session: thread the same session_id, not spawn a fresh one. "
            "No non-empty session_id appears in >= 2 RunSubagent calls."
        )
    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
