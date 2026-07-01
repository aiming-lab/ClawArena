"""check_q2.py — background subagent launched + PLC timestamp extracted.

通过条件（全部满足，exit 0）：
  1. sessions/main.jsonl 中至少 1 次 RunSubagent with run_in_background=true（致命门控）
  2. notes/plc_alarm_summary.md 存在且包含时间戳 "02:14:37"
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, has_background_run, passed, workspace_root


def main() -> int:
    ws = workspace_root()
    # 1) background check
    # instruction-following gate: prompt explicitly asks to launch this in the background
    if not has_background_run(ws):
        fail("background subagent not observed — the task asked you to launch this as a background RunSubagent(run_in_background=true) and not block the main thread")
    # 2) PLC summary
    summary = ws / "notes" / "plc_alarm_summary.md"
    if not summary.exists():
        fail("missing notes/plc_alarm_summary.md")
    text = summary.read_text(encoding="utf-8", errors="ignore")
    if "02:14:37" not in text:
        fail("alarm timestamp '02:14:37' not found in notes/plc_alarm_summary.md")
    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
