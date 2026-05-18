#!/usr/bin/env python3
"""
check_q11.py -- Verify docs/scope_consistency_report.md

M3 cross-file check: agent must cross-reference api_endpoint_register.md,
customer_data_inventory.md, and disclosure_report_initial.md.

Expected content:
  - All 3 source documents cited
  - At least one specific inconsistency identified with specific values
    (e.g., Jake's 12,000 estimate vs 2,340 inventory upper bound)
  - Specific numeric values from multiple sources present

Usage:
    python check_q11.py <workspace_path>
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

    md_path = workspace / "docs" / "scope_consistency_report.md"
    if not md_path.exists():
        print("FAILED: docs/scope_consistency_report.md not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read docs/scope_consistency_report.md: {e}")
        sys.exit(1)

    # Must cite all 3 required source documents
    required_docs = [
        ("api_endpoint_register.md", re.compile(r'api_endpoint_register', re.IGNORECASE)),
        ("customer_data_inventory.md", re.compile(r'customer_data_inventory', re.IGNORECASE)),
        ("disclosure_report_initial.md", re.compile(r'disclosure_report_initial', re.IGNORECASE)),
    ]
    cited = [name for name, pattern in required_docs if pattern.search(content)]
    if len(cited) < 3:
        missing = [name for name, _ in required_docs
                   if not any(p.search(content) for _, p in [(name, required_docs[i][1])
                                                              for i, (n, _) in enumerate(required_docs)
                                                              if n == name])]
        errors.append(
            f"FAILED: must cite all 3 source documents "
            f"(api_endpoint_register.md, customer_data_inventory.md, "
            f"disclosure_report_initial.md). "
            f"Found: {cited}"
        )

    # Must contain 2340 (inventory upper bound)
    if not re.search(r'\b2,?340\b', content):
        errors.append(
            "FAILED: must contain '2340' or '2,340' (total records from "
            "customer_data_inventory.md)"
        )

    # Must identify at least one specific inconsistency
    if not re.search(
        r'inconsisten|contradict|conflict|discrepan|mismatch|differ',
        content, re.IGNORECASE
    ):
        errors.append(
            "FAILED: must identify at least one specific inconsistency between sources"
        )

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
