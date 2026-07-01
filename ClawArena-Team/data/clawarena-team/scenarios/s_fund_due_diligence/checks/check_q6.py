#!/usr/bin/env python3
"""check_q6.py — Validate findings/irr_evolution.md for the fund DD q6 (B-reuse) round.

Ground truth (frozen):
  - IRR peak frame:  72 (0-indexed), peak IRR ~18.4%
  - IRR final value: ~15.6%
  - Source mp4 path: visualizations/irr_evolution.mp4
  - Session reuse:   same non-empty session_id threaded into >= 2 RunSubagent calls across all rounds

Pass conditions (all must hold):

A. findings/irr_evolution.md exists and is substantive (>= 400 bytes).

B. Document contains an IRR percentage in the range [14.0, 20.0] (peak or final IRR).

C. Document references the mp4 file path:
   regex r"visualizations/irr_evolution\\.mp4|irr_evolution\\.mp4"

D. Document cross-references at least two prior-round output files:
   any two of: risk_flag_intake, backtest_sharpe, live_sharpe, sharpe_reconciliation, dd_memo

E. Genuine session reuse: sessions/main.jsonl shows the same non-empty session_id
   threaded into >= 2 RunSubagent calls (across all rounds, not only q6).

真 resume 信号 = agent 把同一个 session_id 续传给 >= 2 次 RunSubagent。复用
subagent_id 而不传 session_id 是假信号（每次新建会话）。此处只看 session_id，
>= 2 次 → 真复用，否则致命 FAIL。
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterator

# ---------------------------------------------------------------------------
# sessions/main.jsonl helper (inlined from wave4 POC _common pattern)
# ---------------------------------------------------------------------------

def _iter_main_events(ws: Path) -> Iterator[dict]:
    """Stream events from sessions/main.jsonl one line at a time."""
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
        if ev.get("tool") or ev.get("name"):
            yield ev
        # Also handle nested tool_calls arrays (some harness formats)
        elif "tool_calls" in ev and isinstance(ev.get("tool_calls"), list):
            yield ev


def _tool_calls_from_event(ev: dict) -> list[dict]:
    """Normalise multiple jsonl layouts into a flat list of tool-call dicts."""
    if "tool_calls" in ev and isinstance(ev["tool_calls"], list):
        return ev["tool_calls"]
    if ev.get("tool") or ev.get("name"):
        return [ev]
    return []


def run_subagent_session_id_counts(ws: Path) -> Counter:
    """Return Counter mapping non-empty session_id -> number of RunSubagent calls.

    只看 args["session_id"]，不回退到 subagent_id/id（后者每次新建会话，是假信号）。
    """
    counts: Counter[str] = Counter()
    for ev in _iter_main_events(ws):
        for tc in _tool_calls_from_event(ev):
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
# Regex constants
# ---------------------------------------------------------------------------

# IRR percentage: digits [14-20] with one decimal place, or bare integers 14-20
IRR_RANGE_RE = re.compile(
    r"\b(1[4-9]|20)\.\d\s*%"          # e.g. 18.4% or 15.6%
    r"|(?<!\d)(1[4-9]|20)(?!\d)\s*%",  # e.g. 18% or 15%
)

MP4_PATH_RE = re.compile(
    r"visualizations/irr_evolution\.mp4|irr_evolution\.mp4",
    re.IGNORECASE,
)

# Cross-reference anchors for prior-round outputs
PRIOR_ROUND_ANCHORS = [
    re.compile(r"risk_flag_intake", re.IGNORECASE),
    re.compile(r"backtest_sharpe", re.IGNORECASE),
    re.compile(r"live_sharpe", re.IGNORECASE),
    re.compile(r"sharpe_reconciliation", re.IGNORECASE),
    re.compile(r"dd_memo", re.IGNORECASE),
]

MIN_BYTES = 400


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q6.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1]).resolve()
    irr_doc = ws / "findings" / "irr_evolution.md"
    errors: list[str] = []

    # ── A. File exists and is substantive ────────────────────────────────────

    if not irr_doc.exists():
        print(
            "FAIL: findings/irr_evolution.md not found; "
            "q6 requires writing the IRR synthesis note to this path",
            file=sys.stderr,
        )
        return 1

    raw = irr_doc.read_bytes()
    text = raw.decode("utf-8", errors="replace")

    if len(raw) < MIN_BYTES:
        errors.append(
            f"findings/irr_evolution.md too short ({len(raw)} bytes); "
            f"must be >= {MIN_BYTES} bytes — the synthesis note must be substantive"
        )

    # ── B. IRR percentage in plausible range ─────────────────────────────────

    if not IRR_RANGE_RE.search(text):
        errors.append(
            "findings/irr_evolution.md missing an IRR percentage in the range [14.0%, 20.0%]; "
            "expected peak IRR ~18.4% and/or final IRR ~15.6% from reading "
            "visualizations/irr_evolution.mp4 frame by frame"
        )

    # ── C. MP4 path referenced ────────────────────────────────────────────────

    if not MP4_PATH_RE.search(text):
        errors.append(
            "findings/irr_evolution.md does not reference the source MP4 path; "
            "must include 'visualizations/irr_evolution.mp4' or 'irr_evolution.mp4'"
        )

    # ── D. Cross-references to at least two prior-round output files ──────────

    matched_anchors = [pat for pat in PRIOR_ROUND_ANCHORS if pat.search(text)]
    if len(matched_anchors) < 2:
        names = [p.pattern for p in PRIOR_ROUND_ANCHORS]
        errors.append(
            f"findings/irr_evolution.md cross-references only {len(matched_anchors)} "
            "prior-round output file(s); must reference at least two of: "
            + ", ".join(names)
            + " — the document must tie IRR findings back to q1–q5 Sharpe analysis "
            "and the synthetic-row risk flag"
        )

    # ── E. Genuine session reuse check ───────────────────────────────────────
    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    counts = run_subagent_session_id_counts(ws)
    if not counts or counts.most_common(1)[0][1] < 2:
        errors.append(
            "genuine session reuse not observed — the task asked you to continue the "
            "same subagent session (thread the same session_id), not spawn a fresh one"
        )

    # ── Result ────────────────────────────────────────────────────────────────

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1

    print(
        "OK: findings/irr_evolution.md passes all checks — "
        "IRR percentage present, mp4 path referenced, prior-round cross-links confirmed, "
        "session reuse verified"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
