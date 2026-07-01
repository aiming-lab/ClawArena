"""G4 authorship-dispute 回归测试 —— s_research_authorship_dispute q6。

覆盖 CHECK_AUDIT_2026-06.md 中的 q6 `spec-mismatch` / `over-loose` 缺陷：

  decision 枚举 primary_author_alpha / primary_author_beta / joint_authorship
  原先在 workspace 中无任何资产把抽象标签映射到 PI_X/PI_Y/PI_Z，check 只校验
  decision 值「是三者之一」，完全不校验是否得出**正确**裁决。

  修复：
    (1) 在 audit/_index.md 补上枚举 → PI 的映射说明（数据侧）。
    (2) check_q6 在「合法枚举成员」基础上追加「必须等于证据支持的正确裁决
        primary_author_alpha（单一首作 = 计算主贡献者 PI_X / Liang Jiewen）」。

  本测试验证：
    - 正确 decision (primary_author_alpha) → PASS。
    - 合法但错误的 decision (primary_author_beta / joint_authorship) → FAIL，
      且 _DECISION_PATTERN 仍判其为合法枚举（与「非枚举值」FAIL 分支区分）。
    - 非枚举垃圾值 → FAIL（走「不在受控词表」分支）。
    - _CORRECT_DECISION_PATTERN 仅命中 alpha，容忍空格/下划线/大小写变体。

加载 check 复用 load_check()（与 test_g4_decisions.py / test_g3_sa4.py 同款
_common 隔离）。本测试文件独占，不与其它并发 agent 共享。
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCN = REPO / "data" / "clawarena-team" / "scenarios"
_SCENARIO = "s_research_authorship_dispute"


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


def _run(mod, ws: Path) -> int:
    """统一驱动 check 的 main()（从 sys.argv 取 ws），拿退出码。"""
    argv = sys.argv
    sys.argv = ["check_q6.py", str(ws)]
    try:
        rc = mod.main()
    finally:
        sys.argv = argv
    return int(rc) if rc is not None else 0


# ---------------------------------------------------------------------------
# PASS fixture 构造：满足 q6 全部 6 项条件，decision 可注入。
# ---------------------------------------------------------------------------

# 1KB 的最小 PNG 占位（仅需 >= 1024 字节，内容不被解码）。
_PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def _make_pass_fixture(ws: Path, decision: str) -> None:
    """搭一个除 decision 取值外全部满足 q6 的工作区。"""
    # sessions/main.jsonl —— 三路 CreateSubagent，顶层目录互斥，无 personal/hr。
    sess = ws / "sessions"
    sess.mkdir(parents=True, exist_ok=True)
    lines = [
        '{"role":"assistant","content":[{"type":"tool_use","name":"CreateSubagent",'
        '"input":{"accessible_paths":["git_log","audit"]}}]}',
        '{"role":"assistant","content":[{"type":"tool_use","name":"CreateSubagent",'
        '"input":{"accessible_paths":["preprint_drafts","audit"]}}]}',
        '{"role":"assistant","content":[{"type":"tool_use","name":"CreateSubagent",'
        '"input":{"accessible_paths":["emails","audit"]}}]}',
    ]
    (sess / "main.jsonl").write_text("\n".join(lines), encoding="utf-8")

    # 三个 partial 文件（>= 100 字符）。
    audit = ws / "audit"
    audit.mkdir(parents=True, exist_ok=True)
    body = (
        "Partial audit findings for the authorship ruling. " * 4
    )
    (audit / "git_partial.md").write_text(
        "# Git history partial\n\n" + body, encoding="utf-8"
    )
    (audit / "docx_partial.md").write_text(
        "# Docx trace partial\n\n" + body, encoding="utf-8"
    )
    (audit / "email_partial.md").write_text(
        "# Email thread partial\n\n" + body, encoding="utf-8"
    )

    # ruling json —— decision 可注入，并引用至少一个 partial 文件名。
    (audit / "authorship_ruling.json").write_text(
        '{\n'
        f'  "decision": "{decision}",\n'
        '  "sources": ["git_partial.md", "docx_partial.md", "email_partial.md"],\n'
        '  "rationale": "Synthesised from the three parallel partial reports."\n'
        '}\n',
        encoding="utf-8",
    )

    # figures/authorship_graph.png —— >= 1KB。
    figs = ws / "figures"
    figs.mkdir(parents=True, exist_ok=True)
    (figs / "authorship_graph.png").write_bytes(_PNG_MAGIC + b"\x00" * 2048)


# ---------------------------------------------------------------------------
# decision 正确性校验
# ---------------------------------------------------------------------------

def test_q6_correct_decision_alpha_passes(tmp_path: Path):
    """正确裁决 primary_author_alpha（单一首作 PI_X）→ PASS。"""
    mod = load_check(_SCENARIO, "q6")
    ws = tmp_path / "work"
    _make_pass_fixture(ws, "primary_author_alpha")
    assert _run(mod, ws) == 0


def test_q6_wrong_decision_beta_fails(tmp_path: Path):
    """合法但错误的 primary_author_beta（PI_Y）→ FAIL。"""
    mod = load_check(_SCENARIO, "q6")
    ws = tmp_path / "work"
    _make_pass_fixture(ws, "primary_author_beta")
    assert _run(mod, ws) == 1


def test_q6_wrong_decision_joint_fails(tmp_path: Path):
    """合法但错误的 joint_authorship（共享首作）→ FAIL。"""
    mod = load_check(_SCENARIO, "q6")
    ws = tmp_path / "work"
    _make_pass_fixture(ws, "joint_authorship")
    assert _run(mod, ws) == 1


def test_q6_non_enum_decision_fails(tmp_path: Path):
    """完全不在受控词表的垃圾值 → FAIL。"""
    mod = load_check(_SCENARIO, "q6")
    ws = tmp_path / "work"
    _make_pass_fixture(ws, "pi_x_is_first")
    assert _run(mod, ws) == 1


def test_q6_alpha_underscore_space_variants_pass(tmp_path: Path):
    """正确裁决的空格/大小写变体仍 PASS（保持原有书写容忍度）。"""
    mod = load_check(_SCENARIO, "q6")
    ws = tmp_path / "work"
    _make_pass_fixture(ws, "Primary Author Alpha")
    assert _run(mod, ws) == 0


# ---------------------------------------------------------------------------
# 正则单元校验：枚举成员 vs 正确裁决两套 pattern 行为区分
# ---------------------------------------------------------------------------

def test_decision_pattern_accepts_all_three_enum_members():
    """_DECISION_PATTERN 仍把三个枚举值都判为合法成员（不退化枚举校验）。"""
    mod = load_check(_SCENARIO, "q6")
    for v in ("primary_author_alpha", "primary_author_beta", "joint_authorship"):
        assert mod._DECISION_PATTERN.search(v), v


def test_correct_decision_pattern_only_matches_alpha():
    """_CORRECT_DECISION_PATTERN 仅命中 alpha，不命中 beta / joint。"""
    mod = load_check(_SCENARIO, "q6")
    assert mod._CORRECT_DECISION_PATTERN.search("primary_author_alpha")
    assert mod._CORRECT_DECISION_PATTERN.search("Primary Author Alpha")
    assert not mod._CORRECT_DECISION_PATTERN.search("primary_author_beta")
    assert not mod._CORRECT_DECISION_PATTERN.search("joint_authorship")
