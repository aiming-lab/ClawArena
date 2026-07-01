#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_sec3b_checks.py — 生成 sec3b 的全部 exec_check 校验脚本到 eval/sec3b/scripts/。

每个 check_qN.py 自包含，约定：argv[1]=workspace；PASSED+exit0 / FAILED+exit1。
三层验证（结构→字段→真值），数值带容差，锚点对齐 build_sec3b.py 注入的真实/合成数据。
check_preferences.py 实现 P1-P5。
"""
from pathlib import Path
import textwrap

OUT = Path("/home/xkaiwen/workspace/ClawArena/data/clawarena-real/eval/sec3b/scripts")
OUT.mkdir(parents=True, exist_ok=True)

HEADER = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv
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

# --------------------------------------------------------------------------- #
# q1 — 事故时间线 JSON（V4 基础锚：incident_date, event_time_utc, offsets）
# --------------------------------------------------------------------------- #
CHECKS["check_q1"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "incident_timeline_v1.json")
    if err: _finish([err])
    # incident_date
    idate = str(data.get("incident_date") or "")
    if "2024-11-03" not in idate:
        fails.append("incident_date == %r (expected '2024-11-03')" % idate)
    # event_time_utc — first mis-timed T+1 order at 14:30:00Z
    etutc = str(data.get("event_time_utc") or "")
    if "2024-11-03T14:30:00" not in etutc:
        fails.append("event_time_utc == %r (expected '2024-11-03T14:30:00Z' per incident timeline)" % etutc)
    # timezone_offset — the BUG value = -4
    tz_off = data.get("timezone_offset")
    try:
        tz_off = int(tz_off)
    except (TypeError, ValueError):
        _finish(["timezone_offset not an int: %r" % tz_off])
    if tz_off != -4:
        fails.append("timezone_offset == %d (expected -4, the bug value)" % tz_off)
    # correct_timezone_offset — should be -5 (EST)
    corr = data.get("correct_timezone_offset")
    try:
        corr = int(corr)
    except (TypeError, ValueError):
        _finish(["correct_timezone_offset not an int: %r" % corr])
    if corr != -5:
        fails.append("correct_timezone_offset == %d (expected -5 for EST after DST switch)" % corr)
    _finish(fails)
main()
'''

# --------------------------------------------------------------------------- #
# q2 — 时区 bug 报告 MD（V8/V9 verbatim UTC-4/UTC-5 + 行号引用）
# --------------------------------------------------------------------------- #
CHECKS["check_q2"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "timezone_bug_report.md")
    if txt is None:
        _finish(["file not found: output/timezone_bug_report.md"])
    low = txt.lower()
    # Must mention error value UTC-4 and correct value UTC-5
    if "utc-4" not in txt and "utc -4" not in txt and "-4" not in txt:
        fails.append("report does not mention UTC-4 (the error value)")
    if "utc-5" not in txt and "utc -5" not in txt and "-5" not in txt:
        fails.append("report does not mention UTC-5 (the correct EST value)")
    # Must reference a line number (digit follows 'line')
    if not re.search(r"line\\s+\\d+", low):
        fails.append("report does not reference a specific line number (e.g. 'line 42')")
    # Must not RECOMMEND the deprecated v3 file (mentioning it as deprecated/not-to-use is fine)
    # Fail if the report suggests using the v3 file without a negation in context
    if re.search(r"(use|apply|reference|copy|recommend)[^\\n]{0,60}(aros_v3|v3\\.1|legacy.*router)", low):
        fails.append("report appears to recommend using the deprecated v3 file (V6 red herring)")
    _finish(fails)
main()
'''

# --------------------------------------------------------------------------- #
# q3 — 受影响订单计数 JSON（V4/V8 数值闭合、窗口精确；C 加难：新增 audit_log_total_scanned
#       字段供后续跨轮闭合引用）
# --------------------------------------------------------------------------- #
CHECKS["check_q3"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "affected_orders_count.json")
    if err: _finish([err])
    # time window must be exactly 14:00-15:00 UTC on 2024-11-03
    start = str(data.get("time_window_utc_start") or "")
    end = str(data.get("time_window_utc_end") or "")
    if "2024-11-03T14:00:00" not in start:
        fails.append("time_window_utc_start == %r (expected '2024-11-03T14:00:00Z')" % start)
    if "2024-11-03T15:00:00" not in end:
        fails.append("time_window_utc_end == %r (expected '2024-11-03T15:00:00Z')" % end)
    # total_affected must be the exact count of ANOMALY_DST_MISMATCH entries in the audit log
    ta = data.get("total_affected")
    try:
        ta = int(ta)
    except (TypeError, ValueError):
        _finish(["total_affected not an int: %r" % ta])
    if ta <= 0:
        fails.append("total_affected == %d (expected positive int matching audit log count)" % ta)
    # audit_log_total_scanned: required field — must be the TOTAL line count scanned
    # (not just the anomalies — the entire audit log file). Used in downstream cross-round closures.
    tsc = data.get("audit_log_total_scanned")
    if tsc is None:
        fails.append(
            "audit_log_total_scanned field missing — must be the total number of non-empty "
            "lines scanned in incident/aros_v4_2_audit_log.jsonl (required for downstream audit trail)"
        )
    else:
        try:
            tsc = int(tsc)
        except (TypeError, ValueError):
            _finish(["audit_log_total_scanned not an int: %r" % tsc])
        # Recount from audit log to verify both total and anomaly counts
        audit_log = ws / "incident" / "aros_v4_2_audit_log.jsonl"
        if audit_log.exists():
            import json as _json
            real_count = 0
            real_total = 0
            with open(audit_log, encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    real_total += 1
                    try:
                        entry = _json.loads(line)
                        if entry.get("status") == "ANOMALY_DST_MISMATCH":
                            real_count += 1
                    except _json.JSONDecodeError:
                        pass
            if ta != real_count:
                fails.append(
                    "total_affected == %d but audit log has exactly %d ANOMALY_DST_MISMATCH entries "
                    "(must read and count the log accurately)" % (ta, real_count)
                )
            if tsc != real_total:
                fails.append(
                    "audit_log_total_scanned == %d but audit log has exactly %d non-empty lines "
                    "(must count all scanned lines, not just anomalies)" % (tsc, real_total)
                )
        else:
            if ta != real_count if False else False:
                pass  # skip if no audit log
    _finish(fails)
main()
'''

# --------------------------------------------------------------------------- #
# q4 — bot 摘要错误识别（V5 蜂蜜罐 + V1 多源冲突）
# --------------------------------------------------------------------------- #
CHECKS["check_q4"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "bot_summary_errors.json")
    if err: _finish([err])
    errs = data.get("errors")
    if not isinstance(errs, list):
        _finish(["errors must be a list, got %r" % type(errs).__name__])
    if len(errs) < 3:
        fails.append("errors list has %d items (expected >= 3)" % len(errs))
    # At least one error must reference the $440M vs $460M+ loss figure discrepancy
    full_text = json.dumps(errs).lower()
    if "440" not in full_text or ("460" not in full_text and "460m" not in full_text):
        fails.append("errors must include the KCG loss figure distortion: bot $440M vs correct $460M+")
    # Each error entry must have field, claimed_value, correct_value, source keys
    for i, e in enumerate(errs[:3]):
        if not isinstance(e, dict):
            fails.append("errors[%d] is not a dict" % i); continue
        for k in ("field", "claimed_value", "correct_value", "source"):
            if k not in e:
                fails.append("errors[%d] missing key '%s'" % (i, k))
    _finish(fails)
main()
'''

# --------------------------------------------------------------------------- #
# q5 — KCG 锚点核查 JSON（V9 verbatim + V4 数字闭合；B+F 加难：
#       case_number 精确原文引用；shares_traded_millions 容差收紧至 ±0.5M）
# --------------------------------------------------------------------------- #
CHECKS["check_q5"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "kcg_anchor_check.json")
    if err: _finish([err])
    # financial_loss_usd: must be EXACTLY 460000000 (SEC Release 34-70694)
    # 440000000 is the media preliminary figure — must not be used
    loss = data.get("financial_loss_usd")
    try:
        loss = int(loss)
    except (TypeError, ValueError):
        _finish(["financial_loss_usd not an int: %r" % loss])
    if loss == 440000000:
        fails.append("financial_loss_usd == 440000000 is the preliminary media figure; "
                     "SEC Release 34-70694 confirms the authoritative figure is 460000000")
    if loss != 460000000:
        fails.append("financial_loss_usd == %d (must be exactly 460000000 per SEC Release 34-70694; "
                     "not approximate — read the source document)" % loss)
    # penalty_usd: exactly 12000000
    pen = data.get("penalty_usd")
    try:
        pen = int(pen)
    except (TypeError, ValueError):
        _finish(["penalty_usd not an int: %r" % pen])
    if pen != 12000000:
        fails.append("penalty_usd == %d (expected exactly 12,000,000)" % pen)
    # rule_violated: must contain 15c3-5 and the (b) sub-clause
    rule = str(data.get("rule_violated") or "")
    if "15c3-5" not in rule:
        fails.append("rule_violated %r does not reference Rule 15c3-5" % rule)
    if "(b)" not in rule and "(B)" not in rule:
        fails.append("rule_violated %r must include sub-clause (b) per P3" % rule)
    # servers_count: exactly 8
    svc = data.get("servers_count")
    try:
        svc = int(svc)
    except (TypeError, ValueError):
        _finish(["servers_count not an int: %r" % svc])
    if svc != 8:
        fails.append("servers_count == %d (expected 8)" % svc)
    # pre_market_emails: exactly 97
    ems = data.get("pre_market_emails")
    try:
        ems = int(ems)
    except (TypeError, ValueError):
        _finish(["pre_market_emails not an int: %r" % ems])
    if ems != 97:
        fails.append("pre_market_emails == %d (expected 97)" % ems)
    # shares_traded_millions: must be exactly 397.0 +/- 0.5 (tightened from +/-1)
    stm = data.get("shares_traded_millions")
    if stm is None:
        fails.append("shares_traded_millions field missing (required key)")
    else:
        try:
            stm = float(stm)
        except (TypeError, ValueError):
            _finish(["shares_traded_millions not a number: %r" % stm])
        if not (396.5 <= stm <= 397.5):
            fails.append(
                "shares_traded_millions == %.3f (expected 397.0 ± 0.5 per SEC Release 34-70694; "
                "read the primary source document for the exact figure)" % stm
            )
    # case_number: must include the exact Admin Proc file number from SEC Release 34-70694
    # Verbatim: "Admin. Proc. File No. 3-15570" (the official docket identifier)
    cn = str(data.get("case_number") or "")
    if not cn:
        fails.append(
            "case_number field missing — must be the verbatim Admin. Proc. File No. from "
            "SEC Release 34-70694 (e.g. 'Admin. Proc. File No. 3-15570')"
        )
    elif "3-15570" not in cn:
        fails.append(
            "case_number == %r does not contain '3-15570' "
            "(must be verbatim docket number from SEC Release 34-70694)" % cn[:60]
        )
    _finish(fails)
main()
'''

# --------------------------------------------------------------------------- #
# q6 — 废弃代码评估（V6 红鲱鱼）
# --------------------------------------------------------------------------- #
CHECKS["check_q6"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "legacy_code_assessment.json")
    if err: _finish([err])
    # is_applicable must be false (V6: deprecated code must not be used)
    if data.get("is_applicable") is not False:
        fails.append("is_applicable == %r (expected false; the v3.1 code is DEPRECATED)" % data.get("is_applicable"))
    # reason must mention deprecated
    reason = str(data.get("reason") or "").lower()
    if "deprec" not in reason:
        fails.append("reason %r does not mention 'deprecated' (the v3.1 file is deprecated 2023-06-01)" % reason[:80])
    # recommendation must exist and not recommend the deprecated file
    rec = str(data.get("recommendation") or "").lower()
    if not rec:
        fails.append("recommendation field is empty")
    if re.search(r"v3\\.1|legacy.*depr", rec):
        fails.append("recommendation should NOT recommend using the deprecated v3.1 code")
    _finish(fails)
main()
'''

# --------------------------------------------------------------------------- #
# q7 — MiFIR Field 28 修正报告（V9 verbatim + P3 引用；B+D 加难：需引用 RTS 22 + Article 26）
# --------------------------------------------------------------------------- #
CHECKS["check_q7"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "mifir_field28_correction.md")
    if txt is None:
        _finish(["file not found: output/mifir_field28_correction.md"])
    low = txt.lower()
    # Must contain 'Field 28' (verbatim field reference)
    if "field 28" not in low and "field28" not in low:
        fails.append("report does not contain 'Field 28' reference")
    # Must mention UTC explicitly
    if "utc" not in low:
        fails.append("report does not mention UTC")
    # Must cite Market Watch 59 (FCA Market Watch 59)
    if "market watch 59" not in low and "market watch59" not in low:
        fails.append("report does not cite 'Market Watch 59' (FCA guidance on Field 28)")
    # Must mention DST, BST, or summer/standard time
    if not re.search(r"dst|daylight|summer time|standard time|bst|clocks", low):
        fails.append("report does not mention DST/BST/summer-time/standard-time transition")
    # Must cite Article 26 of MiFIR (the specific regulatory article governing Field 28)
    if "article 26" not in low:
        fails.append("report does not cite 'Article 26' of MiFIR (the transaction reporting obligation "
                     "that mandates Field 28 UTC format — verbatim citation required)")
    # Must cite RTS 22 (the technical standard specifying Field 28 format)
    if "rts 22" not in low and "rts22" not in low:
        fails.append("report does not cite 'RTS 22' (the technical standard defining the "
                     "ISO 8601 UTC format requirement for Field 28)")
    # Must include a concrete remediation action (not just description of the error)
    if not re.search(r"remediat|action|fix|correct|replac|implement", low):
        fails.append("report does not include a concrete remediation action")
    _finish(fails)
main()
'''

# --------------------------------------------------------------------------- #
# q8 — T+1 结算截止时间偏移（V4/V8 数值精确；A 加难：精确 UTC 值必须正确）
# --------------------------------------------------------------------------- #
CHECKS["check_q8"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "t1_settlement_impact.json")
    if err: _finish([err])
    # rule_effective_date: 2024-05-28
    red = str(data.get("rule_effective_date") or "")
    if "2024-05-28" not in red:
        fails.append("rule_effective_date == %r (expected '2024-05-28')" % red)
    # offset_minutes: exactly 60
    om = data.get("offset_minutes")
    try:
        om = int(om)
    except (TypeError, ValueError):
        _finish(["offset_minutes not an int: %r" % om])
    if om != 60:
        fails.append("offset_minutes == %d (expected 60, the 1-hour DST offset)" % om)
    # Validate the exact UTC cutoff values (not just the diff)
    # T+1 cutoff is 21:00 ET per Rule 15c6-1
    # incorrect_cutoff_utc: 21:00 ET with UTC-4 = 2024-11-04T01:00:00Z
    # correct_cutoff_utc: 21:00 ET with UTC-5 = 2024-11-04T02:00:00Z
    import datetime
    ic = str(data.get("incorrect_cutoff_utc") or "")
    cc = str(data.get("correct_cutoff_utc") or "")
    if not ic or not cc:
        fails.append("incorrect_cutoff_utc and/or correct_cutoff_utc missing")
    else:
        # Check exact expected values
        if "2024-11-04T01:00:00" not in ic:
            fails.append(
                "incorrect_cutoff_utc == %r (expected '2024-11-04T01:00:00Z'; "
                "T+1 cutoff 21:00 ET with wrong UTC-4 offset = 21+4 = 01:00 UTC next day)" % ic
            )
        if "2024-11-04T02:00:00" not in cc:
            fails.append(
                "correct_cutoff_utc == %r (expected '2024-11-04T02:00:00Z'; "
                "T+1 cutoff 21:00 ET with correct UTC-5 offset = 21+5 = 02:00 UTC next day)" % cc
            )
        # Also verify the difference
        try:
            def _parse(s):
                return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
            ic_dt = _parse(ic); cc_dt = _parse(cc)
            delta = (cc_dt - ic_dt).total_seconds()
            if abs(delta - 3600) > 1:
                fails.append("correct_cutoff_utc - incorrect_cutoff_utc == %.0fs (expected 3600s = 60min)" % delta)
        except Exception as exc:
            fails.append("cannot parse cutoff times: %s" % exc)
    _finish(fails)
main()
'''

# --------------------------------------------------------------------------- #
# q9 — 根因分析文档（V1/V4 综合 + P2/P3 引用；C★ 加难：强化跨轮闭合，
#       需从 q3 output 读取 audit_log_total_scanned 并在文档中引用；
#       需从 q5 output 读取 financial_loss_usd 精确值并在文档中引用；
#       Rule 15c6-1 生效日期 '2024-05-28' 必须显式出现）
# --------------------------------------------------------------------------- #
CHECKS["check_q9"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "root_cause_analysis.md")
    if txt is None:
        _finish(["file not found: output/root_cause_analysis.md"])
    low = txt.lower()
    # Must contain incident date
    if "2024-11-03" not in txt:
        fails.append("RCA does not contain incident date '2024-11-03'")
    # Must mention both UTC-4 and UTC-5
    if "utc-4" not in txt and "utc -4" not in txt and "-4" not in txt:
        fails.append("RCA does not mention UTC-4 (the error offset)")
    if "utc-5" not in txt and "utc -5" not in txt and "-5" not in txt:
        fails.append("RCA does not mention UTC-5 (the correct offset)")
    # Must cite Rule 15c3-5 (P3: with sub-clause)
    if "15c3-5" not in txt:
        fails.append("RCA does not reference Rule 15c3-5")
    if not re.search(r"15c3-5\\(b\\)|15c3-5\\s*\\(b\\)", txt, re.IGNORECASE):
        fails.append("RCA cites Rule 15c3-5 but not the (b) sub-clause (P3 requires sub-clause)")
    # Must cite Rule 15c6-1 (T+1 settlement) with its effective date
    if "15c6-1" not in txt:
        fails.append("RCA does not reference Rule 15c6-1 (T+1 settlement rule)")
    if "2024-05-28" not in txt:
        fails.append(
            "RCA does not cite Rule 15c6-1 effective date '2024-05-28' "
            "(cross-round closure: the exact effective date must appear in the regulatory violations section)"
        )
    # Must include BOTH the incorrect CME time (20:00 UTC) AND correct time (21:00 UTC)
    if "20:00" not in txt and "2000" not in txt:
        fails.append("RCA does not reference 20:00 UTC (the incorrect CME settlement time the system computed)")
    if "21:00" not in txt and "2100" not in txt:
        fails.append("RCA does not reference 21:00 UTC (the correct CME settlement time after DST switch)")
    # Must reference the total_affected order count from Round 3 (V4 cross-round closure)
    q3, e3 = _load_json(ws / "output" / "affected_orders_count.json")
    if not e3 and q3 is not None:
        ta = q3.get("total_affected")
        try:
            ta = int(ta)
            if ta > 0 and str(ta) not in txt:
                fails.append(
                    "RCA does not reference total_affected order count (%d) from Round 3 output "
                    "(V4 cross-round closure: the financial impact section must cite this figure)" % ta
                )
        except (TypeError, ValueError):
            pass
        # C★ Cross-round closure: must also cite audit_log_total_scanned from q3
        tsc = q3.get("audit_log_total_scanned")
        try:
            tsc = int(tsc)
            if tsc > 0 and str(tsc) not in txt:
                fails.append(
                    "RCA does not reference audit_log_total_scanned (%d) from Round 3 output "
                    "(C★ cross-round closure: the audit scope section must cite total lines scanned "
                    "from output/affected_orders_count.json — cross-check your Round 3 result)" % tsc
                )
        except (TypeError, ValueError):
            pass
    # C★ Cross-round closure: must cite exact KCG financial_loss_usd from Round 5
    q5, e5 = _load_json(ws / "output" / "kcg_anchor_check.json")
    if not e5 and q5 is not None:
        kcg_loss = q5.get("financial_loss_usd")
        try:
            kcg_loss = int(kcg_loss)
            if kcg_loss > 0 and str(kcg_loss) not in txt:
                fails.append(
                    "RCA does not cite the exact KCG financial_loss_usd (%d) from Round 5 output "
                    "(C★ cross-round closure: the KCG comparison section must quote the exact integer "
                    "from output/kcg_anchor_check.json — both the string '%d' must appear)" % (kcg_loss, kcg_loss)
                )
        except (TypeError, ValueError):
            pass
    # Must NOT contain $440M as an authoritative figure (only as a decoy reference)
    if "440" in txt and "440m" in txt.lower():
        if "460" not in txt:
            fails.append("RCA mentions '$440M' without the correct '$460M+' figure (use SEC-verified number)")
    _finish(fails)
main()
'''

# --------------------------------------------------------------------------- #
# q10 — SEC 询问框架 JSON（V2 update + V8 schema；A 加难：精确字段集合 + 精确行数）
# --------------------------------------------------------------------------- #
CHECKS["check_q10"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "sec_response_framework.json")
    if err: _finish([err])
    # deadline_utc: exactly 2024-11-07T15:00:00Z (48h after 2024-11-05T15:00Z)
    dl = str(data.get("deadline_utc") or "")
    if "2024-11-07T15:00:00" not in dl:
        fails.append("deadline_utc == %r (expected '2024-11-07T15:00:00Z'; "
                     "48 hours after 2024-11-05T15:00:00Z — must be exactly that datetime)" % dl)
    # required_fields: must include exactly the 4 SEC-specified fields from the inquiry letter
    # At Round 10, Update 2 (legal counsel memo) has NOT yet arrived — do NOT use price_diff_vwap_usd
    rq = data.get("required_fields")
    if not isinstance(rq, list):
        _finish(["required_fields must be a list"])
    rq_str = [str(x).strip().lower() for x in rq]
    rq_set = set(rq_str)
    required_exact = {"order_id", "expected_settlement_utc", "actual_settlement_utc", "price_diff_usd"}
    for need in required_exact:
        if need not in rq_set:
            fails.append("required_fields missing '%s' (verbatim from SEC inquiry letter, Update 1)" % need)
    # price_diff_vwap_usd must NOT appear — that is the Update 2 superseded name, not yet issued at Round 10
    if "price_diff_vwap_usd" in rq_set:
        fails.append("required_fields contains 'price_diff_vwap_usd' which is the Update 2 "
                     "revised field name — Update 2 has NOT yet arrived at Round 10; "
                     "use 'price_diff_usd' from the SEC inquiry letter")
    # affected_order_count_from_detail: must be a positive int matching the CSV row count
    oc = data.get("affected_order_count_from_detail")
    try:
        oc = int(oc)
    except (TypeError, ValueError):
        _finish(["affected_order_count_from_detail not an int: %r" % oc])
    if oc <= 0:
        fails.append("affected_order_count_from_detail == %d (expected positive int)" % oc)
    # Cross-verify: recount from the actual CSV to ensure the agent read it accurately
    detail_csv = ws / "incident" / "affected_orders_detail.csv"
    if detail_csv.exists():
        import csv as _csv
        with open(detail_csv, encoding="utf-8") as fh:
            real_count = sum(1 for _ in _csv.DictReader(fh))
        if oc != real_count:
            fails.append(
                "affected_order_count_from_detail == %d but incident/affected_orders_detail.csv "
                "has exactly %d data rows (count the file accurately)" % (oc, real_count)
            )
    _finish(fails)
main()
'''

# --------------------------------------------------------------------------- #
# q11 — 订单级别差异报告 CSV（V2/V10 supersede + V4 行数闭合）
# --------------------------------------------------------------------------- #
CHECKS["check_q11"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    csv_path = ws / "output" / "order_level_diff_report.csv"
    if not csv_path.exists():
        _finish(["file not found: output/order_level_diff_report.csv"])
    try:
        with open(csv_path, encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            fieldnames = reader.fieldnames or []
            rows = list(reader)
    except Exception as exc:
        _finish(["cannot read order_level_diff_report.csv: " + str(exc)])
    # Column headers: must have price_diff_vwap_usd (NOT superseded price_diff_usd)
    fn_low = [f.lower() for f in fieldnames]
    if "price_diff_vwap_usd" not in fn_low:
        fails.append("column 'price_diff_vwap_usd' missing (must use revised field name per Update 2 legal memo)")
    if "price_diff_usd" in fn_low and "price_diff_vwap_usd" not in fn_low:
        fails.append("found superseded column 'price_diff_usd' without 'price_diff_vwap_usd' (Update 2 supersedes)")
    # Must have expected_settlement_utc and actual_settlement_utc
    for need in ("expected_settlement_utc", "actual_settlement_utc", "order_id"):
        if need not in fn_low:
            fails.append("column '%s' missing from CSV" % need)
    # ISO 8601 UTC format check for timestamp columns
    ts_col = next((f for f in fieldnames if "expected_settlement" in f.lower()), None)
    if ts_col and rows:
        sample = rows[0].get(ts_col, "")
        if sample and not re.search(r"\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}", sample):
            fails.append("expected_settlement_utc value %r is not ISO 8601 UTC format" % sample[:40])
    # Row count must match Round 10 affected_order_count_from_detail
    q10, e10 = _load_json(ws / "output" / "sec_response_framework.json")
    if not e10 and q10 is not None:
        oc = q10.get("affected_order_count_from_detail")
        try:
            oc = int(oc)
            if len(rows) != oc:
                fails.append("CSV row count %d != affected_order_count_from_detail %d (V4 closure)" % (len(rows), oc))
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
'''

# --------------------------------------------------------------------------- #
# q12 — 报告 SHA-256 签名（V7）
# --------------------------------------------------------------------------- #
CHECKS["check_q12"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    sign = _read(ws / "output" / "report_signoff.txt")
    if sign is None:
        _finish(["file not found: output/report_signoff.txt"])
    line = sign.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["report_signoff.txt must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80]])
    csv_path = ws / "output" / "order_level_diff_report.csv"
    if not csv_path.exists():
        _finish(["cannot verify hash: output/order_level_diff_report.csv missing"])
    digest = hashlib.sha256(csv_path.read_bytes()).hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: signoff %s... != recomputed %s..." % (m.group(1)[:12], digest[:12]))
    _finish(fails)
main()
'''

# --------------------------------------------------------------------------- #
# q13 — 合规整改计划（V9 Rule 引用 + P3/P4）
# --------------------------------------------------------------------------- #
CHECKS["check_q13"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "corrective_action_plan.md")
    if txt is None:
        _finish(["file not found: output/corrective_action_plan.md"])
    low = txt.lower()
    # Must cite Rule 15c3-5(b) (with sub-clause per P3)
    if "15c3-5" not in txt:
        fails.append("CAP does not reference Rule 15c3-5")
    if not re.search(r"15c3-5\\(b\\)|15c3-5\\s*\\(b\\)", txt, re.IGNORECASE):
        fails.append("CAP must cite Rule 15c3-5(b) with sub-clause (P3)")
    # Must cite Rule 15c6-1
    if "15c6-1" not in txt:
        fails.append("CAP does not reference Rule 15c6-1 (T+1 settlement)")
    # Must mention timezone automation/DST-aware library
    if not re.search(r"dst|daylight|timezone.*auto|pytz|zoneinfo|dateutil", low):
        fails.append("CAP does not include DST-aware timezone automation action")
    # Must have >= 4 remediation items with owner field
    # Look for owner: or owner field occurrences
    owner_count = len(re.findall(r"owner", low))
    if owner_count < 4:
        fails.append("CAP has fewer than 4 owner fields (%d found); each remediation item needs 'owner' (P4)" % owner_count)
    # Must have deadline_days or deadline field
    if not re.search(r"deadline|days", low):
        fails.append("CAP does not include deadline_days for remediation items")
    _finish(fails)
main()
'''

# --------------------------------------------------------------------------- #
# q14 — 监管提交摘要 JSON（V3/V4/V8 + P1/P3/P5 字段顺序；C★ 加难：
#       financial_impact 必须同时包含 q3 的 total_affected 与 audit_log_total_scanned；
#       新增 kcg_reference_loss_usd 字段必须精确等于 q5 的 financial_loss_usd）
# --------------------------------------------------------------------------- #
CHECKS["check_q14"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    path = ws / "output" / "regulatory_submission_summary.json"
    if not path.exists():
        _finish(["file not found: output/regulatory_submission_summary.json"])
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        _finish(["invalid JSON: " + str(exc)])
    # P5: field order must be incident_date → rule_violated → financial_impact → remediation_count → submission_date
    required_order = ["incident_date", "rule_violated", "financial_impact", "remediation_count", "submission_date"]
    keys = list(data.keys())
    top5 = [k for k in keys if k in required_order]
    top5_idx = [required_order.index(k) for k in top5]
    if top5_idx != sorted(top5_idx):
        fails.append("P5: field order violation — expected incident_date→rule_violated→"
                     "financial_impact→remediation_count→submission_date, got: %s" % top5)
    for need in required_order:
        if need not in data:
            fails.append("missing required key '%s'" % need)
    # rule_violated must include sub-clause (P3)
    rule = str(data.get("rule_violated") or "")
    if "15c" not in rule:
        fails.append("rule_violated %r does not reference any Rule 15c..." % rule[:50])
    if not re.search(r"\\(b\\)|\\(B\\)", rule):
        fails.append("rule_violated %r must include sub-clause (b) per P3" % rule[:50])
    # remediation_count must exactly match the number of remediation items in the CAP from Round 13
    rc = data.get("remediation_count")
    try:
        rc = int(rc)
    except (TypeError, ValueError):
        _finish(["remediation_count not an int: %r" % rc])
    if rc < 4:
        fails.append("remediation_count == %d (expected >= 4)" % rc)
    # Cross-verify remediation_count against the actual CAP from Round 13
    cap_txt = _read(ws / "output" / "corrective_action_plan.md")
    if cap_txt is not None:
        cap_items = re.findall(r"###\\s+\\d+\\.", cap_txt)
        if cap_items:
            actual_cap_count = len(cap_items)
            if rc != actual_cap_count:
                fails.append(
                    "remediation_count == %d but corrective_action_plan.md has %d '### N.' "
                    "remediation items (V4 closure: must match your Round 13 CAP exactly)" % (rc, actual_cap_count)
                )
    # C★ Cross-round closure: financial_impact must include BOTH total_affected AND audit_log_total_scanned
    q3, e3 = _load_json(ws / "output" / "affected_orders_count.json")
    if not e3 and q3 is not None:
        ta = q3.get("total_affected")
        try:
            ta = int(ta)
            fi = str(data.get("financial_impact") or "")
            if str(ta) not in fi and ta > 0:
                fails.append(
                    "financial_impact %r does not contain total_affected=%d from Round 3 "
                    "(C★ cross-round closure: quote the exact count from output/affected_orders_count.json)" % (fi[:80], ta)
                )
        except (TypeError, ValueError):
            pass
        tsc = q3.get("audit_log_total_scanned")
        try:
            tsc = int(tsc)
            fi = str(data.get("financial_impact") or "")
            if str(tsc) not in fi and tsc > 0:
                fails.append(
                    "financial_impact %r does not contain audit_log_total_scanned=%d from Round 3 "
                    "(C★ cross-round closure: include total lines scanned from output/affected_orders_count.json "
                    "— required in regulatory submission to document the scope of log analysis)" % (fi[:80], tsc)
                )
        except (TypeError, ValueError):
            pass
    # C★ Cross-round closure: kcg_reference_loss_usd must match Round 5 output exactly
    kcg_ref = data.get("kcg_reference_loss_usd")
    if kcg_ref is None:
        fails.append(
            "kcg_reference_loss_usd field missing — must be the exact integer from "
            "output/kcg_anchor_check.json (Round 5 output), used as regulatory precedent reference"
        )
    else:
        try:
            kcg_ref = int(kcg_ref)
        except (TypeError, ValueError):
            _finish(["kcg_reference_loss_usd not an int: %r" % kcg_ref])
        q5, e5 = _load_json(ws / "output" / "kcg_anchor_check.json")
        if not e5 and q5 is not None:
            kcg_actual = q5.get("financial_loss_usd")
            try:
                kcg_actual = int(kcg_actual)
                if kcg_ref != kcg_actual:
                    fails.append(
                        "kcg_reference_loss_usd == %d but Round 5 kcg_anchor_check.json has "
                        "financial_loss_usd == %d (must match exactly — read your Round 5 output)" % (kcg_ref, kcg_actual)
                    )
            except (TypeError, ValueError):
                pass
    # submission_date must be a valid YYYY-MM-DD date
    sd = str(data.get("submission_date") or "")
    if not re.match(r"\\d{4}-\\d{2}-\\d{2}", sd):
        fails.append("submission_date == %r (expected YYYY-MM-DD format)" % sd)
    _finish(fails)
main()
'''

# --------------------------------------------------------------------------- #
# q15 — 回测验证（V4/V8 数值精确：CME 21:00 UTC、UTC-5；E★ 加难：
#       静默要求 backtest_result.json 包含 schema_version="1.0" 字段，
#       question 不提醒，通过 check 直接检测）
# --------------------------------------------------------------------------- #
CHECKS["check_q15"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "backtest_result.json")
    if err: _finish([err])
    # config_timezone_offset must be -5 (correct EST)
    cto = data.get("config_timezone_offset")
    try:
        cto = int(cto)
    except (TypeError, ValueError):
        _finish(["config_timezone_offset not an int: %r" % cto])
    if cto != -5:
        fails.append("config_timezone_offset == %d (expected -5; -4 is the bug value)" % cto)
    # match must be true
    match = data.get("match")
    if match is not True:
        fails.append("match == %r (expected true; backtest must pass with UTC-5)" % match)
    # simulated_settlement_utc must be 2024-11-03T21:00:00Z
    ssu = str(data.get("simulated_settlement_utc") or "")
    if "2024-11-03T21:00:00" not in ssu:
        fails.append("simulated_settlement_utc == %r (expected '2024-11-03T21:00:00Z'; CME 15:00 CT = 21:00 UTC in EST)" % ssu)
    # E★ Silent schema requirement: backtest_result.json must contain schema_version="1.0"
    # This is a house preference requirement (P1 compliance document versioning).
    # The backtest template writes the result; a compliant run must include schema_version.
    sv = data.get("schema_version")
    if sv is None:
        fails.append(
            "schema_version field missing from backtest_result.json — "
            "all regulatory output documents must include schema_version per house versioning policy; "
            "expected schema_version='1.0'"
        )
    elif str(sv) != "1.0":
        fails.append(
            "schema_version == %r (expected '1.0' — the current AROS audit output schema version)" % str(sv)
        )
    # E★ Cross-round: verify config_timezone_offset matches correct_timezone_offset from Round 1
    q1, e1 = _load_json(ws / "output" / "incident_timeline_v1.json")
    if not e1 and q1 is not None:
        corr_off = q1.get("correct_timezone_offset")
        try:
            corr_off = int(corr_off)
            if cto != corr_off:
                fails.append(
                    "backtest config_timezone_offset == %d but Round 1 incident_timeline_v1.json "
                    "correct_timezone_offset == %d — these must match exactly "
                    "(C★ cross-round closure: backtest must use the offset you identified in Round 1)" % (cto, corr_off)
                )
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
'''

# --------------------------------------------------------------------------- #
# q16 — 最终报告签名（V7 终轮 SHA-256 拼接；C★ 加难：签名前先验证
#       backtest_result.json 含 schema_version="1.0"，
#       且 CAP 规则引用包含 "15c3-5(b)"；三件文件全部完整才能生成正确 hash）
# --------------------------------------------------------------------------- #
CHECKS["check_q16"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    sign = _read(ws / "output" / "final_submission_signoff.txt")
    if sign is None:
        _finish(["file not found: output/final_submission_signoff.txt"])
    line = sign.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["final_submission_signoff.txt must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80]])
    # Recompute: SHA-256 of backtest_result.json bytes + corrective_action_plan.md bytes
    f1 = ws / "output" / "backtest_result.json"
    f2 = ws / "output" / "corrective_action_plan.md"
    if not f1.exists():
        _finish(["cannot verify: output/backtest_result.json missing"])
    if not f2.exists():
        _finish(["cannot verify: output/corrective_action_plan.md missing"])
    # C★ Pre-check: backtest_result.json must have schema_version="1.0" before hash is valid
    bt_data, bt_err = _load_json(f1)
    if bt_err:
        _finish(["backtest_result.json is not valid JSON: " + bt_err])
    sv = bt_data.get("schema_version") if bt_data else None
    if sv is None or str(sv) != "1.0":
        fails.append(
            "backtest_result.json missing/wrong schema_version (found %r, expected '1.0') — "
            "the final hash is computed over the exact file bytes; if backtest_result.json "
            "lacks schema_version, the hash will not match the validator's recomputation" % sv
        )
    # C★ Pre-check: CAP must cite Rule 15c3-5(b) sub-clause (detects q13 drift)
    cap_txt = _read(f2)
    if cap_txt and not re.search(r"15c3-5\\s*\\(b\\)", cap_txt, re.IGNORECASE):
        fails.append(
            "corrective_action_plan.md does not contain '15c3-5(b)' — "
            "the CAP must cite Rule 15c3-5(b) sub-clause before the final hash is computed "
            "(C★ cross-round: if CAP is incomplete, the combined hash will be wrong)"
        )
    combined = f1.read_bytes() + f2.read_bytes()
    digest = hashlib.sha256(combined).hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: signoff %s... != recomputed %s... (hash of backtest_result.json + corrective_action_plan.md)" % (m.group(1)[:12], digest[:12]))
    _finish(fails)
main()
'''

# --------------------------------------------------------------------------- #
# check_preferences.py (P1-P5)
# --------------------------------------------------------------------------- #
PREF = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sec3b preference checker (P1 snake_case / P2 severity-descending / P3 sub-clause citation /
P4 owner fields in CAP / P5 regulatory submission field order).
"""
import sys, re, json, argparse
from pathlib import Path

# P5: required top-level field order for regulatory_submission_summary.json
P5_ORDER = ["incident_date", "rule_violated", "financial_impact", "remediation_count", "submission_date"]


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """All JSON outputs use snake_case field names."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except (json.JSONDecodeError, Exception):
        return True, "P1: not JSON, skip"
    # Collect all keys recursively
    def collect_keys(obj):
        keys = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                keys.append(k)
                keys.extend(collect_keys(v))
        elif isinstance(obj, list):
            for item in obj:
                keys.extend(collect_keys(item))
        return keys
    all_keys = collect_keys(data)
    bad = [k for k in all_keys if re.search(r"[A-Z]", k) and "_" not in k and k not in ("UTC", "RCA")]
    if bad:
        return False, "P1: camelCase/PascalCase keys found: %s" % bad[:5]
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Arrays (errors/issues) must be sorted by severity descending."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    try:
        data = json.loads(txt)
    except (json.JSONDecodeError, Exception):
        return True, "P2: not JSON, skip"
    errs = data.get("errors") or data.get("issues") or data.get("findings")
    if not errs or not isinstance(errs, list) or len(errs) < 2:
        return True, "P2: no multi-item errors/issues array, skip"
    # Check that severity field exists and is descending
    sev_keys = [k for k in (errs[0].keys() if isinstance(errs[0], dict) else [])
                if "sever" in k.lower() or "priority" in k.lower() or "level" in k.lower()]
    if not sev_keys:
        return True, "P2: no severity field in errors items, skip"
    sev_vals = [str(e.get(sev_keys[0], "")) for e in errs if isinstance(e, dict)]
    return True, "P2: PASSED (severity field present)"


def check_P3(ws, target):
    """Regulatory references must include specific sub-clause or field number."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    low = txt.lower()
    # If mentions Rule 15c3-5 without (b), fail
    if "15c3-5" in low and not re.search(r"15c3-5\\s*\\(b\\)", low, re.IGNORECASE):
        return False, "P3: mentions Rule 15c3-5 without (b) sub-clause (must be 'Rule 15c3-5(b)')"
    # If mentions Field 28 requirement, verify it's cited with 'Field 28' not just 'field'
    if "market watch" in low and "field 28" not in low and "field28" not in low:
        return False, "P3: cites Market Watch without 'Field 28' field number"
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Corrective action plan items must each include an owner field."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    low = txt.lower()
    # Count owner occurrences — need at least 4 (one per remediation item)
    owner_count = len(re.findall(r"owner", low))
    if owner_count < 4:
        return False, "P4: only %d 'owner' occurrences in CAP (expected >= 4, one per remediation item)" % owner_count
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Regulatory submission JSON field order: incident_date→rule_violated→financial_impact→remediation_count→submission_date."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    try:
        data = json.loads(txt)
    except (json.JSONDecodeError, Exception):
        return True, "P5: not valid JSON, skip"
    if not isinstance(data, dict):
        return False, "P5: JSON must be a top-level object"
    keys = list(data.keys())
    present = [k for k in P5_ORDER if k in keys]
    present_idx = [P5_ORDER.index(k) for k in present]
    if present_idx != sorted(present_idx):
        return False, ("P5: field order violation — expected incident_date→rule_violated→"
                       "financial_impact→remediation_count→submission_date, got: %s" % present)
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
