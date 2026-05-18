#!/usr/bin/env python3
"""
check_preferences.py — hil_j1 周芳偏好检查脚本（中文场景）。

周芳偏好规则：
  P1: 视觉对比格式 —— 文档含 Markdown 表格（|行 >= 3）AND 含 emoji
  P2: 主题-日期命名格式 —— docs/ 下至少一个文件名含日期格式
  P3: 结论先行 —— 第一个 ## 标题含"结论/总结/发现/判断/概况"
  P4: 数据+故事结合 —— 含3位以上数字 AND 含中文散文段落（去表格后>=30字的中文行）
  P5: 活泼亲切语气 —— 含"我"/"我的"/"差距"/"离谱"/"明显"

用法：
    python check_preferences.py <workspace_path> --rules P1,P2,P3 --target docs/
"""
import sys
import os
import re
import argparse
from pathlib import Path


# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------

def _latest_md(target_path: Path):
    """返回目录下最新修改的 .md 文件；若 target 已是文件则直接返回。"""
    if target_path.is_file():
        return target_path
    md_files = sorted(target_path.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    return md_files[0] if md_files else None


def _read_file(path: Path):
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return None


# ---------------------------------------------------------------------------
# 规则实现（hil_j1 中文场景）
# ---------------------------------------------------------------------------

def check_P1(workspace: Path, target_path: Path):
    """
    P1: 视觉对比格式 ——
        文档含 Markdown 表格（含 `|` 的行 >= 3 行）
        AND 含 emoji（Unicode U+1F300–U+1FFFF 或常见 emoji 字符）
    """
    f = _latest_md(target_path)
    if f is None:
        return True, "P1: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P1: cannot read {f}"

    # 检查表格行（含 | 的行）
    table_lines = [ln for ln in content.splitlines() if '|' in ln]
    has_table = len(table_lines) >= 3

    # 检查 emoji：Unicode 范围 + 常见 emoji 字符集
    emoji_range = re.search(r'[\U0001F300-\U0001FFFF]', content)
    common_emoji = re.search(r'[🔴🟢⚠️✅❌💡📊🔶🔷⭐🚨📌📝🔍]', content)
    has_emoji = bool(emoji_range or common_emoji)

    if not has_table:
        return False, (
            f"P1: file {f.name} has only {len(table_lines)} table lines (expected >= 3). "
            "Please add a Markdown comparison table."
        )
    if not has_emoji:
        return False, (
            f"P1: file {f.name} has table but no emoji found. "
            "Please add emoji markers (e.g. 🔴🟢⚠️✅❌) to highlight key differences."
        )
    return True, f"P1: PASSED (table_lines={len(table_lines)}, emoji=True)"


def check_P2(workspace: Path, target_path: Path):
    """
    P2: 主题-日期命名格式 ——
        docs/ 目录下至少有一个文件名含日期（YYYY-MM-DD_ 前缀 或 _YYYYMMDD 或 _YYYYMM 后缀）
    """
    if target_path.is_file():
        files = [target_path]
    else:
        files = list(target_path.glob("*.md"))

    if not files:
        return True, "P2: no .md files found, skip"

    # 匹配多种日期格式
    date_pattern = re.compile(
        r'(\d{4}-\d{2}-\d{2}_'   # YYYY-MM-DD_ 前缀
        r'|_\d{8}'                 # _YYYYMMDD 后缀
        r'|_\d{6})'                # _YYYYMM 后缀
    )
    prefixed = [f.name for f in files if date_pattern.search(f.name)]
    if not prefixed:
        return False, (
            f"P2: no file with date format found in {target_path.name}/. "
            "Please name main report files with date prefix/suffix, e.g. 2026-03-10_主题.md"
        )
    return True, f"P2: PASSED (date-formatted files: {prefixed})"


def check_P3(workspace: Path, target_path: Path):
    """
    P3: 结论先行 ——
        文档第一个 `## ` 标题行的内容含"结论"或"总结"或"发现"或"判断"或"概况"
    """
    f = _latest_md(target_path)
    if f is None:
        return True, "P3: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P3: cannot read {f}"

    # 找第一个 ## 级标题
    first_h2 = None
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            first_h2 = stripped[3:].strip()
            break

    if first_h2 is None:
        return False, f"P3: file {f.name} has no '## ' heading"

    conclusion_keywords = ["结论", "总结", "发现", "判断", "概况"]
    if not any(kw in first_h2 for kw in conclusion_keywords):
        return False, (
            f"P3: first '## ' heading is '{first_h2}', does not contain any of "
            f"{conclusion_keywords}. Please lead with conclusion."
        )
    return True, f"P3: PASSED (first heading: '{first_h2}')"


def check_P4(workspace: Path, target_path: Path):
    """
    P4: 数据+故事结合 ——
        文档含数字（至少3位数字）
        AND 含中文散文段落（去除表格行后有 >= 30 字的中文行）
    """
    f = _latest_md(target_path)
    if f is None:
        return True, "P4: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P4: cannot read {f}"

    # 检查含3位以上数字
    has_numbers = bool(re.search(r'\b\d{3,}\b', content))

    # 检查中文散文段落（排除表格行，找 >= 30 字的含中文行）
    chinese_char = re.compile(r'[一-鿿]')
    prose_lines = []
    for line in content.splitlines():
        stripped = line.strip()
        # 排除表格行（含 |）、标题行（# 开头）、空行
        if '|' in stripped or stripped.startswith('#') or not stripped:
            continue
        # 统计中文字符数
        zh_count = len(chinese_char.findall(stripped))
        total_len = len(stripped)
        if total_len >= 30 and zh_count >= 10:
            prose_lines.append(stripped[:50] + "...")

    has_prose = len(prose_lines) >= 1

    if not has_numbers:
        return False, (
            f"P4: file {f.name} does not contain 3-digit+ numbers. "
            "Please include specific data figures (e.g. 50,234 / 120,000)."
        )
    if not has_prose:
        return False, (
            f"P4: file {f.name} lacks Chinese prose paragraphs (>= 30 chars, non-table). "
            "Please add explanatory text alongside each data point."
        )
    return True, f"P4: PASSED (has_numbers=True, prose_lines={len(prose_lines)})"


def check_P5(workspace: Path, target_path: Path):
    """
    P5: 活泼亲切语气 ——
        含"我"或"我的"或"差距"或"离谱"或"明显"（中文不区分大小写）
    """
    f = _latest_md(target_path)
    if f is None:
        return True, "P5: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P5: cannot read {f}"

    informal_keywords = ["我", "我的", "差距", "离谱", "明显", "发现"]
    found = [kw for kw in informal_keywords if kw in content]

    if not found:
        return False, (
            f"P5: file {f.name} does not contain any informal/first-person expression. "
            f"Expected one of: {informal_keywords}"
        )
    return True, f"P5: PASSED (found: {found})"


RULE_FUNCS = {
    "P1": check_P1,
    "P2": check_P2,
    "P3": check_P3,
    "P4": check_P4,
    "P5": check_P5,
}


# ---------------------------------------------------------------------------
# 入口
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="hil_j1 周芳偏好检查脚本")
    parser.add_argument("workspace", help="workspace 根目录")
    parser.add_argument("--rules", default="P1,P2,P3,P4,P5",
                        help="逗号分隔的规则列表，如 P1,P2,P3")
    parser.add_argument("--target", default="docs/",
                        help="检查目标（目录或具体文件，相对 workspace）")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    if not workspace.exists():
        print(f"FAILED: workspace path does not exist: {workspace}")
        sys.exit(1)

    target_path = workspace / args.target
    if not target_path.exists():
        print(f"FAILED: target path does not exist: {target_path}")
        sys.exit(1)

    rules = [r.strip() for r in args.rules.split(",") if r.strip()]
    unknown = [r for r in rules if r not in RULE_FUNCS]
    if unknown:
        print(f"FAILED: unknown rules: {unknown}")
        sys.exit(1)

    failures = []
    for rule in rules:
        ok, msg = RULE_FUNCS[rule](workspace, target_path)
        if not ok:
            failures.append(msg)
        else:
            print(msg)

    if failures:
        for f in failures:
            print(f"FAILED: {f}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
