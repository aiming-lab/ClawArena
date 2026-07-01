"""q2: background_subagent (ADVISORY ONLY, non-gating) + notes/strategies_summary.md 5+ bullet."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, has_background_run, passed, workspace_root


def main() -> int:
    ws = workspace_root()
    summary = ws / "notes" / "strategies_summary.md"
    if not summary.exists():
        fail("missing notes/strategies_summary.md")
    text = summary.read_text(encoding="utf-8", errors="ignore")
    # 计 bullet 行（以 -, *, + 起首；或形如 "1. "）
    bullets = re.findall(r"^\s*(?:[-*+]|\d+\.)\s+\S", text, flags=re.MULTILINE)
    if len(bullets) < 5:
        fail(f"need >= 5 bullets in summary, got {len(bullets)}")
    # instruction-following gate: prompt explicitly asks to launch this in the background
    if not has_background_run(ws):
        fail("background subagent not observed — the task asked you to launch this as a background RunSubagent(run_in_background=true) and not block the main thread")
    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
