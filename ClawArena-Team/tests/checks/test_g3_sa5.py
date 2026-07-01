"""回归测试 — G3/SA5 批次：解析 / schema 取值 bug 修复。

覆盖以下已修缺陷（详见 docs/discussions/CHECK_AUDIT_2026-06.md，medium 条目）：

  s_ui_redesign_review q6 (over-loose)
    a11y_fix_required 旧码兜底 `if True in all_values: a11y_required = True`，把
    JSON 中任意位置任何布尔 true 当作满足。即使专门的 a11y_fix_required 键显式为
    false，别处的无关 true 也会误判满足。
    现：只认真正的 a11y_fix_required（含同义键）键值；该键为 false 即 FAIL。

  s_ui_redesign_review q4（result-only：只验根计数 == 12）
    题面建议遍历树得出根数;曾据此排除 'root_layer_count' 键以"逼遍历、防照抄源
    元数据"。但按"check 只验最终结果、不约束解题方法/来源"原则,已移除该排除:
    只要根计数 == 12(正确真值)即满足,不论 agent 表达成 root_count 还是 root_layer_count。
    本判定要求 == 12,值匹配本身已挡住任何错值诱饵。

  s_research_digest_xl q3 (over-strict)
    _extract_slide_number 对 entry 所有 value 逐一扫描，取首个产出数字的 value。
    若 'argument' 字段排在 'slide_number' 之前且含独立数字，会取错值。
    现：优先从名为 slide_number（含同义键）的字段取值，再回退全值扫描。
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


def run_check(mod, ws: Path) -> int:
    """以 ws 为 workspace 跑 check.main()，归一化退出码。

    这些 check 通过 _common.fail/passed 调用 sys.exit，且 main() 经 workspace_root()
    或 sys.argv[1] 读取 workspace 路径。统一用设置 sys.argv + 捕获 SystemExit 驱动。
    返回 0 表示 PASS，非 0 表示 FAIL。
    """
    old_argv = sys.argv
    sys.argv = ["check.py", str(ws)]
    try:
        ret = mod.main()
        return 0 if ret in (0, None) else ret
    except SystemExit as exc:
        code = exc.code
        if code is None:
            return 0
        return code if isinstance(code, int) else 1
    finally:
        sys.argv = old_argv


# ===========================================================================
# s_ui_redesign_review q6 — a11y_fix_required=false 别处有 true 时不再误满足
# ===========================================================================

VALID_TOKEN = None  # 由 mod.EXPECTED_TOKEN 提供，下面注入


def _ui_q6_payload(a11y_value, token: str) -> dict:
    """构造一个除 a11y_fix_required 外其余字段均合规的 ui_decision 载荷。

    其它字段（locales 列表里的 True、approved=True 等）刻意放入无关布尔 true，
    用于验证旧兜底『任意 true 即满足』的误判路径已被堵死。
    """
    return {
        "project_id": "merchant-portal-v7",
        "decision": "approve_v7_with_a11y_fixes",
        "change_summary": "Sidebar.Navigation consolidated 5 items into 3",
        "a11y_fix_required": a11y_value,
        # 别处的无关 true（旧码会把它当 a11y 满足）
        "approved": True,
        "review_complete": True,
        "localization": ["en", "zh-CN", "ja", "de"],
        "compliance_token": token,
    }


def _write_ui_q6(ws: Path, a11y_value) -> None:
    mod = load_check("s_ui_redesign_review", "q6")
    audit = ws / "audit"
    audit.mkdir(parents=True, exist_ok=True)
    payload = _ui_q6_payload(a11y_value, mod.EXPECTED_TOKEN)
    (audit / "ui_decision.json").write_text(json.dumps(payload), encoding="utf-8")


def test_ui_q6_a11y_false_with_other_true_fails(tmp_path: Path):
    """a11y_fix_required 显式 false，但别处有 true → 旧码误判 PASS，现应 FAIL。"""
    mod = load_check("s_ui_redesign_review", "q6")
    ws = tmp_path / "ws"
    _write_ui_q6(ws, False)
    assert run_check(mod, ws) != 0, "a11y_fix_required=false 不应被别处 true 兜底满足"


def test_ui_q6_a11y_missing_with_other_true_fails(tmp_path: Path):
    """a11y_fix_required 键缺失，别处有 true → 现应 FAIL（不再兜底）。"""
    mod = load_check("s_ui_redesign_review", "q6")
    ws = tmp_path / "ws"
    audit = ws / "audit"
    audit.mkdir(parents=True, exist_ok=True)
    payload = _ui_q6_payload(True, mod.EXPECTED_TOKEN)
    payload.pop("a11y_fix_required")
    (audit / "ui_decision.json").write_text(json.dumps(payload), encoding="utf-8")
    assert run_check(mod, ws) != 0, "缺 a11y_fix_required 键时不应被别处 true 兜底满足"


def test_ui_q6_a11y_true_passes(tmp_path: Path):
    """a11y_fix_required 真为 true 且其余合规 → PASS（确保修复未误伤正常路径）。"""
    mod = load_check("s_ui_redesign_review", "q6")
    ws = tmp_path / "ws"
    _write_ui_q6(ws, True)
    assert run_check(mod, ws) == 0


# ===========================================================================
# s_ui_redesign_review q4 — result-only：根计数 == 12 即接受（含 root_layer_count 键）
# ===========================================================================

def _write_ui_q4(ws: Path, payload: dict) -> None:
    analysis = ws / "analysis"
    analysis.mkdir(parents=True, exist_ok=True)
    (analysis / "psd_structure_check.json").write_text(
        json.dumps(payload), encoding="utf-8"
    )


def test_ui_q4_root_layer_count_field_accepted_when_12(tmp_path: Path):
    """root_layer_count=12（正确真值）→ PASS（result-only：不再罚"用了源键名"）。"""
    mod = load_check("s_ui_redesign_review", "q4")
    ws = tmp_path / "ws"
    _write_ui_q4(ws, {
        "root_layer_count": 12,
        "total_nodes": 60,
        "max_depth": 5,
    })
    assert run_check(mod, ws) == 0, "root_layer_count==12 是正确根计数,应被接受"


def test_ui_q4_wrong_root_count_still_fails(tmp_path: Path):
    """根计数错值（≠12）仍 FAIL —— 值匹配守门未被放宽。"""
    mod = load_check("s_ui_redesign_review", "q4")
    ws = tmp_path / "ws"
    _write_ui_q4(ws, {
        "root_layer_count": 9,    # 错值诱饵
        "total_nodes": 60,
        "max_depth": 5,
    })
    assert run_check(mod, ws) != 0, "根计数 != 12 应判 FAIL"


def test_ui_q4_traversed_root_count_passes(tmp_path: Path):
    """真实遍历得到的 root_count=12（合法字段名）→ PASS。"""
    mod = load_check("s_ui_redesign_review", "q4")
    ws = tmp_path / "ws"
    _write_ui_q4(ws, {
        "root_count": 12,         # 遍历 v7_tree.json 顶层 12 个 layer 得出
        "total_nodes": 60,
        "max_depth": 5,
    })
    assert run_check(mod, ws) == 0


def test_ui_q4_actual_traversal_yields_12(tmp_path: Path):
    """对真实 v7_tree.json 做递归遍历，根节点数应为 12（验证 ground truth）。"""
    tree_path = (
        SCN / "s_ui_redesign_review" / "workspace" / "psd_tree" / "v7_tree.json"
    )
    tree = json.loads(tree_path.read_text(encoding="utf-8"))
    # 遍历得出的根层数 == 顶层 layers 数组长度
    assert len(tree["layers"]) == 12


# ===========================================================================
# s_research_digest_xl q3 — 优先从 slide_number 字段取值
# ===========================================================================

def _digest_entries_argument_before_slide() -> list[dict]:
    """构造 10 条 entry，每条 argument 字段排在 slide_number 之前，且 argument
    文本含一个独立数字（与 slide_number 不同）。旧码会先扫到 argument 的数字。
    """
    entries = []
    for n in range(1, 11):
        decoy = (n % 10) + 1  # 与真实 slide 号不同的诱饵数字 (1..10)
        entries.append({
            # argument 在前，含独立数字 decoy（旧码会误取它）
            "argument": f"This point references baseline {decoy} as supporting detail here.",
            "slide_number": n,
        })
    return entries


def _write_digest_q3(ws: Path, entries: list) -> None:
    notes = ws / "output" / "notes"
    notes.mkdir(parents=True, exist_ok=True)
    (notes / "slides_points.md").write_text(
        "# Slide points\n\n" + json.dumps(entries, indent=2) + "\n",
        encoding="utf-8",
    )


def test_digest_q3_prefers_slide_number_field(tmp_path: Path):
    """argument 在前含诱饵数字、slide_number 在后 → 应按 slide_number 取值并 PASS。

    旧码取首个含数字的 value（argument），10 条 entry 的 slide 号会乱/重复 →
    覆盖 1..10 校验 FAIL。修复后优先取 slide_number 字段，恰好覆盖 1..10。
    """
    mod = load_check("s_research_digest_xl", "q3")
    ws = tmp_path / "ws"
    _write_digest_q3(ws, _digest_entries_argument_before_slide())
    assert run_check(mod, ws) == 0, "应优先采纳 slide_number 字段的值"


def test_digest_q3_oldlogic_would_pick_argument(tmp_path: Path):
    """绑定验证：旧『首个含数字 value』逻辑在此数据上会取到 argument 的诱饵号。

    直接对单条 entry 调 _extract_slide_number 逐值扫描，确认 argument 的诱饵数字
    会先于 slide_number 被命中——这正是修复要规避的取值顺序 bug。
    """
    mod = load_check("s_research_digest_xl", "q3")
    entry = {
        "argument": "This point references baseline 7 as supporting detail here.",
        "slide_number": 3,
    }
    values = list(entry.values())
    first_hit = next(
        (mod._extract_slide_number(v) for v in values
         if mod._extract_slide_number(v) is not None),
        None,
    )
    assert first_hit == 7, "旧顺序逻辑会先取 argument 里的 7（诱饵），而非 slide_number 3"


def test_digest_q3_normal_entries_pass(tmp_path: Path):
    """常规 entry（slide_number 在前/无诱饵）仍 PASS（修复未误伤）。"""
    mod = load_check("s_research_digest_xl", "q3")
    ws = tmp_path / "ws"
    entries = [
        {"slide_number": n, "argument": f"Substantive argument text for slide {n} here."}
        for n in range(1, 11)
    ]
    _write_digest_q3(ws, entries)
    assert run_check(mod, ws) == 0


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
