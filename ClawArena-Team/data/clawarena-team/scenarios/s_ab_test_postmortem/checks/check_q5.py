"""q5: findings/replication.md 存在 + schema-by-shape 输出 >= 3 列 + 含 run_crosstab 真实
variant 数据行（A/B 两组）+ 含 conversion delta。

数据现实（实跑 tools/run_crosstab.py data/exp_2421/mobile_us.parquet 确认）：
该工具是 variant × conversion 交叉表，mobile_us 只有 2 个 variant（A=250 / B=250），
表体恒为 2 行真实数据（外加 1 行表头与 3 行 segment_parquet/variant_column/
converted_column 元数据）。题面原写 “5 rows of actual data” 数据根本不支撑，旧 check 用
“非空非分隔行 >= 5” 计数会把 3 行元数据 + 表头凑进去蒙混过关。此处改为：只认带 >= 3 个
tab/| 字段、且非元数据、非表头的真实 variant 数据行，门槛对齐数据可产出的 2 行。

通过条件（全部满足，exit 0）：
  1. findings/replication.md 存在
  2. crosstab 表头/数据行含 >= 3 列（tab 分隔或 markdown table | 分隔）
  3. 含 >= 2 行真实 variant 数据行（排除 segment_parquet/variant_column/converted_column
     元数据行与表头行；不再用元数据行凑数）
  4. 含 conversion delta 指示（'conversion_delta' / '%' / 'lift' / 'delta'）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import fail, passed, workspace_root

# run_crosstab.py 头部固定输出的元数据行 key（非表体数据）。
_META_KEYS = ("segment_parquet", "variant_column", "converted_column")
# run_crosstab.py 表头行字段（用于排除表头，避免把表头当数据行）。
_HEADER_TOKENS = {"variant", "sessions", "converted", "cvr", "conversion_delta"}


def _split_fields(line: str) -> list[str]:
    """把一行拆成字段（tab 分隔优先，其次 markdown | 分隔）。"""
    if "\t" in line:
        return [p.strip() for p in line.split("\t")]
    if "|" in line:
        return [p.strip() for p in line.split("|") if p.strip()]
    return []


def _count_table_cols(line: str) -> int:
    return len(_split_fields(line))


def _is_meta_line(line: str) -> bool:
    """run_crosstab 头部元数据行：第一个字段是固定 key。"""
    fields = _split_fields(line)
    return bool(fields) and fields[0] in _META_KEYS


def _is_header_line(fields: list[str]) -> bool:
    """crosstab 表头行：字段集合与已知表头 token 高度重合。"""
    lowered = {f.lower() for f in fields}
    return len(lowered & _HEADER_TOKENS) >= 3


def main() -> int:
    ws = workspace_root()
    rep = ws / "findings" / "replication.md"
    if not rep.exists():
        fail("missing findings/replication.md")
    text = rep.read_text(encoding="utf-8", errors="ignore")
    if len(text.strip()) < 30:
        fail("findings/replication.md too short")

    lines = [ln for ln in text.splitlines() if ln.strip()]

    # 列数 >= 3 的表格行（表头或数据），用于验证至少存在一张 >= 3 列的交叉表。
    wide_lines = [ln for ln in lines if _count_table_cols(ln) >= 3]
    if len(wide_lines) < 2:
        fail("findings/replication.md does not contain a table with >= 3 columns "
             "(expect tab-separated or markdown table from run_crosstab.py output)")

    # 真实 variant 数据行：>= 3 列、非分隔线、非元数据行、非表头行。
    # 不再把 segment_parquet/variant_column/converted_column 元数据行或表头算作数据。
    data_rows = []
    for ln in lines:
        if re.match(r"^[-|=\s]+$", ln):  # 纯分隔线
            continue
        fields = _split_fields(ln)
        if len(fields) < 3:
            continue
        if _is_meta_line(ln):
            continue
        if _is_header_line(fields):
            continue
        data_rows.append(ln)

    # mobile_us 只有 A/B 两个 variant，真实表体恒为 2 行；门槛对齐数据可产出的行数。
    if len(data_rows) < 2:
        fail(f"findings/replication.md has too few real crosstab data rows "
             f"({len(data_rows)} < 2); metadata/header lines do not count")

    # 含 conversion delta 指示。
    if not re.search(r"conversion_delta|delta|lift|\+\d|\-\d+\.\d+%?|\d+\.\d+%", text, flags=re.IGNORECASE):
        fail("findings/replication.md lacks conversion delta indicator")

    passed()
    return 0


if __name__ == "__main__":
    sys.exit(main())
