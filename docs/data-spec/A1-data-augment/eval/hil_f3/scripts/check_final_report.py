#!/usr/bin/env python3
"""
check_final_report.py — 验证 docs/ 下含 "incident_report" 的最终报告 .md 文件。

用法：
    python check_final_report.py <workspace_path>
"""
import sys
import re
from pathlib import Path


def find_final_report(docs_dir: Path):
    """查找文件名含 'incident_report' 或 'v3_incident' 的 .md 文件。"""
    candidates = [
        p for p in docs_dir.glob("*.md")
        if re.search(r'incident_report|v3_incident', p.name, re.IGNORECASE)
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    docs_dir = workspace / "docs"

    # 1. 找到目标文件
    if not docs_dir.exists():
        print(f"FAILED: docs directory does not exist: {docs_dir}")
        sys.exit(1)

    target = find_final_report(docs_dir)
    if target is None:
        print(
            "FAILED: no .md file with 'incident_report' or 'v3_incident' "
            "found in docs/"
        )
        sys.exit(1)

    try:
        content = target.read_text(encoding="utf-8").strip()
    except Exception as e:
        print(f"FAILED: cannot read {target}: {e}")
        sys.exit(1)

    # 2. 包含 "rule_007"
    if "rule_007" not in content:
        print(f"FAILED: {target.name} does not contain 'rule_007'")
        sys.exit(1)

    # 3. 包含 "127"
    if "127" not in content:
        print(f"FAILED: {target.name} does not contain '127'")
        sys.exit(1)

    # 4. 包含 "60" 和 "分钟"
    if "60" not in content or "分钟" not in content:
        print(f"FAILED: {target.name} does not contain both '60' and '分钟'")
        sys.exit(1)

    # 5. 包含 "5" 和 "秒"
    if not re.search(r'\b5\b', content) or "秒" not in content:
        print(f"FAILED: {target.name} does not contain both '5' and '秒'")
        sys.exit(1)

    # 6. 包含 "7" 和 "天"
    if not re.search(r'\b7\b', content) or "天" not in content:
        print(f"FAILED: {target.name} does not contain both '7' and '天'")
        sys.exit(1)

    # 7. 包含 "2" 和 "near-miss" 或 "近失"
    has_2 = bool(re.search(r'\b2\b', content))
    has_nm = bool(re.search(r'near.miss|近失', content, re.IGNORECASE))
    if not (has_2 and has_nm):
        print(
            f"FAILED: {target.name} does not contain both '2' and 'near-miss'/'近失'"
        )
        sys.exit(1)

    # 8. 包含 "C1" 或 ("矛盾" 且 "CI")
    has_c1 = "C1" in content
    has_contradiction_ci = "矛盾" in content and "CI" in content
    if not (has_c1 or has_contradiction_ci):
        print(
            f"FAILED: {target.name} does not contain 'C1' or ('矛盾' + 'CI')"
        )
        sys.exit(1)

    # 9. 至少 5 个 "##" 开头的标题
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 5:
        print(f"FAILED: expected >= 5 '##' headings, found {len(headings)}")
        sys.exit(1)

    print(f"PASSED (checked: {target.name})")
    sys.exit(0)


if __name__ == "__main__":
    main()
