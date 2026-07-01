#!/usr/bin/env python3
"""
check_initial_analysis.py — 验证 docs/ 目录下 initial_analysis 文件。

用法：
    python check_initial_analysis.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def find_target_file(docs_dir: Path):
    """
    优先查找含 'initial_analysis' 的 .md 文件；
    若无则返回最新修改的 .md 文件。
    """
    candidates = list(docs_dir.glob("*initial_analysis*.md"))
    if candidates:
        return max(candidates, key=lambda p: p.stat().st_mtime)
    all_md = list(docs_dir.glob("*.md"))
    if all_md:
        return max(all_md, key=lambda p: p.stat().st_mtime)
    return None


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    docs_dir = workspace / "docs"

    # 1. docs/ 目录下至少有一个 .md 文件
    if not docs_dir.exists():
        print(f"FAILED: docs directory does not exist: {docs_dir}")
        sys.exit(1)

    target = find_target_file(docs_dir)
    if target is None:
        print("FAILED: no .md file found in docs/")
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8")
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    # 2. 包含 "127" / "127行" / "line 127"
    if not re.search(r'127', content):
        print(f"FAILED: file {target.name} does not contain '127' (line reference)")
        sys.exit(1)

    # 3. 包含 "60" / "60分钟" / "60 min"
    if not re.search(r'60', content):
        print(f"FAILED: file {target.name} does not contain '60' (offset reference)")
        sys.exit(1)

    # 4. 包含 "rule_007"
    if "rule_007" not in content:
        print(f"FAILED: file {target.name} does not contain 'rule_007'")
        sys.exit(1)

    # 5. 包含 TL;DR（不区分大小写）
    if not re.search(r'TL;DR|TLDR|tldr', content, re.IGNORECASE):
        print(f"FAILED: file {target.name} does not contain 'TL;DR' or 'TLDR'")
        sys.exit(1)

    # 6. 至少 3 个 "##" 开头的标题
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 3:
        print(
            f"FAILED: file {target.name} has only {len(headings)} '##' headings "
            "(expected >= 3)"
        )
        sys.exit(1)

    print(f"PASSED (checked: {target.name})")
    sys.exit(0)


if __name__ == "__main__":
    main()
