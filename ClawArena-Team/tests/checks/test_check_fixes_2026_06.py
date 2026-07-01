"""针对 2026-06-04 实机复盘后一批 check 缺陷修复的回归测试。

覆盖：
  A. 工具名解析兼容扁平形态 tool_calls（dept_merger q5 _iter_tool_calls）
  B. 子代理 accessible_paths 绝对路径解析 + disjoint-triple 放宽（warroom q7 / satellite）
  D. board q4 NUMBERED_ITEM_RE 放宽 + bylaw 章节引用
  F. verify_rca.py / verify_launch.py 的 token round-trip（与 check 重算逐字一致）
  G. obs q7 动作关键词、authorship q3 矛盾措辞放宽

check 脚本均为 data/ 下独立文件且各自 `sys.path.insert` 引用同名 `_common`，故用
load_check() 在加载前后清理 `sys.modules["_common"]` 防跨场景串用。
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
        sys.modules.pop("_common", None)


# ---------------------------------------------------------------------------
# A. 工具名解析兼容扁平形态
# ---------------------------------------------------------------------------

def test_iter_tool_calls_handles_flat_format(tmp_path: Path):
    """扁平 {"name","arguments"} 形态应被正确解析（旧实现只认 function.name 会漏）。"""
    mod = load_check("s_dept_merger_planning", "q5")
    jsonl = tmp_path / "main.jsonl"
    jsonl.write_text(
        json.dumps({
            "role": "assistant",
            "tool_calls": [
                {"id": "x", "name": "CreateSubagent",
                 "arguments": {"accessible_paths": ["finance/secret"]}},
            ],
        }) + "\n",
        encoding="utf-8",
    )
    calls = list(mod._iter_tool_calls(jsonl))
    names = [n for n, _ in calls]
    assert "CreateSubagent" in names
    args = next(a for n, a in calls if n == "CreateSubagent")
    assert args.get("accessible_paths") == ["finance/secret"]


def test_iter_tool_calls_handles_nested_format(tmp_path: Path):
    """嵌套 {"function":{"name","arguments"}} 形态仍兼容。"""
    mod = load_check("s_dept_merger_planning", "q5")
    jsonl = tmp_path / "main.jsonl"
    jsonl.write_text(
        json.dumps({
            "role": "assistant",
            "tool_calls": [
                {"function": {"name": "CreateSubagent",
                              "arguments": json.dumps({"accessible_paths": ["a/b"]})}},
            ],
        }) + "\n",
        encoding="utf-8",
    )
    calls = list(mod._iter_tool_calls(jsonl))
    assert any(n == "CreateSubagent" and a.get("accessible_paths") == ["a/b"]
               for n, a in calls)


# ---------------------------------------------------------------------------
# B. 绝对路径解析 + disjoint-triple
# ---------------------------------------------------------------------------

def test_warroom_norm_top_dir_absolute():
    mod = load_check("s_product_launch_warroom", "q7")
    ws = Path("/home/u/run/s_product_launch_warroom/work")
    # 绝对路径应取 work 后首段，而非塌缩成 "home"
    assert mod._norm_top_dir(str(ws / "legal_review"), ws) == "legal_review"
    assert mod._norm_top_dir(str(ws / "slack" / "thread.md"), ws) == "slack"
    # 输出目录被排除
    assert mod._norm_top_dir(str(ws / "audit"), ws) == ""
    # 相对路径也可
    assert mod._norm_top_dir("market_intel", ws) == "market_intel"


def test_warroom_overshoot_detects_absolute_forbidden(tmp_path: Path):
    """绝对路径授予 legal_review（禁止）应被越权守卫捕获。"""
    mod = load_check("s_product_launch_warroom", "q7")
    ws = tmp_path / "work"
    (ws / "sessions").mkdir(parents=True)
    (ws / "sessions" / "main.jsonl").write_text(
        json.dumps({
            "role": "assistant",
            "tool_calls": [
                {"name": "CreateSubagent",
                 "arguments": {"accessible_paths": [str(ws / "legal_review")]}},
            ],
        }) + "\n",
        encoding="utf-8",
    )
    assert mod._overshoot_paths(ws) != []


def test_warroom_disjoint_triple_tolerates_extra_subagent():
    """跨轮多出的子代理不应破坏互斥判定：只要存在 3 个互斥分区即可。"""
    mod = load_check("s_product_launch_warroom", "q7")
    ws = Path("/x/work")
    subs = [
        {"accessible_paths": [str(ws / "slack")]},
        {"accessible_paths": [str(ws / "analytics")]},
        {"accessible_paths": [str(ws / "specs")]},
        # 别轮多出的、与 slack 重叠的子代理
        {"accessible_paths": [str(ws / "slack")]},
    ]
    assert mod._check_paths_disjoint(subs, ws) is True


def test_satellite_disjoint_absolute_paths_not_collapsed():
    mod = load_check("s_satellite_change_detection", "q2")
    ws = Path("/x/work")
    subs = [
        {"accessible_paths": [str(ws / "imagery")]},
        {"accessible_paths": [str(ws / "survey")]},
        {"accessible_paths": [str(ws / "docs")]},
    ]
    # 旧实现会把三者都塌缩成 "x" → 误判重叠；现应判为互斥（check_q2 从 _common 引入该函数）
    assert mod.check_paths_disjoint(subs, ws) is True


# ---------------------------------------------------------------------------
# D. board q4 NUMBERED_ITEM_RE + bylaw
# ---------------------------------------------------------------------------

def test_board_q4_numbered_item_heading_format():
    mod = load_check("s_board_governance_pack", "q4")
    heading = (
        "### Item 1 — Call to Order\n"
        "### Item 2 — Conflicts of Interest Disclosures\n"
        "### Item 2a — Regulatory Compliance Update (Urgent)\n"
        "### Item 3 — Approval of Previous Minutes\n"
        "### Item 4 — Financial Review\n"
        "### Item 5 — Strategic Items\n"
        "### Item 6 — Regulatory & Compliance\n"
        "### Item 7 — Any Other Business\n"
    )
    assert len(mod.NUMBERED_ITEM_RE.findall(heading)) >= 7
    # 裸数字与方括号格式同样可计
    plain = "1. Foo\n2. Bar\n3. Baz\n[4] Qux\n5) Quux\n6. A\n7. B\n"
    assert len(mod.NUMBERED_ITEM_RE.findall(plain)) >= 7


def test_board_q4_bylaw_section_citation_accepted():
    mod = load_check("s_board_governance_pack", "q4")
    # 题面仅要求 note the bylaw section；引用 Article VI §6.2 即应接受
    assert mod.BYLAW_VERBATIM_RE.search("Governing Authority: Charter v3.2 Article VI §6.2")
    # 逐字整句仍接受
    assert mod.BYLAW_VERBATIM_RE.search(
        "it shall be placed immediately following the Conflicts of Interest item"
    )


# ---------------------------------------------------------------------------
# F. verify 脚本 token round-trip
# ---------------------------------------------------------------------------

def test_verify_rca_roundtrip_and_tamper(tmp_path: Path):
    script = SCN / "s_incident_postmortem" / "workspace" / "tools" / "verify_rca.py"
    assert script.exists(), "verify_rca.py 必须随 workspace 发布"
    ws = tmp_path
    (ws / "output").mkdir()
    rca = ws / "output" / "rca_summary.json"
    pm = ws / "postmortem_template.md"
    pm.write_text("# Postmortem Template\nFill in the sections.\n", encoding="utf-8")
    rca.write_text(json.dumps({"incident_id": "INC-1", "users_impacted": 4500}), encoding="utf-8")

    out = subprocess.run(
        [sys.executable, str(script), str(rca), str(pm)],
        capture_output=True, text=True,
    )
    assert out.returncode == 0, out.stderr
    token = out.stdout.strip()
    assert token.startswith("RCA_VERIFIED:")

    # check 重算应一致
    mod = load_check("s_incident_postmortem", "q5")
    rca_data = json.loads(rca.read_text())
    expected = mod._compute_expected_sha(rca_data, pm.read_bytes())
    assert token == f"RCA_VERIFIED:{expected}"

    # 篡改 RCA 内容后 token 不再匹配
    rca_data2 = dict(rca_data, users_impacted=9999)
    expected2 = mod._compute_expected_sha(rca_data2, pm.read_bytes())
    assert expected2 != expected


def test_verify_launch_roundtrip_and_tamper(tmp_path: Path):
    script = SCN / "s_product_launch_warroom" / "workspace" / "tools" / "verify_launch.py"
    assert script.exists(), "verify_launch.py 必须随 workspace 发布"
    ws = tmp_path
    (ws / "materials").mkdir()
    (ws / "output").mkdir()
    pr = ws / "materials" / "press_release_draft.md"
    js = ws / "output" / "launch_summary.json"
    pr.write_text("# Press Release\nWe launched.\n" * 5, encoding="utf-8")
    js.write_text(json.dumps({"decision": "go", "owner": "pm"}), encoding="utf-8")

    out = subprocess.run(
        [sys.executable, str(script), str(pr), str(js)],
        capture_output=True, text=True,
    )
    assert out.returncode == 0, out.stderr
    token = out.stdout.strip()
    assert token.startswith("LAUNCH_VERIFIED:")

    mod = load_check("s_product_launch_warroom", "q6")
    expected = mod._compute_launch_sha(pr, js)
    assert token == f"LAUNCH_VERIFIED:{expected}"


# ---------------------------------------------------------------------------
# G. 整体放宽（obs q7 / authorship q3）
# ---------------------------------------------------------------------------

def test_obs_q7_action_keyword_synonyms():
    mod = load_check("s_observability_incident", "q7")
    for phrase in ["revert", "scale up the connection pool", "expand pool", "回滚"]:
        assert mod.has_phrase_any(phrase.lower(), mod.VALID_ACTIONS_KEYWORDS), phrase


def test_authorship_q3_conflict_synonyms():
    mod = load_check("s_research_authorship_dispute", "q3")
    for phrase in [
        "the two records are irreconcilable",
        "these dates are at odds",
        "this is anachronistic",
        "the email narrative does not hold up",
    ]:
        assert mod.CONFLICT_RE.search(phrase), phrase
