#!/usr/bin/env python3
"""
check_comprehensive_analysis.py — 验证 docs/YYYY-MM-DD_数据差异综合分析.md（q13）。

检查要点：
  1. docs/ 下存在含日期前缀的综合分析 .md 文件
  2. 第一个 ## 标题含"结论"或"总结"或"判断"（结论先行 P3）
  3. 含夸大倍数 "2.39"
  4. 含合同条款引用（"7.3" 或 "9.1" 或 "4.2"）
  5. >= 4 个 ## 标题
"""
import sys
import re
from pathlib import Path


def find_target_file(workspace: Path):
    """在 docs/ 目录下查找含日期前缀的综合分析 .md 文件。"""
    docs_dir = workspace / "docs"
    if not docs_dir.exists():
        return None, "docs/ directory does not exist"

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    md_files = list(docs_dir.glob("*.md"))

    # 优先查找含日期前缀且含综合分析关键词的文件
    for f in md_files:
        if date_prefix.match(f.name) and ("综合" in f.name or "数据差异" in f.name or "分析" in f.name):
            return f, None

    # 次选：最新的含日期前缀文件
    date_files = [f for f in md_files if date_prefix.match(f.name)]
    if date_files:
        latest = sorted(date_files, key=lambda p: p.stat().st_mtime, reverse=True)[0]
        return latest, None

    return None, "no date-prefixed .md file found in docs/"


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

    # 检查第一个 ## 标题是否含结论先行关键词
    first_h2 = None
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            first_h2 = stripped[3:].strip()
            break

    if first_h2 is None:
        failures.append("no '## ' heading found")
    else:
        conclusion_keywords = ["结论", "总结", "发现", "判断", "概况"]
        if not any(kw in first_h2 for kw in conclusion_keywords):
            failures.append(
                f"first '## ' heading '{first_h2}' does not contain conclusion keywords. "
                f"Expected one of: {conclusion_keywords}"
            )

    # 检查夸大倍数 2.39
    if "2.39" not in content:
        failures.append("exaggeration ratio '2.39' not found")

    # 检查合同条款引用
    has_clause = "7.3" in content or "9.1" in content or "4.2" in content
    if not has_clause:
        failures.append("no contract clause reference (7.3 / 9.1 / 4.2) found")

    # 检查 ## 标题数量
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 4:
        failures.append(f"'##' headings: {len(headings)} (expected >= 4)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print(f"PASSED (file: {target.name})")
    sys.exit(0)


if __name__ == "__main__":
    main()
