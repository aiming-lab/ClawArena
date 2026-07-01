"""check_q3.py — Org chart PNG hierarchy extraction.

Ground truth (sourced only from rendered PNG images — no text file states these facts):
  Hospital A: Dr. Garrett Osei (HOSP_A_CARDIO_HEAD), Director of Cardiology,
              2 hops from CMO (CMO -> Director directly).
  Hospital B: Dr. Soo-Jin Lim (HOSP_B_CARDIO_HEAD), Director of Cardiology,
              3 hops from CMO (CMO -> Chief of Medicine -> Director).

Pass conditions:
  output/org_chart_analysis.md
    1. Exists; >= 400 bytes; two named sections (one per hospital).
    2. HOSP_A_CARDIO_HEAD name present (Garrett Osei or placeholder).
    3. HOSP_B_CARDIO_HEAD name present (Soo-Jin Lim or placeholder).
    4. Hospital A depth: 2 hops / direct / reports to CMO.
    5. Hospital B depth: 3 hops / Chief of Medicine as intermediate.
    6. Structural comparison note present.
    7. Anti-decoy: no cross-contamination from clinical_trial_audit content.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HOSP_A_NAME = re.compile(r"Garrett\s+Osei|HOSP_A_CARDIO_HEAD", re.IGNORECASE)
HOSP_B_NAME = re.compile(r"Soo.?Jin\s+Lim|HOSP_B_CARDIO_HEAD", re.IGNORECASE)

HOSP_A_DEPTH = re.compile(
    r"\b2\s*(?:hop|level|step|tier|report)|direct.*CMO|report.*to\s+CMO|CMO.*direct",
    re.IGNORECASE,
)
HOSP_B_DEPTH = re.compile(
    r"\b3\s*(?:hop|level|step|tier)|Chief\s+of\s+Medicine|intermediate.*Chief|Chief.*intermediate",
    re.IGNORECASE,
)
COMPARISON = re.compile(
    r"differ|senior|same\s+title|ambiguit|hierarch|deeper|level.*differ|structural",
    re.IGNORECASE,
)

# Cross-scenario contamination guard.
CROSS_CONTAMINATION = re.compile(
    r"IRB|SAE|clinical\s+trial|whistleblower", re.IGNORECASE
)

HOSP_A_SECTION = re.compile(
    r"St\.?\s*Alban|Hospital\s+A|hosp_a|Garrett\s+Osei|HOSP_A", re.IGNORECASE
)
HOSP_B_SECTION = re.compile(
    r"Riverside|Hospital\s+B|hosp_b|Soo.?Jin\s+Lim|HOSP_B", re.IGNORECASE
)


def _count_sections(text: str) -> int:
    return len(re.findall(r"^#{1,4}\s+\S", text, re.MULTILINE))


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q3.py <workspace>", file=sys.stderr)
        return 1
    ws = Path(sys.argv[1])
    target = ws / "output" / "org_chart_analysis.md"

    if not target.exists():
        print(f"FAIL: {target} does not exist")
        return 1

    text = target.read_text(encoding="utf-8")
    errors: list[str] = []

    # 1. Size and section structure.
    if len(text.encode("utf-8")) < 400:
        errors.append(
            f"org_chart_analysis.md too short ({len(text.encode())} bytes); "
            "must be >= 400 bytes"
        )

    section_count = _count_sections(text)
    has_a_section = HOSP_A_SECTION.search(text) is not None
    has_b_section = HOSP_B_SECTION.search(text) is not None
    if not (has_a_section and has_b_section):
        errors.append(
            "org_chart_analysis.md must contain a section for each hospital "
            "(Hospital A / St. Alban's and Hospital B / Riverside General)"
        )
    elif section_count < 2:
        errors.append(
            "org_chart_analysis.md has fewer than 2 ## section headers; "
            "use separate sections for each hospital"
        )

    # 2–3. Director names.
    if not HOSP_A_NAME.search(text):
        errors.append(
            "org_chart_analysis.md does not name Hospital A Director: "
            "Dr. Garrett Osei (or HOSP_A_CARDIO_HEAD)"
        )
    if not HOSP_B_NAME.search(text):
        errors.append(
            "org_chart_analysis.md does not name Hospital B Director: "
            "Dr. Soo-Jin Lim (or HOSP_B_CARDIO_HEAD)"
        )

    # 4. Hospital A depth (2 hops / direct).
    if not HOSP_A_DEPTH.search(text):
        errors.append(
            "org_chart_analysis.md does not correctly characterize Hospital A Director depth "
            "(expected: 2 hops / direct / reports to CMO)"
        )

    # 5. Hospital B depth (3 hops / Chief of Medicine).
    if not HOSP_B_DEPTH.search(text):
        errors.append(
            "org_chart_analysis.md does not correctly characterize Hospital B Director depth "
            "(expected: 3 hops / Chief of Medicine as intermediate node)"
        )

    # 6. Comparison note.
    if not COMPARISON.search(text):
        errors.append(
            "org_chart_analysis.md lacks a structural comparison note "
            "(e.g., difference in seniority, hierarchy depth, or reporting level)"
        )

    # 7. Cross-contamination guard.
    if CROSS_CONTAMINATION.search(text):
        errors.append(
            "org_chart_analysis.md contains clinical-trial-specific terms (IRB/SAE/etc.) "
            "— likely cross-scenario contamination; re-read only org_charts/ PNG images"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        "PASS: org_chart_analysis.md correctly identifies both Directors, "
        "Hospital A depth=2 hops (direct), Hospital B depth=3 hops (via Chief of Medicine), "
        "and includes a structural comparison"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
