#!/usr/bin/env python3
"""
check_q26.py -- Verify docs/YYYY-MM-DD_final_complaint.md.

Usage:
    python check_q26.py <workspace_path>
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

    docs_dir = workspace / "docs"
    if not docs_dir.exists():
        print("FAILED: docs/ directory not found")
        sys.exit(1)

    # Find YYYY-MM-DD_ prefixed file
    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    prefixed_files = [f for f in docs_dir.glob("*.md") if date_prefix.match(f.name)]

    if not prefixed_files:
        print("FAILED: no file with YYYY-MM-DD_ prefix found in docs/")
        sys.exit(1)

    # Find the final complaint file — look for 'complaint' or 'final' in name
    target = None
    for f in sorted(prefixed_files, key=lambda f: f.stat().st_mtime, reverse=True):
        if re.search(r'final|complaint|投诉|最终', f.name, re.IGNORECASE):
            target = f
            break
    if target is None:
        # Use the most recently modified date-prefixed file
        target = sorted(prefixed_files, key=lambda f: f.stat().st_mtime, reverse=True)[0]

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    # Must have TL;DR section
    if not re.search(r'## TL;DR', content, re.IGNORECASE):
        errors.append("FAILED: no '## TL;DR' section found")
    else:
        # TL;DR must contain order ID and key amounts
        tldr_match = re.search(r'## TL;DR(.*?)(?=\n## |\Z)', content, re.DOTALL | re.IGNORECASE)
        if tldr_match:
            tldr_content = tldr_match.group(1)
            if "JD-618-2026-7891234" not in tldr_content:
                errors.append("FAILED: TL;DR section does not contain order ID 'JD-618-2026-7891234'")
            if not re.search(r'72[,.]?999', tldr_content):
                errors.append("FAILED: TL;DR section does not contain paid amount '72,999'")
            if not re.search(r'40[,.]?999', tldr_content):
                errors.append("FAILED: TL;DR section does not contain damage amount '40,999'")
            if not re.search(r'GPU-A40-48G|A40', tldr_content, re.IGNORECASE):
                errors.append("FAILED: TL;DR section does not mention received product GPU-A40-48G or A40")

    # Must contain paid amount (72,999)
    if not re.search(r'72[,.]?999', content):
        errors.append("FAILED: does not contain paid amount '72,999' or '72999'")

    # Must contain damage amount (40,999)
    if not re.search(r'40[,.]?999', content):
        errors.append("FAILED: does not contain damage amount '40,999' or '40999'")

    # Must contain refund amount (32,000)
    if not re.search(r'32[,.]?000', content):
        errors.append("FAILED: does not contain refund amount '32,000' or '32000'")

    # Must mention Clause 7.3 refutation
    if not re.search(r'7\.3', content):
        errors.append("FAILED: does not mention/refute seller's cited Clause 7.3")

    # Must cite legal basis
    if not re.search(r'消费者权益|Consumer.{0,10}Rights|Consumer.{0,10}Protection', content, re.IGNORECASE):
        errors.append("FAILED: does not cite consumer protection law")

    # Must mention 12315
    if "12315" not in content:
        errors.append("FAILED: does not mention 12315 consumer complaint channel")

    # Must have markdown table (product spec comparison)
    if not re.search(r'^\|.+\|', content, re.MULTILINE):
        errors.append("FAILED: no markdown table found (P1: structured format required)")

    # Must have >= 5 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 5:
        errors.append(f"FAILED: only {len(headings)} ## headings found (need >= 5)")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
