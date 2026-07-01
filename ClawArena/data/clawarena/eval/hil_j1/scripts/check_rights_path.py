#!/usr/bin/env python3
"""
check_rights_path.py — 验证 analysis/维权路径分析.md（q22）。

检查要点：
  1. analysis/ 下存在维权路径分析相关 .md 文件
  2. 含合同条款 "9.1"
  3. >= 3 个维权路径（"更正"/"解除"/"赔偿"/"举报"/"协商" 等至少 3 种）
  4. 含"更正"选项
  5. 含"解除"或"赔偿"选项
  6. >= 3 个 ## 标题
"""
import sys
import re
from pathlib import Path


def find_target_file(workspace: Path):
    """在 analysis/ 目录下查找维权路径分析相关的 .md 文件。"""
    analysis_dir = workspace / "analysis"
    if not analysis_dir.exists():
        return None, "analysis/ directory does not exist"

    exact = analysis_dir / "维权路径分析.md"
    if exact.exists():
        return exact, None

    md_files = list(analysis_dir.glob("*.md"))
    for f in md_files:
        if "维权" in f.name or "路径" in f.name or "权益" in f.name:
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

    # 检查合同条款 9.1
    if "9.1" not in content:
        failures.append("contract clause '9.1' not found")

    # 检查维权路径（至少 3 种）
    rights_options = {
        "更正": ["更正", "纠正", "修正"],
        "解除": ["解除", "终止", "撤销"],
        "赔偿": ["赔偿", "补偿", "索赔"],
        "举报": ["举报", "投诉", "平台"],
        "协商": ["协商", "谈判", "沟通", "重新核算"],
        "法律": ["法律", "法务", "诉讼", "仲裁"],
    }
    found_options = []
    for option_name, keywords in rights_options.items():
        if any(kw in content for kw in keywords):
            found_options.append(option_name)

    if len(found_options) < 3:
        failures.append(
            f"rights options found: {found_options} ({len(found_options)}/3 required). "
            "Need at least 3 of: 更正, 解除, 赔偿, 举报, 协商, 法律"
        )

    # 检查"更正"选项
    if "更正" not in content and "纠正" not in content and "修正" not in content:
        failures.append("'更正' (correction) option not found")

    # 检查"解除"或"赔偿"选项
    has_terminate_or_compensate = (
        "解除" in content or "终止" in content or
        "赔偿" in content or "补偿" in content or "索赔" in content
    )
    if not has_terminate_or_compensate:
        failures.append("'解除' (termination) or '赔偿' (compensation) option not found")

    # 检查 ## 标题数量
    headings = [ln for ln in content.splitlines() if ln.strip().startswith("##")]
    if len(headings) < 3:
        failures.append(f"'##' headings: {len(headings)} (expected >= 3)")

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print(f"PASSED (file: {target.name}, options: {found_options})")
    sys.exit(0)


if __name__ == "__main__":
    main()
