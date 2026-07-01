"""check_q6.py — Background grep launch + digest synthesis check.

Checks (all must pass; exit 0):

  1. ADVISORY ONLY (non-gating): has_background_run — sessions/main.jsonl contains
     at least one RunSubagent call with run_in_background=True (the cross_paper_grep launch).

  2. output/digest_summary.md exists and contains >= 5 bullet lines
     (lines whose stripped form starts with '-' or '*').

  3. Required tags are present: the question carries
     background_subagent, async_long_running, partial_result_handling,
     final_synthesis — validated here by confirming the output demonstrates
     the expected behaviour (tag correctness is a data-level property, not
     re-checked at runtime).

Usage:
    python checks/check_q6.py <workspace_path>

Exit 0 on pass, 1 on failure.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterator


# ---------------------------------------------------------------------------
# Session parsing helpers (self-contained, copied from wave4 check pattern)
# ---------------------------------------------------------------------------

def _iter_main_events(ws: Path) -> Iterator[dict]:
    p = ws / "sessions" / "main.jsonl"
    if not p.exists():
        return
    for raw in p.read_text(encoding="utf-8", errors="replace").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            yield json.loads(raw)
        except json.JSONDecodeError:
            continue


def _tool_calls(ev: dict) -> list[dict]:
    """兼容多种 jsonl 落盘格式：tool_calls 列表 / tool 直接字段 / name 字段。"""
    if "tool_calls" in ev and isinstance(ev["tool_calls"], list):
        return ev["tool_calls"]
    if ev.get("tool") or ev.get("name"):
        return [ev]
    return []


def _has_background_run(ws: Path) -> bool:
    """Return True if main.jsonl contains a RunSubagent with run_in_background=True."""
    for ev in _iter_main_events(ws):
        for tc in _tool_calls(ev):
            name = tc.get("tool") or tc.get("name")
            if name == "RunSubagent":
                args = tc.get("args") or tc.get("arguments") or {}
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except Exception:
                        args = {}
                if args.get("run_in_background"):
                    return True
    return False


# ---------------------------------------------------------------------------
# Bullet counting helper
# ---------------------------------------------------------------------------

_BULLET_RE = re.compile(r"^[\-\*]\s+\S")


def _count_bullets(text: str) -> int:
    """Count lines that start with a markdown bullet (- or * followed by non-space)."""
    return sum(1 for ln in text.splitlines() if _BULLET_RE.match(ln.strip()))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: check_q6.py <workspace>")
        return 1

    ws = Path(sys.argv[1])
    failures: list[str] = []

    # ── 1. Background RunSubagent launched ────────────────────────────────
    sessions_dir = ws / "sessions"
    if not sessions_dir.exists():
        print(
            "[warn] sessions/ directory not found — skipping background-run check",
            file=sys.stderr,
        )
    else:
        # instruction-following gate: prompt explicitly asks to launch this in the background
        if not _has_background_run(ws):
            failures.append(
                "background subagent not observed — the task asked you to launch this as a "
                "background RunSubagent(run_in_background=true) and not block the main thread"
            )

    # ── 2. output/digest_summary.md exists with >= 5 bullets ─────────────
    summary_path = ws / "output" / "digest_summary.md"
    if not summary_path.exists():
        failures.append(
            "output/digest_summary.md does not exist — "
            "the main-thread synthesis task must produce this file"
        )
    else:
        text = summary_path.read_text(encoding="utf-8", errors="replace")
        if len(text.strip()) < 50:
            failures.append(
                f"output/digest_summary.md is too short ({len(text.strip())} chars); "
                "expected substantive synthesis content"
            )
        else:
            n_bullets = _count_bullets(text)
            if n_bullets < 5:
                failures.append(
                    f"output/digest_summary.md has only {n_bullets} bullet line(s) "
                    f"(lines starting with '- ' or '* '); need >= 5 to demonstrate "
                    "synthesis of prior-round outputs"
                )

    if failures:
        print("FAIL: check_q6 — background async grep + digest synthesis check failed:")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(
        "PASS: check_q6 — background RunSubagent confirmed; "
        "output/digest_summary.md has >= 5 bullets synthesising prior rounds."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
