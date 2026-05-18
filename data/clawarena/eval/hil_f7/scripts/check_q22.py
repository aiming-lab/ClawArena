#!/usr/bin/env python3
"""
check_q22.py -- Verify docs/evidence_reliability_ranking.md.

Usage:
    python check_q22.py <workspace_path>
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

    md_path = workspace / "docs" / "evidence_reliability_ranking.md"
    if not md_path.exists():
        print("FAILED: docs/evidence_reliability_ranking.md not found")
        sys.exit(1)

    try:
        content = md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read docs/evidence_reliability_ranking.md: {e}")
        sys.exit(1)

    # Must rank courier evidence as highest
    # Look for courier mentioned in context of "highest", "first", "1", etc.
    courier_high = re.search(
        r'(courier|快递|顺丰|courier.{0,50}high|高|最高|1st|first|最可靠)',
        content, re.IGNORECASE | re.DOTALL
    )
    if not courier_high:
        errors.append(
            "FAILED: courier evidence must be ranked as the highest/most reliable source"
        )

    # Must mention seller/CS statements as least reliable
    if not re.search(r'(seller|商家|客服|CS).{0,100}(least|lowest|last|最低|最不|最差)', content, re.IGNORECASE | re.DOTALL) and \
       not re.search(r'(least|lowest|last|最低|最不|最差).{0,100}(seller|商家|客服|CS)', content, re.IGNORECASE | re.DOTALL):
        errors.append(
            "FAILED: seller/CS statements must be ranked as least reliable source"
        )

    # Must mention independent / third party as reasoning for courier evidence
    if not re.search(r'independent|独立|third.{0,10}party|第三方', content, re.IGNORECASE):
        errors.append(
            "FAILED: does not provide 'independent third-party' reasoning for courier evidence reliability"
        )

    # Must have >= 4 ## headings
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 4:
        errors.append(f"FAILED: only {len(headings)} ## headings found (need >= 4)")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
