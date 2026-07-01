#!/usr/bin/env python3
"""check_q5.py — Validate q5: background lint subagent + analysis/risk_summary.md.

Pass conditions (all must hold):
  1. ADVISORY ONLY (non-gating): sessions/main.jsonl contains at least one RunSubagent
     call with run_in_background == true  (background_subagent check).
  2. analysis/risk_summary.md exists.
  3. The file contains a reference to a prior-round note path, i.e. any
     of the strings: output/notes/q1_modules.md, output/notes/q2_security.md,
     output/notes/q3_deprecated.md, or output/release_summary.json.

Usage: python check_q5.py <workspace_abs_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterator


# ---------------------------------------------------------------------------
# sessions/main.jsonl helpers (inline, no external deps)
# ---------------------------------------------------------------------------

def _iter_events(ws: Path) -> Iterator[dict]:
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


def _has_background_run(ws: Path) -> bool:
    for ev in _iter_events(ws):
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
            if args.get("run_in_background"):
                return True
    return False


def _workflow_call_count(ws: Path) -> int:
    """统计 sessions/main.jsonl 中 name == 'Workflow' 的工具调用次数。"""
    count = 0
    for ev in _iter_events(ws):
        for tc in _tool_calls(ev):
            name = tc.get("tool") or tc.get("name") or (tc.get("function") or {}).get("name", "")
            if name == "Workflow":
                count += 1
    return count


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

ANCHOR_REFS = [
    "output/notes/q1_modules.md",
    "output/notes/q2_security.md",
    "output/notes/q3_deprecated.md",
    "output/release_summary.json",
]


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q5.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1]).resolve()
    errors: list[str] = []

    # 0. Workflow orchestration
    # instruction-following gate: prompt asks to orchestrate this via the Workflow tool (single script managing sub-agents)
    if _workflow_call_count(ws) == 0:
        errors.append(
            "Workflow tool not used — the task asked you to orchestrate this as a single "
            "workflow script managing the sub-agents"
        )

    # 1. Background RunSubagent call
    # instruction-following gate: prompt explicitly asks to launch this in the background
    if not _has_background_run(ws):
        errors.append(
            "background subagent not observed — the task asked you to launch this as a "
            "background RunSubagent(run_in_background=true) and not block the main thread"
        )

    # 2. analysis/risk_summary.md exists
    rsk = ws / "analysis" / "risk_summary.md"
    if not rsk.exists():
        errors.append(f"missing: analysis/risk_summary.md (expected at {rsk})")
    else:
        # 3. cross-round anchor reference
        text = rsk.read_text(encoding="utf-8", errors="ignore").lower()
        if not any(ref.lower() in text for ref in ANCHOR_REFS):
            errors.append(
                "analysis/risk_summary.md does not reference any prior-round note path; "
                "expected at least one of: " + ", ".join(ANCHOR_REFS)
            )

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
