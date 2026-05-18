#!/usr/bin/env python3
"""
check_q29_final_report.py — Verify q29: docs/YYYY-MM-DD_最终欺诈调查报告.md
  - docs/ contains a date-prefixed .md file
  - Contains '50,234' or '50234' (official XHS plays)
  - Contains '120,000' or '120000' (MCN XHS plays)
  - Contains '32,178' or '32178' (official Bilibili plays)
  - Contains '65,000' or '65000' (MCN Bilibili plays)
  - Contains '内部估算' (Liu Jie's admission, exact match)
  - Contains '30,000' or '30000' (contract amount)
  - Contains '70,000' or '70000' (billed amount)
  - Contains legal action recommendation
  - >= 5 '##' headings
  - File length >= 800 characters
"""
import sys
import re
from pathlib import Path


def find_target_file(workspace: Path):
    """Find date-prefixed final report in docs/."""
    docs_dir = workspace / "docs"
    if not docs_dir.exists():
        return None, "docs/ directory does not exist"

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    md_files = list(docs_dir.glob("*.md"))

    # Priority: date-prefixed file with final report keywords
    for f in md_files:
        if date_prefix.match(f.name) and any(
            kw in f.name for kw in ["最终", "欺诈", "调查报告", "final"]
        ):
            return f, None

    # Fallback: most recent date-prefixed file
    date_files = [f for f in md_files if date_prefix.match(f.name)]
    if date_files:
        latest = sorted(date_files, key=lambda p: p.stat().st_mtime, reverse=True)[0]
        return latest, None

    return None, "no date-prefixed .md file found in docs/ (expected YYYY-MM-DD_最终欺诈调查报告.md)"


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    target, err = find_target_file(workspace)

    if target is None:
        print(f"FAILED: {err}")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8").strip()
    except Exception as e:
        print(f"FAILED: cannot read file {target}: {e}")
        sys.exit(1)

    if not content:
        print(f"FAILED: file is empty: {target}")
        sys.exit(1)

    errors = []

    # Check official XHS plays
    if "50,234" not in content and "50234" not in content:
        errors.append("official Xiaohongshu plays '50,234' or '50234' not found")

    # Check MCN XHS plays
    if "120,000" not in content and "120000" not in content:
        errors.append("MCN Xiaohongshu plays '120,000' or '120000' not found")

    # Check official Bilibili plays
    if "32,178" not in content and "32178" not in content:
        errors.append("official Bilibili plays '32,178' or '32178' not found")

    # Check MCN Bilibili plays
    if "65,000" not in content and "65000" not in content:
        errors.append("MCN Bilibili plays '65,000' or '65000' not found")

    # Check Liu Jie's admission (exact string)
    if "内部估算" not in content:
        errors.append("Liu Jie's admission '内部估算' not found (exact string required)")

    # Check contract amount
    if "30,000" not in content and "30000" not in content:
        errors.append("contract amount '30,000' or '30000' not found")

    # Check billed amount
    if "70,000" not in content and "70000" not in content:
        errors.append("billed amount '70,000' or '70000' not found")

    # Check legal action recommendation
    legal_keywords = ["法律", "诉讼", "起诉", "维权", "法务", "追责", "索赔", "赔偿"]
    if not any(kw in content for kw in legal_keywords):
        errors.append(
            f"legal action recommendation not found (expected one of: {legal_keywords})"
        )

    # Check heading count >= 5
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 5:
        errors.append(f"'##' headings: {len(headings)} (expected >= 5)")

    # Check file length >= 800
    if len(content) < 800:
        errors.append(f"file length: {len(content)} chars (expected >= 800)")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print(f"PASSED (file: {target.name}, length: {len(content)} chars)")
    sys.exit(0)


if __name__ == "__main__":
    main()
