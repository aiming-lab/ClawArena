#!/usr/bin/env python3
"""
check_q14_evidence_matrix.py — Verify q14 outputs (M3+M4):
  1. analysis/数据欺诈证据矩阵.md — four dimensions, '2.39', '2.02', >= 4 headings or table rows
  2. analysis/欺诈证据.json — array of 4 elements, all exceeds_2x==true,
     first element ratio in range 2.3-2.5
"""
import sys
import json
from pathlib import Path


def check_md(workspace: Path):
    target = workspace / "analysis" / "数据欺诈证据矩阵.md"
    if not target.exists():
        return ["analysis/数据欺诈证据矩阵.md not found"]
    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        return [f"cannot read analysis/数据欺诈证据矩阵.md: {e}"]

    errors = []

    # Check four evidence dimensions appear in content
    # Small Red Book plays, Bilibili plays, likes, favorites
    dim_keywords = [
        ["小红书", "播放"],
        ["B站", "bilibili", "哔哩"],
        ["点赞"],
        ["收藏"],
    ]
    for dim in dim_keywords:
        if not any(kw.lower() in content.lower() for kw in dim):
            errors.append(f"evidence dimension not found (expected one of: {dim})")

    # Check ratios
    if "2.39" not in content and "2.386" not in content:
        errors.append("ratio '2.39' or '2.386' not found")
    if "2.02" not in content and "2.021" not in content:
        errors.append("ratio '2.02' or '2.021' not found")

    # Check headings >= 4 OR table rows >= 4
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    table_lines = [ln for ln in content.splitlines() if "|" in ln and "---" not in ln]
    if len(headings) < 4 and len(table_lines) < 4:
        errors.append(
            f"'##' headings: {len(headings)} (expected >= 4) OR table rows: {len(table_lines)} (expected >= 4)"
        )

    return errors


def check_json(workspace: Path):
    target = workspace / "analysis" / "欺诈证据.json"
    if not target.exists():
        return ["analysis/欺诈证据.json not found"]
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"analysis/欺诈证据.json parse error: {e}"]

    errors = []

    if not isinstance(data, list):
        return ["JSON: expected array at top level"]

    if len(data) != 4:
        errors.append(f"JSON: array length expected 4, got {len(data)}")
        return errors  # Cannot check individual elements safely

    # All elements must have exceeds_2x == true
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            errors.append(f"JSON: element {i} is not an object")
            continue
        if item.get("exceeds_2x") is not True:
            errors.append(
                f"JSON: element {i} exceeds_2x expected true, got {item.get('exceeds_2x')!r}"
            )
        # Check required fields
        for field in ["dimension", "official", "mcn_report", "ratio"]:
            if field not in item:
                errors.append(f"JSON: element {i} missing field '{field}'")

    # First element ratio should be in range 2.3-2.5 (Xiaohongshu plays)
    if data and isinstance(data[0], dict):
        ratio = data[0].get("ratio", 0)
        try:
            ratio_f = float(ratio)
            if not (2.3 <= ratio_f <= 2.5):
                errors.append(
                    f"JSON: first element ratio expected in range [2.3, 2.5], got {ratio_f}"
                )
        except (TypeError, ValueError):
            errors.append(f"JSON: first element ratio is not a number: {ratio!r}")

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
