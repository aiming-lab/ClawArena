"""check_q6.py — Wave3 s_strategy_backtest_review q6 checker.

Business scenario: Backtest review wrap-up. The model should:
  1. Launch a monte-carlo simulation in the background (tools/monte_carlo.sh, ~60s).
  2. Meanwhile synthesise q1–q5 findings into output/backtest_verdict.md containing:
       a) ≥ 5 bullet points
       b) References ≥ 2 prior rounds by name/number (e.g. "q2", "code_audit", "ratios_audit",
          "audit_summary", "risk_email", "audit_plan")
       c) Decision keyword in {approve, reject, conditional}
  3. Attach figures/equity_curve.mp4 as the video asset for the verdict.

Pass conditions (all must hold, exit 0):
  1. [ADVISORY ONLY (non-gating)] sessions/main.jsonl records at least one RunSubagent(run_in_background=true).
  2. output/backtest_verdict.md exists and has ≥ 5 bullet points.
  3. output/backtest_verdict.md references ≥ 2 prior rounds.
  4. output/backtest_verdict.md contains a decision keyword (approve/reject/conditional).
  5. figures/equity_curve.mp4 exists and is a non-empty file.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# JSONL session helpers (embedded per check-file convention, WAVE4_GUIDE §5.1)
# ---------------------------------------------------------------------------


def _iter_tool_calls(ws: Path):
    """Yield (tool_name, args_dict) for every tool call in sessions/main.jsonl.

    Handles the real flat assistant shape
    {"role":"assistant","tool_calls":[{"id","name","arguments":{...}}]},
    the nested OpenAI-style {"function":{"name","arguments"}} form, and the
    Anthropic content-block form {"type":"tool_use","name","input"}.
    """
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

        for tc in ev.get("tool_calls") or []:
            if not isinstance(tc, dict):
                continue
            name = tc.get("name") or (tc.get("function") or {}).get("name") or ""
            args = tc.get("arguments")
            if args is None:
                args = (tc.get("function") or {}).get("arguments")
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    args = {}
            if not isinstance(args, dict):
                args = {}
            if name:
                yield str(name), args

        content = ev.get("content")
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    name = block.get("name") or ""
                    args = block.get("input")
                    if not isinstance(args, dict):
                        args = {}
                    if name:
                        yield str(name), args


def _has_background_run(ws: Path) -> bool:
    for name, args in _iter_tool_calls(ws):
        if name == "RunSubagent" and args.get("run_in_background"):
            return True
    return False


# ---------------------------------------------------------------------------
# Bullet-point counting helper
# ---------------------------------------------------------------------------


def _count_bullets(text: str) -> int:
    """Count lines that look like bullet points (-, *, •, numbered list items)."""
    pattern = re.compile(
        r"^\s*(?:[-*•]\s+|\d+[\.\)]\s+)",
        re.MULTILINE,
    )
    return len(pattern.findall(text))


# ---------------------------------------------------------------------------
# Prior-round reference detection
# ---------------------------------------------------------------------------

_PRIOR_ROUND_PATTERNS = [
    r"\bq1\b",
    r"\bq2\b",
    r"\bq3\b",
    r"\bq4\b",
    r"\bq5\b",
    r"\baudit[_\s]plan\b",
    r"\bcode[_\s]audit\b",
    r"\bratios[_\s]audit\b",
    r"\baudit[_\s]summary\b",
    r"\brisk[_\s]email\b",
    r"\bround\s*[1-5]\b",
    r"\bstep\s*[1-5]\b",
    r"\bphase\s*[1-5]\b",
    r"\bfinding[s]?\s+from\b",
    r"\bprevious\s+(?:round|step|phase|analysis)\b",
    r"\bearli(?:er|est)\s+(?:round|step|phase|analysis|finding)\b",
]


def _count_prior_round_refs(text: str) -> int:
    count = 0
    for pat in _PRIOR_ROUND_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            count += 1
    return count


# ---------------------------------------------------------------------------
# Decision keyword detection
# ---------------------------------------------------------------------------

_DECISION_PATTERN = re.compile(
    r"\b(?:approve[d]?|reject[ed]?|conditional(?:ly)?|conditionally\s+approve[d]?|"
    r"conditional\s+approval|not\s+approve[d]?)\b",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Main check
# ---------------------------------------------------------------------------


def main(workspace: Path) -> int:
    # 1. Background RunSubagent
    # instruction-following gate: prompt explicitly asks to launch this in the background
    if not _has_background_run(workspace):
        print(
            "FAIL: background subagent not observed — the task asked you to launch this "
            "as a background RunSubagent(run_in_background=true) and not block the main thread"
        )
        return 1

    # 2. output/backtest_verdict.md exists
    verdict_path = workspace / "output" / "backtest_verdict.md"
    if not verdict_path.exists():
        print("FAIL: output/backtest_verdict.md not found.")
        return 1

    text = verdict_path.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 50:
        print("FAIL: output/backtest_verdict.md is too short (< 50 chars).")
        return 1

    # 3. ≥ 5 bullet points
    n_bullets = _count_bullets(text)
    if n_bullets < 5:
        print(
            f"FAIL: output/backtest_verdict.md has only {n_bullets} bullet point(s); "
            "need ≥ 5. Summarise all major findings as numbered or bulleted items."
        )
        return 1

    # 4. ≥ 2 prior-round references
    n_refs = _count_prior_round_refs(text)
    if n_refs < 2:
        print(
            f"FAIL: output/backtest_verdict.md references only {n_refs} prior round(s); "
            "need ≥ 2. Cite earlier rounds explicitly, e.g. 'From q2 (code_audit.md)…' "
            "or 'As established in ratios_audit.md…'."
        )
        return 1

    # 5. Decision keyword present
    if not _DECISION_PATTERN.search(text):
        print(
            "FAIL: output/backtest_verdict.md does not contain a final decision. "
            "The verdict must include one of: approve, reject, conditional (approval)."
        )
        return 1

    # 6. figures/equity_curve.mp4 exists and is non-empty
    mp4_path = workspace / "figures" / "equity_curve.mp4"
    if not mp4_path.exists():
        print("FAIL: figures/equity_curve.mp4 not found.")
        return 1
    if mp4_path.stat().st_size < 1000:
        print(
            f"FAIL: figures/equity_curve.mp4 is suspiciously small "
            f"({mp4_path.stat().st_size} bytes); expected a valid MP4 file."
        )
        return 1

    print(
        f"PASS: q6 — background RunSubagent confirmed; "
        f"backtest_verdict.md has {n_bullets} bullets, "
        f"{n_refs} prior-round reference(s), decision keyword present; "
        f"figures/equity_curve.mp4 ({mp4_path.stat().st_size:,} bytes) attached."
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
