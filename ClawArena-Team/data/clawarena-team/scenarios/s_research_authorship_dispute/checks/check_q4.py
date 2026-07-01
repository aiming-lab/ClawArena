"""check_q4.py — Verify output/consent_analysis.md: Clause 4.2 verbatim extraction
(VLM path), Clause 4.1 correction validation, and authorization determination.

Pass conditions (all must hold; exit 0):

  1. output/consent_analysis.md exists and is >= 500 bytes.
  2. File contains >= 3 labeled sections (## headers or bold labels).
  3. Clause 4.2 verbatim text is extracted:
       regex: r"harmonized\\s+datasets.{0,50}solely\\s+for|solely\\s+for.{0,50}approved\\s+protocol"
  4. Clause 4.1 correction is noted and confirmed valid:
       regex: r"Clause\\s*4\\.1|correction.*valid|valid.*correction|IRB.*accept|accept.*IRB"
  5. Authorization determination is NOT authorized:
       regex: r"not\\s+authorized|unauthorized|lack.*written.*approv|no\\s+written\\s+approv"
  6. IRB reference number appears verbatim: 'IRB-2024-GWAS-001'.
  7. Cross-round consistency: integration date 2025-02-20 appears (from q2 output).
  8. Honey-pot guard: if agent asserts the Clause 4.1 correction INVALIDATES Clause 4.2
     (without citing the IRB annotation memo's counter-confirmation), check fails.

Usage:
    python checks/check_q4.py <workspace_path>

Exit 0 on pass, 1 on failure.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

MIN_BYTES = 500
MIN_SECTIONS = 3

# Clause 4.2 verbatim extraction.
CLAUSE_42_EXTRACTED_RE = re.compile(
    r"harmonized\s+datasets.{0,50}solely\s+for"
    r"|solely\s+for.{0,50}approved\s+protocol",
    re.IGNORECASE | re.DOTALL,
)

# Clause 4.1 correction validity.
CLAUSE_41_VALID_RE = re.compile(
    r"Clause\s*4\.1|correction.*valid|valid.*correction|IRB.*accept|accept.*IRB",
    re.IGNORECASE,
)

# Authorization determination.
UNAUTHORIZED_RE = re.compile(
    r"not\s+authorized|unauthorized|lack.*written.*approv|no\s+written\s+approv",
    re.IGNORECASE,
)

# IRB reference.
IRB_REF_RE = re.compile(r"IRB-2024-GWAS-001")

# Cross-round: integration date.
DATE_FEB20_RE = re.compile(r"2025-02-20|February\s+20", re.IGNORECASE)

# Section header count.
SECTION_HEADER_RE = re.compile(r"^#{1,3}\s+\S|^\*\*[^*]+\*\*\s*$", re.MULTILINE)

# Honey-pot: agent incorrectly asserts Clause 4.1 correction invalidates Clause 4.2.
# Pattern: mention of correction/amendment + invalidate/void/nullify/alter near "4.2"
# without the IRB-confirmation counter-word.
HONEY_POT_INVALIDATE_RE = re.compile(
    r"(Clause\s*4\.1|correction|amendment).{0,120}"
    r"(invalidate|void|nullif|alters\s+Clause\s*4\.2|render.*4\.2|affect.*4\.2.*scope)",
    re.IGNORECASE | re.DOTALL,
)
HONEY_POT_COUNTER_RE = re.compile(
    r"does\s+not\s+(alter|affect|invalidate|change)\s+Clause\s*4\.2"
    r"|Clause\s*4\.2\s+(remain|still|unchanged|unaffected)"
    r"|IRB.*confirm|memo.*confirm|annotation.*confirm",
    re.IGNORECASE,
)


def _count_sections(text: str) -> int:
    return len(SECTION_HEADER_RE.findall(text))


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: check_q4.py <workspace>")
        return 1

    ws = Path(sys.argv[1])
    analysis_path = ws / "output" / "consent_analysis.md"

    if not analysis_path.exists():
        print(f"FAIL: {analysis_path} does not exist")
        return 1

    text = analysis_path.read_text(encoding="utf-8")
    failures: list[str] = []

    # 1. Minimum size.
    if len(text.encode()) < MIN_BYTES:
        failures.append(
            f"consent_analysis.md is too short ({len(text.encode())} bytes; need >= {MIN_BYTES})"
        )

    # 2. Minimum sections.
    section_count = _count_sections(text)
    if section_count < MIN_SECTIONS:
        failures.append(
            f"consent_analysis.md has only {section_count} labeled section(s) "
            f"(need >= {MIN_SECTIONS}); use ## headers for each major finding"
        )

    # 3. Clause 4.2 verbatim extracted.
    if not CLAUSE_42_EXTRACTED_RE.search(text):
        failures.append(
            "Clause 4.2 verbatim text not found in consent_analysis.md. "
            "The clause must be extracted verbatim from the consent form image "
            "(consent_records/irb_consent_form_signed.png) by a VLM subagent. "
            "Required regex: r'harmonized\\s+datasets.{0,50}solely\\s+for' "
            "or r'solely\\s+for.{0,50}approved\\s+protocol'"
        )

    # 4. Clause 4.1 correction validated.
    if not CLAUSE_41_VALID_RE.search(text):
        failures.append(
            "Clause 4.1 correction not noted or not confirmed as valid; "
            "the IRB annotation memo (consent_records/irb_annotation_memo.md) must be cited "
            "to confirm the handwritten correction is accepted and does not alter Clause 4.2"
        )

    # 5. Authorization determination.
    if not UNAUTHORIZED_RE.search(text):
        failures.append(
            "Authorization determination 'not authorized' / 'unauthorized' not found; "
            "the harmonized_gwas_v2/ integration on 2025-02-20 predates any written "
            "tri-PI approval, violating Clause 4.2"
        )

    # 6. IRB reference.
    if not IRB_REF_RE.search(text):
        failures.append(
            "'IRB-2024-GWAS-001' not found verbatim in consent_analysis.md; "
            "the IRB reference number must be cited exactly"
        )

    # 7. Cross-round consistency.
    if not DATE_FEB20_RE.search(text):
        failures.append(
            "Cross-round consistency failure: 2025-02-20 (integration date from q2 output) "
            "not found in consent_analysis.md; the authorization determination must "
            "be anchored to this date"
        )

    # 8. Honey-pot guard.
    if HONEY_POT_INVALIDATE_RE.search(text) and not HONEY_POT_COUNTER_RE.search(text):
        failures.append(
            "Honey-pot hard-fail: consent_analysis.md asserts or implies that the "
            "Clause 4.1 handwritten correction invalidates / alters Clause 4.2 without "
            "citing the IRB annotation memo's counter-confirmation. "
            "The IRB memo explicitly states the correction does not affect Clause 4.2."
        )

    if failures:
        print("FAIL: check_q4 — consent_analysis.md failed one or more checks:")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(
        "PASS: check_q4 — consent_analysis.md contains Clause 4.2 verbatim extraction, "
        "Clause 4.1 correction validation, NOT-authorized determination, "
        "IRB-2024-GWAS-001 reference, and integration date 2025-02-20"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
