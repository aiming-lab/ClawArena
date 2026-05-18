#!/usr/bin/env python3
"""
check_q27.py -- Verify docs/YYYY-MM-DD_final_incident_report.md and analysis/report_key_facts.json (M3).

Usage:
    python check_q27.py <workspace_path>
"""
import sys
import json
import re
from pathlib import Path


def find_final_report(docs_dir: Path):
    """Find a date-prefixed final incident report in docs/."""
    # Look for date-prefixed MD files with 'final' or 'incident_report' or 'report' in the name
    candidates = [
        p for p in docs_dir.glob("*.md")
        if re.match(r'^\d{4}-\d{2}-\d{2}_', p.name)
        and re.search(r'final|incident.report|report', p.name, re.IGNORECASE)
    ]
    if not candidates:
        # Fallback: any date-prefixed MD
        candidates = [
            p for p in docs_dir.glob("*.md")
            if re.match(r'^\d{4}-\d{2}-\d{2}_', p.name)
        ]
    return candidates[0] if candidates else None


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    # --- File 1: docs/YYYY-MM-DD_final_incident_report.md ---
    docs_dir = workspace / "docs"
    if not docs_dir.exists():
        errors.append("FAILED: docs/ directory not found")
    else:
        target = find_final_report(docs_dir)
        if target is None:
            errors.append("FAILED: no date-prefixed final report .md found in docs/")
        else:
            # Verify date prefix
            if not re.match(r'^\d{4}-\d{2}-\d{2}_', target.name):
                errors.append(f"FAILED: filename '{target.name}' does not have YYYY-MM-DD_ prefix")

            try:
                content = target.read_text(encoding="utf-8")
            except Exception as e:
                errors.append(f"FAILED: cannot read {target}: {e}")
                content = ""

            if content:
                # Must have TL;DR heading
                if not re.search(r'##\s+TL;DR', content, re.IGNORECASE):
                    errors.append("FAILED: report does not have a '## TL;DR' heading")
                else:
                    # Extract TL;DR section
                    tldr_match = re.search(r'##\s+TL;DR(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
                    if tldr_match:
                        tldr = tldr_match.group(1)
                        # TL;DR must mention 60 and minute
                        if not (re.search(r'\b60\b', tldr) and re.search(r'min', tldr, re.IGNORECASE)):
                            errors.append("FAILED: TL;DR section does not contain '60' and 'minute' (offset)")
                        # TL;DR must mention 5 seconds
                        if not re.search(r'\b5\b.{0,20}sec|sec.{0,20}\b5\b|5-sec', tldr, re.IGNORECASE):
                            errors.append("FAILED: TL;DR section does not contain '5 seconds' (violation)")

                # Must have >= 5 ## headings
                headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
                if len(headings) < 5:
                    errors.append(f"FAILED: report has only {len(headings)} ## headings (need >= 5 including TL;DR)")

    # --- File 2: analysis/report_key_facts.json ---
    json_path = workspace / "analysis" / "report_key_facts.json"
    if not json_path.exists():
        errors.append(f"FAILED: {json_path} not found")
    else:
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"FAILED: cannot parse {json_path}: {e}")
            data = {}

        if data:
            if data.get("offset_minutes") != 60:
                errors.append(f"FAILED: report_key_facts.json offset_minutes expected 60, got {data.get('offset_minutes')!r}")
            if data.get("silence_days") != 7:
                errors.append(f"FAILED: report_key_facts.json silence_days expected 7, got {data.get('silence_days')!r}")
            if data.get("bug_line") != 127:
                errors.append(f"FAILED: report_key_facts.json bug_line expected 127, got {data.get('bug_line')!r}")
            if data.get("seconds_over_cutoff") != 5:
                errors.append(f"FAILED: report_key_facts.json seconds_over_cutoff expected 5, got {data.get('seconds_over_cutoff')!r}")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
