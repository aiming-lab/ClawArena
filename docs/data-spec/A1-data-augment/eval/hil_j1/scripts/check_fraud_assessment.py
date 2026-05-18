#!/usr/bin/env python3
"""
check_fraud_assessment.py — 验证 analysis/欺诈定性分析.md（q20）。

检查要点：
  1. analysis/ 下存在欺诈定性分析相关 .md 文件
  2. 含合同条款 "7.3"
  3. 含"欺诈"或"虚假"或"违约"
  4. >= 3 个欺诈构成要素被讨论
  5. >= 2 个 ## 标题
"""
import sys
import re
from pathlib import Path


def find_target_file(workspace: Path):
    """在 analysis/ 目录下查找欺诈定性分析相关的 .md 文件。"""
    analysis_dir = workspace / "analysis"
    if not analysis_dir.exists():
        return None, "analysis/ directory does not exist"

    exact = analysis_dir / "欺诈定性分析.md"
    if exact.exists():
        return exact, None

    md_files = list(analysis_dir.glob("*.md"))
    for f in md_files:
        if "欺诈" in f.name or "定性" in f.name or "违约" in f.name:
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

    # 检查合同条款 7.3
    if "7.3" not in content:
        failures.append("contract clause '7.3' not found")

    # 检查欺诈/虚假/违约
    fraud_keywords = ["欺诈", "虚假", "违约", "造假", "虚报", "误导"]
    has_fraud = any(kw in content for kw in fraud_keywords)
    if not has_fraud:
        failures.append(
            "fraud/violation keywords not found. Expected one of: " + str(fraud_keywords)
        )

    # 检查欺诈构成要素（至少 3 种要素被讨论）
    element_keywords = [
        "故意", "知情", "虚假陈述", "误导", "损害", "利益", "主观",
        "客观", "因果", "结果", "构成", "要素", "条件", "违反",
    ]
    found_elements = [kw for kw in element_keywords if kw in content]
    if len(found_elements) < 3:
        failures.append(
            f"fraud elements found: {found_elements} ({len(found_elements)}/3 required). "
            "Need at least 3 different fraud/violation elements."
        )

    # 检查 ## 标题数量
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 2:
        failures.append(f"'##' headings: {len(headings)} (expected >= 2)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print(f"PASSED (file: {target.name})")
    sys.exit(0)


if __name__ == "__main__":
    main()
