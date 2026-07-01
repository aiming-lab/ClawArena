"""s_ab_test_postmortem q5 回归测试（2026-06 CHECK_AUDIT spec-mismatch 修复后）。

背景（docs/discussions/CHECK_AUDIT_2026-06.md，q5 spec-mismatch）：
题面原写 “至少 3 列、5 行 actual data”，但 tools/run_crosstab.py 对
data/exp_2421/mobile_us.parquet 实跑只有 2 个 variant（A=250 / B=250），表体恒为 2 行真实
数据。旧 check 用 “非空非分隔行 >= 5” 计数，会把 segment_parquet/variant_column/
converted_column 三行元数据 + 表头凑进去蒙混过关。

修复后 check_q5：
  - 门槛对齐数据可产出的行数（>= 2 行真实 variant 数据行）；
  - 排除元数据行与表头行，杜绝用元数据凑数。

复用 load_check 动态加载范式（隔离各场景同名 _common）。
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SCN = REPO / "data" / "clawarena-team" / "scenarios"
SCENARIO = "s_ab_test_postmortem"


def load_check(scenario: str, qid: str):
    checks_dir = SCN / scenario / "checks"
    path = checks_dir / f"check_{qid}.py"
    sys.modules.pop("_common", None)
    sys.path.insert(0, str(checks_dir))
    try:
        spec = importlib.util.spec_from_file_location(f"chk_{scenario}_{qid}", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    finally:
        if str(checks_dir) in sys.path:
            sys.path.remove(str(checks_dir))
        sys.modules.pop("_common", None)


def _run_q5(tmp_path: Path, content: str | None) -> int:
    """把 content 写入 findings/replication.md 并执行 check_q5；content=None 表示不创建文件。

    check 以 fail()/passed() 调用 sys.exit，故用 SystemExit 捕获退出码。
    """
    mod = load_check(SCENARIO, "q5")
    if content is not None:
        rep = tmp_path / "findings" / "replication.md"
        rep.parent.mkdir(parents=True, exist_ok=True)
        rep.write_text(content, encoding="utf-8")
    argv = sys.argv
    sys.argv = ["check_q5.py", str(tmp_path)]
    try:
        try:
            rc = mod.main()
        except SystemExit as e:  # passed()/fail() 走 sys.exit
            rc = e.code if isinstance(e.code, int) else 1
        return rc
    finally:
        sys.argv = argv


# tools/run_crosstab.py data/exp_2421/mobile_us.parquet 的真实输出（tab 分隔）。
_REAL_CROSSTAB = (
    "segment_parquet\tmobile_us\n"
    "variant_column\tvariant\n"
    "converted_column\tconverted\n"
    "---\n"
    "variant\tsessions\tconverted\tcvr\tconversion_delta\n"
    "A\t250\t32\t0.1280\tbaseline\n"
    "B\t250\t24\t0.0960\t-25.00%\n"
)

# 旧 check 漏洞复现：只有元数据行 + 表头、零真实 variant 数据行，靠 3 行元数据凑到 “>= 5 行”。
_META_PADDING_ONLY = (
    "segment_parquet\tmobile_us\n"
    "variant_column\tvariant\n"
    "converted_column\tconverted\n"
    "---\n"
    "variant\tsessions\tconverted\tcvr\tconversion_delta\n"
)

# markdown table 形态的真实交叉表（2 行 variant 数据）。
_MARKDOWN_CROSSTAB = (
    "# Replication of mobile_us crosstab\n\n"
    "| variant | sessions | converted | cvr | conversion_delta |\n"
    "| --- | --- | --- | --- | --- |\n"
    "| A | 250 | 32 | 0.1280 | baseline |\n"
    "| B | 250 | 24 | 0.0960 | -25.00% |\n"
)


def test_q5_real_crosstab_passes(tmp_path: Path):
    """run_crosstab 真实输出（2 行 variant 数据 + delta）应 PASS。"""
    assert _run_q5(tmp_path, _REAL_CROSSTAB) == 0


def test_q5_markdown_crosstab_passes(tmp_path: Path):
    """markdown table 形态的真实交叉表（2 行 variant 数据）同样 PASS。"""
    assert _run_q5(tmp_path, _MARKDOWN_CROSSTAB) == 0


def test_q5_metadata_padding_now_fails(tmp_path: Path):
    """旧漏洞：仅元数据行 + 表头、零真实 variant 数据行，修复后必须 FAIL（不许元数据凑数）。"""
    assert _run_q5(tmp_path, _META_PADDING_ONLY) != 0


def test_q5_missing_file_fails(tmp_path: Path):
    """缺 findings/replication.md 应 FAIL。"""
    assert _run_q5(tmp_path, None) != 0


def test_q5_no_delta_fails(tmp_path: Path):
    """有 2 行数据但无 conversion delta 指示应 FAIL。"""
    no_delta = (
        "| variant | sessions | converted |\n"
        "| --- | --- | --- |\n"
        "| A | 250 | 32 |\n"
        "| B | 250 | 24 |\n"
    )
    assert _run_q5(tmp_path, no_delta) != 0
