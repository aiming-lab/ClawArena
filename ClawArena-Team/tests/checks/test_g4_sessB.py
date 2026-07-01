"""G4 session-reuse 致命门控回归测试（test_g4_sessB.py，本文件独占）。

决策（dev2）：跨轮 session-reuse 维度**改回致命门控**（gating），且改用**真信号**——
check 要求 sessions/main.jsonl 里某个非空 `session_id` 被 RunSubagent 续传 **>= 2 次**；
只复用 subagent_id（不带 session_id）每轮新建会话，不算真复用。本测试对下列四个
check 验证：

  - s_hospital_safety_event_review q3   main(workspace: Path)
  - s_devops_runbook_sync          q3   main(workspace: Path)
  - s_climate_simulation_audit     q3   main()，从 sys.argv 取 ws
  - s_release_audit_giant          q6   main()，从 sys.argv 取 ws

每个 check 三条断言：
  (1) 内容齐全 + 无真 session 复用 → FAIL（exit 1），证明门控为致命。
  (2) 内容齐全 + 真 session 复用（同一 session_id 续传 >= 2 次）→ PASS（exit 0）。
  (3) 关键内容缺失 → 仍 FAIL（exit 1），证明内容门槛保持致命。

加载 check 复用 load_check()（与 test_g4_authorship.py 同款 _common 隔离）。
"""
from __future__ import annotations

import importlib.util
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


def _run_with_ws_arg(mod, ws: Path, script: str) -> int:
    """驱动 main()（从 sys.argv 取 ws）的 check，拿退出码。

    climate q3 / release q6 的 main() 无参数、内部读 sys.argv[1]；climate 还可能
    在 workspace_root() / fail() / passed() 里调用 sys.exit，故捕获 SystemExit。
    """
    argv = sys.argv
    sys.argv = [script, str(ws)]
    try:
        rc = mod.main()
        return int(rc) if rc is not None else 0
    except SystemExit as e:
        return int(e.code) if e.code is not None else 0
    finally:
        sys.argv = argv


def _run_with_ws_param(mod, ws: Path) -> int:
    """驱动 main(workspace) 形态的 check（hospital / devops q3）。"""
    rc = mod.main(ws)
    return int(rc) if rc is not None else 0


# ---------------------------------------------------------------------------
# 工具：写一份「无 session 复用」的 main.jsonl
# ---------------------------------------------------------------------------

def _write_no_reuse_sessions(ws: Path) -> None:
    """落一份 main.jsonl：有事件、但不构成任何跨轮 session 复用。

    - 不出现重复 subagent_id（release/climate 的复用计数 < 2）。
    - q2/q3 各自不携带可被关联的 session id（hospital/devops 视为不可验证）。
    """
    sess = ws / "sessions"
    sess.mkdir(parents=True, exist_ok=True)
    lines = [
        '{"role":"user","content":"q1 prompt","is_real_user_question":true}',
        '{"role":"assistant","content":[{"type":"tool_use","name":"RunSubagent",'
        '"input":{"subagent_id":"sub-alpha-0001"}}]}',
        '{"role":"user","content":"q2 prompt","is_real_user_question":true}',
        '{"role":"assistant","content":[{"type":"tool_use","name":"RunSubagent",'
        '"input":{"subagent_id":"sub-beta-0002"}}]}',
        '{"role":"user","content":"q3 prompt","is_real_user_question":true}',
        '{"role":"assistant","content":[{"type":"tool_use","name":"RunSubagent",'
        '"input":{"subagent_id":"sub-gamma-0003"}}]}',
    ]
    (sess / "main.jsonl").write_text("\n".join(lines), encoding="utf-8")


def write_genuine_reuse_sessions(ws: Path, sid: str = "sess-xyz", n: int = 2) -> None:
    """落一份 main.jsonl，构成**真 session 复用**信号。

    含 1 次 CreateSubagent + n 次 RunSubagent，**每次 arguments 都带相同的
    session_id=sid**——这正是 harness 续传同一会话的唯一真信号（只传 subagent_id
    每轮新建会话，不算复用）。n >= 2 时某非空 session_id 出现 >= 2 次，满足门控。

    采用 OpenAI 风格的 tool_calls 包裹形态（{"tool_calls":[{name, arguments}]}），
    这是四个 check 的解析器都识别的最大公约数：release q6 不解析 Anthropic
    content-block，而 devops 不解析顶层扁平单事件，唯有 tool_calls 形态四者通吃。
    """
    import json

    sess = ws / "sessions"
    sess.mkdir(parents=True, exist_ok=True)

    def _ev(name: str, round_idx: int | None = None) -> str:
        args = {"session_id": sid, "subagent_id": "sub-reuse-0001"}
        if round_idx is not None:
            args["round"] = round_idx
        return json.dumps(
            {"role": "assistant", "tool_calls": [{"name": name, "arguments": args}]}
        )

    lines = [_ev("CreateSubagent")]
    lines.extend(_ev("RunSubagent", i) for i in range(n))
    (sess / "main.jsonl").write_text("\n".join(lines), encoding="utf-8")


# ===========================================================================
# s_hospital_safety_event_review q3  (main(workspace))
# ===========================================================================

_HOSP = "s_hospital_safety_event_review"


def _hosp_full_output(ws: Path) -> None:
    out = ws / "output"
    out.mkdir(parents=True, exist_ok=True)
    (out / "timeline_evidence.md").write_text(
        "# Timeline evidence\n\n"
        "CCTV alarm fired at 2026-06-14T23:48:07 with status ALARM_RED.\n"
        "Cross-referenced against device_telemetry/ pump_telemetry.ndjson "
        "(MV7-ICU-2208-0047).\n",
        encoding="utf-8",
    )


def test_hospital_q3_full_content_fails_without_genuine_reuse(tmp_path: Path):
    """内容齐全但无真 session 复用 → FAIL（session-reuse 为致命门控）。"""
    mod = load_check(_HOSP, "q3")
    ws = tmp_path / "work"
    _hosp_full_output(ws)
    _write_no_reuse_sessions(ws)
    assert _run_with_ws_param(mod, ws) != 0


def test_hospital_q3_passes_with_genuine_reuse(tmp_path: Path):
    """内容齐全 + 真 session 复用（同一 session_id 续传 >= 2 次）→ PASS。"""
    mod = load_check(_HOSP, "q3")
    ws = tmp_path / "work"
    _hosp_full_output(ws)
    write_genuine_reuse_sessions(ws)
    assert _run_with_ws_param(mod, ws) == 0


def test_hospital_q3_missing_telemetry_still_fails(tmp_path: Path):
    """缺 telemetry 交叉引用 → 仍 FAIL（内容门槛保持致命）。"""
    mod = load_check(_HOSP, "q3")
    ws = tmp_path / "work"
    out = ws / "output"
    out.mkdir(parents=True, exist_ok=True)
    (out / "timeline_evidence.md").write_text(
        "CCTV alarm at 2026-06-14T23:48:07 status ALARM_RED.\n", encoding="utf-8"
    )
    _write_no_reuse_sessions(ws)
    assert _run_with_ws_param(mod, ws) == 1


# ===========================================================================
# s_devops_runbook_sync q3  (main(workspace))
# ===========================================================================

_DEVOPS = "s_devops_runbook_sync"


def _devops_full_output(ws: Path) -> None:
    out = ws / "output"
    out.mkdir(parents=True, exist_ok=True)
    (out / "test_report.md").write_text(
        "# Test report\n\n"
        "shellcheck: SC2086 on pre_check.sh line 31.\n"
        "bats: pre_migration_checks.bats line 23 failed — "
        "assert_output expected LOCK_TIMEOUT_REQUIRED.\n",
        encoding="utf-8",
    )


def test_devops_q3_full_content_fails_without_genuine_reuse(tmp_path: Path):
    """内容齐全但无真 session 复用 → FAIL（致命门控）。"""
    mod = load_check(_DEVOPS, "q3")
    ws = tmp_path / "work"
    _devops_full_output(ws)
    _write_no_reuse_sessions(ws)
    assert _run_with_ws_param(mod, ws) != 0


def test_devops_q3_passes_with_genuine_reuse(tmp_path: Path):
    """内容齐全 + 真 session 复用 → PASS。"""
    mod = load_check(_DEVOPS, "q3")
    ws = tmp_path / "work"
    _devops_full_output(ws)
    write_genuine_reuse_sessions(ws)
    assert _run_with_ws_param(mod, ws) == 0


def test_devops_q3_missing_lock_timeout_still_fails(tmp_path: Path):
    """缺 LOCK_TIMEOUT_REQUIRED → 仍 FAIL。"""
    mod = load_check(_DEVOPS, "q3")
    ws = tmp_path / "work"
    out = ws / "output"
    out.mkdir(parents=True, exist_ok=True)
    (out / "test_report.md").write_text(
        "SC2086 on pre_check.sh line 31; pre_migration_checks.bats line 23 failed.\n",
        encoding="utf-8",
    )
    _write_no_reuse_sessions(ws)
    assert _run_with_ws_param(mod, ws) == 1


# ===========================================================================
# s_climate_simulation_audit q3  (main()，从 sys.argv 取 ws)
# ===========================================================================

_CLIMATE = "s_climate_simulation_audit"


def _climate_full_output(ws: Path) -> None:
    analysis = ws / "analysis"
    analysis.mkdir(parents=True, exist_ok=True)
    body = (
        "# Quarterly summary\n\n"
        "This report references all four quarters of the W12 run: "
        "w12_q1, w12_q2, w12_q3 and w12_q4. "
    )
    # 补足 >= 200 字符
    body += "Each quarter's drift and energy-balance metrics are summarised here. " * 4
    (analysis / "quarterly_summary.md").write_text(body, encoding="utf-8")


def test_climate_q3_full_content_fails_without_genuine_reuse(tmp_path: Path):
    """4 季度全引用但无真 session 复用 → FAIL（致命门控）。"""
    mod = load_check(_CLIMATE, "q3")
    ws = tmp_path / "work"
    _climate_full_output(ws)
    _write_no_reuse_sessions(ws)
    assert _run_with_ws_arg(mod, ws, "check_q3.py") != 0


def test_climate_q3_passes_with_genuine_reuse(tmp_path: Path):
    """4 季度全引用 + 真 session 复用 → PASS。"""
    mod = load_check(_CLIMATE, "q3")
    ws = tmp_path / "work"
    _climate_full_output(ws)
    write_genuine_reuse_sessions(ws)
    assert _run_with_ws_arg(mod, ws, "check_q3.py") == 0


def test_climate_q3_missing_quarter_still_fails(tmp_path: Path):
    """缺 Q4 引用 → 仍 FAIL（季度引用门槛保持致命）。"""
    mod = load_check(_CLIMATE, "q3")
    ws = tmp_path / "work"
    analysis = ws / "analysis"
    analysis.mkdir(parents=True, exist_ok=True)
    body = "# Quarterly summary\n\nReferences w12_q1, w12_q2 and w12_q3 only. "
    body += "Drift and energy-balance metrics are summarised here. " * 5
    (analysis / "quarterly_summary.md").write_text(body, encoding="utf-8")
    _write_no_reuse_sessions(ws)
    assert _run_with_ws_arg(mod, ws, "check_q3.py") == 1


# ===========================================================================
# s_release_audit_giant q6  (main()，从 sys.argv 取 ws)
# ===========================================================================

_RELEASE = "s_release_audit_giant"


def _release_full_output(ws: Path) -> None:
    findings = ws / "findings"
    findings.mkdir(parents=True, exist_ok=True)
    (findings / "deploy_evolution.md").write_text(
        "# Deploy evolution\n\n"
        "See the rollout animation in figures/deploy_timeline.mp4 for the "
        "stage-by-stage deploy history.\n",
        encoding="utf-8",
    )


def test_release_q6_full_content_fails_without_genuine_reuse(tmp_path: Path):
    """video 引用齐全但无真 session 复用 → FAIL（致命门控）。"""
    mod = load_check(_RELEASE, "q6")
    ws = tmp_path / "work"
    _release_full_output(ws)
    _write_no_reuse_sessions(ws)
    assert _run_with_ws_arg(mod, ws, "check_q6.py") != 0


def test_release_q6_passes_with_genuine_reuse(tmp_path: Path):
    """video 引用齐全 + 真 session 复用 → PASS。"""
    mod = load_check(_RELEASE, "q6")
    ws = tmp_path / "work"
    _release_full_output(ws)
    write_genuine_reuse_sessions(ws)
    assert _run_with_ws_arg(mod, ws, "check_q6.py") == 0


def test_release_q6_missing_video_ref_still_fails(tmp_path: Path):
    """缺 figures/deploy_timeline.mp4 引用 → 仍 FAIL。"""
    mod = load_check(_RELEASE, "q6")
    ws = tmp_path / "work"
    findings = ws / "findings"
    findings.mkdir(parents=True, exist_ok=True)
    (findings / "deploy_evolution.md").write_text(
        "# Deploy evolution\n\nNarrative without any video asset reference.\n",
        encoding="utf-8",
    )
    _write_no_reuse_sessions(ws)
    assert _run_with_ws_arg(mod, ws, "check_q6.py") == 1
