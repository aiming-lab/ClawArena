#!/usr/bin/env python3
"""
check_q6_brand_material.py — Verify q6 outputs:
  1. analysis/品牌方材料分析.md — contains screenshot mention, clause 7.3, clause 9.1, >= 3 headings
  2. analysis/数据来源对比.json — schema checks: compliant==false, xiaohongshu_official==50234, bilibili_official==32178
"""
import sys
import json
from pathlib import Path


def check_md(workspace: Path):
    target = workspace / "analysis" / "品牌方材料分析.md"
    if not target.exists():
        return ["analysis/品牌方材料分析.md not found"]
    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        return [f"cannot read analysis/品牌方材料分析.md: {e}"]

    errors = []

    # Must mention screenshot / 截图
    if "截图" not in content and "screenshot" not in content.lower() and "PNG" not in content:
        errors.append("MD: '截图' or 'screenshot' or 'PNG' not found")

    # Must reference clause 7.3
    if "7.3" not in content:
        errors.append("MD: contract clause '7.3' not found")

    # Must reference clause 9.1
    if "9.1" not in content:
        errors.append("MD: contract clause '9.1' not found")

    # Check heading count >= 3
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 3:
        errors.append(f"MD: '##' headings: {len(headings)} (expected >= 3)")

    return errors


def check_json(workspace: Path):
    target = workspace / "analysis" / "数据来源对比.json"
    if not target.exists():
        return ["analysis/数据来源对比.json not found"]
    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"analysis/数据来源对比.json parse error: {e}"]

    errors = []

    if data.get("compliant") is not False:
        errors.append(f"JSON: compliant expected false, got {data.get('compliant')!r}")
    if data.get("xiaohongshu_official") != 50234:
        errors.append(
            f"JSON: xiaohongshu_official expected 50234, got {data.get('xiaohongshu_official')}"
        )
    if data.get("bilibili_official") != 32178:
        errors.append(
            f"JSON: bilibili_official expected 32178, got {data.get('bilibili_official')}"
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
