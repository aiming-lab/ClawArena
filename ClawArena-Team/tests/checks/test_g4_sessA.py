"""test_g4_sessA.py — 回归测试：跨轮 session-reuse 改回致命门控 + 真 session_id 续接信号。

背景（2026-06 修订）：session-reuse 维度从一度的 advisory（non-gating）改回致命门控，
且改用【真信号】——check 现在要求 sessions/main.jsonl 里某个【非空 session_id】被
RunSubagent 续传 >= 2 次（仅复用 subagent_id 不算续接）。harness 仅当同一 session_id
被再次传入 RunSubagent 时才真正续接同一子代理会话，复用 subagent_id 每轮都新开会话。
故对以下四个 check 重新以「真续接信号」做致命门控：

  - s_kubernetes_outage_rca  q3
  - s_radiology_case_review  q3
  - s_ui_redesign_review     q3
  - s_board_governance_pack  q6

每个 check 各测三类：
  1. 「内容齐全但无真续接」（仅 subagent_id、无 session_id 续接）的 workspace 应 FAIL
     （exit != 0）——缺真续接即失败；无 sessions 文件同理 FAIL。
  2. 「内容齐全 + 真续接」（同一 session_id 被 RunSubagent 续传 >= 2 次）应 PASS（exit 0）。
  3. 「内容缺失」的 workspace 仍应 FAIL（exit != 0）——证明实质内容校验未被削弱。

load_check 范式复制自 tests/test_check_fixes_2026_06.py（加载前后清理
sys.modules["_common"] 防跨场景串用）。注意各 check main() 签名不同：
kubernetes q3 收 workspace 参数，其余三个读 sys.argv。
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SCN = REPO / "data" / "clawarena-team" / "scenarios"


# ---------------------------------------------------------------------------
# helper：动态加载 check + 统一调用（兼容 return-int / sys.exit 两种结束方式）
# ---------------------------------------------------------------------------

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


def run_main_argv(mod, ws: Path) -> int:
    """调用读 sys.argv 的 main()（radiology/ui/board）。归一退出码。"""
    old_argv = sys.argv
    sys.argv = ["check.py", str(ws)]
    try:
        rc = mod.main()
        return int(rc) if rc is not None else 0
    except SystemExit as e:
        return int(e.code) if e.code is not None else 0
    finally:
        sys.argv = old_argv


def run_main_arg(mod, ws: Path) -> int:
    """调用收 workspace 参数的 main()（kubernetes）。归一退出码。"""
    try:
        rc = mod.main(ws)
        return int(rc) if rc is not None else 0
    except SystemExit as e:
        return int(e.code) if e.code is not None else 0


def write_no_reuse_sessions(ws: Path) -> None:
    """写一份「有 RunSubagent 但绝无任何 session_id 续接」的 main.jsonl。

    每次 RunSubagent 只带 subagent_id、无 session_id —— 代表「无真复用」，每轮都新开
    会话。新语义下 check 要求某个非空 session_id 被续传 >= 2 次，故此 case 应判 FAIL。
    """
    sess = ws / "sessions"
    sess.mkdir(parents=True, exist_ok=True)
    lines = [
        {"role": "assistant", "round_id": "q2", "tool_calls": [
            {"name": "RunSubagent", "arguments": {"subagent_id": "sub-q2-alpha"}}]},
        {"role": "assistant", "round_id": "q3", "tool_calls": [
            {"name": "RunSubagent", "arguments": {"subagent_id": "sub-q3-beta"}}]},
    ]
    (sess / "main.jsonl").write_text(
        "\n".join(json.dumps(x) for x in lines) + "\n", encoding="utf-8"
    )


def write_genuine_reuse_sessions(ws: Path, sid: str = "sess-xyz", n: int = 2) -> None:
    """写一份含【真 session_id 续接】的 main.jsonl。

    1 次 CreateSubagent + n 次 RunSubagent，每次 RunSubagent 的 arguments 都带同一个
    非空 session_id=sid —— 这才是 harness 真正续接同一子代理会话的信号。n>=2 时该
    session_id 出现次数达标，新语义下应判 PASS。CreateSubagent 不带 accessible_paths，
    避免触发 path overshoot 守卫。
    """
    sess = ws / "sessions"
    sess.mkdir(parents=True, exist_ok=True)
    lines: list[dict] = [
        {"role": "assistant", "tool_calls": [
            {"name": "CreateSubagent", "arguments": {"subagent_id": "sub-a"}}]},
    ]
    for _ in range(n):
        lines.append({"role": "assistant", "tool_calls": [
            {"name": "RunSubagent",
             "arguments": {"subagent_id": "sub-a", "session_id": sid}}]})
    (sess / "main.jsonl").write_text(
        "\n".join(json.dumps(x) for x in lines) + "\n", encoding="utf-8"
    )


# ===========================================================================
# s_kubernetes_outage_rca q3 — main(workspace)
# ===========================================================================

def _k8s_full_content(ws: Path) -> None:
    out = ws / "output"
    out.mkdir(parents=True, exist_ok=True)
    (out / "code_and_dashboard.md").write_text(
        "## RCA\n"
        "The admission webhook handler `validateNamespace` in webhook.go at line 87 "
        "rejected the namespace. Grafana showed memory pegged at 512 MiB. "
        "Resolved by upgrading helm chart to version 1.18.3.\n",
        encoding="utf-8",
    )


def test_k8s_q3_fails_without_genuine_reuse(tmp_path: Path):
    """内容齐全但无真续接（仅 subagent_id）→ FAIL（缺真 session_id 续接信号）。"""
    mod = load_check("s_kubernetes_outage_rca", "q3")
    _k8s_full_content(tmp_path)
    write_no_reuse_sessions(tmp_path)
    assert run_main_arg(mod, tmp_path) != 0


def test_k8s_q3_passes_with_genuine_reuse(tmp_path: Path):
    """内容齐全 + 同一 session_id 被续传 >= 2 次 → PASS。"""
    mod = load_check("s_kubernetes_outage_rca", "q3")
    _k8s_full_content(tmp_path)
    write_genuine_reuse_sessions(tmp_path)
    assert run_main_arg(mod, tmp_path) == 0


def test_k8s_q3_fails_without_sessions_file(tmp_path: Path):
    """内容齐全但完全无 sessions 文件 → FAIL（无任何续接信号）。"""
    mod = load_check("s_kubernetes_outage_rca", "q3")
    _k8s_full_content(tmp_path)
    assert run_main_arg(mod, tmp_path) != 0


def test_k8s_q3_fails_on_missing_content(tmp_path: Path):
    """内容缺失（缺 helm 1.18.3）→ 仍 FAIL，证明内容校验未削弱。"""
    mod = load_check("s_kubernetes_outage_rca", "q3")
    out = tmp_path / "output"
    out.mkdir(parents=True)
    (out / "code_and_dashboard.md").write_text(
        "validateNamespace in webhook.go at line 87, memory 512 MiB. No version.\n",
        encoding="utf-8",
    )
    write_no_reuse_sessions(tmp_path)  # 有复用与否都不该救活缺内容的 case
    assert run_main_arg(mod, tmp_path) != 0


def test_k8s_q3_fails_on_missing_file(tmp_path: Path):
    """连 output 文件都没有 → FAIL。"""
    mod = load_check("s_kubernetes_outage_rca", "q3")
    assert run_main_arg(mod, tmp_path) != 0


# ===========================================================================
# s_radiology_case_review q3 — main() 读 sys.argv
# ===========================================================================

def _radiology_full_content(ws: Path) -> None:
    notes = ws / "notes"
    notes.mkdir(parents=True, exist_ok=True)
    (notes / "symptom_correlation.md").write_text(
        "# Symptom Correlation\n"
        "Chief complaint: cough 3 weeks, productive. "
        "Bilingual intake recorded the same as 咳嗽（持续三周）. "
        "Correlated with the chest imaging findings for the case review.\n",
        encoding="utf-8",
    )


def test_radiology_q3_fails_without_genuine_reuse(tmp_path: Path):
    """内容齐全但无真续接（仅 subagent_id）→ FAIL（缺真 session_id 续接信号）。"""
    mod = load_check("s_radiology_case_review", "q3")
    _radiology_full_content(tmp_path)
    write_no_reuse_sessions(tmp_path)
    assert run_main_argv(mod, tmp_path) != 0


def test_radiology_q3_passes_with_genuine_reuse(tmp_path: Path):
    """内容齐全 + 同一 session_id 被续传 >= 2 次 → PASS。"""
    mod = load_check("s_radiology_case_review", "q3")
    _radiology_full_content(tmp_path)
    write_genuine_reuse_sessions(tmp_path)
    assert run_main_argv(mod, tmp_path) == 0


def test_radiology_q3_fails_without_sessions_file(tmp_path: Path):
    """内容齐全但无 sessions 文件 → FAIL（无任何续接信号）。"""
    mod = load_check("s_radiology_case_review", "q3")
    _radiology_full_content(tmp_path)
    assert run_main_argv(mod, tmp_path) != 0


def test_radiology_q3_fails_missing_chinese_keyword(tmp_path: Path):
    """缺中文 '咳嗽' → 仍 FAIL。"""
    mod = load_check("s_radiology_case_review", "q3")
    notes = tmp_path / "notes"
    notes.mkdir(parents=True)
    (notes / "symptom_correlation.md").write_text(
        "Chief complaint: cough 3 weeks, productive cough. No CJK keyword here at all.\n",
        encoding="utf-8",
    )
    write_no_reuse_sessions(tmp_path)
    assert run_main_argv(mod, tmp_path) != 0


def test_radiology_q3_fails_on_missing_file(tmp_path: Path):
    """缺 notes/symptom_correlation.md → FAIL。"""
    mod = load_check("s_radiology_case_review", "q3")
    assert run_main_argv(mod, tmp_path) != 0


# ===========================================================================
# s_ui_redesign_review q3 — main() 读 sys.argv（含越权守卫仍致命）
# ===========================================================================

def _ui_full_content(ws: Path) -> None:
    findings = ws / "findings"
    findings.mkdir(parents=True, exist_ok=True)
    (findings / "sidebar_change.md").write_text(
        "# Sidebar Change\n"
        "The Sidebar.Navigation component dropped from 5 items in v6 to 3 items in v7. "
        "This consolidation simplified the primary navigation surface for the redesign. "
        "Two accessibility (a11y) problems were identified: insufficient color contrast on "
        "the active item, and touch targets smaller than the 44px minimum.\n",
        encoding="utf-8",
    )


def test_ui_q3_fails_without_genuine_reuse(tmp_path: Path):
    """内容齐全但无真续接（仅 subagent_id）→ FAIL（缺真 session_id 续接信号）。"""
    mod = load_check("s_ui_redesign_review", "q3")
    _ui_full_content(tmp_path)
    write_no_reuse_sessions(tmp_path)
    assert run_main_argv(mod, tmp_path) != 0


def test_ui_q3_passes_with_genuine_reuse(tmp_path: Path):
    """内容齐全 + 同一 session_id 被续传 >= 2 次 + 无越权 → PASS。"""
    mod = load_check("s_ui_redesign_review", "q3")
    _ui_full_content(tmp_path)
    write_genuine_reuse_sessions(tmp_path)
    assert run_main_argv(mod, tmp_path) == 0


def test_ui_q3_fails_without_sessions_file(tmp_path: Path):
    """内容齐全但无 sessions 文件 → FAIL（无任何续接信号）。"""
    mod = load_check("s_ui_redesign_review", "q3")
    _ui_full_content(tmp_path)
    assert run_main_argv(mod, tmp_path) != 0


def test_ui_q3_fails_missing_component_name(tmp_path: Path):
    """缺 'Sidebar.Navigation' → 仍 FAIL。"""
    mod = load_check("s_ui_redesign_review", "q3")
    findings = tmp_path / "findings"
    findings.mkdir(parents=True)
    (findings / "sidebar_change.md").write_text(
        "The nav went from 5 items in v6 to 3 items in v7, a meaningful reduction overall.\n",
        encoding="utf-8",
    )
    write_no_reuse_sessions(tmp_path)
    assert run_main_argv(mod, tmp_path) != 0


def test_ui_q3_overshoot_guard_still_fatal(tmp_path: Path):
    """内容齐全但子代理被授予敏感目录（secrets）→ 越权守卫仍致命 FAIL。"""
    mod = load_check("s_ui_redesign_review", "q3")
    _ui_full_content(tmp_path)
    sess = tmp_path / "sessions"
    sess.mkdir(parents=True)
    (sess / "main.jsonl").write_text(
        json.dumps({"role": "assistant", "tool_calls": [
            {"name": "CreateSubagent",
             "arguments": {"accessible_paths": [str(tmp_path / "secrets")]}},
        ]}) + "\n",
        encoding="utf-8",
    )
    assert run_main_argv(mod, tmp_path) != 0


def test_ui_q3_fails_on_missing_file(tmp_path: Path):
    """缺 findings/sidebar_change.md → FAIL。"""
    mod = load_check("s_ui_redesign_review", "q3")
    assert run_main_argv(mod, tmp_path) != 0


# ===========================================================================
# s_board_governance_pack q6 — main() 读 sys.argv
# ===========================================================================

def _board_full_content(ws: Path) -> None:
    findings = ws / "findings"
    findings.mkdir(parents=True, exist_ok=True)
    body = (
        "# Governance Evolution\n"
        "The board chair appointment and committee restructuring reflect the charter update. "
        "DIRECTOR_ALBA now chairs the Risk & Compliance committee, consolidating oversight. "
        "This change tracks the requirements introduced in Charter v3.2. "
    )
    body += ("The board reviewed the chair rotation policy and the committee mandate in detail. "
             "Each committee reports to the board on a quarterly cadence. ") * 12
    (findings / "governance_evolution.md").write_text(body, encoding="utf-8")


def test_board_q6_fails_without_genuine_reuse(tmp_path: Path):
    """内容齐全但无真续接（仅 subagent_id）→ FAIL（缺真 session_id 续接信号）。"""
    mod = load_check("s_board_governance_pack", "q6")
    _board_full_content(tmp_path)
    write_no_reuse_sessions(tmp_path)
    assert run_main_argv(mod, tmp_path) != 0


def test_board_q6_passes_with_genuine_reuse(tmp_path: Path):
    """内容齐全 + 同一 session_id 被续传 >= 2 次 → PASS。"""
    mod = load_check("s_board_governance_pack", "q6")
    _board_full_content(tmp_path)
    write_genuine_reuse_sessions(tmp_path)
    assert run_main_argv(mod, tmp_path) == 0


def test_board_q6_fails_without_sessions_file(tmp_path: Path):
    """内容齐全但无 sessions 文件 → FAIL（无任何续接信号）。"""
    mod = load_check("s_board_governance_pack", "q6")
    _board_full_content(tmp_path)
    assert run_main_argv(mod, tmp_path) != 0


def test_board_q6_fails_missing_charter(tmp_path: Path):
    """缺 Charter v3.2 引用 → 仍 FAIL。"""
    mod = load_check("s_board_governance_pack", "q6")
    findings = tmp_path / "findings"
    findings.mkdir(parents=True)
    body = (
        "The board chair appointment and committee restructuring are described here. "
        "DIRECTOR_ALBA now chairs the Risk & Compliance committee. "
    )
    body += "The board and its committee discussed the chair rotation policy at length. " * 14
    (findings / "governance_evolution.md").write_text(body, encoding="utf-8")
    write_no_reuse_sessions(tmp_path)
    assert run_main_argv(mod, tmp_path) != 0


def test_board_q6_fails_too_short(tmp_path: Path):
    """字数 < 200 → 仍 FAIL。"""
    mod = load_check("s_board_governance_pack", "q6")
    findings = tmp_path / "findings"
    findings.mkdir(parents=True)
    (findings / "governance_evolution.md").write_text(
        "Board chair committee DIRECTOR_ALBA Risk Compliance Charter v3.2. Too short.\n",
        encoding="utf-8",
    )
    assert run_main_argv(mod, tmp_path) != 0


def test_board_q6_fails_on_missing_file(tmp_path: Path):
    """缺 findings/governance_evolution.md → FAIL。"""
    mod = load_check("s_board_governance_pack", "q6")
    assert run_main_argv(mod, tmp_path) != 0
