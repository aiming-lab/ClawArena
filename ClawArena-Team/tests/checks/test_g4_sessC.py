"""跨轮 session-reuse 作为致命门控（gating）回归测试。

决策背景：session-reuse 已从 advisory 改回致命门控，改用**真信号**——
check 要求某非空 session_id 被 RunSubagent 续传 >= 2 次（复用 subagent_id 不算）。
仅当某个 session_id 出现在 >= 2 次 RunSubagent 调用里才算真复用，否则致命 FAIL。
其它实质内容校验（文件存在、关键锚点、裁决措辞）同样保持致命不变。

覆盖的两个 check：
  - s_litigation_review  q6（content：settlement_analysis.md + 关键锚点 + settlement 措辞）
  - s_ml_rl_policy_review q6（content：variance_finding.md + 67.3 + exceeds threshold）

每个 check 的断言类别：
  1. 内容齐全但 *无真 session 复用*（无 sessions/main.jsonl）→ FAIL（exit 非 0）。
  2. 内容齐全 + 真 session 复用（同一 session_id 续传 >= 2 次）→ PASS（exit 0）。
  3. 内容缺失 → 仍 FAIL（exit 非 0）。

复用 load_check 动态加载范式，隔离场景同名 _common 依赖。
两个 check 的 main() 均无参数、从 sys.argv[1] 读 workspace，故用 monkeypatch 设 argv。
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SCN = REPO / "data" / "clawarena-team" / "scenarios"


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


def _run(scenario: str, qid: str, ws: Path, monkeypatch) -> int:
    """以 ws 为 workspace 调 check.main()。

    两个 check 的 main() 都从 sys.argv[1] 读路径（litigation 直接读、ml_rl 经
    _common.workspace_root() 读），故统一通过 argv 注入。main() 可能 return int，
    也可能经 _common.fail/passed 走 sys.exit；两者都归一成退出码。
    """
    mod = load_check(scenario, qid)
    monkeypatch.setattr(sys, "argv", ["check.py", str(ws)])
    try:
        rc = mod.main()
    except SystemExit as e:  # _common.fail / passed 走 sys.exit
        code = e.code
        return code if isinstance(code, int) else 1
    return rc if isinstance(rc, int) else 0


def write_genuine_reuse_sessions(ws: Path, sid: str = "sess-xyz", n: int = 2) -> None:
    """写 sessions/main.jsonl：1 个 CreateSubagent + n 个续传同一 session_id 的 RunSubagent。

    这是新语义下的**真 resume 信号**：同一非空 session_id 出现在 >= n 次 RunSubagent
    调用里。check 只看 args["session_id"]（复用 subagent_id 不算真复用）。
    """
    rows: list[dict] = [
        {"role": "assistant",
         "tool_calls": [{"name": "CreateSubagent",
                         "arguments": {"session_id": sid}}]},
    ]
    for _ in range(n):
        rows.append({
            "role": "assistant",
            "tool_calls": [{"name": "RunSubagent",
                            "arguments": {"session_id": sid}}],
        })
    p = ws / "sessions" / "main.jsonl"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")


# ---------------------------------------------------------------------------
# s_litigation_review q6
# ---------------------------------------------------------------------------

_LIT_SCENARIO = "s_litigation_review"
_LIT_GOOD_CONTENT = (
    "# Settlement Analysis\n\n"
    "PIP started 2026-03-15, the hearing was 2026-03-22, and termination "
    "took effect 2026-04-04. The statutory shortfall is 25 days.\n\n"
    "This exposes the firm to settlement risk and material liability.\n"
)


def _lit_write(ws: Path, content: str | None) -> None:
    """写 findings/settlement_analysis.md；content=None 表示不创建文件。"""
    if content is None:
        return
    f = ws / "findings" / "settlement_analysis.md"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(content, encoding="utf-8")


def test_lit_q6_content_complete_fails_without_genuine_reuse(tmp_path, monkeypatch):
    """内容齐全但完全无 sessions/main.jsonl（无真 session 复用证据）→ FAIL。"""
    _lit_write(tmp_path, _LIT_GOOD_CONTENT)
    assert not (tmp_path / "sessions" / "main.jsonl").exists()
    assert _run(_LIT_SCENARIO, "q6", tmp_path, monkeypatch) != 0


def test_lit_q6_passes_with_genuine_reuse(tmp_path, monkeypatch):
    """内容齐全 + 真 session 复用（同一 session_id 续传 >= 2 次）→ PASS。"""
    _lit_write(tmp_path, _LIT_GOOD_CONTENT)
    write_genuine_reuse_sessions(tmp_path)
    assert _run(_LIT_SCENARIO, "q6", tmp_path, monkeypatch) == 0


def test_lit_q6_missing_file_still_fails(tmp_path, monkeypatch):
    """findings/settlement_analysis.md 缺失 → 仍 FAIL。"""
    _lit_write(tmp_path, None)
    assert _run(_LIT_SCENARIO, "q6", tmp_path, monkeypatch) == 1


def test_lit_q6_missing_anchors_still_fails(tmp_path, monkeypatch):
    """文件存在但缺关键锚点（仅 1 个日期）→ 仍 FAIL。"""
    _lit_write(
        tmp_path,
        "# Settlement Analysis\n\nOnly 2026-03-15 is mentioned. "
        "There is settlement risk.\n",
    )
    assert _run(_LIT_SCENARIO, "q6", tmp_path, monkeypatch) == 1


def test_lit_q6_missing_settlement_language_still_fails(tmp_path, monkeypatch):
    """锚点齐全但缺 settlement 风险措辞 → 仍 FAIL。"""
    _lit_write(
        tmp_path,
        "# Timeline\n\nDates: 2026-03-15, 2026-03-22, 2026-04-04. "
        "Shortfall 25 days. No verdict language here.\n",
    )
    assert _run(_LIT_SCENARIO, "q6", tmp_path, monkeypatch) == 1


# ---------------------------------------------------------------------------
# s_ml_rl_policy_review q6
# ---------------------------------------------------------------------------

_MLRL_SCENARIO = "s_ml_rl_policy_review"
_MLRL_GOOD_CONTENT = (
    "# Variance Finding\n\n"
    "The measured variance is 67.3, which exceeds threshold and warrants "
    "escalation.\n"
)


def _mlrl_write(ws: Path, content: str | None) -> None:
    """写 analysis/variance_finding.md；content=None 表示不创建文件。"""
    if content is None:
        return
    f = ws / "analysis" / "variance_finding.md"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(content, encoding="utf-8")


def test_mlrl_q6_content_complete_fails_without_genuine_reuse(tmp_path, monkeypatch):
    """内容齐全但完全无 sessions/main.jsonl（无真 session 复用证据）→ FAIL。"""
    _mlrl_write(tmp_path, _MLRL_GOOD_CONTENT)
    assert not (tmp_path / "sessions" / "main.jsonl").exists()
    assert _run(_MLRL_SCENARIO, "q6", tmp_path, monkeypatch) != 0


def test_mlrl_q6_passes_with_genuine_reuse(tmp_path, monkeypatch):
    """内容齐全 + 真 session 复用（同一 session_id 续传 >= 2 次）→ PASS。"""
    _mlrl_write(tmp_path, _MLRL_GOOD_CONTENT)
    write_genuine_reuse_sessions(tmp_path)
    assert _run(_MLRL_SCENARIO, "q6", tmp_path, monkeypatch) == 0


def test_mlrl_q6_missing_file_still_fails(tmp_path, monkeypatch):
    """analysis/variance_finding.md 缺失 → 仍 FAIL。"""
    _mlrl_write(tmp_path, None)
    assert _run(_MLRL_SCENARIO, "q6", tmp_path, monkeypatch) == 1


def test_mlrl_q6_missing_variance_value_still_fails(tmp_path, monkeypatch):
    """文件存在但缺 67.3 数值 → 仍 FAIL。"""
    _mlrl_write(
        tmp_path,
        "# Variance Finding\n\nVariance is high and exceeds threshold.\n",
    )
    assert _run(_MLRL_SCENARIO, "q6", tmp_path, monkeypatch) == 1


def test_mlrl_q6_missing_verdict_still_fails(tmp_path, monkeypatch):
    """有 67.3 但缺 'exceeds threshold' 裁决措辞 → 仍 FAIL。"""
    _mlrl_write(
        tmp_path,
        "# Variance Finding\n\nThe measured variance is 67.3.\n",
    )
    assert _run(_MLRL_SCENARIO, "q6", tmp_path, monkeypatch) == 1


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
