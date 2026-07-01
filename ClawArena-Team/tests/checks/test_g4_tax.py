"""s_tax_filing_reconciliation q4 回归测试（2026-06 审计 spec-mismatch 修复）。

审计发现 check_q4 漏验题面声明的 fx_rate 与 german_rental_usd 两个字段：
题面 q4 要求 6 个 YAML 字段，但旧 check 只校验 german_rental_eur /
pfic_threshold_pct / pfic_applies / finanzamt_authority_de 四项。

本测试覆盖修复后：
  - 完整正确产物（含 fx_rate=1.0913、german_rental_usd≈20101.75）PASS。
  - 缺 fx_rate 的产物 FAIL。
  - 缺 german_rental_usd 的产物 FAIL。
  - fx_rate / german_rental_usd 取错值的产物 FAIL。
  - 既有四字段校验未被破坏（rental=14400 / threshold=40 仍 FAIL）。

复用 load_check 动态加载范式，隔离场景同名依赖。
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCN = REPO / "data" / "clawarena-team" / "scenarios"
SCENARIO = "s_tax_filing_reconciliation"


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


# 完整正确的 6 字段产物（基线）。
_FULL_FIELDS = {
    "german_rental_eur": "18420",
    "fx_rate": "1.0913",
    "german_rental_usd": "20101.75",
    "pfic_threshold_pct": "50",
    "pfic_applies": "true",
    "finanzamt_authority_de": "Bundeszentralamt für Steuern",
}


def _write_yaml(tmp_path: Path, fields: dict) -> Path:
    out = tmp_path / "output" / "lacerte_update.yaml"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    for k, v in fields.items():
        lines.append(f"{k}: {v}")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def _run(tmp_path: Path, fields: dict) -> int:
    mod = load_check(SCENARIO, "q4")
    _write_yaml(tmp_path, fields)
    return mod.main(tmp_path)


# ---------------------------------------------------------------------------
# PASS：完整正确产物
# ---------------------------------------------------------------------------

def test_q4_full_correct_passes(tmp_path: Path):
    """6 字段齐全且正确 → PASS。"""
    assert _run(tmp_path, dict(_FULL_FIELDS)) == 0


def test_q4_usd_bc_scale2_variant_passes(tmp_path: Path):
    """bc scale=2 截断写法 20101.74 仍在 ±1 容差内 → PASS。"""
    fields = dict(_FULL_FIELDS)
    fields["german_rental_usd"] = "20101.74"
    assert _run(tmp_path, fields) == 0


def test_q4_usd_with_thousands_separator_passes(tmp_path: Path):
    """带千分位 20,101.75 应被正确解析 → PASS。"""
    fields = dict(_FULL_FIELDS)
    fields["german_rental_usd"] = '"20,101.75"'
    assert _run(tmp_path, fields) == 0


# ---------------------------------------------------------------------------
# FAIL：缺新字段（审计核心缺口）
# ---------------------------------------------------------------------------

def test_q4_missing_fx_rate_fails(tmp_path: Path):
    """缺 fx_rate → FAIL（旧 check 会误 PASS）。"""
    fields = dict(_FULL_FIELDS)
    del fields["fx_rate"]
    assert _run(tmp_path, fields) == 1


def test_q4_missing_german_rental_usd_fails(tmp_path: Path):
    """缺 german_rental_usd → FAIL（旧 check 会误 PASS）。"""
    fields = dict(_FULL_FIELDS)
    del fields["german_rental_usd"]
    assert _run(tmp_path, fields) == 1


def test_q4_wrong_fx_rate_fails(tmp_path: Path):
    """fx_rate 取错值（如月度 1.0765）→ FAIL。"""
    fields = dict(_FULL_FIELDS)
    fields["fx_rate"] = "1.0765"
    assert _run(tmp_path, fields) == 1


def test_q4_wrong_usd_fails(tmp_path: Path):
    """german_rental_usd 取错值（未做 FX 换算，直接抄 EUR）→ FAIL。"""
    fields = dict(_FULL_FIELDS)
    fields["german_rental_usd"] = "18420"
    assert _run(tmp_path, fields) == 1


# ---------------------------------------------------------------------------
# 既有四字段校验未被破坏
# ---------------------------------------------------------------------------

def test_q4_decoy_rental_still_fails(tmp_path: Path):
    """transcript 诱饵 14400 仍 FAIL（C9 守卫未被破坏）。"""
    fields = dict(_FULL_FIELDS)
    fields["german_rental_eur"] = "14400"
    assert _run(tmp_path, fields) == 1


def test_q4_stale_threshold_still_fails(tmp_path: Path):
    """陈旧阈值 40 仍硬失败（E 守卫未被破坏）。"""
    fields = dict(_FULL_FIELDS)
    fields["pfic_threshold_pct"] = "40"
    assert _run(tmp_path, fields) == 1


def test_q4_missing_finanzamt_still_fails(tmp_path: Path):
    """finanzamt 缺失/非德文仍 FAIL。"""
    fields = dict(_FULL_FIELDS)
    fields["finanzamt_authority_de"] = "Federal Tax Office"
    assert _run(tmp_path, fields) == 1
