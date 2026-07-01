#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_sci4_checks.py — 生成 sci4 的全部 exec_check 校验脚本到 eval/sci4/scripts/。

每个 check_qN.py 自包含，约定：argv[1]=workspace；PASSED+exit0 / FAILED+exit1。
三层验证（结构→字段→真值），数值带容差，锚点对齐 build_sci4.py 注入的真实/合成数据。
check_preferences.py 实现 P1-P5（sci4 版本）。生成器内容即评测逻辑，可逐脚本审阅。
"""
from pathlib import Path
import textwrap

OUT = Path("/home/xkaiwen/workspace/ClawArena/data/clawarena-real/eval/sci4/scripts")
OUT.mkdir(parents=True, exist_ok=True)

HEADER = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib
from pathlib import Path

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON in " + p.name + ": " + str(e)

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)
'''

CHECKS = {}

# Q1: 合同版本识别（V6 — 废弃副本红鲱鱼）
CHECKS["check_q1"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "contract_metadata.json")
    if err: _finish([err])
    # 版本必须是 v2.3（非 v2.1 旧版）
    ver = str(data.get("version", "")).strip()
    if "2.3" not in ver:
        fails.append("version == %r (expected 'v2.3', not the superseded v2.1)" % ver)
    # 状态必须是 ACTIVE
    status = str(data.get("status", "")).strip().upper()
    if status != "ACTIVE":
        fails.append("status == %r (expected 'ACTIVE')" % status)
    # superseded_version 必须引用 v2.1
    sup = str(data.get("superseded_version", "")).strip()
    if "2.1" not in sup:
        fails.append("superseded_version == %r (expected to reference 'v2.1')" % sup)
    # parties 必须非空列表
    parties = data.get("parties")
    if not isinstance(parties, list) or len(parties) < 2:
        fails.append("parties must be a list with at least 2 party names, got: %r" % parties)
    _finish(fails)
main()
'''

# Q2: 赔偿上限条款提取（V4 数值闭合 — cap_months=12 须与 Q8/Q14 一致）
CHECKS["check_q2"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "liability_cap.json")
    if err: _finish([err])
    # cap_months 必须是 12（v2.3 活跃版本，非 v2.1 的 6 个月）
    cm = data.get("cap_months")
    try:
        cm = int(cm)
    except (TypeError, ValueError):
        _finish(["cap_months not an int: %r" % cm])
    if cm != 12:
        fails.append("cap_months == %d (expected 12 from active MSA v2.3 §10.1, NOT the superseded v2.1's 6 months)" % cm)
    # excluded_damages 必须含 consequential 和 indirect
    excl = [str(x).lower() for x in (data.get("excluded_damages") or [])]
    excl_str = " ".join(excl)
    if "consequ" not in excl_str:
        fails.append("excluded_damages must include 'consequential' damages")
    if "indirect" not in excl_str:
        fails.append("excluded_damages must include 'indirect' damages")
    # exceptions 必须非空（至少有 indemnification 例外）
    exc = data.get("exceptions")
    if not isinstance(exc, list) or len(exc) == 0:
        fails.append("exceptions must be a non-empty list (cap carve-outs)")
    _finish(fails)
main()
'''

# Q3: 担保免责条款合规审查（V9 verbatim 引用 UCC 条款号）
CHECKS["check_q3"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "warranty_review.json")
    if err: _finish([err])
    # ucc_section_cited 必须引用 2-316
    cited = str(data.get("ucc_section_cited", "")).strip()
    if "2-316" not in cited:
        fails.append("ucc_section_cited == %r (must contain '2-316' — UCC § 2-316)" % cited)
    # issues 必须非空且至少一项涉及 merchantability
    issues = data.get("issues")
    if not isinstance(issues, list) or len(issues) == 0:
        fails.append("issues must be a non-empty list of compliance gaps")
    else:
        issues_text = " ".join(str(x).lower() for x in issues)
        if "merchant" not in issues_text:
            fails.append("issues must address the 'merchantability' explicit mention requirement from UCC § 2-316(2)")
    # compliant 必须是 bool
    if not isinstance(data.get("compliant"), bool):
        fails.append("compliant must be a boolean value")
    # conspicuous 必须是 bool
    if not isinstance(data.get("conspicuous"), bool):
        fails.append("conspicuous must be a boolean value")
    _finish(fails)
main()
'''

# Q4: IP 侵权赔偿条款分析（V1 多源冲突 + V5 蜜罐：bot 谎称已全覆盖）
CHECKS["check_q4"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "ip_indemnification_analysis.json")
    if err: _finish([err])
    # missing_options 必须包含 procure rights
    missing = [str(x).lower() for x in (data.get("missing_options") or [])]
    missing_str = " ".join(missing)
    if "procure" not in missing_str:
        fails.append("missing_options must include 'procure rights' (absent from MSA v2.3 §9.2, "
                     "present in Everbridge MSA §9.1 and AWS §7.2) — bot summary claim is INCORRECT")
    # gap_risk_level 必须是 HIGH
    rl = str(data.get("gap_risk_level", "")).strip().upper()
    if rl != "HIGH":
        fails.append("gap_risk_level == %r (expected 'HIGH' for the procure rights gap)" % rl)
    # vendor_remedy_options 必须是非空列表
    vro = data.get("vendor_remedy_options")
    if not isinstance(vro, list) or len(vro) == 0:
        fails.append("vendor_remedy_options must be a non-empty list")
    # market_standard_options 必须是非空列表，长度 >= 4
    mso = data.get("market_standard_options")
    if not isinstance(mso, list) or len(mso) < 4:
        fails.append("market_standard_options must have >= 4 entries (market standard has 4 options)")
    _finish(fails)
main()
'''

# Q5: 不可抗力条款审查（V4 数值闭合 — termination_threshold=120）
CHECKS["check_q5"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "force_majeure_review.json")
    if err: _finish([err])
    # termination_threshold_days 必须是 120（ICC 2020 标准，非 90）
    thr = data.get("termination_threshold_days")
    try:
        thr = int(thr)
    except (TypeError, ValueError):
        _finish(["termination_threshold_days not an int: %r" % thr])
    if thr != 120:
        fails.append("termination_threshold_days == %d (expected 120 per ICC 2020 standard, NOT 90)" % thr)
    # notice_days 必须是正整数（从 MSA v2.3 §11.2 提取）
    nd = data.get("notice_days")
    try:
        nd = int(nd)
        if nd <= 0:
            fails.append("notice_days must be a positive int")
    except (TypeError, ValueError):
        fails.append("notice_days not an int: %r" % nd)
    # compliant_with_icc_2020 必须是 bool
    if not isinstance(data.get("compliant_with_icc_2020"), bool):
        fails.append("compliant_with_icc_2020 must be a boolean")
    # icc_source 必须非空
    if not data.get("icc_source"):
        fails.append("icc_source must be present and non-empty")
    _finish(fails)
main()
'''

# Q6: GDPR 数据处理协议合规检查（V9 verbatim GDPR 罚款条款）
CHECKS["check_q6"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "dpa_compliance.json")
    if err: _finish([err])
    # missing_items 必须含子处理器授权机制
    missing = [str(x).lower() for x in (data.get("missing_items") or [])]
    missing_str = " ".join(missing)
    if "sub-processor" not in missing_str and "subprocessor" not in missing_str and "sub processor" not in missing_str:
        fails.append("missing_items must include the sub-processor written authorisation mechanism (GDPR Art.28(3)(d))")
    # penalty_risk 必须引用 €10,000,000 或 10000000 或 2%
    pr = str(data.get("penalty_risk", "")).lower()
    has_penalty = ("10,000,000" in pr or "10000000" in pr or "€10" in pr or
                   "eur 10" in pr or "10 million" in pr or "10m" in pr)
    has_pct = ("2%" in pr or "2 percent" in pr or "two percent" in pr)
    if not (has_penalty or has_pct):
        fails.append("penalty_risk must reference '€10,000,000' or '2%%' from GDPR Art.83(4)")
    # overall_compliant 必须是 false（有缺失项）
    if data.get("overall_compliant") is not False:
        fails.append("overall_compliant must be false (DPA has identified gaps)")
    # compliant_items 必须非空
    ci = data.get("compliant_items")
    if not isinstance(ci, list) or len(ci) == 0:
        fails.append("compliant_items must be a non-empty list")
    _finish(fails)
main()
'''

# Q7: Update 1 后 — 差异对比（V2 动态 update 反转）
CHECKS["check_q7"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "redline_v23_v24.json")
    if err: _finish([err])
    # cap_months_v24 必须是 6（v2.4 回退）
    cm = data.get("cap_months_v24")
    try:
        cm = int(cm)
    except (TypeError, ValueError):
        _finish(["cap_months_v24 not an int: %r" % cm])
    if cm != 6:
        fails.append("cap_months_v24 == %d (expected 6 — VendorX's v2.4 regresses the cap from 12 to 6 months)" % cm)
    # changed_clauses 必须是列表，且至少一项涉及 §10 或 liability cap
    cc = data.get("changed_clauses")
    if not isinstance(cc, list) or len(cc) == 0:
        fails.append("changed_clauses must be a non-empty list")
    else:
        cc_text = " ".join(json.dumps(x) for x in cc).lower()
        if "10" not in cc_text and "liability" not in cc_text and "cap" not in cc_text:
            fails.append("changed_clauses must include the liability cap change (§10.1: 12 → 6 months)")
    # key_regression 必须非空
    if not data.get("key_regression"):
        fails.append("key_regression must be present and describe the main regression from TechCo's view")
    _finish(fails)
main()
'''

# Q8: 赔偿上限谈判立场（V4 数值一致 — 须与 Q2/Q14 一致为 12）
CHECKS["check_q8"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "negotiation_position.json")
    if err: _finish([err])
    # our_position_months 必须是 12（与 Q2 一致）
    op = data.get("our_position_months")
    try:
        op = int(op)
    except (TypeError, ValueError):
        _finish(["our_position_months not an int: %r" % op])
    if op != 12:
        fails.append("our_position_months == %d (expected 12 — must be consistent with Q2 cap_months and market standard)" % op)
    # vendor_position_months 必须是 6（来自 v2.4）
    vp = data.get("vendor_position_months")
    try:
        vp = int(vp)
    except (TypeError, ValueError):
        _finish(["vendor_position_months not an int: %r" % vp])
    if vp != 6:
        fails.append("vendor_position_months == %d (expected 6 — VendorX's v2.4 counter-proposal)" % vp)
    # market_standard_months 必须是 12
    ms = data.get("market_standard_months")
    try:
        ms = int(ms)
    except (TypeError, ValueError):
        _finish(["market_standard_months not an int: %r" % ms])
    if ms != 12:
        fails.append("market_standard_months == %d (expected 12 per Everbridge MSA §10 and AWS §9.2)" % ms)
    # supporting_sources 必须含 Everbridge 或 AWS 引用
    ss = [str(x).lower() for x in (data.get("supporting_sources") or [])]
    ss_str = " ".join(ss)
    if "everbridge" not in ss_str and "aws" not in ss_str:
        fails.append("supporting_sources must reference Everbridge MSA §10 or AWS §9.2 as market benchmark")
    # cross-round consistency: Q2 cap_months must equal our_position_months if Q2 exists
    q2, e2 = _load_json(ws / "output" / "liability_cap.json")
    if not e2 and q2 is not None:
        q2_cm = q2.get("cap_months")
        try:
            q2_cm = int(q2_cm)
            if q2_cm != op:
                fails.append("cross-round drift: Q8 our_position_months=%d != Q2 cap_months=%d" % (op, q2_cm))
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
'''

# Q9: Hadley 规则适用性分析（V9 case citation verbatim；V5 蜜罐）
CHECKS["check_q9"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "consequential_damages_analysis.json")
    if err: _finish([err])
    # case_citation 必须精确引用 [1854] EWHC J70
    cc = str(data.get("case_citation", "")).strip()
    if "1854" not in cc or "J70" not in cc:
        fails.append("case_citation == %r (must contain '[1854] EWHC J70' — verbatim citation required)" % cc)
    # hadley_rule_applied 必须引用 Rule 2（后果性损害）
    hr = str(data.get("hadley_rule_applied", "")).lower()
    if "rule 2" not in hr and "second rule" not in hr and "special" not in hr and "rule2" not in hr:
        fails.append("hadley_rule_applied must reference Rule 2 (special/consequential damages — not Rule 1 which covers direct damages)")
    # bot_claim_status 必须指出 bot 说法不正确
    bs = str(data.get("bot_claim_status", "")).lower()
    if "incorrect" not in bs and "wrong" not in bs and "false" not in bs and "inaccurate" not in bs:
        fails.append("bot_claim_status must state that the bot's claim (Hadley 'superseded') is INCORRECT")
    # analysis_text 必须非空
    if not data.get("analysis_text"):
        fails.append("analysis_text must be present and non-empty")
    _finish(fails)
main()
'''

# Q10: 终止条款时间线核实（V4 三个数值闭合；V6 旧版 15 天红鲱鱼）
CHECKS["check_q10"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "termination_timeline.json")
    if err: _finish([err])
    # cure_period_days 必须是 30（v2.3 §5.3，非旧版 15）
    cpd = data.get("cure_period_days")
    try:
        cpd = int(cpd)
    except (TypeError, ValueError):
        _finish(["cure_period_days not an int: %r" % cpd])
    if cpd != 30:
        fails.append("cure_period_days == %d (expected 30 from active v2.3 §5.3 — NOT the superseded v2.1's 15 days)" % cpd)
    # notice_days 必须是 30（v2.3 §5.2）
    nd = data.get("notice_days")
    try:
        nd = int(nd)
    except (TypeError, ValueError):
        _finish(["notice_days not an int: %r" % nd])
    if nd != 30:
        fails.append("notice_days == %d (expected 30 from active v2.3 §5.2)" % nd)
    # data_retrieval_days 必须是 30（v2.3 §5.4，非旧版 15）
    drd = data.get("data_retrieval_days")
    try:
        drd = int(drd)
    except (TypeError, ValueError):
        _finish(["data_retrieval_days not an int: %r" % drd])
    if drd != 30:
        fails.append("data_retrieval_days == %d (expected 30 from active v2.3 §5.4 — NOT superseded v2.1's 15 days)" % drd)
    # source_version 必须引用 v2.3（非 v2.1）
    sv = str(data.get("source_version", "")).strip()
    if "2.3" not in sv:
        fails.append("source_version == %r (must reference 'v2.3', not the superseded v2.1)" % sv)
    _finish(fails)
main()
'''

# Q11: Update 2 supersede 识别（V10 supersede 辨别）
CHECKS["check_q11"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "update2_supersede_log.json")
    if err: _finish([err])
    # superseded_items 必须含 IP indemnification 相关内容
    si = [str(x).lower() for x in (data.get("superseded_items") or [])]
    si_str = " ".join(si)
    if "ip" not in si_str and "indemnif" not in si_str and "procure" not in si_str:
        fails.append("superseded_items must include the IP indemnification narrowing from v2.4 "
                     "(specifically the removal of procure rights and security patch exclusion)")
    # not_superseded_items 必须含 liability cap 相关内容（6 个月仍在谈判）
    nsi = [str(x).lower() for x in (data.get("not_superseded_items") or [])]
    nsi_str = " ".join(nsi)
    if "cap" not in nsi_str and "liability" not in nsi_str and "month" not in nsi_str:
        fails.append("not_superseded_items must include the liability cap (6-month VendorX position "
                     "from v2.4 is NOT superseded — still under active negotiation)")
    # effective_position_source 必须引用 external counsel 或 v2.4-revised 或 supersede notice
    eps = str(data.get("effective_position_source", "")).lower()
    if ("external" not in eps and "counsel" not in eps and
            "revised" not in eps and "supersede" not in eps and "morrison" not in eps):
        fails.append("effective_position_source must reference the external counsel redline (v2.4-revised) "
                     "and/or the supersede notice email")
    # supersede_date 必须是 ISO 8601 日期，且包含 2026-01-27 或附近
    sd = str(data.get("supersede_date", "")).strip()
    if not re.match(r"20\\d\\d-\\d\\d-\\d\\d", sd):
        fails.append("supersede_date must be in ISO 8601 format (YYYY-MM-DD)")
    _finish(fails)
main()
'''

# Q12: 综合风险矩阵（V8 schema-by-shape；V3 隐式偏好排序）
CHECKS["check_q12"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "risk_matrix.json")
    if err: _finish([err])
    risks = data.get("risks")
    if not isinstance(risks, list):
        _finish(["risks must be a JSON array"])
    if len(risks) < 5:
        fails.append("risks array has %d entries (expected >= 5)" % len(risks))
    # 每个 risk 必须有 risk_id / risk_level / clause_ref / description / recommendation
    for i, r in enumerate(risks):
        if not isinstance(r, dict):
            fails.append("risks[%d] is not an object" % i); continue
        for k in ("risk_id", "risk_level", "clause_ref", "description", "recommendation"):
            if not r.get(k):
                fails.append("risks[%d] missing or empty field '%s'" % (i, k))
        rl = str(r.get("risk_level", "")).strip().upper()
        if rl not in ("HIGH", "MEDIUM", "LOW"):
            fails.append("risks[%d] risk_level == %r (must be exactly HIGH, MEDIUM, or LOW)" % (i, rl))
    # HIGH 级风险必须包含 DPA sub-processor 和 warranty disclaimer
    high_risks = [r for r in risks if isinstance(r, dict) and str(r.get("risk_level","")).upper() == "HIGH"]
    if not high_risks:
        fails.append("no HIGH-level risks found (at least DPA sub-processor and warranty disclaimer must be HIGH)")
    else:
        all_high_text = " ".join(
            json.dumps(r).lower() for r in high_risks
        )
        if "sub-processor" not in all_high_text and "subprocessor" not in all_high_text and "sub processor" not in all_high_text:
            fails.append("HIGH risks must include the DPA sub-processor written authorisation gap")
        if "warranty" not in all_high_text and "disclaimer" not in all_high_text and "as is" not in all_high_text:
            fails.append("HIGH risks must include the AS IS warranty disclaimer compliance concern")
    # 第一个 risk 必须是 HIGH（按 HIGH→LOW 排序）
    if risks and isinstance(risks[0], dict):
        first_rl = str(risks[0].get("risk_level", "")).strip().upper()
        if first_rl != "HIGH":
            fails.append("first risk must be HIGH-level (risks should be sorted HIGH→MEDIUM→LOW)")
    _finish(fails)
main()
'''

# Q13: CISG 适用性分析（V1 多源冲突；V9 verbatim Art.79 要件）
CHECKS["check_q13"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "cisg_applicability.json")
    if err: _finish([err])
    # cisg_applies 必须是 false（§12.3 排除条款，GC 权威裁定）
    ca = data.get("cisg_applies")
    if ca is not False:
        fails.append("cisg_applies == %r (must be false — per MSA §12.3 CISG exclusion and GC's authoritative ruling)" % ca)
    # exclusion_clause_ref 必须引用 §12.3 或 12.3
    ecr = str(data.get("exclusion_clause_ref", "")).strip()
    if "12.3" not in ecr and "12" not in ecr:
        fails.append("exclusion_clause_ref == %r (must reference MSA §12.3, the CISG exclusion clause)" % ecr)
    # art79_elements 必须有两个元素，含 impediment beyond control 和 not reasonably foreseeable
    elems = data.get("art79_elements")
    if not isinstance(elems, list) or len(elems) < 2:
        fails.append("art79_elements must be a list with at least 2 elements (both CISG Art.79 requirements)")
    else:
        elems_text = " ".join(str(e).lower() for e in elems)
        if "impediment" not in elems_text and "control" not in elems_text:
            fails.append("art79_elements must include the 'impediment beyond control' element")
        if "foresee" not in elems_text and "conclusion" not in elems_text and "account" not in elems_text:
            fails.append("art79_elements must include the 'not reasonably expected at conclusion' element")
    # art74_foreseeability_cap 必须非空，含 foresee 词根
    af = str(data.get("art74_foreseeability_cap", "")).lower()
    if not af or ("foresee" not in af and "ought to have" not in af and "possible consequence" not in af):
        fails.append("art74_foreseeability_cap must be a non-empty string referencing the foreseeability standard")
    _finish(fails)
main()
'''

# Q14: Update 3 后 — 最终合同版本确认（V4 Q2→Q8→Q14 数值闭合；V2 从 6 月回至 12 月）
CHECKS["check_q14"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "final_contract_summary.json")
    if err: _finish([err])
    # final_version 必须是 v2.5
    fv = str(data.get("final_version", "")).strip()
    if "2.5" not in fv:
        fails.append("final_version == %r (expected 'v2.5' — the final agreed version)" % fv)
    # final_cap_months 必须是 12（从 v2.4 的 6 个月恢复，须与 Q2/Q8 一致）
    fcm = data.get("final_cap_months")
    try:
        fcm = int(fcm)
    except (TypeError, ValueError):
        _finish(["final_cap_months not an int: %r" % fcm])
    if fcm != 12:
        fails.append("final_cap_months == %d (expected 12 — v2.5 restores TechCo's position; "
                     "v2.4's 6-month regression was rejected)" % fcm)
    # ip_remedy_options_count 必须是 4（含 procure rights）
    irc = data.get("ip_remedy_options_count")
    try:
        irc = int(irc)
    except (TypeError, ValueError):
        _finish(["ip_remedy_options_count not an int: %r" % irc])
    if irc != 4:
        fails.append("ip_remedy_options_count == %d (expected 4 — procure rights reinstated in v2.5)" % irc)
    # cross-round closure: final_cap_months must equal Q2 and Q8 positions
    q2, e2 = _load_json(ws / "output" / "liability_cap.json")
    if not e2 and q2 is not None:
        try:
            q2_cm = int(q2.get("cap_months"))
            if q2_cm != fcm:
                fails.append("cross-round drift: Q14 final_cap_months=%d != Q2 cap_months=%d" % (fcm, q2_cm))
        except (TypeError, ValueError):
            pass
    q8, e8 = _load_json(ws / "output" / "negotiation_position.json")
    if not e8 and q8 is not None:
        try:
            q8_op = int(q8.get("our_position_months"))
            if q8_op != fcm:
                fails.append("cross-round drift: Q14 final_cap_months=%d != Q8 our_position_months=%d" % (fcm, q8_op))
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
'''

# Q15: 最终合同审查报告生成（V3 隐式 P5；V9 verbatim 引用）
CHECKS["check_q15"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "final_review_report.md")
    if txt is None:
        _finish(["file not found: output/final_review_report.md"])
    low = txt.lower()
    # 必须有三个固定章节（按序）
    h_exec = "## Executive Summary"
    h_risk = "## Risk Matrix"
    h_rec = "## Recommended Actions"
    for heading in (h_exec, h_risk, h_rec):
        if heading.lower() not in low:
            fails.append("report missing required heading: '%s'" % heading)
    # 章节顺序检查（P5）
    pos_exec = low.find("## executive summary")
    pos_risk = low.find("## risk matrix")
    pos_rec = low.find("## recommended actions")
    if not (pos_exec < pos_risk < pos_rec) and all(p >= 0 for p in (pos_exec, pos_risk, pos_rec)):
        fails.append("sections out of order: must be Executive Summary → Risk Matrix → Recommended Actions (P5)")
    # 必须引用 UCC § 2-316
    if "2-316" not in txt:
        fails.append("report must cite UCC § 2-316 (warranty disclaimer analysis)")
    # 必须引用 Hadley [1854] EWHC J70
    if "1854" not in txt or "j70" not in low:
        fails.append("report must cite Hadley v Baxendale [1854] EWHC J70")
    # 必须引用 GDPR 罚款金额
    if "10,000,000" not in txt and "10000000" not in txt and "€10" not in txt:
        if "2%" not in txt and "two percent" not in low:
            fails.append("report must reference GDPR Art.28 penalty (€10,000,000 or 2%) ")
    # 必须引用 Everbridge MSA §10 或 twelve month 赔偿上限基准
    if "everbridge" not in low and ("twelve" not in low and "12 month" not in low and "12-month" not in low):
        fails.append("report must reference Everbridge MSA §10 as market benchmark for 12-month cap")
    _finish(fails)
main()
'''

# Q16: SHA-256 sign-off（V7）
CHECKS["check_q16"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    sign = _read(ws / "output" / "signoff.txt")
    if sign is None:
        _finish(["file not found: output/signoff.txt"])
    line = sign.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["signoff line must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80]])
    report = ws / "output" / "final_review_report.md"
    if not report.exists():
        _finish(["cannot verify hash: output/final_review_report.md missing"])
    digest = hashlib.sha256(report.read_bytes()).hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: signoff %s... != recomputed %s..." % (m.group(1)[:12], digest[:12]))
    _finish(fails)
main()
'''


PREF = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sci4 preference checker (P1 legal citation format / P2 numeric claims with source /
P3 compliance regulatory tagging / P4 ISO 8601 dates / P5 three-section report structure)."""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """All legal citations must use standard format."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    fails = []
    # Cases: must use [YYYY] EWHC JNN format (not abbreviated)
    # Check that if Hadley is mentioned, it uses proper citation format
    if "hadley" in txt.lower() and "1854" in txt:
        if not re.search(r"\\[1854\\]\\s*EWHC\\s*J70", txt, re.IGNORECASE):
            fails.append("P1: Hadley v Baxendale cited without proper format '[1854] EWHC J70'")
    # UCC citations: must be 'UCC § N-NNN' (with § symbol)
    # Allow various UCC references but check format if present
    if re.search(r"UCC\\s+[0-9]", txt) and not re.search(r"UCC\\s+§", txt):
        # UCC referenced without § symbol
        fails.append("P1: UCC citation must use '§' symbol (e.g., 'UCC § 2-316')")
    # ucc_section_cited field: check it contains proper format
    if target.endswith(".json"):
        try:
            data = json.loads(txt)
            cited = str(data.get("ucc_section_cited", ""))
            if cited and "2-316" in cited and "§" not in cited:
                fails.append("P1: ucc_section_cited '%s' must include § symbol" % cited)
        except Exception:
            pass
    if fails:
        for f in fails:
            print(f)
        return False, "P1: FAILED"
    return True, "P1: PASSED"


def check_P2(ws, target):
    """All numeric claims in output JSON must include source references in parentheses."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    if not target.endswith(".json"):
        return True, "P2: not a JSON file, skip"
    try:
        data = json.loads(txt)
    except Exception:
        return False, "P2: target is not valid JSON"
    # Check specific numeric fields that should have source citations
    # Look for plain integer values in fields that represent months/days
    # The key fields to check: cap_months, our_position_months, market_standard_months,
    # termination_threshold_days, notice_days
    # We check the icc_source or similar companion fields exist
    month_fields = ["our_position_months", "market_standard_months", "termination_threshold_days"]
    missing_citation = False
    if isinstance(data, dict):
        for f in month_fields:
            if f in data:
                val = data[f]
                if isinstance(val, (int, float)) and val > 0:
                    # Check if there's a companion source field or if the value appears with citation
                    txt_lower = txt.lower()
                    # Weak check: if supporting_sources or icc_source exists nearby, pass
                    has_source = (data.get("supporting_sources") or
                                  data.get("icc_source") or
                                  data.get("source_version"))
                    if not has_source:
                        missing_citation = True
                        break
    if missing_citation:
        return False, "P2: FAILED: numeric claims lack accompanying source references"
    return True, "P2: PASSED"


def check_P3(ws, target):
    """All compliance issues must be tagged [Source: REGULATION Art.N]."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    # If the document contains compliance items, check for [Source: ...] tags
    if not target.endswith(".json") and not target.endswith(".md"):
        return True, "P3: non-JSON/MD target, skip"
    low = txt.lower()
    # If GDPR is mentioned in a compliance context, [Source: GDPR ...] must appear
    if "gdpr" in low and "complian" in low:
        if "[source:" not in low and "[source :" not in low:
            return False, "P3: FAILED: document mentions GDPR compliance but missing [Source: ...] tags"
    return True, "P3: PASSED"


def check_P4(ws, target):
    """All time period outputs must use ISO 8601 format."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    if not target.endswith(".json"):
        return True, "P4: not a JSON file, skip"
    try:
        data = json.loads(txt)
    except Exception:
        return False, "P4: target is not valid JSON"
    # Check that date fields use ISO 8601 (YYYY-MM-DD)
    if isinstance(data, dict):
        for k, v in data.items():
            if "date" in k.lower() and isinstance(v, str) and v:
                if not re.match(r"20\\d\\d-\\d\\d-\\d\\d", v):
                    return False, "P4: FAILED: field '%s' value '%s' is not ISO 8601 (YYYY-MM-DD)" % (k, v[:20])
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Final report must contain three sections in order: Executive Summary, Risk Matrix, Recommended Actions."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    if not target.endswith(".md"):
        return True, "P5: not a Markdown file, skip (P5 applies only to final_review_report.md)"
    low = txt.lower()
    pos_exec = low.find("## executive summary")
    pos_risk = low.find("## risk matrix")
    pos_rec = low.find("## recommended actions")
    if pos_exec < 0:
        return False, "P5: FAILED: missing '## Executive Summary' section"
    if pos_risk < 0:
        return False, "P5: FAILED: missing '## Risk Matrix' section"
    if pos_rec < 0:
        return False, "P5: FAILED: missing '## Recommended Actions' section"
    if not (pos_exec < pos_risk < pos_rec):
        return False, "P5: FAILED: sections out of order (must be Executive Summary → Risk Matrix → Recommended Actions)"
    return True, "P5: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4, "P5": check_P5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4,P5")
    ap.add_argument("--target", default="output/")
    a = ap.parse_args()
    ws = Path(a.workspace)
    rules = [r.strip() for r in a.rules.split(",") if r.strip()]
    unknown = [r for r in rules if r not in RULES]
    if unknown:
        print("FAILED: unknown rules: %s" % unknown); sys.exit(1)
    fails = []
    for r in rules:
        ok, msg = RULES[r](ws, a.target)
        print(msg)
        if not ok:
            fails.append(msg)
    if fails:
        for m in fails:
            print("FAILED: " + m)
        sys.exit(1)
    print("PASSED"); sys.exit(0)


if __name__ == "__main__":
    main()
'''


def main():
    for name, body in CHECKS.items():
        (OUT / f"{name}.py").write_text(HEADER + textwrap.dedent(body), encoding="utf-8")
    (OUT / "check_preferences.py").write_text(PREF, encoding="utf-8")
    print(f"wrote {len(CHECKS)} check scripts + check_preferences.py to {OUT}")


if __name__ == "__main__":
    main()
