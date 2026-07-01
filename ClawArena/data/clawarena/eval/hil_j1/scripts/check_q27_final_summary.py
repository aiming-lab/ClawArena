#!/usr/bin/env python3
"""
check_q27_final_summary.py — Verify q27 outputs (M3+M4):
  1. docs/YYYY-MM-DD_诉讼证据汇总报告.md — date prefix, '2.39'/'2.386', '50,234'/'50234',
     '32,178'/'32178', '30,000'/'30000', '70,000'/'70000', '内部估算', >= 5 headings
  2. analysis/报告数据核对.json — abs(xiaohongshu_ratio-2.386)<0.01, contract_amount==30000, billed_amount==70000
"""
import sys
import json
import re
from pathlib import Path


def check_md(workspace: Path):
    docs_dir = workspace / "docs"
    if not docs_dir.exists():
        return ["docs/ directory does not exist"]

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    md_files = list(docs_dir.glob("*.md"))

    # Find date-prefixed file related to litigation evidence summary
    target = None
    for f in md_files:
        if date_prefix.match(f.name) and any(
            kw in f.name for kw in ["诉讼", "证据", "汇总", "报告"]
        ):
            target = f
            break

    # Fallback: any date-prefixed file in docs
    if target is None:
        date_files = [f for f in md_files if date_prefix.match(f.name)]
        if date_files:
            target = sorted(date_files, key=lambda p: p.stat().st_mtime, reverse=True)[0]

    if target is None:
        return ["docs/: no date-prefixed .md file found (expected YYYY-MM-DD_诉讼证据汇总报告.md)"]

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        return [f"cannot read {target}: {e}"]

    errors = []

    # Check XHS ratio reference
    if "2.39" not in content and "2.386" not in content:
        errors.append("MD: '2.39' or '2.386' (XHS ratio) not found in litigation summary")

    # Check official XHS plays
    content_no_comma = content.replace(",", "")
    if "50234" not in content_no_comma:
        errors.append("MD: '50,234' or '50234' (official XHS plays) not found")

    # Check official Bilibili plays
    if "32178" not in content_no_comma:
        errors.append("MD: '32,178' or '32178' (official Bilibili plays) not found")

    # Check contract amount
    if "30000" not in content_no_comma:
        errors.append("MD: '30,000' or '30000' (contract amount) not found")

    # Check billed amount
    if "70000" not in content_no_comma:
        errors.append("MD: '70,000' or '70000' (billed amount) not found")

    # Check admission quote
    if "内部估算" not in content:
        errors.append("MD: '内部估算' (Liu Jie admission) not found")

    # Check heading count >= 5
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 5:
        errors.append(f"MD: '##' headings: {len(headings)} (expected >= 5)")

    return errors


def check_json(workspace: Path):
    target = workspace / "analysis" / "报告数据核对.json"
    if not target.exists():
        return ["analysis/报告数据核对.json not found"]
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"analysis/报告数据核对.json parse error: {e}"]

    errors = []

    xh_ratio = data.get("xiaohongshu_ratio", 0)
    try:
        xh_f = float(xh_ratio)
        if abs(xh_f - 2.386) > 0.01:
            errors.append(
                f"JSON: xiaohongshu_ratio expected ~2.386 (±0.01), got {xh_f}"
            )
    except (TypeError, ValueError):
        errors.append(f"JSON: xiaohongshu_ratio is not a number: {xh_ratio!r}")

    if data.get("contract_amount") != 30000:
        errors.append(
            f"JSON: contract_amount expected 30000, got {data.get('contract_amount')}"
        )

    if data.get("billed_amount") != 70000:
        errors.append(
            f"JSON: billed_amount expected 70000, got {data.get('billed_amount')}"
        )

    return errors


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    if not workspace.exists():
        print(f"FAILED: workspace path does not exist: {workspace}")
        sys.exit(1)

    errors = []
    errors.extend(check_md(workspace))
    errors.extend(check_json(workspace))

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
