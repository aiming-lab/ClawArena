#!/usr/bin/env python3
"""check_q4.py — Validate q4: reference call arbitration report.

C9 modality-mismatch trap: ref_call_transcript_auto.md omits "plan" from
"performance improvement plan" and drops the PIP/resignation context entirely.
An agent that reads the transcript instead of dispatching an omni subagent to
the audio will miss the critical PIP finding and fail this check.

Ground truth (from audio files — omni subagent required):
  REF_PERSON_1 (Alex Drummond), segment 3:
    "I believe it was late October 2022. Maybe the twenty-fourth or twenty-fifth."
    → Helios Cloud end date: "late October 2022" (confirms LinkedIn, contradicts resume Aug 2022)
    → "Jordan left on good terms" — no elaboration on departure reason.
  REF_PERSON_1, segment 2:
    "I'm not in a position to comment on the specifics of that project."
    → Non-committal / no-comment response.
  REF_PERSON_2 (Sam Okafor), segment 3 (2:20–4:00) — CRITICAL SEGMENT:
    "there was a performance improvement plan. Jordan was put on a PIP by the
     engineering manager in August 2025. And then Jordan resigned in November
     rather than go through the full PIP process."
    → PIP initiated August 2025; Jordan resigned November 2025 rather than completing PIP.
    → This fact is NOT in any text file in the initial workspace.

Cross-round consistency requirement:
  output/linkedin_date_check.md (q2) must contain "Oct 2022".
  output/reference_findings.md must also reference "Oct 2022" — confirming the same
  Helios Cloud end date discrepancy from two independent sources.

Pass conditions (all must hold; exit 0):
  Layer 1 — Structure:
    1. output/reference_findings.md exists.
    2. >= 600 bytes.
    3. >= 6 distinct sections or list items.
    4. Mentions both "Alex Drummond" (or "REF_PERSON_1") and "Sam Okafor" (or "REF_PERSON_2").
  Layer 2 — Field presence (key facts from audio):
    5. REF_PERSON_1 Helios Cloud end date: "late Oct" / "October 2022" / "Oct 2022".
    6. REF_PERSON_1 non-response: "not in a position" / "no comment" / "decline" / "couldn't comment".
    7. REF_PERSON_2 PIP finding: "Performance Improvement Plan" or "PIP" — modality-locked.
    8. REF_PERSON_2 resignation context: "resign" near "PIP" or "rather than" near "PIP".
  Layer 3 — Sourcing and cross-round guards:
    9. ADVISORY ONLY (non-gating): omni subagent appears in sessions/main.jsonl.
   10. Cross-round: output/linkedin_date_check.md must exist and contain "Oct 2022";
       output/reference_findings.md must also contain "Oct 2022".
   11. Transcript-reliance guard: if PIP is ABSENT and transcript is cited as source,
       hard-fail with C9 modality-mismatch diagnosis.

Usage: python check_q4.py <workspace_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


LIST_ITEM_OR_HEADER_RE = re.compile(
    r"^\s*(?:[-*•]|\d+[.):]|#{1,4}\s)\s*\S", re.MULTILINE
)

REF1_NAME_RE = re.compile(r"[Aa]lex\s+[Dd]rummond|REF_PERSON_1", re.IGNORECASE)
REF2_NAME_RE = re.compile(r"[Ss]am\s+[Oo]kafor|REF_PERSON_2", re.IGNORECASE)

# REF_PERSON_1 Helios end date — tolerates line-wrapping via re.DOTALL on spans
REF1_HELIOS_DATE_RE = re.compile(
    r"[Ll]ate[\s\n]+[Oo]ct(?:ober)?|"
    r"[Oo]ct(?:ober)?[\s\n]+2022|"
    r"2022-10",
    re.IGNORECASE,
)

# REF_PERSON_1 non-committal response
REF1_NO_COMMENT_RE = re.compile(
    r"not\s+in\s+a\s+position|no[\s-]?comment|declin|couldn.{0,4}t\s+comment|"
    r"can.{0,4}t\s+speak|not\s+able\s+to\s+comment",
    re.IGNORECASE,
)

# REF_PERSON_2 PIP finding — the modality-locked critical fact
PIP_RE = re.compile(
    r"[Pp]erformance\s+[Ii]mprovement\s+[Pp]lan|"
    r"\bPIP\b",
)

# REF_PERSON_2 resignation context — regex tolerates line-wrapping with DOTALL
RESIGN_CONTEXT_RE = re.compile(
    r"resign.{0,120}(?:PIP|performance\s+improvement)|"
    r"(?:PIP|performance\s+improvement).{0,120}resign|"
    r"rather\s+than.{0,60}(?:PIP|complet|process)|"
    r"(?:PIP|complet|process).{0,60}rather\s+than",
    re.IGNORECASE | re.DOTALL,
)

# Auto-transcript as the stated source
TRANSCRIPT_SOURCE_RE = re.compile(
    r"transcript|auto[\s-]?generat|ref_call_transcript",
    re.IGNORECASE,
)

# Oct 2022 cross-round concordance
OCT_2022_RE = re.compile(r"[Oo]ct(?:ober)?\s+2022|2022-10", re.IGNORECASE)


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


def _check_omni_session(ws: Path) -> bool:
    """Return True if an omni CreateSubagent call appears in sessions/main.jsonl."""
    sessions_dir = ws / "sessions"
    jsonl_path = sessions_dir / "main.jsonl"
    if not jsonl_path.exists():
        print(
            f"[warn] sessions/main.jsonl not found at {jsonl_path} — "
            "skipping omni subagent presence check",
            file=sys.stderr,
        )
        return True  # cannot enforce; give benefit of the doubt

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
                model = str(args.get("model_key") or args.get("model") or "")
                if "omni" in model.lower():
                    return True
    except OSError as e:
        print(f"[warn] could not read sessions/main.jsonl: {e}", file=sys.stderr)

    return False


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q4.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    target = ws / "output" / "reference_findings.md"

    if not target.exists():
        print("FAIL: output/reference_findings.md does not exist")
        return 1

    content = target.read_text(encoding="utf-8")
    raw_bytes = content.encode("utf-8")
    errors: list[str] = []

    # Layer 1: structure
    if len(raw_bytes) < 600:
        errors.append(
            f"output/reference_findings.md too short ({len(raw_bytes)} bytes; need >= 600)"
        )

    items = LIST_ITEM_OR_HEADER_RE.findall(content)
    if len(items) < 6:
        errors.append(
            f"found only {len(items)} section headers or list item(s); need >= 6 "
            "(report should cover both references with separate subsections)"
        )

    if not REF1_NAME_RE.search(content):
        errors.append(
            "'Alex Drummond' or 'REF_PERSON_1' not mentioned in output/reference_findings.md"
        )
    if not REF2_NAME_RE.search(content):
        errors.append(
            "'Sam Okafor' or 'REF_PERSON_2' not mentioned in output/reference_findings.md"
        )

    # Layer 2: key audio facts
    if not REF1_HELIOS_DATE_RE.search(content):
        errors.append(
            "REF_PERSON_1 (Alex Drummond) Helios Cloud end date not found — "
            "audio segment 3 states 'late October 2022'; this must appear in the report "
            "(regex accepts 'late Oct', 'October 2022', '2022-10')"
        )

    if not REF1_NO_COMMENT_RE.search(content):
        errors.append(
            "REF_PERSON_1 non-committal response not documented — "
            "audio segment 2: 'not in a position to comment on specifics of that project'"
        )

    has_pip = PIP_RE.search(content) is not None
    if not has_pip:
        errors.append(
            "HARD-FAIL (modality-locked fact missing): 'Performance Improvement Plan' or "
            "'PIP' not found in output/reference_findings.md — "
            "this critical finding is ONLY in ref_call_sam_okafor.wav audio segment 3 "
            "(2:20–4:00); an agent using the auto-transcript will miss it"
        )

    if not RESIGN_CONTEXT_RE.search(content):
        errors.append(
            "REF_PERSON_2 resignation context not documented — "
            "audio segment 3: Jordan 'resigned in November rather than go through the "
            "full PIP process'; the report must connect the resignation to the PIP "
            "(regex looks for 'resign' near 'PIP' or 'rather than' near 'PIP/complet')"
        )

    # Layer 3a: omni subagent sourcing check (advisory only, non-gating)
    if not _check_omni_session(ws):
        print(
            "NOTE: modality subagent delegation not verified — advisory only, non-gating",
            file=sys.stderr,
        )

    # Layer 3b: transcript-reliance guard (if PIP missing and transcript cited as source)
    if not has_pip and TRANSCRIPT_SOURCE_RE.search(content):
        errors.append(
            "C9 MODALITY-MISMATCH: output/reference_findings.md cites the auto-transcript "
            "as a source but is missing the PIP finding — the auto-transcript omits 'plan' "
            "from 'performance improvement plan' and drops the PIP/resignation context; "
            "the audio recording is the authoritative source"
        )

    # Layer 3c: cross-round consistency
    linkedin_check = ws / "output" / "linkedin_date_check.md"
    if linkedin_check.exists():
        lc_content = linkedin_check.read_text(encoding="utf-8")
        if not OCT_2022_RE.search(lc_content):
            errors.append(
                "cross-round failure: output/linkedin_date_check.md (q2) does not "
                "contain 'Oct 2022' — q2 should have established the LinkedIn Helios "
                "end date before q4 attempts to confirm it via REF_PERSON_1 audio"
            )
        elif not OCT_2022_RE.search(content):
            errors.append(
                "cross-round failure: output/linkedin_date_check.md contains 'Oct 2022' "
                "but output/reference_findings.md does not — REF_PERSON_1 audio confirms "
                "this same date and it must appear in both documents for concordance"
            )
    else:
        errors.append(
            "cross-round failure: output/linkedin_date_check.md (q2) does not exist — "
            "complete q2 before q4 to establish the Helios Cloud end date baseline"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        f"PASS: output/reference_findings.md ({len(raw_bytes)} bytes) captures "
        "REF_PERSON_1 late October 2022 Helios date and non-response, "
        "REF_PERSON_2 PIP disclosure and resignation context (audio segment 3), "
        "cross-round Oct 2022 concordance confirmed"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
