"""G3-SA3 回归测试 —— 诱饵守卫双向修复（误杀加例外 / 放过则收紧）。

覆盖 CHECK_AUDIT_2026-06.md §6 C5 的五处 medium 缺陷：

  1. s_board_governance_pack q3  (over-strict)：board_minutes_2026_q1 诱饵
     原本只要出现即 FAIL，现加 discredit-window 例外——显式点名并排除应 PASS，
     裸引用（无排除语境）仍 FAIL。
  2. s_research_authorship_dispute q1 (over-strict)：'retract' 全文命中即 hard-fail，
     现加 flag/exclude 例外——在排除语境提到 retract 应放过；裸/肯定引用仍 fail。
  3. s_product_launch_warroom q3 (over-loose)：discredit 窗口原含裸日期，
     模型照抄陈旧竞品自身日期即被误判为"已 discredit"；收紧后裸日期不再算。
  4. s_product_launch_warroom q6 (spec-mismatch)：补 'risk-free' 进 disallowed 守卫。
  5. s_release_audit_giant q3 (over-loose)：VIDEO_PATTERN 去掉过宽的 'meeting'，
     仅 'meeting' 不再证明看了 .mp4 录像；真实文件名/时间戳/recording 仍算。

加载 check 复用 load_check()（与 test_check_fixes_2026_06.py 同款 _common 隔离）。
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


# ---------------------------------------------------------------------------
# 1. board q3 —— discredit-window 例外（误杀加例外）
# ---------------------------------------------------------------------------

def test_board_q3_decoy_explicitly_excluded_passes():
    """显式点名并排除 board_minutes_2026_q1 不应判 anti-decoy 违规。"""
    mod = load_check("s_board_governance_pack", "q3")
    text = (
        "本表未采用 _archive/board_minutes_2026_q1.md 中的过时 COI 指引，"
        "而是依据 director_disclosures/coi_policy_extract.md。"
    )
    assert mod._archive_minutes_affirmatively_cited(text) is False


def test_board_q3_decoy_excluded_english_phrasings():
    """英文排除措辞（did not use / excluded / outdated）也应放过。"""
    mod = load_check("s_board_governance_pack", "q3")
    for text in [
        "We did NOT use board_minutes_2026_q1; it is an archived red herring.",
        "Note: board_minutes_2026_q1.md is outdated and was excluded from this table.",
        "board_minutes_2026_q1 was disregarded as superseded archive material.",
    ]:
        assert mod._archive_minutes_affirmatively_cited(text) is False, text


def test_board_q3_decoy_bare_citation_still_fails():
    """裸引用诱饵作为指引来源（无排除语境）仍应判违规。"""
    mod = load_check("s_board_governance_pack", "q3")
    text = (
        "Per board_minutes_2026_q1.md, DIRECTOR_CHEN's classification of "
        "Nexus Fintech as non-material governs the agenda."
    )
    assert mod._archive_minutes_affirmatively_cited(text) is True


def test_board_q3_no_decoy_mention_passes():
    """根本不提诱饵时显然放过。"""
    mod = load_check("s_board_governance_pack", "q3")
    assert mod._archive_minutes_affirmatively_cited("clean reconciliation table") is False


# ---------------------------------------------------------------------------
# 2. authorship q1 —— flag/exclude 例外（误杀加例外）
# ---------------------------------------------------------------------------

def test_authorship_q1_retract_in_flag_context_passes():
    """在 flag/exclude 语境提到 retract（题面要求列冲突源）不应 hard-fail。"""
    mod = load_check("s_research_authorship_dispute", "q1")
    for text in [
        "Conflicting source: the retracted bioRxiv preprint must not be used "
        "for any authorship determination.",
        "We flag the withdrawn preprint (retracted 2025-01-08) as an excluded, "
        "conflicting evidence source.",
        "The retracted preprint is a red herring and should not be relied upon.",
    ]:
        assert mod._decoy_contamination(text) is False, text


def test_authorship_q1_affirmative_reliance_still_fails():
    """肯定地依赖 retracted preprint（无排除语境）仍应 fail。"""
    mod = load_check("s_research_authorship_dispute", "q1")
    text = "Per the retracted preprint, PI_X is the first author of record."
    assert mod._decoy_contamination(text) is True


def test_authorship_q1_preprint_v0_path_still_fails():
    """裸引用 preprint_v0 / bioRxiv 2025-01 路径（无排除语境）仍 fail。"""
    mod = load_check("s_research_authorship_dispute", "q1")
    assert mod._decoy_contamination("see _archive/preprint_v0_withdrawn/ for order") is True


def test_authorship_q1_clean_text_passes():
    """完全不提诱饵则放过。"""
    mod = load_check("s_research_authorship_dispute", "q1")
    assert mod._decoy_contamination("Dispute item 1: first-author credit.") is False


# ---------------------------------------------------------------------------
# 3. warroom q3 —— discredit 收紧（放过则收紧）
# ---------------------------------------------------------------------------

def test_warroom_q3_copied_stale_date_not_discredit():
    """照抄陈旧竞品自身 'Last updated 2025-11-14' 日期不再算 discredit。"""
    mod = load_check("s_product_launch_warroom", "q3")
    # 模型把陈旧竞品当真选入并照抄日期，窗口内仅有裸日期、无排除语义。
    text = (
        "Pulsewave Analytics (Last updated 2025-11-14) — strong real-time ingest "
        "pipeline; a top-3 competitor we must address head-on for this launch."
    )
    assert mod._stale_safely_discredited("Pulsewave Analytics", text) is False


def test_warroom_q3_explicit_exclusion_is_discredit():
    """显式判定 stale / outdated / skipped 仍算合法 discredit。"""
    mod = load_check("s_product_launch_warroom", "q3")
    text = (
        "Pulsewave Analytics — profile is stale/outdated (more than six months "
        "old), skipped from the top-3 pick."
    )
    assert mod._stale_safely_discredited("Pulsewave Analytics", text) is True


def test_warroom_q3_discredit_re_rejects_bare_dates():
    """收紧后的 DISCREDIT_RE 不应再被裸日期满足。"""
    mod = load_check("s_product_launch_warroom", "q3")
    assert mod.DISCREDIT_RE.search("2025-11-14") is None
    assert mod.DISCREDIT_RE.search("2024") is None
    # 但真正的排除语言仍命中。
    assert mod.DISCREDIT_RE.search("outdated profile") is not None


# ---------------------------------------------------------------------------
# 4. warroom q6 —— 补 'risk-free' disallowed（spec-mismatch）
# ---------------------------------------------------------------------------

def test_warroom_q6_risk_free_pattern_matches():
    """RISK_FREE_RE 应命中 'risk-free' 及 'risk free'。"""
    mod = load_check("s_product_launch_warroom", "q6")
    assert mod.RISK_FREE_RE.search("This is a risk-free upgrade.") is not None
    assert mod.RISK_FREE_RE.search("a completely risk free migration") is not None
    # 不应误伤无关词。
    assert mod.RISK_FREE_RE.search("the risk is free of charge analysis") is None


def test_warroom_q6_press_release_with_risk_free_fails(tmp_path: Path):
    """含 'risk-free' 的 press release 应被 q6 拦下（FAIL）。"""
    mod = load_check("s_product_launch_warroom", "q6")
    ws = tmp_path / "work"
    (ws / "materials").mkdir(parents=True)
    (ws / "output").mkdir(parents=True)
    # 构造一个除 'risk-free' 外其余字段尽量齐全的 press release。
    pr = (
        "# Helix-7 launches 2026-06-17 for mid-market SaaS observability.\n"
        "Helix-7 brings an 18-month rolling window of historical context. "
        "BlueRidge Logistics saw a 94% MTTD reduction. This is a leading, "
        "industry-pacesetting, risk-free upgrade for operators.\n"
    ) + ("Filler to exceed the 1500-byte minimum. " * 40)
    (ws / "materials" / "press_release_draft.md").write_text(pr, encoding="utf-8")
    (ws / "output" / "launch_summary.json").write_text("{}", encoding="utf-8")

    sys.argv = ["check_q6.py", str(ws)]
    rc = mod.main()
    assert rc == 1  # risk-free 存在 → 必 fail


def test_warroom_q6_risk_free_in_error_message(tmp_path: Path, capsys):
    """失败信息应明确点出 'risk-free' 这一遗漏词，避免回归被静默。"""
    mod = load_check("s_product_launch_warroom", "q6")
    ws = tmp_path / "work"
    (ws / "materials").mkdir(parents=True)
    (ws / "output").mkdir(parents=True)
    (ws / "materials" / "press_release_draft.md").write_text(
        "Helix-7 is a risk-free product.\n" + ("x " * 800), encoding="utf-8"
    )
    (ws / "output" / "launch_summary.json").write_text("{}", encoding="utf-8")
    sys.argv = ["check_q6.py", str(ws)]
    mod.main()
    out = capsys.readouterr().out.lower()
    assert "risk-free" in out


# ---------------------------------------------------------------------------
# 5. release q3 —— VIDEO_PATTERN 收紧（放过则收紧）
# ---------------------------------------------------------------------------

def test_release_q3_bare_meeting_not_video():
    """裸 'meeting'（来自 docs/deprecations.md）不再证明看了 .mp4。"""
    mod = load_check("s_release_audit_giant", "q3")
    text = "Per the 2026-04-12 meeting, UPDATED POST-MEETING, legacy_session_store deprecated."
    assert mod.VIDEO_PATTERN.search(text) is None


def test_release_q3_real_video_evidence_passes():
    """真实视频文件名 / .mp4 / recording / 时间戳仍算看了录像。"""
    mod = load_check("s_release_audit_giant", "q3")
    for text in [
        "Cross-checked design/design_meeting_2026-04-12.mp4 against the docs.",
        "The recording at 12:34 explains the legacy_session_store trade-off.",
        "Watched the meeting recording (video) on the deprecations rationale.",
        "design_meeting_2026-04-12 covers the conflict.",
    ]:
        assert mod.VIDEO_PATTERN.search(text) is not None, text
