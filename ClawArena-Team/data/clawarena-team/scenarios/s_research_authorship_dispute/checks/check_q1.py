"""check_q1.py — Verify output/dispute_triage.md covers all three dispute items,
the arbitration deadline, and the deliverable set.

Pass conditions (all must hold; exit 0):

  1. output/dispute_triage.md exists and is >= 300 bytes.
  2. The file contains >= 3 distinct numbered or bulleted list items.
  3. All three dispute items are matched by their respective regexes:
       - Dispute 1 (authorship credit): first-author / corresponding-author mention.
       - Dispute 2 (unauthorized dataset use): Clause 4.2 / harmonized_gwas / consent mention.
       - Dispute 3 (git integrity): amended commit / git log / tamper mention.
  4. Deadline is mentioned: 72 hours from 2026-05-15 = 2026-05-18.
  5. Decoy contamination guard: file must not cite the retracted bioRxiv preprint
     (preprint_v0 / bioRxiv.*2025-01 / "retracted" in a factual-assertion context).

Usage:
    python checks/check_q1.py <workspace_path>

Exit 0 on pass, 1 on failure.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Minimum file size in bytes.
MIN_BYTES = 300

# Minimum numbered/bulleted list items.
MIN_BULLETS = 3

# Field-layer regexes (case-insensitive).
DISPUTE_ITEM_PATTERNS: list[tuple[str, str]] = [
    (
        "Dispute item 1 (authorship credit)",
        r"first.?author|corresponding.?author|authorship|credit",
    ),
    (
        "Dispute item 2 (unauthorized dataset use)",
        r"unauthorized|consent|harmonized_gwas|dataset.*use|use.*dataset|Clause\s*4\.2",
    ),
    (
        "Dispute item 3 (git history integrity)",
        r"amend|git.*log|commit.*author|author.*commit|history|tamper|red\s*herring",
    ),
]

DEADLINE_PATTERN = re.compile(r"72\s*hour|2026-05-18|May\s+18", re.IGNORECASE)

# Decoy contamination: retracted preprint.
DECOY_PATTERN = re.compile(r"preprint_v0|bioRxiv.*2025-01|retract", re.IGNORECASE)

# Flag/exclude context: q1 explicitly asks the triage note to list the evidence
# sources cited as conflicting, and arbitration_brief.md §3 NOTE names the
# retracted bioRxiv preprint as a source that must NOT be used. A correct answer
# therefore must mention the preprint precisely in order to flag/exclude it.
# A DECOY_PATTERN hit is only a contamination violation when it is NOT in such a
# flag/exclude context (within 120 chars on either side of the match).
# NOTE: 'retract'/'withdrawn' are intentionally NOT cues here — they are the
# decoy terms themselves. A genuine flag/exclude context requires an explicit
# exclusion/conflict verb so that an *affirmative* reliance on the retracted
# preprint (e.g. "per the retracted preprint, PI_X is first author") still fails.
DECOY_FLAG_CONTEXT = re.compile(
    r"must\s+not|not\s+be?\s+used|do\s+not\s+use|cannot\s+be\s+used"
    r"|excluded?|exclud|disregard|ignore[d]?|conflict|red\s*herring|flag"
    r"|outdated|obsolete|superseded?|invalid|tainted|contaminat|decoy"
    r"|withdraw\w*\s|set\s+aside|not\s+rely|should\s+not",
    re.IGNORECASE,
)


def _decoy_contamination(text: str) -> bool:
    """Return True only if a DECOY_PATTERN match lacks a flag/exclude context
    nearby (within 120 chars). Naming the retracted preprint to flag it as a
    conflicting/excluded source is allowed and required by the q1 prompt; an
    affirmative reliance on it (no exclusion cue nearby) still fails."""
    for m in DECOY_PATTERN.finditer(text):
        start = max(0, m.start() - 120)
        end = min(len(text), m.end() + 120)
        window = text[start:end]
        if DECOY_FLAG_CONTEXT.search(window):
            continue
        return True
    return False


def _count_bullet_lines(text: str) -> int:
    """Count lines that begin with a bullet or ordinal marker."""
    count = 0
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and re.match(r"^[-*•]|^\d+[.)]\s", stripped):
            count += 1
    return count


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: check_q1.py <workspace>")
        return 1

    ws = Path(sys.argv[1])
    triage_path = ws / "output" / "dispute_triage.md"

    if not triage_path.exists():
        print(f"FAIL: {triage_path} does not exist")
        return 1

    text = triage_path.read_text(encoding="utf-8")
    failures: list[str] = []

    # 1. Minimum size.
    if len(text.encode()) < MIN_BYTES:
        failures.append(
            f"dispute_triage.md is too short ({len(text.encode())} bytes; need >= {MIN_BYTES})"
        )

    # 2. Minimum bullet/numbered items.
    bullet_count = _count_bullet_lines(text)
    if bullet_count < MIN_BULLETS:
        failures.append(
            f"dispute_triage.md has only {bullet_count} bullet/numbered lines "
            f"(need >= {MIN_BULLETS}); each dispute item must be a separate entry"
        )

    # 3. Dispute item coverage.
    for label, pattern in DISPUTE_ITEM_PATTERNS:
        if not re.search(pattern, text, re.IGNORECASE):
            failures.append(
                f"{label}: not found — regex r'{pattern}' matched nothing in the file"
            )

    # 4. Deadline.
    if not DEADLINE_PATTERN.search(text):
        failures.append(
            "Deadline (72 hours / 2026-05-18 / May 18) not mentioned in dispute_triage.md"
        )

    # 5. Decoy contamination guard.
    #    Flag/exclude exception: the q1 prompt asks for the conflicting evidence
    #    sources, and arbitration_brief.md §3 NOTE names the retracted bioRxiv
    #    preprint as a source that must NOT be used. Naming it to flag/exclude it
    #    is allowed; only an affirmative reliance (no exclusion cue nearby) fails.
    if _decoy_contamination(text):
        failures.append(
            "FAIL: dispute_triage.md appears to rely on the retracted bioRxiv preprint "
            "(matches r'preprint_v0|bioRxiv.*2025-01|retract') without flagging it as "
            "excluded/conflicting. Do not use the withdrawn preprint for factual claims; "
            "if you mention it, do so only to flag it as a source that must not be used."
        )

    if failures:
        print("FAIL: check_q1 — dispute_triage.md failed one or more checks:")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(
        f"PASS: check_q1 — dispute_triage.md covers all 3 dispute items, "
        f"deadline 2026-05-18, and has {bullet_count} bullet/numbered entries"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
