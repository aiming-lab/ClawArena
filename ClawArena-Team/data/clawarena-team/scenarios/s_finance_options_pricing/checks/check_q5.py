"""q5 (after u1): findings/var_report.md contains VaR ~0.34 + "VaR" label
    + session reused >= 3 times total.

Pass conditions (all required):
  1. findings/var_report.md exists and >= 80 chars.
  2. Contains a float in [0.30, 0.38] (VaR 95% estimate ≈ 0.34).
  3. Contains "VaR" or "value at risk" (case-insensitive).
  4. [致命门控] sessions/main.jsonl 中某非空 session_id 被 RunSubagent 续传 >= 3 次（真实续接信号：
     q2 + q3 + q5 共用同一 session_id）。
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
    doc = ws / "findings" / "var_report.md"
    if not doc.exists():
        fail("missing findings/var_report.md")
    text = doc.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 80:
        fail("findings/var_report.md is too short")

    # VaR label
    if not re.search(r"\bVaR\b|[Vv]alue[\s\-]?[Aa]t[\s\-]?[Rr]isk", text):
        fail("var_report.md must contain 'VaR' or 'Value at Risk'")

    # VaR value ≈ 0.34 ± 0.04
    var_hit = re.search(r"\b0\.\s*3[0-8]\b", text)
    if not var_hit:
        fail("var_report.md missing VaR estimate in [0.30, 0.38] (expected ≈ 0.34)")

    # 真实 session 续接（致命门控）
    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    counts = session_id_counts(ws)
    if not counts or max(counts.values()) < 3:
        fail(
            "genuine session reuse not observed — the task asked you to continue the same "
            "subagent session: thread the same session_id, not spawn a fresh one. "
            "No non-empty session_id appears in >= 3 RunSubagent calls."
        )
    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
