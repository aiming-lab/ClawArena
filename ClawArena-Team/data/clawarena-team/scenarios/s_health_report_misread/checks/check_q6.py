"""check_q6.py -- Wave3 s_health_report_misread q6 checker.

Verifies findings/image_review.md produced during the imaging-session reuse round:

1. session_reuse (FATAL GATE): some non-empty RunSubagent session_id appears >= 2 times
   (genuine resume signal: the same session_id is threaded into >= 2 RunSubagent calls)
2. Word count >= 150
3. At least one imaging path reference (e.g. liver_roi_annotated.png or fibroscan_roi_annotated.png)
4. At least two cross-references to prior-round output files
   (output/lab_and_medication.md / output/imaging_summary.md /
    output/diagnosis_recommendation.md / output/specialist_referral.md /
    output/patient_letter.md / output/triage_plan.md)
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterator


# ---------------------------------------------------------------------------
# sessions/main.jsonl helpers (copied from POC _common.py pattern)
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
    """Normalise different jsonl event shapes to a list of tool-call dicts."""
    if "tool_calls" in ev and isinstance(ev["tool_calls"], list):
        return ev["tool_calls"]
    if ev.get("tool") or ev.get("name"):
        return [ev]
    return []


def _run_subagent_id_counts(ws: Path) -> Counter:
    counts: Counter[str] = Counter()
    for ev in _iter_main_events(ws):
        for tc in _tool_calls(ev):
            name = tc.get("tool") or tc.get("name") or ""
            if name != "RunSubagent":
                continue
            args = tc.get("args") or tc.get("arguments") or {}
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    args = {}
            sid = args.get("subagent_id") or args.get("id") or args.get("session_id")
            if sid:
                counts[str(sid)] += 1
    return counts


def _session_id_counts(ws: Path) -> Counter:
    """Count non-empty session_id values threaded into RunSubagent calls.

    Genuine resume signal: harness treats a call as a continuation only when the
    SAME session_id is passed again (new_session = session_id is None or unseen).
    Reusing a subagent_id alone does NOT continue a session, so we key on
    session_id explicitly.
    """
    counts: Counter[str] = Counter()
    for ev in _iter_main_events(ws):
        for tc in _tool_calls(ev):
            name = tc.get("tool") or tc.get("name") or ""
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

_IMAGING_PATH_PATTERN = re.compile(
    r"(?:liver_roi_annotated|fibroscan_roi_annotated)\.png",
    re.IGNORECASE,
)

_PRIOR_OUTPUT_NAMES = [
    "lab_and_medication",
    "imaging_summary",
    "diagnosis_recommendation",
    "specialist_referral",
    "patient_letter",
    "triage_plan",
]


def _count_prior_refs(text: str) -> int:
    count = 0
    for name in _PRIOR_OUTPUT_NAMES:
        if name in text.lower():
            count += 1
    return count


def _word_count(text: str) -> int:
    return len(text.split())


def main(workspace: Path) -> int:
    report = workspace / "findings" / "image_review.md"
    if not report.exists():
        print("FAIL: findings/image_review.md not found")
        return 1

    text = report.read_text(encoding="utf-8", errors="ignore")

    # --- Check 1: genuine session reuse (FATAL GATE) ---
    # instruction-following gate: prompt asks to continue the same subagent session (no fresh spawn)
    sess_counts = _session_id_counts(workspace)
    if not sess_counts or max(sess_counts.values()) < 2:
        print(
            "FAIL: genuine session reuse not observed — the task asked you to continue "
            "the SAME subagent session: thread the same session_id, not spawn a fresh one. "
            "No non-empty session_id appears in >= 2 RunSubagent calls."
        )
        return 1

    # --- Check 2: word count >= 150 ---
    wc = _word_count(text)
    if wc < 150:
        print(
            f"FAIL: findings/image_review.md is too short ({wc} words, need >= 150). "
            "The review must include ROI-linked clinical interpretation and cross-references."
        )
        return 1

    # --- Check 3: at least one annotated imaging path referenced ---
    if not _IMAGING_PATH_PATTERN.search(text):
        print(
            "FAIL: findings/image_review.md does not reference any annotated imaging file "
            "(expected liver_roi_annotated.png or fibroscan_roi_annotated.png). "
            "Use the vision subagent to read the new annotated images and cite their paths."
        )
        return 1

    # --- Check 4: at least 2 cross-references to prior-round output files ---
    prior_refs = _count_prior_refs(text)
    if prior_refs < 2:
        print(
            f"FAIL: findings/image_review.md references only {prior_refs} prior-round "
            f"output file(s) (need >= 2 from: {_PRIOR_OUTPUT_NAMES}). "
            "The review must explicitly anchor to at least 2 earlier findings."
        )
        return 1

    print(
        f"PASS: findings/image_review.md — "
        f"genuine session reuse: max session_id RunSubagent count = {max(sess_counts.values())} (>= 2), "
        f"word count = {wc} (>= 150), "
        f"annotated image path referenced OK, "
        f"prior-round cross-references = {prior_refs} (>= 2)."
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
