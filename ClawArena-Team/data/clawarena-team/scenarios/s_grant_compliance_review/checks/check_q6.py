#!/usr/bin/env python3
"""check_q6.py — Validate output/compliance_report.md for q6 (post-u2 compliance re-review).

Key requirements:
  - NC-A-001 marked as waived / resolved / retracted (not removed silently).
  - NC-A-004 introduced as new item for missing Indirect Cost Justification Form (ICJF).
  - All other NC codes (NC-A-002, NC-A-003, NC-B-001, NC-B-002, NC-C-001, NC-C-002,
    NC-C-003) preserved without renumbering.
  - nc_item_codes JSON array contains the 8 active post-u2 items
    (NC-A-001 removed, NC-A-004 added).
  - total_nc_count still = 8.
  - New COMPLIANCE_CHECK token matching post-u2 sha256.
  - Edit constraint: >= 4 '## ' section headers preserved from q5 (file was edited, not rewritten).
  - Cross-round numbering continuity: every NC code in q4 noncompliance_list.md (except
    NC-A-001) must appear verbatim in the updated q6 report.

COMPLIANCE_CHECK canonical inputs (q6 — post-u2 active items):
  nc_ids_q6 = sorted(["NC-A-002","NC-A-003","NC-A-004","NC-B-001","NC-B-002",
                        "NC-C-001","NC-C-002","NC-C-003"])

Usage: python check_q6.py <workspace_abs_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

BYTE_MIN = 1400
SECTION_HEADER_RE = re.compile(r"^##\s+\S", re.MULTILINE)
JSON_FENCE_RE = re.compile(r"```json\s*([\s\S]*?)```", re.DOTALL)
NC_CODE_RE = re.compile(r"NC-[ABC]-\d{3}")
COMPLIANCE_TOKEN_RE = re.compile(r"COMPLIANCE_CHECK:([0-9a-fA-F]{64})")

# q6 active NC items (post-u2)
Q6_ACTIVE_NC_CODES = sorted([
    "NC-A-002", "NC-A-003", "NC-A-004",
    "NC-B-001", "NC-B-002",
    "NC-C-001", "NC-C-002", "NC-C-003",
])

# NC codes that must be preserved verbatim from q4 (excluding NC-A-001)
Q4_PRESERVED_CODES = [
    "NC-A-002", "NC-A-003",
    "NC-B-001", "NC-B-002",
    "NC-C-001", "NC-C-002", "NC-C-003",
]

# NC-A-001 waiver acknowledgment
NC_A_001_RE = re.compile(r"NC.?A.?001", re.IGNORECASE)
WAIVER_RE = re.compile(
    r"waiv|resolv|retract|exempt|writ.*approv|formally\s+withdrawn|one.?time.*exception",
    re.IGNORECASE,
)

# NC-A-004 and ICJF requirement
NC_A_004_RE = re.compile(r"NC.?A.?004", re.IGNORECASE)
ICJF_RE = re.compile(
    r"ICJF|Indirect\s+Cost\s+Justification\s+Form|justification\s+form|"
    r"indirect\s+cost.*form|form.*indirect\s+cost",
    re.IGNORECASE,
)

# Canonical agreement paths (same as q5)
CANONICAL_AGREEMENT_PATHS = [
    "grant_agreements/halcyon_agreement_2025.md",
    "grant_agreements/nordic_agreement_2025.md",
    "grant_agreements/opal_city_contract_2025.md",
]


def _compute_canonical_sha_q6(ws: Path) -> str:
    nc_canonical = "|".join(Q6_ACTIVE_NC_CODES)
    h = hashlib.sha256()
    for rel_path in CANONICAL_AGREEMENT_PATHS:
        p = ws / rel_path
        if p.exists():
            h.update(p.read_bytes())
    h.update(nc_canonical.encode())
    return h.hexdigest()


def _extract_last_json_block(text: str) -> dict | None:
    matches = list(JSON_FENCE_RE.finditer(text))
    if not matches:
        return None
    last_content = matches[-1].group(1).strip()
    try:
        return json.loads(last_content)
    except json.JSONDecodeError:
        return None


def _co_occur_within(text: str, anchor_re: re.Pattern, check_re: re.Pattern, window: int) -> bool:
    for m in anchor_re.finditer(text):
        start = max(0, m.start() - window)
        end = min(len(text), m.end() + window)
        if check_re.search(text[start:end]):
            return True
    return False


def _read_q4_nc_codes(ws: Path) -> list[str]:
    """Extract NC codes from q4 noncompliance_list.md."""
    q4_path = ws / "output" / "noncompliance_list.md"
    if not q4_path.exists():
        return []
    text = q4_path.read_text(encoding="utf-8")
    return NC_CODE_RE.findall(text)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q6.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    target = ws / "output" / "compliance_report.md"

    if not target.exists():
        print(f"FAIL: missing {target}", file=sys.stderr)
        return 1

    text = target.read_text(encoding="utf-8")
    errors: list[str] = []

    # 1. Byte length
    byte_len = len(text.encode("utf-8"))
    if byte_len < BYTE_MIN:
        errors.append(
            f"compliance_report.md too short ({byte_len} bytes); expected >= {BYTE_MIN} bytes "
            "after post-u2 updates (NC-A-001 waiver + NC-A-004 addition)"
        )

    # 2. Section headers >= 4 (structure preserved from q5 via Edit)
    headers = SECTION_HEADER_RE.findall(text)
    if len(headers) < 4:
        errors.append(
            f"compliance_report.md has only {len(headers)} '## ' section header(s); "
            "expected >= 4 (q5 sections must be preserved — use Edit tool, not Write)"
        )

    # 3. NC-A-001 waived acknowledgment
    if NC_A_001_RE.search(text):
        if not _co_occur_within(text, NC_A_001_RE, WAIVER_RE, 400):
            errors.append(
                "NC-A-001 present in report but not accompanied by waiver / resolved / "
                "retracted language within 400 chars; GRANTOR_A_OFFICER issued a formal "
                "written waiver — NC-A-001 must be explicitly marked as waived/resolved"
            )
    else:
        errors.append(
            "NC-A-001 not found in compliance_report.md; it must appear (marked as "
            "waived/resolved) so that the history of the finding is preserved"
        )

    # 4. NC-A-004 introduced with ICJF reference
    if not NC_A_004_RE.search(text):
        errors.append(
            "NC-A-004 not found in compliance_report.md; "
            "the new documentation gap (missing Indirect Cost Justification Form for GRA-0041) "
            "must be added as NC-A-004"
        )
    else:
        if not _co_occur_within(text, NC_A_004_RE, ICJF_RE, 400):
            errors.append(
                "NC-A-004 present but ICJF / Indirect Cost Justification Form not referenced "
                "within 400 chars; the new finding must explicitly cite the missing ICJF"
            )

    # 5. JSON block: parse and validate
    json_block = _extract_last_json_block(text)
    if json_block is None:
        errors.append(
            "no valid ```json``` fenced block found in compliance_report.md"
        )
    else:
        # 5a. total_nc_count still 8
        total = json_block.get("total_nc_count")
        if total != 8:
            errors.append(
                f"JSON: total_nc_count = {total!r}; expected 8 "
                "(NC-A-001 removed, NC-A-004 added — net count unchanged)"
            )

        # 5b. nc_item_codes: must contain active post-u2 set; must NOT contain NC-A-001
        nc_codes_json = json_block.get("nc_item_codes")
        if not isinstance(nc_codes_json, list):
            errors.append("JSON: nc_item_codes field missing or not a list")
        else:
            # Must NOT contain NC-A-001 in active array
            if "NC-A-001" in nc_codes_json:
                errors.append(
                    "JSON: nc_item_codes still contains 'NC-A-001'; "
                    "NC-A-001 was waived by GRANTOR_A_OFFICER and must be removed "
                    "from the active items array"
                )
            # Must contain NC-A-004
            if "NC-A-004" not in nc_codes_json:
                errors.append(
                    "JSON: nc_item_codes missing 'NC-A-004'; "
                    "the new ICJF documentation gap must appear in the active items array"
                )
            # Must contain all other preserved codes
            missing_preserved = [c for c in Q4_PRESERVED_CODES if c not in nc_codes_json]
            if missing_preserved:
                errors.append(
                    f"JSON: nc_item_codes missing preserved codes: {missing_preserved}; "
                    "do not renumber or drop existing NC codes other than NC-A-001"
                )
            # All codes must conform to NC-[ABC]-NNN format
            invalid_codes = [c for c in nc_codes_json if not NC_CODE_RE.match(c)]
            if invalid_codes:
                errors.append(
                    f"JSON: nc_item_codes contains non-conforming entries: {invalid_codes}"
                )

        # 5c. COMPLIANCE_CHECK token (post-u2 recomputation)
        token_match = COMPLIANCE_TOKEN_RE.search(text)
        if token_match is None:
            errors.append(
                "COMPLIANCE_CHECK:<sha256> token not found in updated compliance_report.md; "
                "re-run `tools/verify_compliance.py` with the post-u2 active NC item IDs "
                "(NC-A-002 through NC-C-003, NC-A-004; excluding NC-A-001)"
            )
        else:
            reported_sha = token_match.group(1).lower()
            expected_sha = _compute_canonical_sha_q6(ws)
            if reported_sha != expected_sha:
                errors.append(
                    f"COMPLIANCE_CHECK token sha does not match post-u2 canonical recomputation; "
                    f"reported: {reported_sha[:16]}..., expected: {expected_sha[:16]}... "
                    "(use the updated active NC item set, sorted: "
                    f"{Q6_ACTIVE_NC_CODES})"
                )

    # 6. Cross-round numbering continuity: q4 preserved codes appear verbatim in q6 report
    q4_codes = _read_q4_nc_codes(ws)
    if q4_codes:
        q4_preserved_in_q4 = [c for c in q4_codes if c != "NC-A-001"]
        missing_from_report = [c for c in q4_preserved_in_q4 if c not in text]
        if missing_from_report:
            errors.append(
                f"cross-round numbering continuity failed: NC codes from q4 "
                f"noncompliance_list.md missing from q6 report: {missing_from_report}; "
                "do not renumber or omit existing items when editing the report"
            )
    else:
        # q4 file missing — issue a warning-level note
        errors.append(
            "output/noncompliance_list.md (q4 output) not found; "
            "cannot verify cross-round numbering continuity"
        )

    if errors:
        for e in errors:
            print(f"FAIL: {e}", file=sys.stderr)
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
