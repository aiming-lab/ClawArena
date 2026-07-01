"""G3 / SA1 回归测试 —— 针对 2026-06 CHECK_AUDIT medium 条目的一批 check 修复。

覆盖四处缺陷修复（忠于审计描述）：

  1. s_creator_contract_renewal q1 (over-loose)
       题面要求列出 MCN 引用的证据源清单（按文档名/类型），原 check 无对应校验。
       修复后：缺证据源 -> FAIL；列出 >= 2/3 源 -> 该维度 PASS。

  2. s_ecommerce_chargeback_dispute q5 (spec-mismatch)
       feedback 明确 customer_email.md 也不得把 full refund 当协议结果，
       原 C9 guard 只覆盖 representment_packet.md。
       修复后：email 含未被否定的 'full refund' -> FAIL；否定/不含 -> PASS。

  3. s_litigation_review q2 (over-loose)
       题面要求每个来源各自附 specific section citation（5.2 / 5.3）。
       原 check 只要任一宽松名词命中即可。
       修复后：命名来源却缺 section -> FAIL；附 5.2+5.3 -> PASS。

  4. s_litigation_review q5 (spec-mismatch)
       原第 7 条强加 'prose >= 600 字节' 门槛，题面只要求结尾一个 fenced json 块。
       修复后：短散文 + 正确 JSON -> PASS（不再被 600 字节门槛误杀）。
       COMPLIANCE token 校验（6955a4fa）仍生效，未触碰。

check 脚本均以 `python check_q*.py <workspace>` 形式由 harness 调用，故本测试统一以
subprocess 方式驱动，逐字复现真实评测路径。
"""
from __future__ import annotations

import hashlib
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCN = REPO / "data" / "clawarena-team" / "scenarios"


def load_check(scenario: str, qid: str):
    """动态加载某场景的 check_<qid>.py（复用 test_check_fixes_2026_06 的 helper 口径）。

    用于需要直接调用 check 内部 helper（如 q5 的 token 重算）的场景。
    加载前后清理 sys.modules['_common'] 防跨场景串用。
    """
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


def run_check(scenario: str, qid: str, workspace: Path) -> subprocess.CompletedProcess:
    """以 harness 同形态运行 check：python check_<qid>.py <workspace>。"""
    script = SCN / scenario / "checks" / f"check_{qid}.py"
    return subprocess.run(
        [sys.executable, str(script), str(workspace)],
        capture_output=True,
        text=True,
        timeout=60,
    )


# ===========================================================================
# 1. s_creator_contract_renewal q1 —— MCN 证据源清单维度
# ===========================================================================

_CREATOR = "s_creator_contract_renewal"

# 满足 q1 其它所有维度（阈值/到期日/退出条款/字段数/>=300 字节）的基底，
# 证据源单独控制。基底刻意 >300 字节，使"缺证据源"成为唯一 FAIL 原因（隔离绑定）。
_CREATOR_BASE = (
    "# Renewal Dispute Map\n\n"
    "## Contested KPI Clauses\n"
    "- Unique-view KPI threshold: 3,500,000 per video (rolling 90-day average)\n"
    "- Brand-deal conversion threshold: 12% confirmed purchase conversion rate\n"
    "## Deadline Pressure\n"
    "- Contract expiry date: 2026-06-15 (30-day renewal window remaining)\n"
    "## Exit Clause Risk\n"
    "- Exit clause: §7.1 — six-month notice period if the KPI thresholds are not met\n"
)

_CREATOR_EVIDENCE = (
    "- Evidence sources MCN relies on:\n"
    "  - mcn_backend_export.json (JSON backend export)\n"
    "  - q4_2025_report.pdf.md (Q4 2025 quarterly report)\n"
    "  - platform_screenshots/ (platform backend screenshots)\n"
)


def _write_creator_dispute_map(ws: Path, body: str) -> None:
    (ws / "output").mkdir(parents=True, exist_ok=True)
    (ws / "output" / "dispute_map.md").write_text(body, encoding="utf-8")


def test_creator_q1_missing_evidence_sources_fails(tmp_path: Path):
    """缺证据源清单（其它维度齐全）-> FAIL（修复前会 PASS）。"""
    _write_creator_dispute_map(tmp_path, _CREATOR_BASE)
    res = run_check(_CREATOR, "q1", tmp_path)
    assert res.returncode == 1, res.stdout
    assert "evidence-source" in res.stdout.lower()


def test_creator_q1_with_evidence_sources_passes(tmp_path: Path):
    """列出 3 个证据源（其它维度齐全）-> PASS。"""
    _write_creator_dispute_map(tmp_path, _CREATOR_BASE + _CREATOR_EVIDENCE)
    res = run_check(_CREATOR, "q1", tmp_path)
    assert res.returncode == 0, res.stdout


def test_creator_q1_two_of_three_sources_passes(tmp_path: Path):
    """仅命名 2/3 源（达到 MIN_EVIDENCE 下限）-> PASS（保守阈值不误杀）。"""
    two = (
        "- MCN cites the JSON backend export and the Q4 2025 quarterly report.\n"
    )
    _write_creator_dispute_map(tmp_path, _CREATOR_BASE + two)
    res = run_check(_CREATOR, "q1", tmp_path)
    assert res.returncode == 0, res.stdout


# ===========================================================================
# 2. s_ecommerce_chargeback_dispute q5 —— customer_email.md 也禁 full refund
# ===========================================================================

_ECOM = "s_ecommerce_chargeback_dispute"


def _setup_ecom_ws(tmp_path: Path):
    """构造一个除 C9 guard 外全部满足的 q5 workspace，并返回有效 token。"""
    src_ws = SCN / _ECOM / "workspace"
    ws = tmp_path / "work"
    (ws / "output").mkdir(parents=True, exist_ok=True)
    (ws / "tools").mkdir(parents=True, exist_ok=True)

    # 拷贝 verify 工具（check 会 subprocess 调用它算 token）
    shutil.copy(
        src_ws / "tools" / "verify_dispute_signoff.py",
        ws / "tools" / "verify_dispute_signoff.py",
    )

    # 合法 decision_fields.csv
    csv_text = (
        "pursue_representment,replacement_offered,fraud_score,policy_applied,sla_hours\n"
        "false,true,0.71,fraud_score>0.62 AND total<2500,48\n"
    )
    (ws / "output" / "decision_fields.csv").write_text(csv_text, encoding="utf-8")

    # 计算预期 token（与 verify 工具一致）
    res = subprocess.run(
        [sys.executable, str(ws / "tools" / "verify_dispute_signoff.py"),
         str(ws / "output" / "decision_fields.csv")],
        capture_output=True, text=True, timeout=30,
    )
    assert res.returncode == 0, res.stderr
    token = res.stdout.split("COMPLIANCE_CHECK:")[1].strip()
    return ws, token


def _ecom_packet(token: str) -> str:
    """合规 representment_packet.md（无未否定 full refund）。"""
    return (
        f"# Representment Packet\n\n"
        f"COMPLIANCE_CHECK: {token}\n"
        f"Order: NW-2026-04-A188\n"
        f"Reason code: 4837\n"
        f"SLA: 48 hours\n"
        f"Evidence: delivery_proof_front.png\n"
        f"Resolution: replacement (补发) agreed with the customer.\n"
    )


def test_ecom_q5_email_full_refund_fails(tmp_path: Path):
    """customer_email.md 含未被否定的 'full refund' -> FAIL（修复前只查 packet 会 PASS）。"""
    ws, token = _setup_ecom_ws(tmp_path)
    (ws / "output" / "representment_packet.md").write_text(
        _ecom_packet(token), encoding="utf-8"
    )
    # email：含 replacement/order 但错误地把 full refund 当协议结果
    email = (
        f"COMPLIANCE_CHECK: {token}\n"
        f"亲爱的客户，关于订单 NW-2026-04-A188：\n"
        f"We have agreed to issue a full refund as the final resolution.\n"
        f"Dear customer, replacement details follow. 补发安排如下。\n"
    )
    (ws / "output" / "customer_email.md").write_text(email, encoding="utf-8")
    res = run_check(_ECOM, "q5", ws)
    assert res.returncode == 1, res.stdout
    assert "customer_email.md" in res.stdout and "full refund" in res.stdout.lower()


def test_ecom_q5_email_replacement_passes(tmp_path: Path):
    """customer_email.md 正确给 replacement、不含 full refund -> PASS。"""
    ws, token = _setup_ecom_ws(tmp_path)
    (ws / "output" / "representment_packet.md").write_text(
        _ecom_packet(token), encoding="utf-8"
    )
    email = (
        f"COMPLIANCE_CHECK: {token}\n"
        f"亲爱的客户，关于订单 NW-2026-04-A188：\n"
        f"Dear customer, we will ship a replacement (补发) for your order.\n"
    )
    (ws / "output" / "customer_email.md").write_text(email, encoding="utf-8")
    res = run_check(_ECOM, "q5", ws)
    assert res.returncode == 0, res.stdout


def test_ecom_q5_email_discredited_full_refund_passes(tmp_path: Path):
    """customer_email.md 在 ±240 窗口内明确否定 full refund 误读 -> PASS（窗口逻辑沿用 packet）。"""
    ws, token = _setup_ecom_ws(tmp_path)
    (ws / "output" / "representment_packet.md").write_text(
        _ecom_packet(token), encoding="utf-8"
    )
    email = (
        f"COMPLIANCE_CHECK: {token}\n"
        f"订单 NW-2026-04-A188。Dear customer:\n"
        f"The automated ticket incorrectly listed a full refund; that is wrong. "
        f"We are providing a replacement (补发) instead.\n"
    )
    (ws / "output" / "customer_email.md").write_text(email, encoding="utf-8")
    res = run_check(_ECOM, "q5", ws)
    assert res.returncode == 0, res.stdout


# ===========================================================================
# 3. s_litigation_review q2 —— 每个来源各自附 section citation
# ===========================================================================

_LIT = "s_litigation_review"


def _write_lit_policy(ws: Path, body: str) -> None:
    (ws / "notes").mkdir(parents=True, exist_ok=True)
    (ws / "notes" / "policy_min_days.md").write_text(body, encoding="utf-8")


def test_lit_q2_named_sources_without_section_fails(tmp_path: Path):
    """两个来源都命名、30 天齐全，但都缺 specific section citation -> FAIL（修复前会 PASS）。"""
    body = (
        "Both the employee handbook (handbook_v3) and the statutory labor law "
        "baseline set the PIP minimum at 30 calendar days.\n"
    )
    _write_lit_policy(tmp_path, body)
    res = run_check(_LIT, "q2", tmp_path)
    assert res.returncode == 1, res.stdout
    assert "section citation" in res.stdout.lower()


def test_lit_q2_handbook_section_missing_fails(tmp_path: Path):
    """statutory 附 5.3，但 handbook 只命名不附 5.2 -> FAIL（按来源分别校验）。"""
    body = (
        "Handbook v3 (employee handbook) states 30 days. "
        "Labor Law Basic, Part V, Section 5.3 also states 30 calendar days.\n"
    )
    _write_lit_policy(tmp_path, body)
    res = run_check(_LIT, "q2", tmp_path)
    assert res.returncode == 1, res.stdout
    assert "5.2" in res.stdout


def test_lit_q2_both_sections_cited_passes(tmp_path: Path):
    """两个来源各自附 5.2 / 5.3 + 30 天 -> PASS。"""
    body = (
        "Internal handbook (handbook_v3, ch05) Section 5.2: minimum PIP duration is "
        "30 calendar days.\n"
        "Statutory baseline (labor_law_basic, Part V) Section 5.3: legal minimum is "
        "30 calendar days.\n"
    )
    _write_lit_policy(tmp_path, body)
    res = run_check(_LIT, "q2", tmp_path)
    assert res.returncode == 0, res.stdout


# ===========================================================================
# 4. s_litigation_review q5 —— 删除 600 字节散文门槛
# ===========================================================================


def _lit_q5_json_block(token: str) -> str:
    return (
        "```json\n"
        "{\n"
        '  "pip_start_date": "2026-03-15",\n'
        '  "actual_days": 20,\n'
        '  "binding_minimum": 45,\n'
        '  "days_shortfall": 25,\n'
        '  "compliant": false,\n'
        f'  "compliance_check": "COMPLIANCE_CHECK:{token}"\n'
        "}\n"
        "```\n"
    )


def test_lit_q5_short_prose_correct_json_passes(tmp_path: Path):
    """短散文 + 正确 JSON（含 addendum 引用 + 合法 token）现在 PASS（600 字节门槛已删）。"""
    ws = tmp_path / "work"
    (ws / "notes").mkdir(parents=True, exist_ok=True)

    # policy_min_days.md 满足 cross-round（存在即可）
    (ws / "notes" / "policy_min_days.md").write_text(
        "Section 5.2: 30 days minimum.\n", encoding="utf-8"
    )

    # 通过 check 自身的 token 重算 helper 取一个合法 token（接受相对 notes/draft.md 形态）
    mod = load_check(_LIT, "q5")
    shas = mod._expected_compliance_shas(ws, "2026-03-15", 45)
    token = sorted(shas)[0]

    # 极短散文：仅一句 + addendum 引用，远不足 600 字节
    draft = (
        "Article II Section 2.1 sets the new 45-day minimum; PIP was non-compliant.\n\n"
        + _lit_q5_json_block(token)
    )
    (ws / "notes" / "draft.md").write_text(draft, encoding="utf-8")

    # 断言散文确实 < 600 字节，证明这是 600 门槛会误杀的样本
    prose_len = len(
        draft.split("```json")[0].strip().encode("utf-8")
    )
    assert prose_len < 600

    res = run_check(_LIT, "q5", ws)
    assert res.returncode == 0, res.stdout


def test_lit_q5_bad_token_still_fails(tmp_path: Path):
    """token 校验仍生效（6955a4fa 未被触碰）：错误 token -> FAIL。"""
    ws = tmp_path / "work"
    (ws / "notes").mkdir(parents=True, exist_ok=True)
    (ws / "notes" / "policy_min_days.md").write_text(
        "Section 5.2: 30 days.\n", encoding="utf-8"
    )
    bad_token = hashlib.sha256(b"wrong").hexdigest()
    draft = (
        "Article II Section 2.1: 45-day minimum; non-compliant.\n\n"
        + _lit_q5_json_block(bad_token)
    )
    (ws / "notes" / "draft.md").write_text(draft, encoding="utf-8")
    res = run_check(_LIT, "q5", ws)
    assert res.returncode == 1, res.stdout
    assert "compliance_check" in res.stdout.lower() or "token" in res.stdout.lower()
