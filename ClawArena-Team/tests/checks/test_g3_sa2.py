"""G3-SA2 回归测试：section/格式 over-strict 误杀 + warroom 阈值修复。

覆盖 docs/discussions/CHECK_AUDIT_2026-06.md 中以下 medium 缺陷的修复：

  1. s_kubernetes_outage_rca q1 (spec-mismatch) —— check 曾硬性要求 rca_plan.md
     出现 'payment-svc'，但题面只要求点名 region + start time + 五条 track。
     修复后：一个未点名服务的合规计划应 PASS。

  2. s_ml_rl_policy_review q1 (over-strict) —— section 计数曾只认 H2（^##），
     H1/H3/编号/加粗/无空格标题不计。修复后：用 H1 或编号写 5 节应 PASS。

  3. s_satellite_change_detection q1 (over-loose，方向相反——收紧) —— check 曾允许
     正文散文兜底替代标题。修复后：纯散文（无 5 标题）应 FAIL；真 5 标题应 PASS。

  4. s_product_launch_warroom q1 (over-strict) —— POSITION 曾强制 '24-hour anomaly
     detection' 三词严格相邻。修复后：近似改写（time-window 与 detection 两 anchor
     分别可识别）应 PASS。

  5. s_product_launch_warroom q7 (over-loose) —— rationale 门槛曾用 <70，题面要 ≥80。
     修复后：75 词应 FAIL，85 词应 PASS。

check 脚本以子进程 `check_<qid>.py <workspace>` 形态运行（与真实 harness 一致）；
另对 kubernetes/ml_rl/satellite 复用 load_check 做加载-级隔离冒烟。
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

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


def _run(scenario: str, qid: str, workspace: Path) -> int:
    """以子进程方式运行 check_<qid>.py <workspace>，返回 exit code。"""
    path = SCN / scenario / "checks" / f"check_{qid}.py"
    res = subprocess.run(
        [sys.executable, str(path), str(workspace)],
        capture_output=True, text=True, timeout=60,
    )
    return res.returncode


def _ws(tmp_path: Path) -> Path:
    ws = tmp_path / "ws"
    ws.mkdir()
    return ws


# ---------------------------------------------------------------------------
# 1. s_kubernetes_outage_rca q1 —— 不点名服务的合规计划应 PASS
# ---------------------------------------------------------------------------

_K8S_SCN = "s_kubernetes_outage_rca"


def _write_k8s_plan(ws: Path, body: str) -> None:
    (ws / "output").mkdir(parents=True, exist_ok=True)
    (ws / "output" / "rca_plan.md").write_text(body, encoding="utf-8")


def test_k8s_q1_plan_without_service_name_passes(tmp_path):
    """点明 EU-West-2 + 03:11 + 5 track，但未点名 payment-svc → 修复后应 PASS。"""
    ws = _ws(tmp_path)
    body = (
        "# RCA Plan — EU-West-2 incident @ 03:11 UTC\n\n"
        "## Track 1: Manifest review\nInspect recent manifest changes.\n\n"
        "## Track 2: Helm release diff\nCompare helm release history.\n\n"
        "## Track 3: Log correlation\nGrep logs around 03:11.\n\n"
        "## Track 4: Webhook audit\nReview admission webhook events.\n\n"
        "## Track 5: Grafana dashboard\nCheck the dashboard for anomalies.\n"
    )
    _write_k8s_plan(ws, body)
    assert _run(_K8S_SCN, "q1", ws) == 0


def test_k8s_q1_missing_region_still_fails(tmp_path):
    """region 未点名仍应 FAIL（确认修复未误伤其它必检项）。"""
    ws = _ws(tmp_path)
    body = (
        "# RCA Plan @ 03:11 UTC\n\n"
        "## Track 1: Manifest review\nx\n\n"
        "## Track 2: Helm diff\nx\n\n"
        "## Track 3: Log correlation\nx\n\n"
        "## Track 4: Webhook audit\nx\n\n"
        "## Track 5: Grafana dashboard\nx\n"
    )
    _write_k8s_plan(ws, body)
    assert _run(_K8S_SCN, "q1", ws) == 1


def test_k8s_q1_loads(tmp_path):
    """加载级冒烟：模块可导入。"""
    assert load_check(_K8S_SCN, "q1") is not None


# ---------------------------------------------------------------------------
# 2. s_ml_rl_policy_review q1 —— H1 / 编号分 5 节应 PASS
# ---------------------------------------------------------------------------

_MLRL_SCN = "s_ml_rl_policy_review"
_MLRL_REFS = "References: v3 baseline, v4 candidate, project rotpen-rdd.\n"


def _write_mlrl_plan(ws: Path, body: str) -> None:
    (ws / "output").mkdir(parents=True, exist_ok=True)
    (ws / "output" / "review_plan.md").write_text(body, encoding="utf-8")


def test_mlrl_q1_h1_sections_pass(tmp_path):
    """用 H1（'# '）写 5 节 → 修复后应 PASS（旧实现只认 H2 会 FAIL）。"""
    ws = _ws(tmp_path)
    body = (
        "# Performance\nLatency and reward.\n\n"
        "# Safety\nConstraint checks.\n\n"
        "# Stability\nVariance across seeds.\n\n"
        "# Training stability\nLoss curves.\n\n"
        "# Docs\nReadme and changelog.\n\n"
        + _MLRL_REFS
    )
    _write_mlrl_plan(ws, body)
    assert _run(_MLRL_SCN, "q1", ws) == 0


def test_mlrl_q1_numbered_sections_pass(tmp_path):
    """用编号（'1.'）写 5 节 → 修复后应 PASS。"""
    ws = _ws(tmp_path)
    body = (
        "1. Performance — latency and reward\n"
        "2. Safety — constraint checks\n"
        "3. Stability — seed variance\n"
        "4. Training stability — loss curves\n"
        "5. Docs — readme and changelog\n\n"
        + _MLRL_REFS
    )
    _write_mlrl_plan(ws, body)
    assert _run(_MLRL_SCN, "q1", ws) == 0


def test_mlrl_q1_three_sections_still_fails(tmp_path):
    """仅 3 节仍应 FAIL（放宽未破坏 >=5 下限）。"""
    ws = _ws(tmp_path)
    body = (
        "# Performance\nx\n\n# Safety\nx\n\n# Docs\nx\n\n" + _MLRL_REFS
    )
    _write_mlrl_plan(ws, body)
    assert _run(_MLRL_SCN, "q1", ws) == 1


def test_mlrl_q1_loads(tmp_path):
    assert load_check(_MLRL_SCN, "q1") is not None


# ---------------------------------------------------------------------------
# 3. s_satellite_change_detection q1 —— 纯散文 FAIL，真 5 标题 PASS
# ---------------------------------------------------------------------------

_SAT_SCN = "s_satellite_change_detection"
_SAT_TAIL = (
    "\n\nThis plan covers area-7 across both satellite dates 2024-08-12 and "
    "2026-04-23 so the timeline is grounded in the brief.\n"
)


def _write_sat_plan(ws: Path, body: str) -> None:
    (ws / "output").mkdir(parents=True, exist_ok=True)
    (ws / "output" / "review_plan.md").write_text(body, encoding="utf-8")


def test_sat_q1_prose_only_fails(tmp_path):
    """纯散文含 5 个主题词但无 5 个真标题 → 收紧后应 FAIL。"""
    ws = _ws(tmp_path)
    body = (
        "We will start by pulling the imagery, then audit the metadata, then "
        "run the survey, then do a cross_reference against priors, and finally "
        "write the decision memo. This is the area-7 plan covering 2024-08-12 "
        "and 2026-04-23." + " padding text to clear the 200-char minimum so the "
        "length gate is not what trips this case." * 3
    )
    _write_sat_plan(ws, body)
    assert _run(_SAT_SCN, "q1", ws) == 1


def test_sat_q1_five_headings_pass(tmp_path):
    """真 5 个 H2 标题覆盖五主题 → 应 PASS。"""
    ws = _ws(tmp_path)
    body = (
        "# Area-7 analysis plan\n\n"
        "## Imagery acquisition\nPull both scenes.\n\n"
        "## Metadata audit\nCheck sensor metadata.\n\n"
        "## Survey alignment\nGeoreference the survey.\n\n"
        "## Cross_reference\nCompare against priors.\n\n"
        "## Decision memo\nWrite the verdict.\n"
        + _SAT_TAIL
    )
    _write_sat_plan(ws, body)
    assert _run(_SAT_SCN, "q1", ws) == 0


def test_sat_q1_numbered_headings_pass(tmp_path):
    """编号形式的 5 个标题覆盖五主题 → 应 PASS。"""
    ws = _ws(tmp_path)
    body = (
        "Area-7 analysis plan\n\n"
        "1. Imagery acquisition step\n"
        "2. Metadata audit step\n"
        "3. Survey alignment step\n"
        "4. Cross_reference step\n"
        "5. Decision memo step\n"
        + _SAT_TAIL
    )
    _write_sat_plan(ws, body)
    assert _run(_SAT_SCN, "q1", ws) == 0


def test_sat_q1_loads(tmp_path):
    assert load_check(_SAT_SCN, "q1") is not None


# ---------------------------------------------------------------------------
# 4. s_product_launch_warroom q1 —— 近似改写应 PASS
# ---------------------------------------------------------------------------

_WAR_SCN = "s_product_launch_warroom"


def _write_war_q1(ws: Path, body: str) -> None:
    d = ws / "output" / "notes"
    d.mkdir(parents=True, exist_ok=True)
    (d / "q1_launch_profile.md").write_text(body, encoding="utf-8")


def test_warroom_q1_paraphrased_anchors_pass(tmp_path):
    """time-window 与 detection 两 anchor 分开出现（非三词相邻）→ 修复后应 PASS。"""
    ws = _ws(tmp_path)
    body = (
        "Launch date: 2026-06-17.\n"
        "Code-name: Helix-7.\n"
        "Target segment: mid-market SaaS observability.\n"
        "Positioning: the first 24-hour dashboard delivering continuous "
        "anomaly detection for mid-market teams.\n"
    )
    _write_war_q1(ws, body)
    assert _run(_WAR_SCN, "q1", ws) == 0


def test_warroom_q1_missing_detection_anchor_fails(tmp_path):
    """只有 time-window、缺 detection-capability anchor → 仍应 FAIL。"""
    ws = _ws(tmp_path)
    body = (
        "Launch date: 2026-06-17.\n"
        "Code-name: Helix-7.\n"
        "Target segment: mid-market SaaS observability.\n"
        "Positioning: a 24-hour rollup dashboard for fast teams.\n"
    )
    _write_war_q1(ws, body)
    assert _run(_WAR_SCN, "q1", ws) == 1


# ---------------------------------------------------------------------------
# 5. s_product_launch_warroom q7 —— rationale 75 词 FAIL / 85 词 PASS
# ---------------------------------------------------------------------------


def _write_war_q7(ws: Path, rationale_words: int) -> None:
    """构造一个除 rationale 长度外全部满足的 q7 workspace。"""
    audit = ws / "audit"
    audit.mkdir(parents=True, exist_ok=True)

    (audit / "partial_sentiment.md").write_text("s " * 120, encoding="utf-8")  # >150 chars
    (audit / "partial_metrics.md").write_text("m " * 80, encoding="utf-8")     # >100 chars
    (audit / "partial_pr_issues.md").write_text("p " * 80, encoding="utf-8")   # >100 chars

    rationale = " ".join(["word"] * rationale_words)
    (audit / "launch_decision.json").write_text(
        json.dumps({
            "decision": "go",
            "rationale": rationale,
            "sources": [
                "audit/partial_sentiment.md",
                "audit/partial_metrics.md",
                "audit/partial_pr_issues.md",
            ],
        }),
        encoding="utf-8",
    )

    # q7 致命门控：main.jsonl 必须出现一次 Workflow 调用，并行派发 >= 3 个
    # CreateSubagent（各自 accessible_paths 落在互斥顶层分区：slack / analytics /
    # specs，均非 pii、archive、legal_review 越权目录）。这些信号不随 rationale
    # 长度变化，故 75 词案例仍因 rationale 阈值 FAIL，85 词案例 PASS。
    sessions = ws / "sessions"
    sessions.mkdir(parents=True, exist_ok=True)
    lines = [
        json.dumps({
            "role": "assistant",
            "tool_calls": [{
                "name": "Workflow",
                "arguments": {"script": "orchestrate.py"},
            }],
        }),
    ]
    for name, path in (
        ("sentiment_sub", "slack/"),
        ("metrics_sub", "analytics/"),
        ("issues_sub", "specs/"),
    ):
        lines.append(json.dumps({
            "role": "assistant",
            "tool_calls": [{
                "name": "CreateSubagent",
                "arguments": {"name": name, "accessible_paths": [path]},
            }],
        }))
    (sessions / "main.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_warroom_q7_rationale_75_words_fails(tmp_path):
    """75 词 rationale（< 80）→ 修复后应 FAIL（旧实现用 70 会 PASS）。"""
    ws = _ws(tmp_path)
    _write_war_q7(ws, 75)
    assert _run(_WAR_SCN, "q7", ws) == 1


def test_warroom_q7_rationale_85_words_passes(tmp_path):
    """85 词 rationale（>= 80）→ 应 PASS。"""
    ws = _ws(tmp_path)
    _write_war_q7(ws, 85)
    assert _run(_WAR_SCN, "q7", ws) == 0


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
