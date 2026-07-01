#!/usr/bin/env python3
"""check_formal_case_summary_json.py — Validates docs/YYYY-MM-DD_formal_case_summary.json for q26."""
import sys
import json
import re
from pathlib import Path


def main():
    workspace = Path(sys.argv[1])
    docs_dir = workspace / "docs"

    if not docs_dir.exists():
        print("FAILED: docs/ directory not found")
        sys.exit(1)

    # Find the date-prefixed formal_case_summary.json
    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    summary_files = [
        f for f in docs_dir.glob("*.json")
        if date_prefix.match(f.name) and "formal" in f.name.lower()
        and "case" in f.name.lower()
    ]

    if not summary_files:
        # More lenient: any date-prefixed json
        summary_files = [
            f for f in docs_dir.glob("*.json")
            if date_prefix.match(f.name) and "summary" in f.name.lower()
        ]

    if not summary_files:
        print("FAILED: No date-prefixed formal_case_summary.json found in docs/")
        sys.exit(1)

    target = sorted(summary_files, key=lambda p: p.stat().st_mtime, reverse=True)[0]

    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: JSON parse error in {target.name}: {e}")
        sys.exit(1)

    errors = []

    if not isinstance(data, dict):
        print("FAILED: formal_case_summary.json must be a JSON object")
        sys.exit(1)

    # Required top-level keys
    required_keys = [
        "incident_id", "suspect", "incident_date",
        "evidence_chain", "contradictions_resolved",
        "conclusion", "recommended_actions"
    ]
    for key in required_keys:
        if key not in data:
            errors.append(f"Missing required top-level key '{key}'")

    if not errors:
        # evidence_chain >= 5 items
        ec = data.get("evidence_chain", [])
        if not isinstance(ec, list) or len(ec) < 5:
            errors.append(
                f"evidence_chain must have >= 5 items, got {len(ec) if isinstance(ec, list) else 'not a list'}"
            )

        # contradictions_resolved >= 4 items
        cr = data.get("contradictions_resolved", [])
        if not isinstance(cr, list) or len(cr) < 4:
            errors.append(
                f"contradictions_resolved must have >= 4 items, got {len(cr) if isinstance(cr, list) else 'not a list'}"
            )
        else:
            # Must include IT report scope gap
            cr_text = json.dumps(cr, ensure_ascii=False).lower()
            if not any(
                kw in cr_text
                for kw in ["it-sec", "it sec", "scope", "it report"]
            ):
                errors.append(
                    "contradictions_resolved must include an entry about the IT report scope gap "
                    "(IT-SEC-2026-INV-042)"
                )

        # conclusion.verdict must not be inconclusive
        conclusion = data.get("conclusion", {})
        if not isinstance(conclusion, dict):
            errors.append("'conclusion' must be a JSON object")
        else:
            verdict = conclusion.get("verdict", "").lower()
            invalid_verdicts = ["inconclusive", "insufficient evidence", "unclear", "undetermined"]
            if any(iv in verdict for iv in invalid_verdicts):
                errors.append(
                    f"conclusion.verdict must be a definitive finding, not '{verdict}'"
                )

        # recommended_actions >= 3 items
        ra = data.get("recommended_actions", [])
        if not isinstance(ra, list) or len(ra) < 3:
            errors.append(
                f"recommended_actions must have >= 3 items, got {len(ra) if isinstance(ra, list) else 'not a list'}"
            )

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
