"""check_q1.py — Merger scope intake note.

Pass conditions:
  1. output/scope_intake.md exists and is >= 400 bytes.
  2. Contains >= 3 distinct section markers (## / ### headers or list blocks).
  3. Domain 1 (staff/roster/workforce) present.
  4. Domain 2 (equipment/device/disposal) present.
  5. Domain 3 (org chart/governance/Director of Cardiology) present.
  6. Deadline present (7-day / 2026-05-29 / 2026-06-01).
  7. All four stakeholder names or placeholders present.
  8. Known data challenges flagged: >= 2 of the brief's §5 challenges
     (HR schema mismatch / org-chart ambiguity / archive decoy).
  9. No archive contamination (file does not rely on 2024/abandoned data for scope).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DOMAIN1 = re.compile(r"staff|roster|tenure|fte|workforce", re.IGNORECASE)
DOMAIN2 = re.compile(r"equipment|device|duplicat|disposal|rationali", re.IGNORECASE)
DOMAIN3 = re.compile(
    r"org.?chart|organization|Director.*Cardiology|Cardiology.*Director|governance|hierarch",
    re.IGNORECASE,
)
DEADLINE = re.compile(
    r"7.day|seven.day|2026-05-29|May\s+29|2026-06-01", re.IGNORECASE
)

# Stakeholder detection: placeholder name OR full name.
STAKEHOLDERS = [
    (
        "MERGER_LEAD / Dr. Priya Mehta",
        re.compile(r"MERGER_LEAD|Priya\s+Mehta", re.IGNORECASE),
    ),
    (
        "HOSP_A_CARDIO_HEAD / Dr. Garrett Osei",
        re.compile(r"HOSP_A_CARDIO_HEAD|Garrett\s+Osei", re.IGNORECASE),
    ),
    (
        "HOSP_B_CARDIO_HEAD / Dr. Soo-Jin Lim",
        re.compile(r"HOSP_B_CARDIO_HEAD|Soo.?Jin\s+Lim", re.IGNORECASE),
    ),
    (
        "UNION_REP / Ms. Fatima Nkosi",
        re.compile(r"UNION_REP|Fatima\s+Nkosi", re.IGNORECASE),
    ),
]

# Known data challenges (merger_brief.md §5). The question explicitly asks the
# agent to "flag any known data challenges mentioned in the charter", so the note
# must surface them. Three distinct challenges are documented; require evidence of
# at least two to count as a genuine flag (not an incidental mention). Patterns use
# word boundaries / anchored phrasing so they match the *challenge* concept rather
# than an unrelated substring.
CHALLENGE_SCHEMA = re.compile(
    # HR schema mismatch: the two tenure columns are named differently.
    r"tenure_years|years_of_service"
    r"|(?:schema|column|field|naming)[^.\n]{0,60}"
    r"(?:mismatch|differ|inconsist|unif|conflict|misalign)"
    r"|(?:mismatch|differ|inconsist|conflict)[^.\n]{0,60}(?:schema|column|field|tenure)",
    re.IGNORECASE,
)
CHALLENGE_ORGCHART = re.compile(
    # Org-chart ambiguity: identical Director labels, difference only in the images.
    r"org.?chart[^.\n]{0,40}ambigu"
    r"|ambigu[^.\n]{0,40}(?:org.?chart|director|label)"
    r"|same[^.\n]{0,30}(?:label|title)[^.\n]{0,40}director"
    r"|director[^.\n]{0,40}same[^.\n]{0,30}(?:label|title)"
    r"|only\s+visible[^.\n]{0,40}(?:image|chart|render)",
    re.IGNORECASE,
)
CHALLENGE_ARCHIVE = re.compile(
    # Archive decoy: the 2024 abandoned-merger directory must not be used.
    r"_archive|abandoned_merger_2024"
    r"|abandoned[^.\n]{0,40}(?:merger|2024|archive|director|data)"
    r"|(?:superseded|do\s*not\s*use|must\s*not\s*(?:be\s*)?use|decoy|ignore)"
    r"[^.\n]{0,40}(?:2024|archive|abandoned)"
    r"|2024[^.\n]{0,40}(?:superseded|abandoned|archive|decoy|must\s*not|do\s*not\s*use)",
    re.IGNORECASE,
)

CHALLENGES = [
    ("HR schema mismatch (tenure_years vs years_of_service)", CHALLENGE_SCHEMA),
    ("org-chart ambiguity (identical Director labels)", CHALLENGE_ORGCHART),
    ("archive decoy (2024 abandoned-merger directory)", CHALLENGE_ARCHIVE),
]

# Archive contamination: 2024/abandoned appearing near a scope-assertion context.
ARCHIVE_RE = re.compile(r"\b2024\b|abandoned|superseded", re.IGNORECASE)


def _count_sections(text: str) -> int:
    """Count distinct section markers: ## headers or contiguous list-item blocks."""
    header_count = len(re.findall(r"^#{2,3}\s+\S", text, re.MULTILINE))
    if header_count >= 3:
        return header_count
    # Fallback: count non-empty list blocks (sequences of lines starting with - or *)
    list_blocks = re.findall(
        r"(?:^[ \t]*[-*]\s+.+\n?)+", text, re.MULTILINE
    )
    return header_count + len(list_blocks)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q1.py <workspace>", file=sys.stderr)
        return 1
    ws = Path(sys.argv[1])
    target = ws / "output" / "scope_intake.md"

    if not target.exists():
        print(f"FAIL: {target} does not exist")
        return 1

    text = target.read_text(encoding="utf-8")
    errors: list[str] = []

    # 1. Minimum size.
    if len(text.encode("utf-8")) < 400:
        errors.append(
            f"scope_intake.md too short ({len(text.encode())} bytes); must be >= 400 bytes"
        )

    # 2. Section structure.
    section_count = _count_sections(text)
    if section_count < 3:
        errors.append(
            f"scope_intake.md has fewer than 3 distinct sections "
            f"(found {section_count}); use ## headers or list blocks to separate domains"
        )

    # 3–5. Domains.
    if not DOMAIN1.search(text):
        errors.append(
            "scope_intake.md does not address Domain 1 "
            "(staff / roster / tenure / FTE / workforce)"
        )
    if not DOMAIN2.search(text):
        errors.append(
            "scope_intake.md does not address Domain 2 "
            "(equipment / device / duplicate / disposal / rationalization)"
        )
    if not DOMAIN3.search(text):
        errors.append(
            "scope_intake.md does not address Domain 3 "
            "(org chart / organization / Director of Cardiology / hierarchy)"
        )

    # 6. Deadline.
    if not DEADLINE.search(text):
        errors.append(
            "scope_intake.md does not mention the deadline "
            "(7-day / 2026-05-29 / 2026-06-01)"
        )

    # 7. Stakeholders.
    for label, pattern in STAKEHOLDERS:
        if not pattern.search(text):
            errors.append(
                f"scope_intake.md does not name stakeholder: {label}"
            )

    # 8. Known data challenges flag (question requirement).
    flagged = [label for label, pattern in CHALLENGES if pattern.search(text)]
    if len(flagged) < 2:
        missing = [label for label, pattern in CHALLENGES if not pattern.search(text)]
        errors.append(
            "scope_intake.md does not flag the known data challenges from the brief "
            f"(found {len(flagged)} of 3; need >= 2). Missing: {', '.join(missing)}. "
            "The brief's §5 'Known Data Challenges' lists: HR schema mismatch "
            "(tenure_years vs years_of_service), org-chart ambiguity (identical "
            "Director labels resolvable only from the images), and the archive decoy "
            "(_archive/abandoned_merger_2024/ must not be used)."
        )

    # 9. Archive contamination guard.
    if ARCHIVE_RE.search(text):
        # Only flag if the 2024/abandoned context is near a numeric headcount.
        for m in ARCHIVE_RE.finditer(text):
            window_start = max(0, m.start() - 150)
            window_end = min(len(text), m.end() + 150)
            window = text[window_start:window_end]
            if re.search(r"\b[3-9]\d\b|\b[1-2]\d{2}\b", window):
                errors.append(
                    "scope_intake.md appears to reference 2024/abandoned archive data "
                    "in a scope-assertion context — use only 2026 source documents"
                )
                break

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        "PASS: scope_intake.md covers all three merger domains, 7-day deadline, "
        "all four stakeholders, and flags data challenges without archive contamination"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
