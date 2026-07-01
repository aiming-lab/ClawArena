#!/usr/bin/env python3
"""check_q2.py — Validate q2: LinkedIn date comparison from VLM image extraction.

Ground truth (from linkedin_screenshots/*.png — VLM-only):
  Helios Cloud: LinkedIn shows "Mar 2019 – Oct 2022"; resume claims "Mar 2019 – Aug 2022"
  Stratum Labs:  LinkedIn shows "Sep 2022 – Nov 2025"; resume claims same — no discrepancy
  Old account thumbnail: linkedin_old_account_preview.png — decoy; no authoritative dates

Pass conditions (all must hold; exit 0):
  Layer 1 — Structure:
    1. output/linkedin_date_check.md exists.
    2. >= 300 bytes.
    3. Both "Helios Cloud" and "Stratum Labs" mentioned.
  Layer 2 — Field presence:
    4. LinkedIn Helios end date "Oct 2022" (the VLM ground truth from the image).
    5. Resume Helios end date "Aug 2022".
    6. Discrepancy acknowledged (discrepan / mismatch / differ / conflict / gap).
    7. Stratum Sep 2022 start date present.
    8. Stratum Nov 2025 end date present.
  Layer 3 — Decoy guards:
    9. File must NOT use the old account thumbnail as authoritative LinkedIn data
       (hard-fail pattern: old account described as "confirming" or "contradicting").
   10. ADVISORY ONLY (non-gating): if "Oct 2022" appears in file but sessions/main.jsonl
       shows no CreateSubagent call with a vlm model_key — indicates possible text shortcut.

Usage: python check_q2.py <workspace_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


HELIOS_LINKEDIN_END_RE = re.compile(
    r"Oct(?:ober)?\s+2022|2022-10", re.IGNORECASE
)
HELIOS_RESUME_END_RE = re.compile(
    r"Aug(?:ust)?\s+2022|2022-08", re.IGNORECASE
)
DISCREPANCY_RE = re.compile(
    r"discrepan|mismatch|differ|conflict|gap", re.IGNORECASE
)
STRATUM_START_RE = re.compile(
    r"[Ss]ep(?:tember)?\s+2022|2022-09", re.IGNORECASE
)
STRATUM_END_RE = re.compile(
    r"[Nn]ov(?:ember)?\s+2025|2025-11", re.IGNORECASE
)
HELIOS_RE = re.compile(r"[Hh]elios\s+[Cc]loud")
STRATUM_RE = re.compile(r"[Ss]tratum\s+[Ll]abs")

# Hard-fail: agent treats old account thumbnail as authoritative LinkedIn data。
# 间隔限定 {0,40}：仅捕"老账号 ↔ 确认/权威"在同一短语内相邻的真实误用；避免误伤
# 跨子句的正确否定（如"J. Reyes - Developer …标记 Unverified…无 authoritative 数据"）。
OLD_ACCOUNT_AUTHORITATIVE_RE = re.compile(
    r"(?:old[\s_]?account|J\.\s*Reyes.{0,20}Developer|sidebar).{0,40}(?:confirm|contradict|establish|authoritative)|"
    r"(?:confirm|contradict|establish|authoritative).{0,40}(?:old[\s_]?account|J\.\s*Reyes.{0,20}Developer|sidebar)",
    re.IGNORECASE | re.DOTALL,
)


def _iter_tool_calls(obj: dict):
    """Yield (name, args_dict) for every tool call in a session event.

    Tolerates the three real-world shapes:
      1. Flat OpenAI-style:  {"role":"assistant","tool_calls":[{"name","arguments":{...}}]}
      2. function-nested:    {"tool_calls":[{"function":{"name","arguments":...}}]}
      3. Anthropic content-block: {"content":[{"type":"tool_use","name","input":{...}}]}
    Plus the legacy top-level {"type"/"tool":"CreateSubagent", ...} shape.
    ``arguments`` may be a dict or a JSON string; ``input`` is the content-block form.
    The CreateSubagent ``model_key`` lives inside the arguments object, not on the call.
    """
    top_name = obj.get("type") or obj.get("tool") or obj.get("name") or ""
    if isinstance(top_name, str) and top_name:
        yield top_name, obj

    for call in obj.get("tool_calls") or obj.get("calls") or []:
        if not isinstance(call, dict):
            continue
        name = call.get("name") or (call.get("function") or {}).get("name", "")
        args = call.get("arguments")
        if args is None:
            args = (call.get("function") or {}).get("arguments")
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except json.JSONDecodeError:
                args = {}
        if not isinstance(args, dict):
            args = {}
        yield str(name or ""), args

    content = obj.get("content")
    if isinstance(content, list):
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") != "tool_use":
                continue
            name = block.get("name", "")
            args = block.get("input")
            if not isinstance(args, dict):
                args = {}
            yield str(name or ""), args


def _check_vlm_session(ws: Path) -> bool:
    """Return True if a vlm CreateSubagent call appears in sessions/main.jsonl."""
    sessions_dir = ws / "sessions"
    jsonl_path = sessions_dir / "main.jsonl"
    if not jsonl_path.exists():
        return True  # cannot verify; skip warn

    try:
        lines = jsonl_path.read_text(encoding="utf-8", errors="replace").splitlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(obj, dict):
                continue
            for name, args in _iter_tool_calls(obj):
                if "CreateSubagent" not in name:
                    continue
                model_key = str(args.get("model_key") or args.get("model") or "")
                if "vlm" in model_key.lower():
                    return True
    except OSError:
        pass
    return False


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q2.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    target = ws / "output" / "linkedin_date_check.md"

    if not target.exists():
        print("FAIL: output/linkedin_date_check.md does not exist")
        return 1

    content = target.read_text(encoding="utf-8")
    raw_bytes = content.encode("utf-8")
    errors: list[str] = []

    # Layer 1: structure
    if len(raw_bytes) < 300:
        errors.append(
            f"output/linkedin_date_check.md too short ({len(raw_bytes)} bytes; need >= 300)"
        )
    if not HELIOS_RE.search(content):
        errors.append("'Helios Cloud' not mentioned in output/linkedin_date_check.md")
    if not STRATUM_RE.search(content):
        errors.append("'Stratum Labs' not mentioned in output/linkedin_date_check.md")

    # Layer 2: field presence
    if not HELIOS_LINKEDIN_END_RE.search(content):
        errors.append(
            "LinkedIn Helios Cloud end date 'Oct 2022' not found — "
            "must be extracted from the PNG image by a vlm subagent"
        )
    if not HELIOS_RESUME_END_RE.search(content):
        errors.append(
            "resume Helios Cloud end date 'Aug 2022' not found in output/linkedin_date_check.md"
        )
    if not DISCREPANCY_RE.search(content):
        errors.append(
            "no discrepancy word found (discrepancy / mismatch / differ / conflict / gap) — "
            "the 2-month Helios Cloud end date difference must be explicitly flagged"
        )
    if not STRATUM_START_RE.search(content):
        errors.append(
            "Stratum Labs start date (Sep 2022 / 2022-09) not found in output/linkedin_date_check.md"
        )
    if not STRATUM_END_RE.search(content):
        errors.append(
            "Stratum Labs end date (Nov 2025 / 2025-11) not found in output/linkedin_date_check.md"
        )

    # Layer 3: decoy guards
    if OLD_ACCOUNT_AUTHORITATIVE_RE.search(content):
        errors.append(
            "HARD-FAIL (decoy contamination): agent treated the old account thumbnail "
            "(linkedin_old_account_preview.png) as authoritative LinkedIn data — "
            "that image carries no employment dates and must not be used to confirm or "
            "contradict the primary profile"
        )

    # VLM sourcing check (advisory only, non-gating)
    if HELIOS_LINKEDIN_END_RE.search(content) and not _check_vlm_session(ws):
        print(
            "NOTE: modality subagent delegation not verified — advisory only, non-gating",
            file=sys.stderr,
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        f"PASS: output/linkedin_date_check.md ({len(raw_bytes)} bytes) records "
        "LinkedIn Helios Cloud end date Oct 2022, resume end date Aug 2022, "
        "Stratum Labs dates Sep 2022 – Nov 2025, discrepancy flagged; "
        "no authoritative old-account contamination"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
