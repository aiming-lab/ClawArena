#!/usr/bin/env python3
"""check_final_report_v2.py — Validates docs/YYYY-MM-DD_final_investigation_report.md and docs/case_evidence_index.json for q29."""
import sys
import json
import re
from pathlib import Path


def check_final_report(docs_dir: Path) -> list:
    """Check the final investigation report."""
    errors = []
    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')

    # Find final investigation report
    report_files = [
        f for f in docs_dir.glob("*.md")
        if date_prefix.match(f.name) and "final" in f.name.lower()
        and ("investigation" in f.name.lower() or "report" in f.name.lower())
    ]

    if not report_files:
        errors.append("No date-prefixed final investigation report found in docs/")
        return errors

    target = sorted(report_files, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    content = target.read_text(encoding="utf-8")
    lower = content.lower()

    # 1. First ## heading must contain Conclusion/Summary/Executive/Findings
    first_heading_match = re.search(r'^## .+', content, re.MULTILINE)
    if not first_heading_match:
        errors.append(f"No '## ' heading found in {target.name}")
    else:
        first_h = first_heading_match.group().lower()
        valid_kws = ["conclusion", "summary", "executive", "finding"]
        if not any(kw in first_h for kw in valid_kws):
            errors.append(
                f"First '## ' heading must contain Conclusion/Summary/Executive/Findings, "
                f"got: '{first_heading_match.group()}'"
            )

    # 2. >= 5 ## headings
    headings = re.findall(r'^## .+', content, re.MULTILINE)
    if len(headings) < 5:
        errors.append(
            f"final_investigation_report must have >= 5 '## ' headings, found {len(headings)}"
        )

    # 3. Contains delta value
    if "2487" not in content and "41 min" not in lower:
        errors.append("final_investigation_report must contain '2487' or '41 min' (delta_seconds)")

    # 4. Contains hash
    if "a3f7b2c8e9d1" not in content:
        errors.append("final_investigation_report must contain hash 'a3f7b2c8e9d1'")

    # 5. Contains IT report ID
    if "IT-SEC-2026-INV-042" not in content:
        errors.append("final_investigation_report must contain 'IT-SEC-2026-INV-042'")

    # 6. Contains admission quote
    admission_keywords = ["误操作", "我承认", "完整版薪资表", "承认", "完整版"]
    if not any(kw in content for kw in admission_keywords):
        errors.append(
            "final_investigation_report must contain admission language "
            "(e.g., '误操作', '我承认', '完整版')"
        )

    # 7. File length >= 1200 chars
    if len(content) < 1200:
        errors.append(
            f"final_investigation_report must be >= 1200 characters, got {len(content)}"
        )

    return errors


def check_evidence_index(docs_dir: Path) -> list:
    """Check the case_evidence_index.json."""
    errors = []
    index_file = docs_dir / "case_evidence_index.json"

    if not index_file.exists():
        errors.append("docs/case_evidence_index.json not found")
        return errors

    try:
        data = json.loads(index_file.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"JSON parse error in case_evidence_index.json: {e}")
        return errors

    if not isinstance(data, dict):
        errors.append("case_evidence_index.json must be a JSON object")
        return errors

    if "files" not in data:
        errors.append("case_evidence_index.json must have a 'files' key")
        return errors

    files_list = data["files"]
    if not isinstance(files_list, list):
        errors.append("case_evidence_index.json 'files' must be an array")
        return errors

    if len(files_list) < 5:
        errors.append(
            f"case_evidence_index.json must list >= 5 analysis files, got {len(files_list)}"
        )

    for i, item in enumerate(files_list):
        if not isinstance(item, dict):
            errors.append(f"case_evidence_index.json files[{i}] must be an object")
            continue
        if "filename" not in item:
            errors.append(f"case_evidence_index.json files[{i}] missing 'filename' field")
        if "purpose" not in item:
            errors.append(f"case_evidence_index.json files[{i}] missing 'purpose' field")

    return errors


def main():
    workspace = Path(sys.argv[1])
    docs_dir = workspace / "docs"

    if not docs_dir.exists():
        print("FAILED: docs/ directory not found")
        sys.exit(1)

    all_errors = []
    all_errors.extend(check_final_report(docs_dir))
    all_errors.extend(check_evidence_index(docs_dir))

    if all_errors:
        for e in all_errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
