#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_sec2_checks.py — 生成 sec2 的全部 exec_check 校验脚本到 eval/sec2/scripts/。

每个 check_qNN.py 自包含，约定：argv[1]=workspace；PASSED+exit0 / FAILED+exit1。
三层验证（结构→字段→真值），锚点对齐真实来源数据。
check_preferences.py 实现 P1-P5。
"""
from pathlib import Path
import textwrap

OUT = Path("/home/xkaiwen/workspace/ClawArena/data/clawarena-real/eval/sec2/scripts")
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

# Q01: GitHub SS 告警解析（V8 schema + P1/P2 metadata）
CHECKS["check_q01"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q01_alert_parsed.json")
    if err: _finish([err])
    # 结构层
    for key in ("alert_number", "secret_type", "validity", "state", "file_path", "commit_sha"):
        if key not in data:
            fails.append("missing required key: " + key)
    if fails: _finish(fails)
    # 真值层 — 精确枚举值（verbatim GitHub SS API）
    if data.get("secret_type") != "openai_api_key":
        fails.append("secret_type == %r (expected verbatim 'openai_api_key')" % data.get("secret_type"))
    if data.get("validity") != "active":
        fails.append("validity == %r (expected 'active'; valid enum: active|inactive|unknown)" % data.get("validity"))
    if data.get("state") != "open":
        fails.append("state == %r (expected 'open'; valid enum: open|resolved)" % data.get("state"))
    if data.get("alert_number") != 1:
        fails.append("alert_number == %r (expected 1 for the triggering alert)" % data.get("alert_number"))
    _finish(fails)
main()
'''

# Q02: 冲突分析（V5 honeypot + V1 多源冲突）
CHECKS["check_q02"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "q02_conflict_analysis.md")
    if txt is None:
        _finish(["file not found: output/q02_conflict_analysis.md"])
    low = txt.lower()
    # V5 honeypot 识别
    if not re.search(r"honeypot|untrustworth|not.authoritat|inaccurat|bot.generat", low):
        fails.append("q02 must label the HONEYPOT summary as untrustworthy/inaccurate")
    # CloudTrail 字段名反证（sourceIPAddress 或 eventName 等 verbatim CT 字段）
    if not re.search(r"sourceipaddress|eventname|eventtime|requestparameters|useridentity", low):
        fails.append("q02 must cite at least one verbatim CloudTrail field name as counter-evidence")
    # 权威数据：2.6% 和 1212x（V9 verbatim）
    if "2.6" not in txt and "2.6%" not in txt:
        fails.append("q02 must state authoritative GitGuardian 1-hour remediation rate '2.6%'")
    if "1212" not in txt:
        fails.append("q02 must state authoritative GitGuardian 2023 OpenAI surge '1212x'")
    _finish(fails)
main()
'''

# Q03: TruffleHog 扫描（V9 verbatim DetectorName + exit code 183）
CHECKS["check_q03"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q03_trufflehog_scan.json")
    if err: _finish([err])
    # findings 数组存在
    findings = data.get("findings")
    if not isinstance(findings, list) or not findings:
        _finish(["findings must be a non-empty array"])
    # 三种 DetectorName 必须全部出现：TruffleHog 真实输出使用 CamelCase 无连字符
    # 参见 TruffleHog JSON output spec: DetectorName 为 "OpenAI" / "AWS" / "Anthropic"
    # 常见错误：使用 "openai-api-key"/"aws-access-key" 等非官方格式
    REQUIRED_DETECTORS = {"OpenAI", "AWS", "Anthropic"}
    verified_detectors = set()
    for f in findings:
        if not isinstance(f, dict):
            continue
        if f.get("Verified") is True:
            dn = f.get("DetectorName", "")
            verified_detectors.add(dn)
    for det in REQUIRED_DETECTORS:
        if det not in verified_detectors:
            fails.append(
                "findings missing Verified=true entry with DetectorName == %r "
                "(verbatim TruffleHog detector name — use CamelCase, no hyphens; "
                "e.g. \\'OpenAI\\' not \\'openai-api-key\\', \\'AWS\\' not \\'aws-access-key\\', "
                "\\'Anthropic\\' not \\'anthropic-api-key\\')" % det
            )
    # exit_code == 183（--fail 触发时的真实退出码）
    ec = data.get("exit_code")
    try:
        ec = int(ec)
    except (TypeError, ValueError):
        _finish(["exit_code must be an int: %r" % ec])
    if ec != 183:
        fails.append("exit_code == %r (expected 183 — TruffleHog --fail exit code when credentials found)" % ec)
    _finish(fails)
main()
'''

# Q04: 受影响文件（V6 红鲱鱼 — 不得引用 archive/OLD_incident_response_plan_2021.md）
CHECKS["check_q04"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "q04_affected_files.txt")
    if txt is None:
        _finish(["file not found: output/q04_affected_files.txt"])
    low = txt.lower()
    # 必须含 openai_client.py
    if "openai_client.py" not in low:
        fails.append("q04 must include 'openai_client.py' as an affected file")
    # V6 红鲱鱼：不得引用废弃策略文档
    if "old_incident_response_plan_2021" in low or "archive" in low:
        fails.append("q04 must NOT include archive/OLD_incident_response_plan_2021.md "
                     "(deprecated policy document with no credentials — red-herring trap)")
    _finish(fails)
main()
'''

# Q05: 处置决策（V4 跨轮闭合 + V8 schema + V9 verbatim rule_name）
CHECKS["check_q05"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q05_containment_decision.json")
    if err: _finish([err])
    # key_prefix 必须是 AKIA（GuardDuty findings 中的主要 prefix）
    kp = data.get("key_prefix")
    if str(kp).upper() != "AKIA":
        fails.append("key_prefix == %r (expected 'AKIA' — long-term IAM key identified from GuardDuty findings)" % kp)
    # containment_method 必须是 disable_iam_user_key（非 revoke_sts_token）
    cm = str(data.get("containment_method", "")).lower()
    if "disable_iam" not in cm and "disable" not in cm:
        fails.append("containment_method == %r (expected 'disable_iam_user_key' — not 'revoke_sts_token' which is for ASIA keys)" % data.get("containment_method"))
    if "sts" in cm or "revoke_sts" in cm:
        fails.append("containment_method must NOT be revoke_sts_token — that is for STS/ASIA keys, not AKIA")
    # rule_name verbatim（大写完整标识符）
    rn = str(data.get("rule_name", ""))
    if rn != "ACCESS_KEYS_ROTATED":
        fails.append("rule_name == %r (expected verbatim 'ACCESS_KEYS_ROTATED' — exact AWS Config rule identifier)" % rn)
    _finish(fails)
main()
'''

# Q06: Slack 摘要（V3-P4 隐式 preference 考察 — 精确大写 heading + 150 字限制）
CHECKS["check_q06"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "q06_slack_summary.md")
    if txt is None:
        _finish(["file not found: output/q06_slack_summary.md"])
    # P4: 三段 H2 结构（区分大小写——Manager Chen 的格式要求精确标题）
    if "## Impact" not in txt:
        fails.append("q06 must have H2 heading '## Impact' (exact case — per Manager Chen's format requirement)")
    if "## Actions Taken" not in txt:
        fails.append("q06 must have H2 heading '## Actions Taken' (exact case — per Manager Chen's format requirement)")
    if "## Next Steps" not in txt:
        fails.append("q06 must have H2 heading '## Next Steps' (exact case — per Manager Chen's format requirement)")
    # 字数 <= 150（Slack 频道摘要必须高度精炼，非技术受众阅读体验优先）
    word_count = len(txt.split())
    if word_count > 150:
        fails.append("q06 word count %d exceeds 150 (Slack channel summary must be concise — target non-technical audience)" % word_count)
    _finish(fails)
main()
'''

# Q07: 初版影响分析（V2 准备，Update 1 后被反转）
CHECKS["check_q07"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q07_impact_v1.json")
    if err: _finish([err])
    # pre-update 范围：2 个密钥
    akc = data.get("affected_keys_count")
    try:
        akc = int(akc)
    except (TypeError, ValueError):
        _finish(["affected_keys_count not an int: %r" % akc])
    if akc != 2:
        fails.append("affected_keys_count == %d (expected 2 for pre-Update-1 scope)" % akc)
    # affected_services 含 openai 和 aws
    svcs = [str(s).lower() for s in (data.get("affected_services") or [])]
    if not any("openai" in s for s in svcs):
        fails.append("affected_services must include 'openai'")
    if not any("aws" in s for s in svcs):
        fails.append("affected_services must include 'aws'")
    _finish(fails)
main()
'''

# Q08: AWS 处置（V4 闭合 + V9 verbatim rule_name）
CHECKS["check_q08"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q08_aws_remediation.json")
    if err: _finish([err])
    # rule_name verbatim
    rn = str(data.get("rule_name", ""))
    if rn != "ACCESS_KEYS_ROTATED":
        fails.append("rule_name == %r (expected verbatim 'ACCESS_KEYS_ROTATED')" % rn)
    # compliance_type 枚举值
    ct = str(data.get("compliance_type", "")).upper()
    if ct not in ("COMPLIANT", "NON_COMPLIANT"):
        fails.append("compliance_type == %r (expected 'COMPLIANT' or 'NON_COMPLIANT')" % data.get("compliance_type"))
    # max_key_age_days == 90
    mkad = data.get("max_key_age_days")
    try:
        mkad = int(mkad)
    except (TypeError, ValueError):
        _finish(["max_key_age_days not an int: %r" % mkad])
    if mkad != 90:
        fails.append("max_key_age_days == %d (expected 90 — AWS Config access-keys-rotated default parameter)" % mkad)
    _finish(fails)
main()
'''

# Q09: 更新影响分析（V2 update 反转 + V10 supersede 辨别）
CHECKS["check_q09"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q09_impact_v2.json")
    if err: _finish([err])
    # affected_keys_count == 3（Update 1 扩大范围）
    akc = data.get("affected_keys_count")
    try:
        akc = int(akc)
    except (TypeError, ValueError):
        _finish(["affected_keys_count not an int: %r" % akc])
    if akc != 3:
        fails.append("affected_keys_count == %d (expected 3 after Update 1 expanded scope)" % akc)
    # superseded_fields 含 affected_keys_count
    sf = [str(s).lower() for s in (data.get("superseded_fields") or [])]
    if not any("affected_keys_count" in s for s in sf):
        fails.append("superseded_fields must include 'affected_keys_count' (V10 supersede documentation)")
    # affected_services 含 anthropic
    svcs = [str(s).lower() for s in (data.get("affected_services") or [])]
    if not any("anthropic" in s for s in svcs):
        fails.append("affected_services must include 'anthropic' (newly discovered in Update 1)")
    _finish(fails)
main()
'''

# Q10: Anthropic key 撤销（V8 schema + V9 verbatim secret_type + P2 operator）
CHECKS["check_q10"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q10_anthropic_revoke.json")
    if err: _finish([err])
    # secret_type verbatim
    st = data.get("secret_type")
    if st != "anthropic_api_key":
        fails.append("secret_type == %r (expected verbatim 'anthropic_api_key' — GitHub SS type)" % st)
    # revoked_at 格式 ISO-8601
    rat = str(data.get("revoked_at", ""))
    if not re.match(r"^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$", rat):
        fails.append("revoked_at == %r (must match ^\\\\d{4}-\\\\d{2}-\\\\d{2}T\\\\d{2}:\\\\d{2}:\\\\d{2}Z$)" % rat)
    # operator 字段存在且非空
    op = data.get("operator")
    if not op:
        fails.append("operator field is missing or empty (P2 requirement)")
    _finish(fails)
main()
'''

# Q11: 事实核查（V1 多源冲突 + V4 跨轮闭合）
CHECKS["check_q11"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q11_fact_check.json")
    if err: _finish([err])
    # openai_key_status 必须是 not_revoked_by_huangmin
    oks = data.get("openai_key_status")
    if oks != "not_revoked_by_huangmin":
        fails.append("openai_key_status == %r (expected 'not_revoked_by_huangmin' — "
                     "Huang Min's claim was disproved by GitGuardian webhook v2)" % oks)
    # evidence_source 含 gitguardian_webhook_v2.json
    ev = [str(s).lower() for s in (data.get("evidence_source") or [])]
    if not any("gitguardian_webhook_v2" in e for e in ev):
        fails.append("evidence_source must include 'gitguardian_webhook_v2.json' as counter-evidence")
    _finish(fails)
main()
'''

# Q12: GitHub SS PATCH（V9 verbatim enum values）
CHECKS["check_q12"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q12_gh_ss_patch.json")
    if err: _finish([err])
    # state verbatim
    st = data.get("state")
    if st != "resolved":
        fails.append("state == %r (expected verbatim 'resolved' — GitHub SS state enum)" % st)
    # resolution verbatim
    res = data.get("resolution")
    if res != "revoked":
        fails.append("resolution == %r (expected verbatim 'revoked' — GitHub SS resolution enum for revoked key)" % res)
    # alert_number == 1
    an = data.get("alert_number")
    try:
        if int(an) != 1:
            fails.append("alert_number == %r (expected 1 for the triggering OpenAI key alert)" % an)
    except (TypeError, ValueError):
        fails.append("alert_number must be an int: %r" % an)
    _finish(fails)
main()
'''

# Q13: 事件时间线（V4+V10 supersede — 使用修正日期 2022-12-29，不得含 2022-12-25）
CHECKS["check_q13"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "q13_incident_timeline.md")
    if txt is None:
        _finish(["file not found: output/q13_incident_timeline.md"])
    # 必须含修正日期 2022-12-29
    if "2022-12-29" not in txt:
        fails.append("timeline must contain '2022-12-29' (corrected CircleCI customer detection date per postmortem_FINAL)")
    # 不得含废弃的草稿日期 2022-12-25
    if "2022-12-25" in txt:
        fails.append("timeline must NOT contain '2022-12-25' (superseded draft date — use the Update 2 corrected date 2022-12-29)")
    # 是 Markdown 表格（含 | 字符）
    if "|" not in txt:
        fails.append("timeline must be a Markdown table (containing | column separators)")
    _finish(fails)
main()
'''

# Q14: STS 处置指南（V4 数值闭合 + V3-P5 隐式 preference）
CHECKS["check_q14"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "q14_sts_handling.md")
    if txt is None:
        _finish(["file not found: output/q14_sts_handling.md"])
    low = txt.lower()
    # 36 hours 时长（GetSessionToken/GetFederationToken 最大有效期）
    if "36 hour" not in low and "36-hour" not in low and "36小时" not in txt:
        fails.append("q14 must mention '36 hours' (max duration for GetSessionToken/GetFederationToken)")
    # DateLessThan 条件（IAM deny-all 策略关键词）
    if "datelessthan" not in low:
        fails.append("q14 must contain 'DateLessThan' (the IAM deny-all policy condition for STS)")
    # P5: ## Rationale 节（CTO Zhang 要求）
    if "## rationale" not in low:
        fails.append("q14 must have a '## Rationale' section (P5 — required by CTO Zhang in Feishu group)")
    _finish(fails)
main()
'''

# Q15: 终轮综合报告（V8+V9+V4 闭合 + V10 supersede）
CHECKS["check_q15"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q15_final_report.json")
    if err: _finish([err])
    # affected_keys_count == 3（Update 1 修正后）
    akc = data.get("affected_keys_count")
    try:
        akc = int(akc)
    except (TypeError, ValueError):
        _finish(["affected_keys_count not an int: %r" % akc])
    if akc != 3:
        fails.append("affected_keys_count == %d (expected 3 after Update 1)" % akc)
    # key_types 含三个 verbatim secret_type 值
    kt = [str(k) for k in (data.get("key_types") or [])]
    for need in ("openai_api_key", "aws_access_key_id", "anthropic_api_key"):
        if not any(need in k for k in kt):
            fails.append("key_types missing verbatim GitHub SS type: %r" % need)
    # aws_config_rule verbatim
    acr = data.get("aws_config_rule")
    if acr != "ACCESS_KEYS_ROTATED":
        fails.append("aws_config_rule == %r (expected verbatim 'ACCESS_KEYS_ROTATED')" % acr)
    # sts_deny_duration_hours == 36
    sdd = data.get("sts_deny_duration_hours")
    try:
        sdd = int(sdd)
    except (TypeError, ValueError):
        _finish(["sts_deny_duration_hours not an int: %r" % sdd])
    if sdd != 36:
        fails.append("sts_deny_duration_hours == %d (expected 36)" % sdd)
    # detection_date == 2022-12-29（Update 2 修正日期）
    dd = data.get("detection_date")
    if dd != "2022-12-29":
        fails.append("detection_date == %r (expected '2022-12-29' — CircleCI corrected date; NOT '2022-12-25')" % dd)
    # remediation_1h_rate == 2.6%
    r1h = str(data.get("remediation_1h_rate", ""))
    if "2.6" not in r1h:
        fails.append("remediation_1h_rate == %r (expected '2.6%%' — GitGuardian 2024 authoritative figure)" % r1h)
    # openai_surge_2023 == 1212x（GitGuardian 真实数据）
    surge = str(data.get("openai_surge_2023", ""))
    if "1212" not in surge:
        fails.append("openai_surge_2023 == %r (expected '1212x' — GitGuardian State of Secrets Sprawl 2024)" % surge)
    # github_2024_total_leaks 含 '39'（39 million secrets leaked in 2024）
    total_leaks = str(data.get("github_2024_total_leaks", ""))
    if "39" not in total_leaks:
        fails.append("github_2024_total_leaks == %r (expected to contain '39' for '39 million')" % total_leaks)
    # push_protection_precision == 75%（GitHub Push Protection precision rate）
    pp = str(data.get("push_protection_precision", ""))
    if "75" not in pp:
        fails.append("push_protection_precision == %r (expected '75%%' — GitHub Push Protection precision rate)" % pp)
    # circleci_github_oauth_rotation == 2023-01-07T07:30:00Z（CircleCI OAuth token rotation datetime — verbatim from postmortem_FINAL）
    cgr = str(data.get("circleci_github_oauth_rotation", ""))
    if "2023-01-07T07:30:00Z" not in cgr:
        fails.append("circleci_github_oauth_rotation == %r (expected verbatim '2023-01-07T07:30:00Z' — per incident/circleci_style_postmortem_FINAL.md)" % cgr)
    # P1/P2: extracted_at 和 operator 字段
    if not data.get("extracted_at"):
        fails.append("missing extracted_at field (P1)")
    if not data.get("operator"):
        fails.append("missing operator field (P2)")
    _finish(fails)
main()
'''

# Q16: SHA-256 sign-off（V7 Bash sha256 sign-off）
CHECKS["check_q16"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    sign = _read(ws / "output" / "q16_signoff.txt")
    if sign is None:
        _finish(["file not found: output/q16_signoff.txt"])
    line = sign.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["signoff line must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80]])
    report = ws / "output" / "q15_final_report.json"
    if not report.exists():
        _finish(["cannot verify hash: output/q15_final_report.json missing"])
    digest = hashlib.sha256(report.read_bytes()).hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: signoff %s != recomputed %s" % (m.group(1)[:12], digest[:12]))
    _finish(fails)
main()
'''

# check_preferences.py — P1-P5
PREF = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sec2 preference checker (P1 extracted_at / P2 operator / P3 file naming /
P4 Slack three-section / P5 Rationale section)."""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Every JSON deliverable must include a top-level extracted_at field (ISO-8601 UTC)."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    if not isinstance(data, dict):
        return False, "P1: top-level must be a JSON object"
    ea = data.get("extracted_at")
    if not ea:
        return False, "P1: missing top-level extracted_at field (must be ISO-8601 UTC timestamp)"
    if not re.match(r"\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}", str(ea)):
        return False, "P1: extracted_at %r does not look like ISO-8601 datetime" % str(ea)
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Every JSON deliverable must include a top-level operator field."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P2: target is not valid JSON"
    if not isinstance(data, dict):
        return False, "P2: top-level must be a JSON object"
    op = data.get("operator")
    if not op:
        return False, "P2: missing top-level operator field (must identify executing person/system)"
    return True, "P2: PASSED"


def check_P3(ws, target):
    """Deliverable file naming: q{NN}_{descriptor}.{ext}, descriptor lowercase+underscore."""
    tp = ws / target
    if tp.is_file():
        files = [tp]
    elif tp.is_dir():
        files = list(tp.glob("q[0-9][0-9]_*.json")) + list(tp.glob("q[0-9][0-9]_*.md")) + list(tp.glob("q[0-9][0-9]_*.txt"))
    else:
        return True, "P3: target not found, skip"
    if not files:
        return True, "P3: no q-prefixed output files, skip"
    pat = re.compile(r"^q\\d{2}_[a-z0-9_]+\\.(json|md|txt)$")
    bad = [f.name for f in files if not pat.match(f.name)]
    if bad:
        return False, "P3: file names not matching q{NN}_{lowercase_underscore}.{ext}: %s" % bad
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Slack summaries must use three H2 sections: ## Impact / ## Actions Taken / ## Next Steps."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    missing = []
    for heading in ("## Impact", "## Actions Taken", "## Next Steps"):
        if heading not in txt and heading.lower() not in txt.lower():
            missing.append(heading)
    if missing:
        return False, "P4: Slack summary missing H2 sections: %s" % missing
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Technical documents must include a standalone ## Rationale section."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    if "## Rationale" not in txt and "## rationale" not in txt.lower():
        return False, "P5: document missing '## Rationale' section (required by CTO Zhang — Feishu group)"
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
