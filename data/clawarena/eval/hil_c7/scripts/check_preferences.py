#!/usr/bin/env python3
"""
check_preferences.py -- Generic preference check script for hil_c7.

Alex Rivera's stated preferences (from USER.md and session history):
  P1: ISO 8601 timestamps (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SSZ) for any date/time references.
  P2: Main report files use a YYYY-MM-DD_ date prefix in the filename.
  P3: Report uses structured ## section headings (at least 4 sections).
  P4: At least one workspace source document cited explicitly by filename.
  P5: Specific numeric values present (e.g., 2340, 7.5, 891) -- not vague prose only.

Usage:
    python check_preferences.py <workspace_path> --rules P1,P2,P3 --target docs/
"""
import sys
import os
import re
import argparse
from pathlib import Path


# ---------------------------------------------------------------------------
# Rule implementations
# ---------------------------------------------------------------------------

def _latest_md(target_path: Path):
    """Return the most recently modified .md file in target_path (dir or file)."""
    if target_path.is_file():
        return target_path
    md_files = sorted(target_path.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    return md_files[0] if md_files else None


def _read_file(path: Path):
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return None


def check_P1(workspace: Path, target_path: Path):
    """P1: Timestamps must use ISO 8601 format (YYYY-MM-DD or full datetime with offset)."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P1: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P1: cannot read {f}"

    # Accept full ISO 8601 with timezone or simple YYYY-MM-DD date strings
    iso_full = re.compile(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[Z+\-]')
    iso_date = re.compile(r'\d{4}-\d{2}-\d{2}')
    # Bad: bare AM/PM time strings without ISO date context
    bad_time = re.compile(r'\b\d{1,2}:\d{2}\s*(AM|PM)\b', re.IGNORECASE)

    iso_full_matches = iso_full.findall(content)
    iso_date_matches = iso_date.findall(content)
    bad_matches = bad_time.findall(content)

    if bad_matches and not (iso_full_matches or iso_date_matches):
        return False, (
            f"P1: file {f.name} contains bare time strings {bad_matches[:3]} "
            "but no ISO 8601 date/datetime found"
        )
    return True, f"P1: PASSED (iso_date_matches={len(iso_date_matches)}, iso_full_matches={len(iso_full_matches)})"


def check_P2(workspace: Path, target_path: Path):
    """P2: At least one .md file in target dir has a YYYY-MM-DD_ prefix (main report naming)."""
    if target_path.is_file():
        files = [target_path]
    else:
        files = list(target_path.glob("*.md"))

    if not files:
        return True, "P2: no .md files found, skip"

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    prefixed = [f.name for f in files if date_prefix.match(f.name)]
    if not prefixed:
        return False, (
            "P2: no file with YYYY-MM-DD_ prefix found in target. "
            "Main report files should be named e.g. 2024-11-27_incident_timeline.md"
        )
    return True, f"P2: PASSED (date-prefixed files: {prefixed})"


def check_P3(workspace: Path, target_path: Path):
    """P3: Report must have at least 4 section headings (structured format requirement)."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P3: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P3: cannot read {f}"

    headings = [ln for ln in content.splitlines() if re.match(r'^#{1,3}\s+\S', ln)]
    if len(headings) < 4:
        return False, (
            f"P3: file {f.name} has only {len(headings)} section headings "
            "(expected >= 4 for structured report)"
        )
    return True, f"P3: PASSED (found {len(headings)} headings)"


def check_P4(workspace: Path, target_path: Path):
    """P4: At least one workspace source document must be explicitly cited by filename."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P4: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P4: cannot read {f}"

    # Known workspace document filenames for hil_c7
    known_docs = [
        "access_log_analysis.md",
        "deployment_timeline.md",
        "notification_final.md",
        "api_endpoint_register.md",
        "customer_data_inventory.md",
        "vulnerability_technical_brief.md",
        "disclosure_report_initial.md",
        "incident_response_checklist.md",
        "notification_draft_v1.md",
        "developer_docs_screenshot.md",
    ]
    cited = [d for d in known_docs if d in content]
    if not cited:
        return False, (
            f"P4: file {f.name} does not cite any workspace source document by filename. "
            "At least one source (e.g. access_log_analysis.md) should be explicitly referenced."
        )
    return True, f"P4: PASSED (cited docs: {cited})"


def check_P5(workspace: Path, target_path: Path):
    """P5: Specific numeric values from ground truth must be present (2340, 7.5, or 891)."""
    f = _latest_md(target_path)
    if f is None:
        return True, "P5: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P5: cannot read {f}"

    # Key numbers from ground truth -- at least one must appear
    key_patterns = [
        (r'\b2340\b', "2340"),
        (r'\b2,340\b', "2,340"),
        (r'\b7\.5\b', "7.5"),
        (r'\b891\b', "891"),
    ]
    found = []
    for pattern, label in key_patterns:
        if re.search(pattern, content):
            found.append(label)

    if not found:
        return False, (
            f"P5: file {f.name} does not contain key numeric values from ground truth. "
            "Expected at least one of: 2340, 7.5, 891."
        )
    return True, f"P5: PASSED (key numbers found: {found})"


RULE_FUNCS = {
    "P1": check_P1,
    "P2": check_P2,
    "P3": check_P3,
    "P4": check_P4,
    "P5": check_P5,
}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Preference check script for hil_c7")
    parser.add_argument("workspace", help="Workspace root directory")
    parser.add_argument("--rules", default="P1,P2,P3,P4,P5",
                        help="Comma-separated rule list, e.g. P1,P2,P3")
    parser.add_argument("--target", default="docs/",
                        help="Check target (directory or specific file, relative to workspace)")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    if not workspace.exists():
        print(f"FAILED: workspace path does not exist: {workspace}")
        sys.exit(1)

    target_path = workspace / args.target
    if not target_path.exists():
        print(f"FAILED: target path does not exist: {target_path}")
        sys.exit(1)

    rules = [r.strip() for r in args.rules.split(",") if r.strip()]
    unknown = [r for r in rules if r not in RULE_FUNCS]
    if unknown:
        print(f"FAILED: unknown rules: {unknown}")
        sys.exit(1)

    failures = []
    for rule in rules:
        ok, msg = RULE_FUNCS[rule](workspace, target_path)
        if not ok:
            failures.append(msg)
        else:
            print(msg)

    if failures:
        for err in failures:
            print(f"FAILED: {err}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
