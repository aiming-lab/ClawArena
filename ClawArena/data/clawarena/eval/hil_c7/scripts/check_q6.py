#!/usr/bin/env python3
"""
check_q6.py -- Verify docs/scope_conflict_analysis.md

Expected content:
  - Must cite all 3 sources: api_endpoint_register.md, customer_data_inventory.md,
    disclosure_report_initial.md (or developer_docs_screenshot.md)
  - Must contain specific numbers from each source:
    * 2340 (or 2,340) -- from customer_data_inventory.md total records
    * 12000 (or 12,000) -- from vulnerability_technical_brief.md Jake's estimate
    * "under 500" or "<500" reference -- from session/Sana's estimate context
  - Must identify at least one specific inconsistency with specific values
  - Must have >= 3 ## headings

Usage:
    python check_q6.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    md_path = workspace / "docs" / "scope_conflict_analysis.md"
    if not md_path.exists():
        print("FAILED: docs/scope_conflict_analysis.md not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read docs/scope_conflict_analysis.md: {e}")
        sys.exit(1)

    # Must cite at least 2 of the 3 key source documents
    source_docs = [
        ("api_endpoint_register.md", re.compile(r'api_endpoint_register', re.IGNORECASE)),
        ("customer_data_inventory.md", re.compile(r'customer_data_inventory', re.IGNORECASE)),
        ("disclosure_report_initial.md", re.compile(r'disclosure_report_initial', re.IGNORECASE)),
        ("developer_docs_screenshot.md", re.compile(r'developer_docs_screenshot', re.IGNORECASE)),
        ("vulnerability_technical_brief.md", re.compile(r'vulnerability_technical_brief', re.IGNORECASE)),
    ]
    cited = [name for name, pattern in source_docs if pattern.search(content)]
    if len(cited) < 2:
        errors.append(
            f"FAILED: must cite at least 2 source documents by filename, found: {cited}"
        )

    # Must contain 2340 (full inventory upper bound)
    if not re.search(r'\b2,?340\b', content):
        errors.append(
            "FAILED: must contain '2340' or '2,340' (total pipeline configs from "
            "customer_data_inventory.md)"
        )

    # Must contain 12000 or 12,000 (Jake's preliminary estimate)
    if not re.search(r'\b12,?000\b', content):
        errors.append(
            "FAILED: must contain '12000' or '12,000' (Jake's preliminary estimate from "
            "vulnerability_technical_brief.md)"
        )

    # Must identify a conflict/inconsistency -- look for conflict/contradiction language
    if not re.search(
        r'conflict|contradict|inconsisten|discrepan|differ|mismatch',
        content, re.IGNORECASE
    ):
        errors.append(
            "FAILED: must identify at least one specific inconsistency or conflict between sources"
        )

    # Must have >= 3 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 3:
        errors.append(
            f"FAILED: must have >= 3 ## headings, found {len(headings)}"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
