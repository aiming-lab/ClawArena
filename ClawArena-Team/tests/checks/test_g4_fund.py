"""G4 fund DD 回归测试 — s_fund_due_diligence q4 spec/data 三方矛盾修复绑定测试。

覆盖审计 docs/discussions/CHECK_AUDIT_2026-06.md 中的 spec-mismatch 缺陷：

  s_fund_due_diligence q4 — 题面/数据/check 三方自相矛盾。
    题面原文要求 agent 用 u1 CSV 的 fee_adj_return_pct 列、对 live 期(2023+)
    "直接从 backtest 重算 post-cost Sharpe"，且 u1 _index.md 宣称该计算应得 ~1.59。
    但实测 updates/u1/backtest_data/apex_backtest_2018_2025.csv 日期只到 2020-11-24
    (date>=2023 行数=0)、fee_adj_return_pct 列 100% 为空 → 该计算在数据上无解。
    与此同时 check_q4 用 POST_COST_RE=r"\\b1.6[0-4]\\b" 强制 1.60–1.64(=q3 的 1.62)，
    拒绝 ~1.59。诚实跟题面走的 agent 算不出或得 1.59 而被判失败。

修复方向(option b，不臆造数据)：
  - 改题面 q4：不再要求从 backtest 直接重算 live Sharpe；post-cost 复用 q3 的 ~1.62，
    fee_adj 列仅作 fee-drag 归因的支撑证据。
  - 改 u1 backtest_data/_index.md：删除 "CSV 含 2023-2025 live 行 / 算出 ~1.59" 的虚假宣称，
    改述 fee_adj_return_pct 仅文档化扣费方法、本 CSV 只覆盖 pre-live backtest 窗口。
  - check_q4 逻辑本就正确(验 pre 2.01 / post 1.62 / gap 0.39 / fee 归因 / 跨轮一致)，
    仅同步 docstring。

绑定验证：
  1. 数据事实未变(回归护栏)：u1 CSV 仍无 2023+ 行、fee_adj 仍全空。
     => 证明 check 不能依赖从该 CSV 算 live Sharpe。
  2. 题面/index 不再宣称从 backtest 重算 live Sharpe 或 ~1.59。
  3. 诚实按修正口径(pre 2.01 / post 1.62)的 reconciliation 文档 PASS。
  4. 跨轮不一致(q4 post 写成 1.59 而 q3 写 1.62 偏差>0.04)仍 FAIL —— 守卫未被削弱。
  5. 缺 fee 归因数值 / 命中 archive(0.83/pre-pivot) 仍 FAIL。
"""
from __future__ import annotations

import csv
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCN = REPO / "data" / "clawarena-team" / "scenarios"
FUND = SCN / "s_fund_due_diligence"
U1_CSV = FUND / "updates" / "u1" / "backtest_data" / "apex_backtest_2018_2025.csv"
U1_INDEX = FUND / "updates" / "u1" / "backtest_data" / "_index.md"
QUESTIONS = FUND / "questions.json"


def load_check(scenario: str, qid: str):
    """动态加载某场景的 check_<qid>.py，隔离其可能的 _common 依赖。"""
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


def _run_check(script: Path, ws: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(script), str(ws)],
        capture_output=True,
        text=True,
    )


# ---------------------------------------------------------------------------
# 1+2. 数据事实 / 题面文案 回归护栏
# ---------------------------------------------------------------------------


def test_u1_csv_has_no_live_rows_and_empty_fee_adj():
    """护栏：u1 CSV 仍无 2023+ 行、fee_adj_return_pct 仍全空。

    若有人日后往 CSV 塞 live 行/fee 值以"满足旧题面"，本测试会提醒同步 index/题面口径。
    """
    rows = list(csv.DictReader(U1_CSV.open(encoding="utf-8")))
    assert rows, "u1 CSV 应有数据行"
    live_rows = [r for r in rows if (r["date"] or "").strip() >= "2023"]
    assert live_rows == [], "u1 CSV 不应含 2023+ live 行(数据事实)"
    nonempty_fee = [r for r in rows if (r.get("fee_adj_return_pct") or "").strip()]
    assert nonempty_fee == [], "fee_adj_return_pct 应全空(数据事实)"


def test_q4_spec_no_longer_demands_recompute_live_sharpe_from_backtest():
    """题面 q4 不应再要求"从 backtest 直接重算 live post-cost Sharpe"。"""
    q4 = next(q for q in json.loads(QUESTIONS.read_text()) if q["id"] == "q4")
    text = q4["question"].lower()
    assert "recompute the post-cost sharpe directly from the backtest" not in text
    # 应明确把 post-cost 指向 q3 的 live 报告值
    assert "q3" in text or "live report" in text or "live reports" in text


def test_u1_index_drops_false_159_and_live_row_claims():
    """u1 _index.md 不应再宣称 CSV 含 2023-2025 live 行或可算出 ~1.59。"""
    idx = U1_INDEX.read_text(encoding="utf-8")
    assert "1.59" not in idx, "index 不应再保留虚假的 ~1.59 live Sharpe 宣称"
    assert "2018-01-02 to 2025-12-31" not in idx, "index 不应再宣称数据到 2025"
    # 应明确指引 post-cost 取自 live_reports / q3
    assert "live_reports" in idx


# ---------------------------------------------------------------------------
# 3+4+5. check_q4 行为绑定
# ---------------------------------------------------------------------------

_Q2_OUTPUT = (
    "# Backtest Sharpe\n\n"
    "- Total rows in CSV: 756\n"
    "- Rows included (synthetic_aug == 0): 569; excluded: 187\n"
    "- Annualised pre-cost Sharpe (filtered): **2.01**\n"
    "- Unfiltered Sharpe would be ~2.41 (inflated by synthetic rows).\n"
)

_Q3_OUTPUT = (
    "# Live Net-of-Fees Sharpe\n\n"
    "- The net-of-fees figures appear only in the page footer blockquote.\n"
    "- 2024 annualised net-of-fees Sharpe: **1.62**\n"
    "- Gross body figure was ~2.03 (not used for post-cost analysis).\n"
)


def _good_recon(post: str = "1.62") -> str:
    return (
        "# Sharpe Reconciliation — Apex Fund II\n\n"
        "## Figures\n"
        "- Pre-cost backtest Sharpe (q2): 2.01\n"
        f"- Post-cost live net Sharpe (q3): {post}\n"
        "## Gap\n"
        "- Total gap: 0.39 (pre 2.01 minus post 1.62).\n"
        "## Attribution\n"
        "- Fee drag accounts for ~0.28 Sharpe units, driven by the 1.5% "
        "management fee plus the 20% performance allocation per the fee schedule.\n"
        "- Management fee and performance fee deduction is documented in the "
        "fee_adj_return_pct column methodology.\n"
        "## Residual\n"
        "- Live-vs-backtest period effects / signal degradation explain the "
        "remaining ~0.11 residual.\n"
        "## Methodology Notes\n"
        "- Pre-cost Sharpe uses excess_return_pct with synthetic_aug == 0 on the "
        "backtest CSV (q2). The post-cost live net Sharpe is taken from the 2024 "
        "live performance reports (q3), not re-derived from the backtest file, "
        "which covers only the pre-live backtest window. The u1 fee_adj_return_pct "
        "column documents the per-day fee deduction methodology used to attribute "
        "the fee-drag component of the reconciliation.\n"
    )


def _make_ws(tmp_path: Path, recon: str) -> Path:
    ws = tmp_path / "work"
    (ws / "output").mkdir(parents=True)
    (ws / "output" / "backtest_sharpe.md").write_text(_Q2_OUTPUT, encoding="utf-8")
    (ws / "output" / "live_sharpe.md").write_text(_Q3_OUTPUT, encoding="utf-8")
    (ws / "output" / "sharpe_reconciliation.md").write_text(recon, encoding="utf-8")
    return ws


def test_q4_honest_reconciliation_passes(tmp_path):
    """诚实按修正口径(pre 2.01 / post 1.62)的 reconciliation 应 PASS。"""
    script = FUND / "checks" / "check_q4.py"
    ws = _make_ws(tmp_path, _good_recon())
    res = _run_check(script, ws)
    assert res.returncode == 0, f"应 PASS, 实得 FAIL: {res.stderr}"


def test_q4_cross_round_inconsistent_post_cost_fails(tmp_path):
    """q4 post 写 1.59 而 q3 写 1.62(偏差>0.04)应 FAIL —— 跨轮守卫未被削弱。"""
    script = FUND / "checks" / "check_q4.py"
    # post=1.59 落在 [1.58,1.66] 提取窗口内，与 q3 的 1.62 偏差 0.03? -> 用 1.58 制造>0.04
    ws = _make_ws(tmp_path, _good_recon(post="1.58"))
    # 同时把 q3 改成 1.62 已是默认；1.62 vs 1.58 = 0.04 边界。用更远值确保 FAIL。
    recon = _good_recon(post="1.62").replace(
        "Post-cost live net Sharpe (q3): 1.62",
        "Post-cost live net Sharpe (q3): 1.58",
    )
    # 替换 gap 区里出现的 1.62 不影响首个落窗口浮点(标题处 1.58 先命中)
    (ws / "output" / "sharpe_reconciliation.md").write_text(recon, encoding="utf-8")
    res = _run_check(script, ws)
    assert res.returncode != 0, "跨轮 post-cost 不一致应 FAIL"
    assert "cross-round" in res.stderr.lower() or "post-cost" in res.stderr.lower()


def test_q4_missing_fee_attribution_fails(tmp_path):
    """缺 fee 归因数值应 FAIL。"""
    script = FUND / "checks" / "check_q4.py"
    recon = (
        "# Sharpe Reconciliation\n\n"
        "## Figures\n- Pre-cost: 2.01\n- Post-cost: 1.62\n"
        "## Gap\n- Gap: 0.39\n"
        "## Notes\n- Live vs backtest period effects exist.\n"
        "- Signal degradation noted.\n- Fees were charged.\n"
    )
    ws = _make_ws(tmp_path, recon)
    res = _run_check(script, ws)
    assert res.returncode != 0, "缺 fee 归因数值应 FAIL"


def test_q4_archive_pollution_fails(tmp_path):
    """命中 archive(pre-pivot / 0.83 / strategy_v0)应 FAIL。"""
    script = FUND / "checks" / "check_q4.py"
    recon = _good_recon() + "\n## Archive\n- Pre-pivot strategy_v0 Sharpe was 0.83.\n"
    ws = _make_ws(tmp_path, recon)
    res = _run_check(script, ws)
    assert res.returncode != 0, "archive 污染应 FAIL"


def test_q4_check_loads_via_load_check():
    """load_check 范式可正常加载 check_q4(无 _common 依赖断裂)。"""
    mod = load_check("s_fund_due_diligence", "q4")
    assert hasattr(mod, "main")
    assert mod.POST_COST_RE.search("1.62") is not None
