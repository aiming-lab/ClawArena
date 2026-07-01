"""q3: findings/swingup_fail_analysis.md 含 frame 67 ± 2 + balance loss + 真 session 复用（致命门控）."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (
    fail,
    find_first_int_near,
    has_phrase_any,
    passed,
    run_subagent_session_id_counts,
    workspace_root,
)


def main() -> int:
    ws = workspace_root()
    finding = ws / "findings" / "swingup_fail_analysis.md"
    if not finding.exists():
        fail("missing findings/swingup_fail_analysis.md")
    text = finding.read_text(encoding="utf-8", errors="ignore")
    if find_first_int_near(text, 67, tolerance=2) is None:
        fail("frame number near 67 (±2) not found in analysis")
    if not has_phrase_any(text, ["balance loss", "失稳", "lost balance", "loss of balance", "balance failure"]):
        fail("failure mode 'balance loss' (or zh equivalent) not mentioned")
    if "v4_swingup_fail.mp4" not in text:
        fail("missing reference to videos/v4_swingup_fail.mp4")
    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    counts = run_subagent_session_id_counts(ws)
    if not counts or max(counts.values()) < 2:
        fail(
            "genuine session reuse not observed — the task asked you to continue the "
            "same subagent session (thread the same session_id), not spawn a fresh one"
        )
    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
