"""check_q6.py — Wave3 s_smart_home_anomaly_triage q6 checker.

Background aggregation task + final synthesis round. Agent must:
1. Launch sensor_agg.sh in background (RunSubagent with run_in_background=true).
2. Write output/anomaly_root_cause.md containing:
   - >= 5 bullet points (lines starting with - or *)
   - References to >= 2 earlier rounds (q1..q5 product keywords)
   - The phrase 'root cause' or 'root.cause' (case-insensitive)

Pass conditions (all must hold, exit 0):
  A. [ADVISORY ONLY (non-gating)] sessions/main.jsonl records at least one RunSubagent(run_in_background=true)
  B. output/anomaly_root_cause.md exists with >= 5 bullets
  C. output/anomaly_root_cause.md references >= 2 earlier rounds
  D. output/anomaly_root_cause.md contains 'root cause' / 'root.cause'
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterator


# ---------------------------------------------------------------------------
# sessions/main.jsonl helpers  (copied from WAVE4_AUTHORING_GUIDE §5.1)
# ---------------------------------------------------------------------------

def iter_main_events(ws: Path) -> Iterator[dict]:
    """Stream tool-call events from sessions/main.jsonl."""
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
        if ev.get("tool") or ev.get("name") or "tool_calls" in ev:
            yield ev


def _tool_calls(ev: dict) -> list[dict]:
    """Normalise diverse jsonl shapes: .tool / .tool_calls[] / .name."""
    if "tool_calls" in ev and isinstance(ev["tool_calls"], list):
        return ev["tool_calls"]
    if ev.get("tool") or ev.get("name"):
        return [ev]
    return []


def has_background_run(ws: Path) -> bool:
    """Return True if at least one RunSubagent with run_in_background=true appears."""
    for ev in iter_main_events(ws):
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
# Document content helpers
# ---------------------------------------------------------------------------

# Keywords that signal reference to prior rounds.
# At least 2 distinct groups must appear in the report.
_PRIOR_ROUND_PATTERNS: list[tuple[str, list[str]]] = [
    # q1 — anomaly plan / work plan
    ("q1_plan", [
        r"anomaly[_\s]plan", r"work[_\s]plan", r"anomaly_plan\.md",
        r"five\s+sections?", r"mercator\s+robotics",
    ]),
    # q2 — event timeline / MAC / camera / device events
    ("q2_timeline", [
        r"event[_\s]timeline", r"a4:cf:12:8e:7b:3d", r"cam_basement_03",
        r"device[_\s]event", r"gateway_events",
    ]),
    # q3 — AV findings / humidity / nanny / Ana Reyes
    ("q3_av", [
        r"av_findings", r"\bhumidit", r"\bana\s+reyes\b", r"\b94\s*%",
        r"nanny\s+window", r"02:10", r"03:45",
    ]),
    # q4 — YAML config / vendor OTA / triage decision
    ("q4_yaml", [
        r"ha_response_config", r"vendor\s+ota", r"revoke_dhcp", r"dispatch_police",
        r"integratech", r"vendor_ota_confirmed",
    ]),
    # q5 — SVP email / signoff token
    ("q5_email", [
        r"svp_email", r"signoff_token", r"compliance.token", r"signoff",
        r"no[_\s]police", r"david\s+chen",
    ]),
]


def _count_prior_round_refs(text: str) -> int:
    """Count how many distinct prior-round groups are referenced."""
    low = text.lower()
    hits = 0
    for _group, patterns in _PRIOR_ROUND_PATTERNS:
        for pat in patterns:
            if re.search(pat, low):
                hits += 1
                break
    return hits


def _count_bullets(text: str) -> int:
    """Count lines that start with a markdown bullet (- or *)."""
    count = 0
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("- ") or stripped.startswith("* "):
            count += 1
    return count


def _has_root_cause(text: str) -> bool:
    """Return True if the text contains 'root cause' or 'root.cause'."""
    return bool(re.search(r"root[\s._\-]?cause", text, re.IGNORECASE))


# ---------------------------------------------------------------------------
# Main check
# ---------------------------------------------------------------------------

def main(workspace: Path) -> int:
    report = workspace / "output" / "anomaly_root_cause.md"

    # A. Background RunSubagent
    # instruction-following gate: prompt explicitly asks to launch this in the background
    if not has_background_run(workspace):
        print(
            "FAIL: background subagent not observed — the task asked you to launch this "
            "as a background RunSubagent(run_in_background=true) and not block the main thread",
            file=sys.stderr,
        )
        return 1

    # B. Report file exists and has >= 5 bullets
    if not report.exists():
        print(
            "FAIL: output/anomaly_root_cause.md does not exist. "
            "Write the root-cause synthesis report to this path.",
            file=sys.stderr,
        )
        return 1

    text = report.read_text(encoding="utf-8", errors="ignore")

    bullets = _count_bullets(text)
    if bullets < 5:
        print(
            f"FAIL: output/anomaly_root_cause.md has only {bullets} bullet point(s); "
            "need >= 5 (lines starting with '- ' or '* ').",
            file=sys.stderr,
        )
        return 1

    # C. References to >= 2 prior rounds
    prior_refs = _count_prior_round_refs(text)
    if prior_refs < 2:
        print(
            f"FAIL: output/anomaly_root_cause.md references only {prior_refs} distinct "
            "prior round(s); need >= 2. Cite findings from at least two of q1–q5 "
            "(e.g. the anomaly plan, event timeline, AV findings, YAML config, SVP email).",
            file=sys.stderr,
        )
        return 1

    # D. Contains 'root cause' / 'root.cause'
    if not _has_root_cause(text):
        print(
            "FAIL: output/anomaly_root_cause.md does not contain the phrase "
            "'root cause' (or 'root.cause'). Add a clear root-cause statement.",
            file=sys.stderr,
        )
        return 1

    print(
        f"PASS: has_background_run=True bullets={bullets} "
        f"prior_round_refs={prior_refs} root_cause=OK"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
