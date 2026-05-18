#!/usr/bin/env python3
"""
check_risk_register.py — Validates docs/YYYY-MM-DD_hr_risk_register.md.

Checks:
- docs/ contains a date-prefixed file (risk register)
- >= 4 risk entries
- Each entry has severity/action/evidence language
- C4 (CTO pressure) included as process risk
- >= 4 ## headings or table rows
"""
import sys
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: check_risk_register.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    docs_dir = workspace / "docs"

    if not docs_dir.exists():
        print("FAILED: docs/ directory not found")
        sys.exit(1)

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    candidates = [
        f for f in docs_dir.glob("*.md")
        if date_prefix.match(f.name)
        and re.search(r'risk|register', f.name, re.IGNORECASE)
    ]
    if not candidates:
        candidates = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]

    if not candidates:
        print("FAILED: no date-prefixed .md file found in docs/")
        sys.exit(1)

    target = sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    content = target.read_text(encoding="utf-8")
    failures = []

    # >= 4 risk entries: count ## headings or table data rows
    headings = re.findall(r'^## ', content, re.MULTILINE)
    table_rows = [line for line in content.splitlines()
                  if '|' in line and not re.match(r'\s*\|[-:| ]+\|\s*$', line)]
    # Consider either structural form
    if len(headings) < 4 and len(table_rows) < 5:
        failures.append(
            f"Insufficient risk entries: {len(headings)} ## headings, "
            f"{len(table_rows)} table rows (need >= 4 entries)"
        )

    # Severity / action / evidence language
    if not re.search(r'severity|high|medium|low', content, re.IGNORECASE):
        failures.append("Missing severity classification (High/Medium/Low)")
    if not re.search(r'action|recommend|mitigation|response', content, re.IGNORECASE):
        failures.append("Missing recommended action language")
    if not re.search(r'evidence|source|document', content, re.IGNORECASE):
        failures.append("Missing evidence/source reference")

    # C4: CTO pressure as process risk
    if not re.search(r'C4|CTO|organizational pressure|process integrity', content, re.IGNORECASE):
        failures.append("Missing C4 / CTO pressure as process risk entry")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print(f"PASSED (checked: {target.name})")
    sys.exit(0)


if __name__ == "__main__":
    main()
