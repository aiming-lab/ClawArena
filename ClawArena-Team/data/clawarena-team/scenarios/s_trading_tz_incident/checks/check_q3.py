"""check_q3.py — Verify output/root_cause_analysis.md isolates the correct
matching-engine root-cause event and discredits the decoy events.

Ground truth:
  Root-cause event : 2026-03-27T17:23:09Z  (in matching_2026-03-27_part2.log)
  Adapter          : dispatch_adapter  (NOT test_dispatch_adapter)
  Config field     : tz_offset_applied
  Old value        : "+00:00"
  New (wrong) value: "+08:00"
  Build ID         : BUILD-20260327-0041

  Decoy event 1    : 2026-03-27T10:42:17Z — test_dispatch_adapter; must be
                     discredited if mentioned
  Decoy event 2    : 2026-03-27T11:05:44Z — test_dispatch_adapter; must be
                     discredited if mentioned

Pass conditions (all must hold):

1. File exists; >= 600 bytes; >= 4 labeled sections or fields.
2. Root-cause timestamp present:
     r"2026-03-27T17:23:09Z|17:23:09\\s*UTC"
3. Config field present: r"tz_offset_applied"
4. Both offset values present: r"\\+08:00" AND r"\\+00:00"
5. Build ID present: r"BUILD-20260327-0041"
6. Production adapter named: "dispatch_adapter" appears (must not be
   exclusively prefixed by "test_"; see logic below).
7. Decoy discredit: if 10:42:17 or 11:05:44 appear, each must be
   accompanied within 500 chars by discredit language confirming it
   affects the test adapter, not production.
8. Cleared hypothesis: the initial Slack hypothesis (clearing-side DST)
   must be addressed — at least one of: MATCHING_ENG_LEAD / Damian /
   initial hypothesis / clearing.*not / not.*clearing / wrong.*hypothesis.
9. Anti-archive: file must NOT contain "MIG-" or "migration.*root" or
   "root.*migration" in context of the current incident.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT_CAUSE_TS_RE = re.compile(
    r"2026-03-27T17:23:09Z|17:23:09\s*UTC",
    re.IGNORECASE,
)

TZ_FIELD_RE = re.compile(r"tz_offset_applied", re.IGNORECASE)

WRONG_OFFSET_RE = re.compile(r"\+08:00")
CORRECT_OFFSET_RE = re.compile(r"\+00:00")

BUILD_ID_RE = re.compile(r"BUILD-20260327-0041")

# Production adapter: "dispatch_adapter" must appear without always being preceded by "test_"
PROD_ADAPTER_RE = re.compile(r"dispatch_adapter", re.IGNORECASE)
TEST_ADAPTER_RE = re.compile(r"test_dispatch_adapter", re.IGNORECASE)

DECOY_TS_1 = re.compile(r"10:42:17")
DECOY_TS_2 = re.compile(r"11:05:44")

DECOY_DISCREDIT_RE = re.compile(
    r"test.{0,20}adapter|not.{0,20}root|decoy|not.{0,20}production|"
    r"production.{0,20}dispatch|test.only|not.{0,20}cause|test_dispatch_adapter",
    re.IGNORECASE,
)

HYPOTHESIS_RE = re.compile(
    r"MATCHING_ENG_LEAD|Damian|initial.{0,20}hypothesis|"
    r"clearing.{0,20}(?:not|wrong|incorrect)|(?:not|wrong|incorrect).{0,20}clearing|"
    r"wrong.{0,20}hypothesis|hypothesis.{0,20}wrong|clearing.side",
    re.IGNORECASE,
)

ARCHIVE_CONTAMINATION_RE = re.compile(
    r"MIG-|migration.{0,20}root.cause|root.cause.{0,20}migration",
    re.IGNORECASE,
)

MIN_BYTES = 600
MIN_SECTIONS = 4


def _count_sections(text: str) -> int:
    count = 0
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r"^#{1,4}\s+\S", stripped):
            count += 1
        elif re.match(r"^[-*]\s+\S.{10,}", stripped):
            count += 1
        elif re.match(r"^\*\*[^*]+\*\*\s*:", stripped):
            count += 1
        elif ":" in stripped and len(stripped) > 10 and stripped[0].isupper():
            count += 1
    return count


def _decoy_discredited_near(text: str, decoy_re: re.Pattern) -> bool:
    """Return True if every occurrence of the decoy timestamp is accompanied
    by discredit language within 500 characters (before or after)."""
    idx = 0
    found = False
    while True:
        m = decoy_re.search(text, idx)
        if not m:
            break
        found = True
        start = max(0, m.start() - 500)
        end = min(len(text), m.end() + 500)
        window = text[start:end]
        if not DECOY_DISCREDIT_RE.search(window):
            return False
        idx = m.end()
    # If never found, return True (no mention = no problem)
    return True


def _production_adapter_present(text: str) -> bool:
    """Return True if 'dispatch_adapter' appears in a context that is NOT
    exclusively 'test_dispatch_adapter' (i.e., the production adapter is named)."""
    # Find all occurrences of dispatch_adapter
    for m in PROD_ADAPTER_RE.finditer(text):
        # Check the 15 characters before to see if it's prefixed by "test_"
        prefix_start = max(0, m.start() - 5)
        prefix = text[prefix_start:m.start()]
        if "test_" not in prefix:
            return True
    return False


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q3.py <workspace>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    note = ws / "output" / "root_cause_analysis.md"
    if not note.exists():
        print(f"FAIL: {note} does not exist")
        return 1

    text = note.read_text(encoding="utf-8")
    raw_bytes = len(note.read_bytes())
    errors: list[str] = []

    # 1. Size and structure
    if raw_bytes < MIN_BYTES:
        errors.append(
            f"root_cause_analysis.md is too short ({raw_bytes} bytes; minimum {MIN_BYTES})"
        )

    sections = _count_sections(text)
    if sections < MIN_SECTIONS:
        errors.append(
            f"root_cause_analysis.md has only {sections} labeled section(s); "
            f"need >= {MIN_SECTIONS} distinct fields or headings"
        )

    # 2. Root-cause timestamp
    if not ROOT_CAUSE_TS_RE.search(text):
        errors.append(
            "missing root-cause timestamp '2026-03-27T17:23:09Z' — the actual "
            "CONFIG_RELOAD event is in matching_2026-03-27_part2.log (15:00–23:00 UTC); "
            "dispatching only to part1 will miss it and incorrectly name 10:42:17 as root cause"
        )

    # 3. Config field
    if not TZ_FIELD_RE.search(text):
        errors.append(
            "missing config field name 'tz_offset_applied' — this is the field changed "
            "by the CONFIG_RELOAD event at 17:23:09 UTC"
        )

    # 4. Both offset values
    if not WRONG_OFFSET_RE.search(text):
        errors.append(
            "missing wrong offset value '+08:00' — the CONFIG_RELOAD set "
            "tz_offset_applied to '+08:00', causing dispatch timestamps to carry SGT offset"
        )
    if not CORRECT_OFFSET_RE.search(text):
        errors.append(
            "missing correct offset value '+00:00' — the previous correct value of "
            "tz_offset_applied was '+00:00' (UTC)"
        )

    # 5. Build ID
    if not BUILD_ID_RE.search(text):
        errors.append(
            "missing build ID 'BUILD-20260327-0041' — this identifies the automated "
            "deploy that triggered the misconfiguration"
        )

    # 6. Production adapter named
    if not _production_adapter_present(text):
        errors.append(
            "production adapter 'dispatch_adapter' (without 'test_' prefix) does not "
            "appear as the affected adapter — the root cause affects the production "
            "dispatch_adapter, not test_dispatch_adapter"
        )

    # 7. Decoy discredit
    if not _decoy_discredited_near(text, DECOY_TS_1):
        errors.append(
            "timestamp '10:42:17' appears without being discredited within 500 chars "
            "— this event in part1 affects test_dispatch_adapter and is NOT the root "
            "cause; the file must explain why it is a decoy"
        )
    if not _decoy_discredited_near(text, DECOY_TS_2):
        errors.append(
            "timestamp '11:05:44' appears without being discredited within 500 chars "
            "— this event in part1 is a corrective reload on test_dispatch_adapter and "
            "is NOT the root cause; the file must explain why it is a decoy"
        )

    # 8. Cleared hypothesis
    if not HYPOTHESIS_RE.search(text):
        errors.append(
            "missing acknowledgement that MATCHING_ENG_LEAD's initial hypothesis "
            "(clearing-side DST misconfiguration) is incorrect — the root cause is "
            "on the FinClear Asia dispatch adapter side, not ClearRoute EU's clearing system"
        )

    # 9. Anti-archive contamination
    m = ARCHIVE_CONTAMINATION_RE.search(text)
    if m:
        errors.append(
            f"archive contamination detected ('{m.group()}') — the analysis must not "
            "reference _archive/migration_jan_2026/ content as part of the root cause"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        "PASS: root_cause_analysis.md identifies 2026-03-27T17:23:09Z CONFIG_RELOAD "
        "on dispatch_adapter, tz_offset_applied +00:00→+08:00, BUILD-20260327-0041, "
        "discredits both decoy events, and corrects the initial clearing-side hypothesis"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
