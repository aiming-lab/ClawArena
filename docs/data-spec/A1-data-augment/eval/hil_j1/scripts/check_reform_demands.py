#!/usr/bin/env python3
"""
check_reform_demands.py — 验证 analysis/MCN整改要求清单.md（q27）。

检查要点：
  1. analysis/ 下存在 MCN 整改要求清单相关 .md 文件
  2. >= 4 个整改要求（"API"/"历史"/"赔偿"/"透明"/"审计"/"数据" 等至少 4 种）
  3. 含"API"数据要求
  4. 含"历史"审计要求
  5. 含"赔偿"要求
  6. >= 3 个 ## 标题
"""
import sys
import re
from pathlib import Path


def find_target_file(workspace: Path):
    """在 analysis/ 目录下查找 MCN 整改要求清单相关的 .md 文件。"""
    analysis_dir = workspace / "analysis"
    if not analysis_dir.exists():
        return None, "analysis/ directory does not exist"

    exact = analysis_dir / "MCN整改要求清单.md"
    if exact.exists():
        return exact, None

    md_files = list(analysis_dir.glob("*.md"))
    for f in md_files:
        if "整改" in f.name or "要求" in f.name or "清单" in f.name:
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

    # 检查整改要求（至少 4 种）
    demand_categories = {
        "API数据": ["API", "api", "官方数据", "平台数据"],
        "历史审计": ["历史", "审计", "回溯"],
        "赔偿": ["赔偿", "补偿", "索赔"],
        "透明度": ["透明", "公开", "透明度"],
        "截图替换": ["截图", "替换", "改用"],
        "合规机制": ["合规", "机制", "未来", "规范"],
    }
    found_demands = []
    for demand_name, keywords in demand_categories.items():
        if any(kw in content for kw in keywords):
            found_demands.append(demand_name)

    if len(found_demands) < 4:
        failures.append(
            f"demand categories found: {found_demands} ({len(found_demands)}/4 required). "
            "Need at least 4 of: API数据, 历史审计, 赔偿, 透明度, 截图替换, 合规机制"
        )

    # 检查 API 数据要求
    if "API" not in content and "api" not in content.lower():
        failures.append("API data requirement not found")

    # 检查历史审计要求
    if "历史" not in content and "审计" not in content:
        failures.append("historical audit requirement not found")

    # 检查赔偿要求
    if "赔偿" not in content and "补偿" not in content:
        failures.append("compensation/penalty requirement not found")

    # 检查 ## 标题数量
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 3:
        failures.append(f"'##' headings: {len(headings)} (expected >= 3)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print(f"PASSED (file: {target.name}, demands: {found_demands})")
    sys.exit(0)


if __name__ == "__main__":
    main()
