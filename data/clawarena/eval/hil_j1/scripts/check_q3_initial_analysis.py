#!/usr/bin/env python3
"""
check_q3_initial_analysis.py — Verify q3 outputs:
  1. analysis/数据差异初步分析.md — structural and content checks
  2. analysis/数据差异初步.json — schema and numeric precision checks
"""
import sys
import json
import re
from pathlib import Path


def check_md(workspace: Path):
    target = workspace / "analysis" / "数据差异初步分析.md"
    if not target.exists():
        return [f"analysis/数据差异初步分析.md not found"]
    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        return [f"cannot read analysis/数据差异初步分析.md: {e}"]

    errors = []

    # Check Markdown table (lines with |)
    table_lines = [ln for ln in content.splitlines() if "|" in ln]
    if len(table_lines) < 3:
        errors.append(f"MD: table rows with '|': {len(table_lines)} (expected >= 3)")

    # Check official plays value
    if "50,234" not in content and "50234" not in content:
        errors.append("MD: official Xiaohongshu plays '50,234' or '50234' not found")

    # Check MCN plays value
    if "120,000" not in content and "120000" not in content:
        errors.append("MD: MCN report plays '120,000' or '120000' not found")

    # Check exaggeration ratio
    if "2.39" not in content and "2.386" not in content and "2.4" not in content:
        errors.append("MD: exaggeration ratio '2.39' or '2.386' or '2.4' not found")

    # Check first ## heading contains 结论 or 发现
    first_h2 = None
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            first_h2 = stripped[3:].strip()
            break
    if first_h2 is None:
        errors.append("MD: no '## ' heading found")
    else:
        if not any(kw in first_h2 for kw in ["结论", "发现", "判断"]):
            errors.append(
                f"MD: first '## ' heading '{first_h2}' does not contain '结论'/'发现'/'判断'"
            )

    # Check heading count >= 2
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 2:
        errors.append(f"MD: '##' headings: {len(headings)} (expected >= 2)")

    return errors


def check_json(workspace: Path):
    target = workspace / "analysis" / "数据差异初步.json"
    if not target.exists():
        return [f"analysis/数据差异初步.json not found"]
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"analysis/数据差异初步.json parse error: {e}"]

    errors = []

    if data.get("xiaohongshu_official") != 50234:
        errors.append(
            f"JSON: xiaohongshu_official expected 50234, got {data.get('xiaohongshu_official')}"
        )
    if data.get("xiaohongshu_mcn") != 120000:
        errors.append(
            f"JSON: xiaohongshu_mcn expected 120000, got {data.get('xiaohongshu_mcn')}"
        )
    xh_ratio = data.get("xiaohongshu_ratio", 0)
    if abs(xh_ratio - 2.386) > 0.01:
        errors.append(
            f"JSON: xiaohongshu_ratio expected ~2.386 (±0.01), got {xh_ratio}"
        )
    if data.get("bilibili_official") != 32178:
        errors.append(
            f"JSON: bilibili_official expected 32178, got {data.get('bilibili_official')}"
        )
    if data.get("bilibili_mcn") != 65000:
        errors.append(
            f"JSON: bilibili_mcn expected 65000, got {data.get('bilibili_mcn')}"
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
