#!/usr/bin/env python3
"""
check_brand_risk.py — 验证 analysis/品牌方风险评估.md（q16）。

检查要点：
  1. analysis/ 下存在品牌方风险评估相关 .md 文件
  2. 含 "品牌" 或 "赵敏"
  3. >= 3 个风险点（含"风险"或"损失"或"纠纷"或"影响"等关键词 >= 3 种）
  4. 含"合同"风险相关内容
  5. >= 2 个 ## 标题
"""
import sys
import re
from pathlib import Path


def find_target_file(workspace: Path):
    """在 analysis/ 目录下查找品牌方风险评估相关的 .md 文件。"""
    analysis_dir = workspace / "analysis"
    if not analysis_dir.exists():
        return None, "analysis/ directory does not exist"

    exact = analysis_dir / "品牌方风险评估.md"
    if exact.exists():
        return exact, None

    md_files = list(analysis_dir.glob("*.md"))
    for f in md_files:
        if "品牌" in f.name or "风险" in f.name or "赵敏" in f.name:
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

    # 检查品牌方/赵敏
    if "品牌" not in content and "赵敏" not in content:
        failures.append("'品牌' or '赵敏' not found in content")

    # 检查风险点（至少 3 种风险关键词出现）
    risk_keywords = [
        "风险", "损失", "纠纷", "影响", "信任", "决策", "虚假数据",
        "营销", "赔偿", "法务", "合规", "声誉",
    ]
    found_risks = [kw for kw in risk_keywords if kw in content]
    if len(found_risks) < 3:
        failures.append(
            f"risk keywords found: {found_risks} ({len(found_risks)}/3 required). "
            "Need at least 3 different risk points."
        )

    # 检查合同风险
    if "合同" not in content:
        failures.append("'合同' (contract) risk not mentioned")

    # 检查 ## 标题数量
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 2:
        failures.append(f"'##' headings: {len(headings)} (expected >= 2)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print(f"PASSED (file: {target.name}, risk keywords: {found_risks})")
    sys.exit(0)


if __name__ == "__main__":
    main()
