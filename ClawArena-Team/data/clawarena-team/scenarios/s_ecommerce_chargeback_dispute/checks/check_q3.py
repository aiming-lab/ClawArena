"""check_q3.py — wave3 s_ecommerce_chargeback_dispute q3 checker.

Verifies output/delivery_proof.md (B + I 维度):
1. File exists
2. Delivery date 2026-04-22 present
3. Carrier FedEx present
4. Recipient last name Mehta present
5. 真实 session 续接（致命门控）：某非空 session_id 被 RunSubagent 续传 >= 2 次
   （instruction-following gate：prompt 要求在同一 subagent session 内继续，不新建）
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterator


# ---------------------------------------------------------------------------
# sessions/main.jsonl 解析 helper（真实续接信号）
# ---------------------------------------------------------------------------

def _iter_main_events(ws: Path) -> Iterator[dict]:
    p = ws / "sessions" / "main.jsonl"
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue


def _tool_calls(ev: dict) -> list[dict]:
    if "tool_calls" in ev and isinstance(ev["tool_calls"], list):
        return ev["tool_calls"]
    if ev.get("tool") or ev.get("name"):
        return [ev]
    return []


def session_id_counts(ws: Path) -> Counter:
    """统计被 RunSubagent 显式续传的非空 session_id 出现次数。

    真实续接信号：harness 仅当同一 session_id 被再次传入时才视为续接
    （new_session = session_id is None or session_id not in harnesses）。
    复用 subagent_id 并不会续接 session，故只按 session_id 计数。
    """
    counts: Counter[str] = Counter()
    for ev in _iter_main_events(ws):
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


# ---------------------------------------------------------------------------
# Main check
# ---------------------------------------------------------------------------

def main(workspace: Path) -> int:
    out = workspace / "output" / "delivery_proof.md"
    if not out.exists():
        print("FAIL: output/delivery_proof.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. Delivery date
    if not re.search(r"2026-04-22|April\s+22,?\s+2026", text, re.IGNORECASE):
        print("FAIL: delivery date 2026-04-22 not found in delivery_proof.md")
        return 1

    # 2. Carrier
    if not re.search(r"\bFedEx\b", text, re.IGNORECASE):
        print("FAIL: carrier 'FedEx' not found in delivery_proof.md")
        return 1

    # 3. Recipient last name
    if not re.search(r"\bMehta\b", text, re.IGNORECASE):
        print("FAIL: recipient last name 'Mehta' not found in delivery_proof.md")
        return 1

    # 4. 真实 session 续接（致命门控）
    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    counts = session_id_counts(workspace)
    if not counts or max(counts.values()) < 2:
        print(
            "FAIL: genuine session reuse not observed — the task asked you to continue the "
            "same subagent session: thread the same session_id, not spawn a fresh one. "
            "No non-empty session_id appears in >= 2 RunSubagent calls."
        )
        return 1

    print(
        "PASS: delivery_date=2026-04-22 + carrier=FedEx + recipient=Mehta + "
        f"genuine session reuse (max session_id RunSubagent count = {max(counts.values())} >= 2)"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
