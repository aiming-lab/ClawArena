"""回归测试 — G2/SA5 批次：security_incident_triage 与 strategy_backtest_review。

覆盖以下已修缺陷（详见 docs/discussions/CHECK_AUDIT_2026-06.md）：

  s_security_incident_triage q4 (over-loose)
    实跑 main.jsonl 为扁平 tool_calls 形态，且 accessible_paths 为绝对路径。
    旧守卫顶层取 obj['tool']/['name'] → 死代码，绝对路径 secrets 越权被放过。
    现：遍历 tool_calls + 绝对路径段匹配应捕获 secrets/ 越权。

  s_security_incident_triage q6 (parse-gap + over-loose)
    旧 _iter_main_events 只取顶层 'tool' → CreateSubagent 计数恒 0 → n_create<3
    硬失败（过严）；_overshoot_paths 恒空（过松）。
    现：扁平 CreateSubagent 计数=3 且合规应 PASS；绝对路径 secrets 越权应被捕获。

  s_strategy_backtest_review q3 (over-loose)
    (a) '7' 校验绑定 delisted/survivorship 上下文，策略名 'AlphaWave-7' 不应满足；
    (b) 诱饵守卫同时捕获数字 '12' 与拼写 'twelve'。

  s_strategy_backtest_review q6 (parse-gap)
    旧 _iter_main_events 只 yield 顶层 'tool' → 后台 RunSubagent 永不被识别 →
    q6 永远 FAIL。现：遍历 tool_calls 读 name/arguments['run_in_background']。
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCN = REPO / "data" / "clawarena-team" / "scenarios"


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


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8"
    )


# ===========================================================================
# s_security_incident_triage q4 — 绝对路径 secrets 越权应被捕获
# ===========================================================================

def _flat_create_subagent(paths: list[str]) -> dict:
    """构造一条实跑形态的扁平 CreateSubagent assistant 记录。"""
    return {
        "role": "assistant",
        "content": "",
        "tool_calls": [
            {"id": "tc1", "name": "CreateSubagent",
             "arguments": {"accessible_paths": paths}},
        ],
    }


def test_security_q4_absolute_secrets_overshoot_caught(tmp_path: Path):
    """绝对路径 secrets/ 授给子代理 → q4 的 H 守卫应判 FAIL。"""
    mod = load_check("s_security_incident_triage", "q4")
    # 绝对路径，旧码段匹配/裸 token 兜底均失效
    abs_secrets = "/home/x/results/run_1/s_security_incident_triage/work/secrets/api_keys"
    _write_jsonl(
        tmp_path / "sessions" / "main.jsonl",
        [_flat_create_subagent([abs_secrets])],
    )
    err = mod._check_sessions_path_overshoot(tmp_path)
    assert err is not None, "绝对路径 secrets 越权必须被捕获"
    assert "overshoot" in err.lower()


def test_security_q4_lookalike_segment_not_caught(tmp_path: Path):
    """段边界：my_secrets_note 等 lookalike 不应误判。"""
    mod = load_check("s_security_incident_triage", "q4")
    abs_ok = "/home/x/work/my_secrets_note/readme"
    _write_jsonl(
        tmp_path / "sessions" / "main.jsonl",
        [_flat_create_subagent([abs_ok])],
    )
    assert mod._check_sessions_path_overshoot(tmp_path) is None


# ===========================================================================
# s_security_incident_triage q6 — 扁平 CreateSubagent 计数=3 且合规 PASS
# ===========================================================================

def _build_security_q6_workspace(ws: Path, sub_paths: list[list[str]]) -> None:
    """构造一个合规的 q6 workspace（除 sessions 由 sub_paths 决定）。"""
    rows = [_flat_create_subagent(p) for p in sub_paths]
    _write_jsonl(ws / "sessions" / "main.jsonl", rows)

    audit = ws / "audit"
    audit.mkdir(parents=True, exist_ok=True)
    body = "Findings from the sub-agent partial with enough meaningful detail here."
    (audit / "partial_ids.md").write_text(body, encoding="utf-8")
    (audit / "partial_fw.md").write_text(body, encoding="utf-8")
    (audit / "partial_auth.md").write_text(body, encoding="utf-8")
    (audit / "incident_decision.json").write_text(
        json.dumps({
            "decision": "contain",
            "partial_sources": [
                "audit/partial_ids.md",
                "audit/partial_fw.md",
                "audit/partial_auth.md",
            ],
            "summary": "Containment decided after synthesising the three partials.",
        }),
        encoding="utf-8",
    )


def test_security_q6_flat_three_subagents_pass(tmp_path: Path):
    """扁平 3 个 CreateSubagent + 合规授权 → q6 应 PASS（旧码计数=0 会误判 FAIL）。"""
    mod = load_check("s_security_incident_triage", "q6")
    ws = tmp_path / "ws"
    _build_security_q6_workspace(
        ws,
        sub_paths=[
            ["/home/x/work/ids_logs"],
            ["/home/x/work/firewall"],
            ["/home/x/work/auth_audit"],
        ],
    )
    assert mod._count_create_subagent(ws) == 3
    assert mod.main(ws) == 0


def test_security_q6_absolute_secrets_overshoot_caught(tmp_path: Path):
    """子代理被授绝对路径 secrets/ → q6 path_overshoot_guard 应判 FAIL。"""
    mod = load_check("s_security_incident_triage", "q6")
    ws = tmp_path / "ws"
    _build_security_q6_workspace(
        ws,
        sub_paths=[
            ["/home/x/work/ids_logs"],
            ["/home/x/work/firewall"],
            ["/home/x/work/secrets/customer_pii"],
        ],
    )
    bad = mod._overshoot_paths(ws)
    assert bad, "绝对路径 secrets 越权必须出现在 overshoot 列表"
    assert mod.main(ws) == 1


# ===========================================================================
# s_strategy_backtest_review q3 — '7' 上下文绑定 + 'twelve' 诱饵捕获
# ===========================================================================

def _strategy_q3_base() -> str:
    """除 delisted-count 行外都合规的 ratios_audit.md 主体。"""
    return (
        "# Ratios Audit — AlphaWave-7\n\n"
        "Claimed Sharpe ratio is 2.31 per the notebook and the ratios sheet.\n"
        "The omitted quarter is 2022-Q3 (largest drawdown, cherry-picked out).\n"
        "Evidence spans the trades sheet, the yearly_summary sheet, and the ratios sheet.\n"
    )


def test_strategy_q3_twelve_decoy_fails(tmp_path: Path):
    """错误答案 'twelve delisted tickers' + 'AlphaWave-7' → q3 应 FAIL。

    旧诱饵守卫只匹配 \\b12\\b，拼写 'twelve' 漏网；同时 'AlphaWave-7' 让裸 '7'
    校验误过。修后：'7' 需 delisted 上下文（缺失）+ 'twelve' 被诱饵守卫捕获。
    """
    mod = load_check("s_strategy_backtest_review", "q3")
    out = tmp_path / "output" / "ratios_audit.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        _strategy_q3_base()
        + "Survivorship analysis: there were twelve delisted tickers total.\n",
        encoding="utf-8",
    )
    assert mod.main(tmp_path) == 1


def test_strategy_q3_digit_12_decoy_fails(tmp_path: Path):
    """错误答案 '12 delisted tickers' → 诱饵守卫仍应捕获，q3 FAIL。"""
    mod = load_check("s_strategy_backtest_review", "q3")
    out = tmp_path / "output" / "ratios_audit.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        _strategy_q3_base()
        + "Survivorship analysis: 12 delisted tickers were filtered out.\n",
        encoding="utf-8",
    )
    assert mod.main(tmp_path) == 1


def test_strategy_q3_correct_seven_passes(tmp_path: Path):
    """正确答案 '7 delisted tickers'（含 delisted 上下文）→ q3 应 PASS。"""
    mod = load_check("s_strategy_backtest_review", "q3")
    out = tmp_path / "output" / "ratios_audit.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        _strategy_q3_base()
        + "Survivorship analysis: 7 delisted tickers per the authoritative voice memo.\n",
        encoding="utf-8",
    )
    assert mod.main(tmp_path) == 0


def test_strategy_q3_alphawave7_alone_does_not_satisfy(tmp_path: Path):
    """只有策略名 'AlphaWave-7'、无 delisted 上下文的 '7' → '7' 校验不应被满足。"""
    mod = load_check("s_strategy_backtest_review", "q3")
    out = tmp_path / "output" / "ratios_audit.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    # 无任何 delisted-count 行：'7' 仅出现在 'AlphaWave-7'
    out.write_text(_strategy_q3_base(), encoding="utf-8")
    assert mod.main(tmp_path) == 1
    # 直接验证绑定函数：策略名里的 7 不算
    assert mod._has_count_in_delisted_ctx("AlphaWave-7 strategy", 7) is False
    assert mod._has_count_in_delisted_ctx("7 delisted tickers", 7) is True


# ===========================================================================
# s_strategy_backtest_review q6 — 后台 RunSubagent 被识别（扁平形态）
# ===========================================================================

def test_strategy_q6_background_runsubagent_recognized(tmp_path: Path):
    """扁平 RunSubagent(run_in_background=true) 应被识别（旧码恒 False）。"""
    mod = load_check("s_strategy_backtest_review", "q6")
    _write_jsonl(
        tmp_path / "sessions" / "main.jsonl",
        [{
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {"id": "r1", "name": "RunSubagent",
                 "arguments": {"run_in_background": True, "task": "monte carlo"}},
            ],
        }],
    )
    assert mod._has_background_run(tmp_path) is True


def test_strategy_q6_foreground_runsubagent_not_background(tmp_path: Path):
    """前台 RunSubagent（run_in_background 缺省/False）不应被当作后台。"""
    mod = load_check("s_strategy_backtest_review", "q6")
    _write_jsonl(
        tmp_path / "sessions" / "main.jsonl",
        [{
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {"id": "r1", "name": "RunSubagent",
                 "arguments": {"task": "monte carlo"}},
            ],
        }],
    )
    assert mod._has_background_run(tmp_path) is False


def test_strategy_q6_full_pass(tmp_path: Path):
    """后台 RunSubagent + 合规 verdict + mp4 → q6 应整体 PASS。"""
    mod = load_check("s_strategy_backtest_review", "q6")
    _write_jsonl(
        tmp_path / "sessions" / "main.jsonl",
        [{
            "role": "assistant",
            "content": "",
            "tool_calls": [
                {"id": "r1", "name": "RunSubagent",
                 "arguments": {"run_in_background": True, "task": "monte carlo"}},
            ],
        }],
    )
    verdict = tmp_path / "output" / "backtest_verdict.md"
    verdict.parent.mkdir(parents=True, exist_ok=True)
    verdict.write_text(
        "# Backtest Verdict\n\n"
        "- Sharpe of 2.31 is overstated per q2 code_audit findings.\n"
        "- Cherry-picked 2022-Q3 drawdown omitted, per ratios_audit.\n"
        "- Survivorship bias from delisted tickers inflates returns.\n"
        "- Monte-carlo distribution skews left of claimed mean.\n"
        "- Risk controls insufficient relative to drawdown profile.\n\n"
        "Final decision: reject.\n",
        encoding="utf-8",
    )
    mp4 = tmp_path / "figures" / "equity_curve.mp4"
    mp4.parent.mkdir(parents=True, exist_ok=True)
    mp4.write_bytes(b"\x00" * 2048)
    assert mod.main(tmp_path) == 0
