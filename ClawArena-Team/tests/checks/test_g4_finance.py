"""s_finance_options_pricing — VaR 锚点（0.34）回归锁定测试。

背景（2026-06 审计复核）：
  CHECK_AUDIT_2026-06.md 曾把 q5/q6 的 VaR∈[0.30,0.38]（≈0.34）锚点判为
  "spec-mismatch / 无法从数据复算"。复核结论是 **审计算错**——它漏掉了题面
  /权威方法学第 3 步 "apply option delta to convert underlying returns to
  option P&L"，并误用均价 spot≈49 而非 at-the-money K=52.5。

  按 dataset_lab/.../build_wave4.py 写明的完整 4 步方法学复算：
    1. 按日取 close（每日最后一笔 tick）；
    2. 日 log-return r_t = ln(P_t / P_{t-1})；
    3. 用期权 delta 把标的收益折算为期权 P&L；
    4. VaR-95 = |delta * spot * 第5百分位(日 log-return)| × 1 张合约。

  其中 ATM 看涨 delta（K=spot=52.5, T=0.25, r=0.04, sigma=0.18）≈ 0.562，
  数据复算得 VaR ≈ 0.3408，落在 check 的 [0.30,0.38] 区间内。故 check_q5/q6
  的接受区间是正确的，本测试把该锚点对数据锁死，防止再次被误判。

测试内容：
  1. 从 data/market_snapshot.parquet 实算忠实 VaR，断言 ∈ [0.30,0.38] 且 ≈0.34。
  2. 用 load_check 范式功能性跑通 check_q5：合规 var_report + 充分 session_reuse
     → 通过；区间外 VaR → 失败。
  3. 同法跑通 check_q6 的 VaR 一致性分支。
"""
from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SCN = REPO / "data" / "clawarena-team" / "scenarios"
SCENARIO = "s_finance_options_pricing"
PARQUET = SCN / SCENARIO / "workspace" / "data" / "market_snapshot.parquet"

# check_q5 / check_q6 的接受区间（正则 \b0\.\s*3[0-8]\b ⇒ [0.30, 0.38]）。
VAR_LOW, VAR_HIGH = 0.30, 0.38

# 期权合约参数（build_wave4.py: K_STRIKE / T_YEARS / r / sigma；spot 取 ATM=K）。
K_STRIKE = 52.50
SPOT = 52.50
T_YEARS = 0.25
R_RATE = 0.04
SIGMA = 0.18


def load_check(scenario: str, qid: str):
    """动态加载某场景的 check_<qid>.py，隔离其 _common 依赖。"""
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


def _ncdf(x: float) -> float:
    """标准正态 CDF（erf 实现，免 scipy 依赖）。"""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _atm_call_delta() -> float:
    d1 = (math.log(SPOT / K_STRIKE) + (R_RATE + 0.5 * SIGMA**2) * T_YEARS) / (
        SIGMA * math.sqrt(T_YEARS)
    )
    return _ncdf(d1)


def _faithful_var_from_parquet() -> float:
    """按 build_wave4.py 权威 4 步方法学复算 VaR-95（绝对、delta 折算）。"""
    pd = pytest.importorskip("pandas")
    pytest.importorskip("pyarrow")
    import numpy as np

    df = pd.read_parquet(PARQUET).sort_values("timestamp_us").reset_index(drop=True)
    df["ts"] = pd.to_datetime(df["timestamp_us"], unit="us")
    # 步骤 1：按日取每日最后一笔 close。
    daily = df.set_index("ts")["close"].resample("1D").last().dropna()
    # 步骤 2：日 log-return。
    dlog = np.diff(np.log(daily.values))
    # 步骤 3+4：delta 折算 → 第 5 百分位 P&L（每张合约 spot 名义）。
    delta = _atm_call_delta()
    p5_logret = np.percentile(dlog, 5)
    return abs(delta * SPOT * p5_logret)


# ---------------------------------------------------------------------------
# 1. 数据复算锁定：忠实 VaR ≈ 0.34，落在 check 区间内。
# ---------------------------------------------------------------------------

def test_atm_call_delta_value():
    """ATM 看涨 delta 应 ≈ 0.562（方法学第 3 步的折算系数）。"""
    assert _atm_call_delta() == pytest.approx(0.5620, abs=1e-3)


def test_faithful_var_matches_check_window():
    """按完整 4 步方法学（含 option delta）复算的 VaR 必须落在 [0.30,0.38] 且 ≈0.34。

    锁定审计复核结论：0.34 锚点忠实于数据，check_q5/q6 区间正确。
    """
    var = _faithful_var_from_parquet()
    assert VAR_LOW <= var <= VAR_HIGH, f"faithful VaR={var:.4f} 落在区间外"
    assert var == pytest.approx(0.34, abs=0.01), f"faithful VaR={var:.4f} 偏离 0.34"


# ---------------------------------------------------------------------------
# 2. check_q5 功能性：区间内通过 / 区间外失败 + session_reuse 门槛。
# ---------------------------------------------------------------------------

def _write_main_jsonl_with_reuse(
    ws: Path, sub_id: str, runs: int, session_id: str | None = "sess-finance"
) -> None:
    """构造 sessions/main.jsonl：1 次 CreateSubagent + runs 次 RunSubagent 同一 sub。

    check_q5 的致命门控按 **非空 session_id 被显式续传的次数** 判真实续接：
    仅当同一 session_id 被回传 >= 3 次才算真续接（复用 subagent_id 不会续接 session）。
    故默认给每次 RunSubagent 续传同一 session_id；传 session_id=None 可构造
    "无真实续接" 反例（应 FAIL）。
    """
    sessions = ws / "sessions"
    sessions.mkdir(parents=True, exist_ok=True)
    lines = [
        json.dumps({
            "role": "assistant",
            "tool_calls": [{
                "id": "c0", "name": "CreateSubagent",
                "arguments": {"name": "data_sub", "accessible_paths": ["data/"]},
            }],
        }),
    ]
    for i in range(runs):
        args = {"subagent_id": sub_id, "prompt": "..."}
        if session_id is not None:
            args["session_id"] = session_id
        lines.append(json.dumps({
            "role": "assistant",
            "tool_calls": [{
                "id": f"r{i}", "name": "RunSubagent",
                "arguments": args,
            }],
        }))
    (sessions / "main.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _run_check(mod, ws: Path) -> int:
    """以 ws 为 argv 跑 check.main()，捕获 SystemExit 返回码。"""
    old_argv = sys.argv
    sys.argv = ["check.py", str(ws)]
    try:
        try:
            rc = mod.main()
        except SystemExit as e:
            rc = e.code if isinstance(e.code, int) else 1
        return rc or 0
    finally:
        sys.argv = old_argv


def test_check_q5_passes_with_in_window_var(tmp_path: Path):
    mod = load_check(SCENARIO, "q5")
    (tmp_path / "findings").mkdir()
    (tmp_path / "findings" / "var_report.md").write_text(
        "# VaR Report\n\n"
        "VaR-95 (daily log-returns, 5th-percentile P&L, option-delta adjusted) = 0.34.\n"
        "Methodology: daily log-returns from market_snapshot.parquet, delta-folded "
        "option P&L, 5th percentile of the loss distribution per contract.\n",
        encoding="utf-8",
    )
    _write_main_jsonl_with_reuse(tmp_path, "data_sub", runs=3)
    assert _run_check(mod, tmp_path) == 0


def test_check_q5_fails_with_out_of_window_var(tmp_path: Path):
    """审计臆造的 0.0115 这类区间外值必须被拒（防止把区间放宽到错误锚点）。"""
    mod = load_check(SCENARIO, "q5")
    (tmp_path / "findings").mkdir()
    (tmp_path / "findings" / "var_report.md").write_text(
        "# VaR Report\n\n"
        "VaR-95 (daily log-returns, 5th-percentile P&L) = 0.0115.\n"
        "Methodology: daily log-returns from market_snapshot.parquet, 5th percentile.\n",
        encoding="utf-8",
    )
    _write_main_jsonl_with_reuse(tmp_path, "data_sub", runs=3)
    assert _run_check(mod, tmp_path) != 0


def test_check_q5_fails_without_genuine_reuse(tmp_path: Path):
    """内容齐全但无真实 session 续接（RunSubagent 不回传 session_id）→ FAIL。

    致命门控：q5 要求某非空 session_id 被 RunSubagent 续传 >= 3 次。复用
    subagent_id 而不回传 session_id 不构成真实续接，故即便内容正确也应失败。
    """
    mod = load_check(SCENARIO, "q5")
    (tmp_path / "findings").mkdir()
    (tmp_path / "findings" / "var_report.md").write_text(
        "# VaR Report\n\nVaR-95 = 0.34 via daily log-returns 5th-percentile P&L.\n"
        "Methodology paragraph long enough to clear the 80-char minimum here.\n",
        encoding="utf-8",
    )
    # 续传 subagent_id 但不回传 session_id → 无真实续接信号。
    _write_main_jsonl_with_reuse(tmp_path, "data_sub", runs=3, session_id=None)
    assert _run_check(mod, tmp_path) != 0


# ---------------------------------------------------------------------------
# 3. check_q6 VaR 一致性分支：区间内通过 / 区间外失败。
# ---------------------------------------------------------------------------

_CROSS_CHECK_OK = (
    "# Cross-round consistency check\n\n"
    "| anchor | value |\n|---|---|\n"
    "| MC estimate | 2.1552 |\n"
    "| BS reference | 2.1477 |\n"
    "| K (strike) | 52.50 |\n"
    "| VaR-95 | {var} |\n\n"
    "All anchors are internally consistent across earlier turns.\n"
)


def test_check_q6_passes_with_in_window_var(tmp_path: Path):
    mod = load_check(SCENARIO, "q6")
    (tmp_path / "audit").mkdir()
    (tmp_path / "audit" / "cross_check.md").write_text(
        _CROSS_CHECK_OK.format(var="0.34"), encoding="utf-8"
    )
    assert _run_check(mod, tmp_path) == 0


def test_check_q6_fails_with_out_of_window_var(tmp_path: Path):
    mod = load_check(SCENARIO, "q6")
    (tmp_path / "audit").mkdir()
    (tmp_path / "audit" / "cross_check.md").write_text(
        _CROSS_CHECK_OK.format(var="0.0115"), encoding="utf-8"
    )
    assert _run_check(mod, tmp_path) != 0
