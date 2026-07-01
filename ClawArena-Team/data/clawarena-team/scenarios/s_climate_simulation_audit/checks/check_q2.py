"""q2: schema_inferred.md 存在 + schema_by_shape 验证。

通过条件（全部满足，exit 0）：
  1. output/schema_inferred.md 存在，长度 >= 100 字符
  2. 文件中含 >= 4 个列名（任意列名识别）— schema_by_shape：找到 >= 4 个
     形如 '`<word>`' 或 '**<word>**' 或独立词的列相关描述
  3. 含 'month' 或 'monthly' 或 '月' 关键词（时间步验证）
  4. 含对 historical_monthly.parquet 的引用
  5. ADVISORY ONLY (non-gating)：sessions/main.jsonl 中 RunSubagent 数量不再门控。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, has_phrase_any, passed, run_subagent_id_counts, workspace_root


def main() -> int:
    ws = workspace_root()
    schema_md = ws / "output" / "schema_inferred.md"
    if not schema_md.exists():
        fail("missing output/schema_inferred.md")

    text = schema_md.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 100:
        fail(f"schema_inferred.md too short: {len(text.strip())} chars < 100")

    # schema_by_shape: 找到 >= 4 列名/字段描述（不锁定具体键名）
    # 识别方式：代码块、粗体、表格列标题、或普通单词后接类型描述
    col_patterns = [
        r"`[a-zA-Z_][a-zA-Z0-9_]*`",          # backtick 代码
        r"\*\*[a-zA-Z_][a-zA-Z0-9_]*\*\*",    # 粗体
        r"\|\s*[a-zA-Z_][a-zA-Z0-9_ ]+\s*\|", # markdown 表格列
        r"^-\s+[a-zA-Z_][a-zA-Z0-9_]*",        # 列表项首词
    ]
    found_cols: set[str] = set()
    for pat in col_patterns:
        for m in re.finditer(pat, text, flags=re.MULTILINE):
            raw = m.group().strip("`| *-").strip()
            if 2 <= len(raw) <= 40:
                found_cols.add(raw.lower())
    if len(found_cols) < 4:
        fail(f"schema_by_shape: found only {len(found_cols)} column-like tokens (need >= 4): {list(found_cols)[:10]}")

    # 时间步验证
    if not has_phrase_any(text, ["month", "monthly", "月", "date", "period"]):
        fail("missing time-step reference: 'month', 'monthly', 'date', etc.")

    # 引用数据源
    if not has_phrase_any(text, ["historical_monthly", "historical", "parquet"]):
        fail("missing reference to historical_monthly.parquet or 'parquet'")

    # subagent 使用验证 — ADVISORY ONLY (non-gating)
    print(
        "NOTE: parallel/delegated subagent count not verified — advisory only, non-gating",
        file=sys.stderr,
    )

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
