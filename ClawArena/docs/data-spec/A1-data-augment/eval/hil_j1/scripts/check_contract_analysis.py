#!/usr/bin/env python3
"""
check_contract_analysis.py — 验证 analysis/合同条款分析.md（q6）。

检查要点：
  1. analysis/ 下存在合同条款分析相关 .md 文件
  2. 含条款 "7.3" AND "截图"
  3. 含条款 "9.1" AND ("更正" OR "15个工作日" OR "15 个工作日")
  4. 含条款 "4.2" AND ("API" OR "verified")
  5. >= 3 个 ## 标题
"""
import sys
import re
from pathlib import Path


def find_target_file(workspace: Path):
    """在 analysis/ 目录下查找合同条款分析相关的 .md 文件。"""
    analysis_dir = workspace / "analysis"
    if not analysis_dir.exists():
        return None, "analysis/ directory does not exist"

    exact = analysis_dir / "合同条款分析.md"
    if exact.exists():
        return exact, None

    md_files = list(analysis_dir.glob("*.md"))
    for f in md_files:
        if "合同" in f.name or "条款" in f.name:
            return f, None

    if md_files:
        latest = sorted(md_files, key=lambda p: p.stat().st_mtime, reverse=True)[0]
        return latest, None

    return None, "no .md files found in analysis/"


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

    failures = []

    # 检查条款 7.3 + 截图
    if "7.3" not in content:
        failures.append("clause '7.3' not found")
    elif "截图" not in content:
        failures.append("clause 7.3 found but '截图' (screenshot) not mentioned")

    # 检查条款 9.1 + 更正/15个工作日
    if "9.1" not in content:
        failures.append("clause '9.1' not found")
    else:
        has_correction = "更正" in content or "15个工作日" in content or "15 个工作日" in content
        if not has_correction:
            failures.append("clause 9.1 found but '更正'/'15个工作日' not mentioned")

    # 检查条款 4.2 + API/verified
    if "4.2" not in content:
        failures.append("clause '4.2' not found")
    else:
        has_api = "API" in content or "api" in content.lower() or "verified" in content.lower()
        if not has_api:
            failures.append("clause 4.2 found but 'API'/'verified' not mentioned")

    # 检查 ## 标题数量
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 3:
        failures.append(f"'##' headings: {len(headings)} (expected >= 3)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print(f"PASSED (file: {target.name})")
    sys.exit(0)


if __name__ == "__main__":
    main()
