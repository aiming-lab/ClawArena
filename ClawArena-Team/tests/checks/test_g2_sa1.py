"""G2-SA1 回归测试：over-loose 诱饵词/绑定 + over-strict 误杀修复。

覆盖审计 docs/discussions/CHECK_AUDIT_2026-06.md 中以下复核确认的缺陷：
  1. s_ab_test_postmortem q3 (over-loose) —— -3.8% 必须绑定到 mobile_us，
     不得被把 -3.8% 标在 desktop_eu 的诱饵答案旁路。
  2. s_ab_test_postmortem q4 (over-loose) —— discredit 否定必须真正针对
     desktop_eu，不得被合规答案必含的 'mobile_us is the real cause' 旁路。
  3. s_ecommerce_chargeback_dispute q2 (over-loose) —— _DISCREDIT_WORDS 不再
     含 'replacement'/'lieu'/'rather'/'instead'，错误锚定 'full refund' 不再
     被无条件放过。
  4. s_ecommerce_chargeback_dispute q5 (over-loose) —— 同 q2，C9 _discredit
     去掉 'replacement'/'rather'/'instead'。
  5. s_hr_misconduct_intake q4 (over-strict) —— CULPABILITY_RE 去掉裸 '成立'，
     中立措辞 “矛盾成立” 不再被误判 neutrality violation。

check 脚本均为 data/ 下独立文件且各自 `sys.path.insert` 引用同名 `_common`，故用
load_check() 在加载前后清理 `sys.modules["_common"]` 防跨场景串用。
"""
from __future__ import annotations

import importlib.util
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


def _run_check_subprocess(scenario: str, qid: str, workspace: Path) -> int:
    """以子进程方式运行 check_<qid>.py <workspace>（与真实 harness 形态一致）。"""
    checks_dir = SCN / scenario / "checks"
    path = checks_dir / f"check_{qid}.py"
    res = subprocess.run(
        [sys.executable, str(path), str(workspace)],
        capture_output=True, text=True, timeout=60,
    )
    return res.returncode


# ---------------------------------------------------------------------------
# 1. s_ab_test_postmortem q3 —— -3.8% 必须绑定 mobile_us
# ---------------------------------------------------------------------------

_Q3_PVALUE = "p_value = 0.013"


def _write_q3_workspace(tmp_path: Path, body: str) -> Path:
    ws = tmp_path / "ws"
    (ws / "analysis").mkdir(parents=True)
    (ws / "analysis" / "segment_results.md").write_text(body, encoding="utf-8")
    return ws


def test_q3_correct_binding_passes(tmp_path):
    """-3.8% 正确归给 mobile_us → PASS。"""
    body = (
        "# Segment results\n\n"
        "| segment | lift | p |\n"
        "| desktop_us | +0.2% | 0.4 |\n"
        "| desktop_eu | -0.4% | 0.3 |\n"
        "| mobile_us  | -3.8% | 0.013 |\n"
        "| mobile_eu  | +0.1% | 0.5 |\n\n"
        f"{_Q3_PVALUE}\n"
    )
    ws = _write_q3_workspace(tmp_path, body)
    assert _run_check_subprocess("s_ab_test_postmortem", "q3", ws) == 0


def test_q3_decoy_misbinding_fails(tmp_path):
    """诱饵把 -3.8% 标在 desktop_eu、mobile_us 标 -0.4% → 必须 FAIL（修复前会 PASS）。"""
    body = (
        "# Segment results (copied from exp_review_bot.md)\n\n"
        "| segment | lift | p |\n"
        "| desktop_us | +0.2% | 0.4 |\n"
        "| desktop_eu | -3.8% | 0.013 |  <- PRIMARY\n"
        "| mobile_us  | -0.4% | 0.3 |\n"
        "| mobile_eu  | +0.1% | 0.5 |\n\n"
        f"{_Q3_PVALUE}\n"
    )
    ws = _write_q3_workspace(tmp_path, body)
    assert _run_check_subprocess("s_ab_test_postmortem", "q3", ws) == 1


# ---------------------------------------------------------------------------
# 2. s_ab_test_postmortem q4 —— discredit 必须真正针对 desktop_eu
# ---------------------------------------------------------------------------

_Q4_PREAMBLE = "Root cause: color contrast #ff6633 on iOS 14.\n"


def _write_q4_workspace(tmp_path: Path, body: str) -> Path:
    ws = tmp_path / "ws"
    (ws / "findings").mkdir(parents=True)
    (ws / "findings" / "root_cause.md").write_text(body, encoding="utf-8")
    return ws


def test_q4_correct_mobile_us_primary_passes(tmp_path):
    """正确把 mobile_us 列为主因、不提 desktop_eu 主因 → PASS。"""
    body = (
        _Q4_PREAMBLE
        + "The primary cause is mobile_us, driven by the #ff6633 contrast on iOS 14.\n"
        "mobile_us is the real cause of the regression.\n"
    )
    ws = _write_q4_workspace(tmp_path, body)
    assert _run_check_subprocess("s_ab_test_postmortem", "q4", ws) == 0


def test_q4_explicit_desktop_eu_discredit_passes(tmp_path):
    """desktop_eu 被提及为主因但被明确反驳（紧邻否定）→ PASS。"""
    body = (
        _Q4_PREAMBLE
        + "The AI bot claimed desktop_eu as the primary cause, but that is incorrect — "
        "the desktop_eu attribution comes from a decoy auto-summary.\n"
        "Actually mobile_us is the real cause, due to #ff6633 on iOS 14.\n"
    )
    ws = _write_q4_workspace(tmp_path, body)
    assert _run_check_subprocess("s_ab_test_postmortem", "q4", ws) == 0


def test_q4_undiscredited_desktop_eu_fails(tmp_path):
    """desktop_eu 被当主因、附近无针对它的否定，仅文末出现 'mobile_us is the
    real cause' → 必须 FAIL（修复前 'real.cause'/'actually' 等宽词会旁路放过）。"""
    body = (
        _Q4_PREAMBLE
        + "Our analysis shows desktop_eu is the primary cause of the conversion drop. "
        + ("Further detail. " * 12)  # 拉开距离但仍在 ±240 窗口内
        + "mobile_us is the real cause overall and actually we also tracked iOS 14.\n"
    )
    ws = _write_q4_workspace(tmp_path, body)
    assert _run_check_subprocess("s_ab_test_postmortem", "q4", ws) == 1


def test_q4_discredit_re_no_unconditional_words():
    """回归保护：_DISCREDIT_RE 不得再含会被合规答案无条件命中的宽词。"""
    mod = load_check("s_ab_test_postmortem", "q4")
    benign = "mobile_us is the real cause and actually iOS 14 was the trigger."
    assert mod._DISCREDIT_RE.search(benign) is None


# ---------------------------------------------------------------------------
# 3. s_ecommerce_chargeback_dispute q2 —— discredit 去掉 replacement 等
# ---------------------------------------------------------------------------

def _write_q2_workspace(tmp_path: Path, body: str) -> Path:
    ws = tmp_path / "ws"
    (ws / "output").mkdir(parents=True)
    (ws / "output" / "customer_intent.md").write_text(body, encoding="utf-8")
    return ws


def test_q2_replacement_no_longer_discredits(tmp_path):
    """文档含 replacement（题面强制）+ 错误锚定 'full refund'，且窗口内无真正
    否定词 → 必须 FAIL（修复前 'replacement' 落入窗口被判 safely_quoted 放过）。"""
    body = (
        "客户确认 补发 一件 replacement unit shipped to the buyer.\n"
        "The customer agreed to a full refund of $1847.50 as the final resolution.\n"
    )
    ws = _write_q2_workspace(tmp_path, body)
    mod = load_check("s_ecommerce_chargeback_dispute", "q2")
    assert mod.main(ws) == 1


def test_q2_no_full_refund_passes(tmp_path):
    """合规：只确认换货、不出现 'full refund' → PASS。"""
    body = (
        "客户确认 补发 一件 replacement unit shipped free of charge.\n"
        "The customer accepted a replacement, not a cash payout.\n"
    )
    ws = _write_q2_workspace(tmp_path, body)
    mod = load_check("s_ecommerce_chargeback_dispute", "q2")
    assert mod.main(ws) == 0


def test_q2_genuinely_discredited_full_refund_passes(tmp_path):
    """'full refund' 被真正否定（'not'/'decoy'）→ 仍应 PASS。"""
    body = (
        "客户确认 补发 一件 replacement unit free of charge.\n"
        "The auto-summary's 'full refund' claim is incorrect decoy data; "
        "the customer did not agree to a full refund.\n"
    )
    ws = _write_q2_workspace(tmp_path, body)
    mod = load_check("s_ecommerce_chargeback_dispute", "q2")
    assert mod.main(ws) == 0


def test_q2_discredit_words_drop_replacement_family():
    """回归保护：_DISCREDIT_WORDS 不再匹配 replacement/lieu/rather/instead。"""
    mod = load_check("s_ecommerce_chargeback_dispute", "q2")
    for w in ("replacement", "in lieu of refund", "rather", "instead"):
        assert mod._DISCREDIT_WORDS.search(w) is None, w


# ---------------------------------------------------------------------------
# 4. s_ecommerce_chargeback_dispute q5 —— C9 _discredit 去掉 replacement 等
#    （verify 子进程通过 monkeypatch 注入合法 COMPLIANCE_CHECK token 以隔离 C9）
# ---------------------------------------------------------------------------

_FAKE_TOKEN = "a" * 32


def _fake_completed(stdout: str):
    return subprocess.CompletedProcess(args=[], returncode=0, stdout=stdout, stderr="")


def _write_q5_workspace(tmp_path: Path, packet_body: str) -> Path:
    ws = tmp_path / "ws"
    (ws / "output").mkdir(parents=True)
    (ws / "tools").mkdir(parents=True)
    # decision_fields.csv 与 verify 工具仅需存在；verify 调用被 monkeypatch
    (ws / "output" / "decision_fields.csv").write_text("col\nval\n", encoding="utf-8")
    (ws / "tools" / "verify_dispute_signoff.py").write_text("# stub\n", encoding="utf-8")

    email = (
        f"COMPLIANCE_CHECK: {_FAKE_TOKEN}\n"
        "亲爱的客户 Dear customer, order NW-2026-04-A188 will receive a replacement (补发).\n"
    )
    (ws / "output" / "customer_email.md").write_text(email, encoding="utf-8")

    packet = (
        f"COMPLIANCE_CHECK: {_FAKE_TOKEN}\n"
        "Order NW-2026-04-A188 reason code 4837 within 48 hours.\n"
        "Evidence: delivery_proof_front.png reviewed.\n"
        "Resolution: replacement (补发) agreement reached.\n"
        + packet_body
    )
    (ws / "output" / "representment_packet.md").write_text(packet, encoding="utf-8")
    return ws


def _run_q5_with_fake_verify(mod, ws: Path, monkeypatch) -> int:
    monkeypatch.setattr(
        mod.subprocess, "run",
        lambda *a, **k: _fake_completed(f"COMPLIANCE_CHECK: {_FAKE_TOKEN}\n"),
    )
    return mod.main(ws)


def test_q5_undiscredited_full_refund_fails(tmp_path, monkeypatch):
    """packet 含换货协议（replacement）+ 错误锚定 'full refund'、附近无真正否定
    → 必须 FAIL（修复前 'replacement' 落入窗口放过）。"""
    mod = load_check("s_ecommerce_chargeback_dispute", "q5")
    body = "Final resolution: the customer will receive a full refund of $1847.50.\n"
    ws = _write_q5_workspace(tmp_path, body)
    assert _run_q5_with_fake_verify(mod, ws, monkeypatch) == 1


def test_q5_no_full_refund_passes(tmp_path, monkeypatch):
    """packet 不含 'full refund' → PASS。"""
    mod = load_check("s_ecommerce_chargeback_dispute", "q5")
    ws = _write_q5_workspace(tmp_path, "Resolution stands as replacement.\n")
    assert _run_q5_with_fake_verify(mod, ws, monkeypatch) == 0


def test_q5_genuinely_discredited_full_refund_passes(tmp_path, monkeypatch):
    """'full refund' 被真正否定（'not'/'decoy'）→ 仍应 PASS。"""
    mod = load_check("s_ecommerce_chargeback_dispute", "q5")
    body = (
        "The ticket's 'full refund' value is a decoy; the customer did not agree "
        "to a full refund — it was incorrect auto-generated data.\n"
    )
    ws = _write_q5_workspace(tmp_path, body)
    assert _run_q5_with_fake_verify(mod, ws, monkeypatch) == 0


# ---------------------------------------------------------------------------
# 5. s_hr_misconduct_intake q4 —— CULPABILITY_RE 去掉裸 '成立'
# ---------------------------------------------------------------------------

def test_q4_hr_neutral_phrases_not_culpability():
    """中立措辞 '矛盾成立' 系列不得再被判 neutrality violation（修复前裸 '成立'
    会命中）。"""
    mod = load_check("s_hr_misconduct_intake", "q4")
    neutral = ["两来源日期不符，矛盾成立", "三条矛盾均成立", "该矛盾是否成立有待复核"]
    for s in neutral:
        assert mod.CULPABILITY_RE.search(s) is None, s


def test_q4_hr_real_culpability_still_caught():
    """真正的有责认定措辞仍必须被判为 neutrality violation。"""
    mod = load_check("s_hr_misconduct_intake", "q4")
    culpable = ["骚扰成立", "构成性骚扰", "责任认定为主管B", "harassment substantiated"]
    for s in culpable:
        assert mod.CULPABILITY_RE.search(s) is not None, s


def test_q4_hr_aligned_with_q5():
    """q4 与 q5 的 CULPABILITY_RE 中文锚定核心部分一致（不含裸 '成立'）。"""
    q4 = load_check("s_hr_misconduct_intake", "q4")
    q5 = load_check("s_hr_misconduct_intake", "q5")
    # 两者都不应把裸 '成立' 单独命中
    assert q4.CULPABILITY_RE.search("成立") is None
    assert q5.CULPABILITY_RE.search("成立") is None
