#!/usr/bin/env python3
"""
check_formal_statement.py — 验证 docs/YYYY-MM-DD_向品牌方的正式声明.md（q26）。

检查要点：
  1. docs/ 下存在含日期前缀的正式声明 .md 文件
  2. 含"赵敏"或"品牌方"
  3. 含 "50,234" 或 "50234" 或其他官方数据
  4. 含"重新核算"或"更正"
  5. >= 4 个 ## 标题
"""
import sys
import re
from pathlib import Path


def find_target_file(workspace: Path):
    """在 docs/ 目录下查找含日期前缀的正式声明 .md 文件。"""
    docs_dir = workspace / "docs"
    if not docs_dir.exists():
        return None, "docs/ directory does not exist"

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    md_files = list(docs_dir.glob("*.md"))

    # 优先查找含日期前缀且含声明关键词的文件
    for f in md_files:
        if date_prefix.match(f.name) and ("声明" in f.name or "品牌方" in f.name or "赵敏" in f.name):
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

    # 检查赵敏/品牌方
    if "赵敏" not in content and "品牌方" not in content:
        failures.append("'赵敏' or '品牌方' not found in content")

    # 检查官方数据
    official_data_keywords = ["50,234", "50234", "官方数据", "后台数据", "32,178", "32178"]
    has_official = any(kw in content for kw in official_data_keywords)
    if not has_official:
        failures.append(
            "official data not found. Expected one of: " + str(official_data_keywords)
        )

    # 检查重新核算/更正
    correction_keywords = ["重新核算", "更正", "纠正", "核算", "重新计算"]
    has_correction = any(kw in content for kw in correction_keywords)
    if not has_correction:
        failures.append(
            "'重新核算' or '更正' not found. Expected one of: " + str(correction_keywords)
        )

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
