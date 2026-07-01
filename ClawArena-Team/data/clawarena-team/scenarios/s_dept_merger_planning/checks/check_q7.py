"""check_q7.py — Week-2 merger status synthesis with background headcount delta.

Pass conditions (all required, exit 0):
  1. ADVISORY ONLY (non-gating): sessions/main.jsonl contains >= 1
     RunSubagent(run_in_background=true).
  2. output/merger_status.md exists.
  3. output/merger_status.md has >= 5 bullet-point items (lines starting with "- " or "* ").
  4. output/merger_status.md references >= 2 files from prior rounds
     (consolidated_roster, equipment_dedup, org_chart_analysis, findings,
      merger_plan, merger_summary, union_feedback_prediction, scope_intake,
      roster_summary, equipment_disposition, sections/findings).
  5. figures/org_headcount_delta.png exists (chart produced by background sub).

Tags verified: background_subagent, async_long_running, partial_result_handling,
               final_synthesis
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterator


# ---------------------------------------------------------------------------
# sessions/main.jsonl helpers (self-contained, no shared _common import)
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
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        yield ev


def _tool_calls(ev: dict) -> list[dict]:
    """兼容多种 jsonl 落盘形态。"""
    if "tool_calls" in ev and isinstance(ev["tool_calls"], list):
        return ev["tool_calls"]
    if ev.get("tool") or ev.get("name"):
        return [ev]
    return []


def has_background_run(ws: Path) -> bool:
    """Return True if at least one RunSubagent with run_in_background=true is present."""
    for ev in _iter_main_events(ws):
        for tc in _tool_calls(ev):
            name = tc.get("tool") or tc.get("name")
            if name in ("RunSubagent", "Bash"):
                args = tc.get("args") or tc.get("arguments") or {}
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except Exception:
                        args = {}
                rib = args.get("run_in_background")
                if rib in (True, 1) or (
                    isinstance(rib, str) and rib.strip().lower() in ("true", "1", "yes")
                ):
                    return True
                if name == "Bash":
                    _cmd = str(args.get("command") or args.get("cmd") or "")
                    if (
                        re.search(r"(?<!&)&\s*$", _cmd.strip())
                        or re.search(r"(?:^|\s)(?:nohup|setsid)\b", _cmd)
                        or "disown" in _cmd
                    ):
                        return True
    return False


# ---------------------------------------------------------------------------
# Prior-round file references expected in merger_status.md
# ---------------------------------------------------------------------------

PRIOR_ROUND_FILE_PATTERNS: list[re.Pattern] = [
    re.compile(r"consolidated_roster", re.IGNORECASE),
    re.compile(r"equipment_dedup", re.IGNORECASE),
    re.compile(r"org_chart_analysis", re.IGNORECASE),
    re.compile(r"findings\.md|sections/findings", re.IGNORECASE),
    re.compile(r"merger_plan", re.IGNORECASE),
    re.compile(r"merger_summary", re.IGNORECASE),
    re.compile(r"union_feedback_prediction", re.IGNORECASE),
    re.compile(r"scope_intake", re.IGNORECASE),
    re.compile(r"roster_summary", re.IGNORECASE),
    re.compile(r"equipment_disposition", re.IGNORECASE),
]


def _count_prior_file_refs(text: str) -> int:
    """Count how many distinct prior-round file patterns appear in text."""
    return sum(1 for pat in PRIOR_ROUND_FILE_PATTERNS if pat.search(text))


def _count_bullets(text: str) -> int:
    """Count bullet-point lines (lines starting with '- ' or '* ' after optional whitespace)."""
    return len(re.findall(r"^[ \t]*[-*]\s+\S", text, re.MULTILINE))


# ---------------------------------------------------------------------------
# Main check
# ---------------------------------------------------------------------------

def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q7.py <workspace>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    errors: list[str] = []

    # ------------------------------------------------------------------
    # Check 1: background RunSubagent observed in session log
    # ------------------------------------------------------------------
    if not has_background_run(ws):
        # instruction-following gate: prompt explicitly asks to launch this in the background
        errors.append(
            "background subagent not observed — the task asked you to launch this "
            "as a background RunSubagent(run_in_background=true) and not block the main thread"
        )

    # ------------------------------------------------------------------
    # Check 2: output/merger_status.md exists
    # ------------------------------------------------------------------
    status_md = ws / "output" / "merger_status.md"
    if not status_md.exists():
        errors.append("output/merger_status.md does not exist")
        # Cannot proceed with content checks.
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    text = status_md.read_text(encoding="utf-8", errors="ignore")

    # ------------------------------------------------------------------
    # Check 3: >= 5 bullet points
    # ------------------------------------------------------------------
    bullet_count = _count_bullets(text)
    if bullet_count < 5:
        errors.append(
            f"output/merger_status.md has {bullet_count} bullet-point item(s); "
            "must have >= 5 bullets summarising the week-1 merger findings"
        )

    # ------------------------------------------------------------------
    # Check 4: >= 2 references to prior-round output files
    # ------------------------------------------------------------------
    ref_count = _count_prior_file_refs(text)
    if ref_count < 2:
        errors.append(
            f"output/merger_status.md references {ref_count} prior-round file(s); "
            "must reference >= 2 (e.g. consolidated_roster, equipment_dedup, "
            "org_chart_analysis, merger_plan, findings.md, merger_summary, etc.) "
            "to establish continuity from rounds 1–6"
        )

    # ------------------------------------------------------------------
    # Check 5: figures/org_headcount_delta.png exists
    # ------------------------------------------------------------------
    chart_png = ws / "figures" / "org_headcount_delta.png"
    if not chart_png.exists():
        errors.append(
            "figures/org_headcount_delta.png does not exist — "
            "the background headcount delta subagent must render and save this chart "
            "showing before/after departmental headcount (Hospital A vs Hospital B)"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        "PASS: output/merger_status.md has >= 5 bullets "
        "and >= 2 prior-round file references; figures/org_headcount_delta.png present"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
