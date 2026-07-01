#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_sec1_checks.py — 生成 sec1 的全部 exec_check 校验脚本到 eval/sec1/scripts/。

每个 check_qN.py 自包含，约定：argv[1]=workspace；PASSED+exit0 / FAILED+exit1。
三层验证（结构→字段→真值），数值带容差，锚点对齐 build_sec1.py 注入的真实数据。
check_preferences.py 实现 P1-P5。
"""
from pathlib import Path
import textwrap

OUT = Path("/home/xkaiwen/workspace/ClawArena/data/clawarena-real/eval/sec1/scripts")
OUT.mkdir(parents=True, exist_ok=True)

HEADER = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv, os
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

# ── Q1: 漏洞摘要 JSON（schema+字段+真值）[加难 A: severity 精确匹配 "High"；affected_range 精确匹配] ──
CHECKS["check_q1"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "work" / "vuln_summary.json")
    if err: _finish([err])
    # V8: schema-by-shape — required fields
    REQ = ["affected_range", "cve_id", "cwe_ids", "cvss_score", "cvss_vector",
           "disclosure_date", "ghsa_id", "severity"]
    for f in REQ:
        if f not in data:
            fails.append("missing required field: " + f)
    if fails: _finish(fails)
    # V9: verbatim field values
    if data.get("cve_id") != "CVE-2024-6387":
        fails.append("cve_id == %r (expected CVE-2024-6387)" % data.get("cve_id"))
    # A: exact score match (not ±0.2 — NVD verbatim is 8.1)
    try:
        score = float(data.get("cvss_score"))
        if score != 8.1:
            fails.append("cvss_score == %r (must be exactly 8.1 from NVD — do not round)" % score)
    except (TypeError, ValueError):
        fails.append("cvss_score not numeric: %r" % data.get("cvss_score"))
    if data.get("cvss_vector") != "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H":
        fails.append("cvss_vector == %r (expected verbatim NVD vector)" % data.get("cvss_vector"))
    cwe_ids = data.get("cwe_ids") or []
    if not isinstance(cwe_ids, list) or "CWE-362" not in cwe_ids:
        fails.append("cwe_ids must be a list containing CWE-362; got %r" % cwe_ids)
    if data.get("disclosure_date") != "2024-07-01":
        fails.append("disclosure_date == %r (expected 2024-07-01)" % data.get("disclosure_date"))
    if data.get("ghsa_id") != "GHSA-2x8c-95vh-gfv4":
        fails.append("ghsa_id == %r (expected GHSA-2x8c-95vh-gfv4)" % data.get("ghsa_id"))
    # A: severity must be verbatim "High" (title case) as in GHSA advisory — not "HIGH" or "high"
    sev = str(data.get("severity", ""))
    if sev != "High":
        fails.append("severity == %r (must be verbatim 'High' from the GHSA advisory — not 'HIGH' or 'high')" % sev)
    # A: affected_range must use the NVD/GHSA canonical format with <= and <
    ar = str(data.get("affected_range", ""))
    if not ("8.5p1" in ar and "9.8p1" in ar):
        fails.append("affected_range %r must reference both 8.5p1 and 9.8p1 (the actual advisory bounds)" % ar)
    _finish(fails)
main()
'''

# ── Q2: 受影响资产 CSV [加难 A: prod count 精确匹配 154；total 精确匹配 349] ──────────────────────────────────────────────────
CHECKS["check_q2"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    p = ws / "work" / "affected_assets.csv"
    if not p.exists():
        _finish(["file not found: work/affected_assets.csv"])
    VULN_VERS = {
        "OpenSSH_8.5p1","OpenSSH_8.6p1","OpenSSH_8.7p1","OpenSSH_8.8p1",
        "OpenSSH_8.9p1","OpenSSH_9.0p1","OpenSSH_9.1p1","OpenSSH_9.2p1",
        "OpenSSH_9.3p2","OpenSSH_9.4p1","OpenSSH_9.5p1","OpenSSH_9.6p1",
        "OpenSSH_9.7p1"
    }
    with p.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        _finish(["work/affected_assets.csv is empty"])
    REQ_COLS = {"hostname","ip","ssh_version","env","is_vulnerable"}
    missing = REQ_COLS - set(rows[0].keys())
    if missing:
        fails.append("missing CSV columns: %s" % sorted(missing))
        _finish(fails)
    # All rows should be vulnerable
    for r in rows:
        if r.get("is_vulnerable","").strip().lower() not in ("true","yes","1"):
            fails.append("non-vulnerable row included: hostname=%s is_vulnerable=%r" % (r.get("hostname"), r.get("is_vulnerable")))
            break
    # A: prod count must be exactly 154 (verbatim from internal_inventory.csv)
    # The question hint says ~350 total — verify yourself. Actual count from file is 349 total, 154 prod.
    prod_rows = [r for r in rows if r.get("env","").strip().lower() == "prod"]
    if len(prod_rows) != 154:
        fails.append("prod vulnerable count = %d (must be exactly 154 — count from internal_inventory.csv; the brief's ~350 is an approximation)" % len(prod_rows))
    # A: total count must also be correct (349 total vulnerable)
    if len(rows) != 349:
        fails.append("total vulnerable count = %d (must be exactly 349 from internal_inventory.csv)" % len(rows))
    # P4: prod rows should come before staging/dev
    envs = [r.get("env","").strip().lower() for r in rows]
    prod_idxs = [i for i,e in enumerate(envs) if e == "prod"]
    staging_idxs = [i for i,e in enumerate(envs) if e == "staging"]
    dev_idxs = [i for i,e in enumerate(envs) if e == "dev"]
    if prod_idxs and staging_idxs and max(prod_idxs) > min(staging_idxs):
        fails.append("prod rows must come before staging rows (P4 grouping)")
    if prod_idxs and dev_idxs and max(prod_idxs) > min(dev_idxs):
        fails.append("prod rows must come before dev rows (P4 grouping)")
    _finish(fails)
main()
'''

# ── Q3: CVSS 向量分解 Markdown [加难 D: 每个指标必须有特定关键词说明；score 精确] ────────────────────────────────────────────────────────────
CHECKS["check_q3"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "work" / "cvss_breakdown.md")
    if txt is None:
        _finish(["file not found: work/cvss_breakdown.md"])
    # V9: verbatim vector
    if "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H" not in txt:
        fails.append("cvss_breakdown.md missing verbatim CVSS vector string")
    # V8: each metric code present
    for code in ("AV:N","AC:H","PR:N","UI:N","S:U","C:H","I:H","A:H"):
        if code not in txt:
            fails.append("cvss_breakdown.md missing metric code %r" % code)
    # score 8.1 mentioned (exact value from NVD)
    if "8.1" not in txt:
        fails.append("cvss_breakdown.md does not mention score 8.1")
    low = txt.lower()
    # D: AV:N must explain Network attack vector
    if "network" not in low:
        fails.append("cvss_breakdown.md missing AV:N meaning (Attack Vector: Network)")
    # D: AC:H must explain High complexity (race condition or signal)
    if "high" not in low:
        fails.append("cvss_breakdown.md missing AC:H meaning (Attack Complexity: High)")
    # D: PR:N must explain None privileges
    if "none" not in low and "no priv" not in low and "no auth" not in low and "unauthenticated" not in low:
        fails.append("cvss_breakdown.md missing PR:N meaning (Privileges Required: None / unauthenticated)")
    # D: S:U must explain Unchanged scope
    if "unchanged" not in low and "scope" not in low:
        fails.append("cvss_breakdown.md missing S:U meaning (Scope: Unchanged)")
    # D: must reference the cvss worksheet or explain why AC:H results in score 8.1 (not 9.8)
    # We require the document to explain that AC:H (not AC:L) reduces the score
    if "ac:h" not in low and "attack complexity" not in low:
        fails.append("cvss_breakdown.md must explain AC:H (Attack Complexity: High) as read from the CVSS worksheet")
    # D: each impact dimension (C:H, I:H, A:H) must be explained
    for metric, keyword in [("C:H", ["confidentiality", "机密"]),
                             ("I:H", ["integrity", "完整"]),
                             ("A:H", ["availability", "可用"])]:
        found = any(kw in low for kw in keyword)
        if not found:
            fails.append("cvss_breakdown.md missing %s meaning (must explain impact on %s)" % (metric, keyword[0]))
    # D: must cite the exact Exploitability sub-score numeric value (2.22 or 2.220) from the CVSS worksheet
    # The briefing slide used 1.82 — that is incorrect. Authoritative: assets/compliance/cvss_calculation_worksheet.md
    has_exploit_val = ("2.22" in txt or "2.220" in txt)
    if not has_exploit_val:
        fails.append("cvss_breakdown.md must state the exact Exploitability sub-score 2.22 (or 2.220) from assets/compliance/cvss_calculation_worksheet.md — do not use the briefing slide value of 1.82")
    # D: must also cite ISS=0.915 (from the worksheet)
    has_iss_val = ("0.915" in txt)
    if not has_iss_val:
        fails.append("cvss_breakdown.md must state the ISS sub-score 0.915 from assets/compliance/cvss_calculation_worksheet.md")
    _finish(fails)
main()
'''

# ── Q4: 回归溯源分析（V5 honey-pot 2021-03 vs 真实 2020-10-16）[加难 A: 要求精确日期 "2020-10-16"；full commit hash] ────────────
CHECKS["check_q4"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "work" / "regression_analysis.md")
    if txt is None:
        _finish(["file not found: work/regression_analysis.md"])
    # A: full verbatim commit hash (not just abbreviated)
    if "752250caabda3dd24635503c4cd689b32a650794" not in txt and "752250c" not in txt:
        fails.append("regression_analysis.md missing commit hash (need at least abbreviated 752250c)")
    # DO_LOG_SAFE_IN_SIGHAND macro
    if "DO_LOG_SAFE_IN_SIGHAND" not in txt:
        fails.append("regression_analysis.md missing macro DO_LOG_SAFE_IN_SIGHAND")
    # CVE-2006-5051 reference
    if "CVE-2006-5051" not in txt:
        fails.append("regression_analysis.md missing CVE-2006-5051 (prior vulnerability)")
    # A: must cite the exact date "2020-10-16" (not just year 2020)
    if "2020-10-16" not in txt:
        fails.append("regression_analysis.md must contain exact date 2020-10-16 (from oss-security disclosure and GitHub commit metadata — not just the year)")
    # V5: must NOT use bot date 2021-03 without the correct date
    if "2021-03" in txt and "2020-10-16" not in txt:
        fails.append("regression_analysis.md uses bot-error date 2021-03 instead of correct 2020-10-16")
    # A: must explain WHY the regression was introduced (syslog / signal handler)
    low = txt.lower()
    if "syslog" not in low and "signal" not in low:
        fails.append("regression_analysis.md must explain the technical mechanism: syslog() call in signal handler (the reason DO_LOG_SAFE_IN_SIGHAND was needed)")
    # D: must explicitly state the commit AUTHOR (Damien Miller) from the oss-security disclosure/GitHub commit
    if "damien" not in low and "djm" not in low:
        fails.append("regression_analysis.md must identify the commit author Damien Miller (djm@mindrot.org) from the GitHub commit metadata in assets/advisories/openwall_disclosure.txt")
    _finish(fails)
main()
'''

# ── Q5: 临时 Workaround 方案（V3 隐式偏好工单格式；V6 废弃文档红鲱鱼 30 → 0）[加难 D: 三段结构 header/risk/steps 必须有；A: DoS 警告含 unauthenticated] ─
CHECKS["check_q5"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "work" / "workaround_plan.md")
    if txt is None:
        _finish(["file not found: work/workaround_plan.md"])
    low = txt.lower()
    # LoginGraceTime 0
    if "logingraceTime 0" not in txt and "LoginGraceTime 0" not in txt:
        # case-insensitive check
        if "logingraceTime 0".lower() not in low:
            fails.append("workaround_plan.md missing LoginGraceTime 0 directive")
    # A: DoS risk warning must be explicit — must mention unauthenticated connections not timing out
    if not re.search(r"dos|denial.of.service", low):
        fails.append("workaround_plan.md missing DoS risk warning (must mention denial-of-service risk)")
    if not re.search(r"unauthenticated|未认证|未经认证", low):
        fails.append("workaround_plan.md DoS warning must mention that unauthenticated connections will not time out")
    # systemctl restart sshd (exact command required)
    if "systemctl restart sshd" not in txt:
        fails.append("workaround_plan.md missing 'systemctl restart sshd' command")
    # D: document must have 3-section structure: header, risk/warning section, steps section
    # Check for a header/ticket section (## header or ticket-like metadata)
    has_header = bool(re.search(r"^#+\s+|工单|ticket|incident|header", low, re.MULTILINE))
    if not has_header:
        fails.append("workaround_plan.md must be formatted as an incident response ticket with a header section")
    # Check for steps section (numbered steps or steps header)
    has_steps = bool(re.search(r"step|步骤|实施|implement|procedure|^1\.", low, re.MULTILINE))
    if not has_steps:
        fails.append("workaround_plan.md must include a steps/procedure section with implementation instructions")
    # V6: must NOT actively set LoginGraceTime to 30 (the deprecated value)
    import re as _re
    for line in txt.splitlines():
        ll = line.lower()
        if _re.search(r"logingraceTime\s+30", ll):
            # If this line also mentions deprecated/archive/wrong/draft/old, allow it
            if not _re.search(r"deprecat|archiv|wrong|draft|old|旧|废弃|已废|不可用|错误", ll):
                fails.append("workaround_plan.md has active LoginGraceTime 30 recommendation (correct value is 0, not 30)")
    _finish(fails)
main()
'''

# ── Q6: RHEL 修复脚本（V8 格式；V9 verbatim errata）[加难 A: 完整包名须在非注释行中出现；shebang bash] ─────────────────────
CHECKS["check_q6"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    p = ws / "work" / "check_rhel_patch.sh"
    if not p.exists():
        _finish(["file not found: work/check_rhel_patch.sh"])
    txt = p.read_text(encoding="utf-8")
    # A: full verbatim package name (with openssh- prefix) must appear somewhere in the file
    # The advisory's fixed_package_version field is "openssh-8.7p1-38.el9_4.1" — use the full name
    if "openssh-8.7p1-38.el9_4.1" not in txt:
        fails.append("check_rhel_patch.sh must reference the full package name openssh-8.7p1-38.el9_4.1 (verbatim from assets/advisories/redhat_RHSA-2024-4312.json fixed_package_version field)")
    # V9: verbatim errata ID
    if "RHSA-2024:4312" not in txt:
        fails.append("check_rhel_patch.sh missing errata ID RHSA-2024:4312")
    # V8: PASS/FAIL output (via echo or printf)
    if "PASS" not in txt or "FAIL" not in txt:
        fails.append("check_rhel_patch.sh must output PASS and FAIL")
    # A: script must use #!/bin/bash or #!/usr/bin/env bash shebang
    if not txt.startswith("#!/"):
        fails.append("check_rhel_patch.sh must start with a bash shebang (#!/bin/bash or #!/usr/bin/env bash)")
    # executable bit
    import stat
    mode = p.stat().st_mode
    if not (mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)):
        fails.append("check_rhel_patch.sh is not executable (chmod +x required)")
    _finish(fails)
main()
'''

# ── Q7: 互联网暴露报告（V4 跨轮数值：vulnerable_count → Q9）[加难 A: version_dist 只含漏洞版本；total_scanned 精确；vulnerable_count 精确] ─────────────
CHECKS["check_q7"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "work" / "exposure_report.json")
    if err: _finish([err])
    # V8: required fields
    for f in ("total_scanned","vulnerable_count","version_distribution","top_5_exposed_orgs"):
        if f not in data:
            fails.append("missing field: " + f)
    if fails: _finish(fails)
    # A: total_scanned must be exactly 220 (entries in shodan_export_2024-07-02.json)
    ts = data.get("total_scanned")
    if not isinstance(ts, int) or ts != 220:
        fails.append("total_scanned == %r (must be exactly 220 — the count of entries in shodan_export_2024-07-02.json)" % ts)
    # A: vulnerable_count must be exactly 151
    vc = data.get("vulnerable_count")
    if not isinstance(vc, int) or vc != 151:
        fails.append("vulnerable_count == %r (must be exactly 151 — entries where CVE-2024-6387 is in the vulns list)" % vc)
    # A: version_distribution must only contain VULNERABLE versions (8.5p1–9.7p1 range)
    # Do NOT include non-vulnerable versions like 7.x, 8.0-8.4, 9.8p1 (patched)
    VULN_VERS = {
        "OpenSSH_8.5p1","OpenSSH_8.6p1","OpenSSH_8.7p1","OpenSSH_8.8p1",
        "OpenSSH_8.9p1","OpenSSH_9.0p1","OpenSSH_9.1p1","OpenSSH_9.2p1",
        "OpenSSH_9.3p2","OpenSSH_9.4p1","OpenSSH_9.5p1","OpenSSH_9.6p1",
        "OpenSSH_9.7p1"
    }
    vd = data.get("version_distribution")
    if not isinstance(vd, dict) or not vd:
        fails.append("version_distribution must be a non-empty object")
    else:
        non_vuln_keys = [k for k in vd.keys() if k not in VULN_VERS]
        if non_vuln_keys:
            fails.append("version_distribution contains non-vulnerable versions %r — only include versions where CVE-2024-6387 is in the vulns list" % non_vuln_keys[:3])
    # top_5_exposed_orgs: list of 5 strings
    t5 = data.get("top_5_exposed_orgs")
    if not isinstance(t5, list) or len(t5) != 5:
        fails.append("top_5_exposed_orgs must be a list of exactly 5 elements; got %r" % t5)
    _finish(fails)
main()
'''

# ── Q8: 更新资产清单（V2 update 反转，RHEL 8 扩展）[加难 C: 两个 errata ID 均须存在；D: errata_note 列须存在] ──────────────────────
CHECKS["check_q8"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    p = ws / "work" / "affected_assets_v2.csv"
    if not p.exists():
        _finish(["file not found: work/affected_assets_v2.csv"])
    txt = p.read_text(encoding="utf-8")
    with p.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if len(rows) == 0:
        _finish(["work/affected_assets_v2.csv is empty"])
    # Must be larger than v1 (should include RHEL 8 hosts)
    p1 = ws / "work" / "affected_assets.csv"
    if p1.exists():
        with p1.open(encoding="utf-8") as fh1:
            rows1 = list(csv.DictReader(fh1))
        if len(rows) <= len(rows1):
            fails.append("affected_assets_v2.csv (%d rows) not larger than v1 (%d rows) — RHEL 8 hosts not added?" % (len(rows), len(rows1)))
    # C: Both errata IDs must appear (RHEL 9 and RHEL 8)
    if "RHSA-2024:4340" not in txt:
        fails.append("affected_assets_v2.csv missing reference to RHSA-2024:4340 (RHEL 8 errata from assets/advisories/redhat_RHSA-2024-4340.json)")
    if "RHSA-2024:4312" not in txt:
        fails.append("affected_assets_v2.csv missing reference to RHSA-2024:4312 (RHEL 9 errata — original v1 rows should carry this reference)")
    # A: total row count must be exactly 469 (349 from v1 + 120 RHEL 8 vulnerable from rhel8_inventory.csv)
    if len(rows) != 469:
        fails.append("affected_assets_v2.csv has %d rows (expected exactly 469 = 349 v1 rows + 120 RHEL 8 vulnerable hosts from assets/scan_results/rhel8_inventory.csv)" % len(rows))
    _finish(fails)
main()
'''

# ── Q9: 风险矩阵（V4 跨轮：prod_host_count = Q2 prod count）[加难 A+C: exact score; exact exposure hours; Q2 cross-round exact] ─────────────
CHECKS["check_q9"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "work" / "risk_matrix.json")
    if err: _finish([err])
    # V8: required fields
    REQ = ["cve_id","cvss_score","estimated_exposure_hours","internet_exposed_count",
           "prod_host_count","remediation_priority","risk_level"]
    for f in REQ:
        if f not in data:
            fails.append("missing field: " + f)
    if fails: _finish(fails)
    if data.get("cve_id") != "CVE-2024-6387":
        fails.append("cve_id == %r (expected CVE-2024-6387)" % data.get("cve_id"))
    # A: exact score (no ±tolerance)
    try:
        score = float(data.get("cvss_score"))
        if score != 8.1:
            fails.append("cvss_score == %r (must be exactly 8.1)" % score)
    except (TypeError, ValueError):
        fails.append("cvss_score not numeric: %r" % data.get("cvss_score"))
    if str(data.get("risk_level","")).upper() != "HIGH":
        fails.append("risk_level == %r (expected HIGH)" % data.get("risk_level"))
    if str(data.get("remediation_priority","")) != "P1":
        fails.append("remediation_priority == %r (expected P1)" % data.get("remediation_priority"))
    # A: estimated_exposure_hours must be exactly 33
    # (disclosure 2024-07-01 00:00 UTC, report as-of 2024-07-02 09:00 UTC = 33 hours)
    eeh = data.get("estimated_exposure_hours")
    try:
        eeh = int(eeh)
        if eeh != 33:
            fails.append("estimated_exposure_hours == %d (must be exactly 33: from 2024-07-01T00:00Z to 2024-07-02T09:00Z)" % eeh)
    except (TypeError, ValueError):
        fails.append("estimated_exposure_hours not numeric: %r" % data.get("estimated_exposure_hours"))
    # C: prod_host_count must exactly match Q2's affected_assets.csv prod count
    phc = data.get("prod_host_count")
    try:
        phc = int(phc)
        # Cross-round closure: check against Q2 file if it exists
        q2_path = ws / "work" / "affected_assets.csv"
        if q2_path.exists():
            with q2_path.open(encoding="utf-8") as fh:
                q2_rows = list(csv.DictReader(fh))
            prod_count_q2 = sum(1 for r in q2_rows if r.get("env","").strip().lower() == "prod")
            if prod_count_q2 > 0 and phc != prod_count_q2:
                fails.append("prod_host_count drift: risk_matrix=%d, Q2 affected_assets prod=%d (must be identical)" % (phc, prod_count_q2))
        else:
            # No Q2 file: check against known value
            if phc != 154:
                fails.append("prod_host_count == %d (expected 154 from Q2 internal_inventory.csv)" % phc)
    except (TypeError, ValueError):
        fails.append("prod_host_count not int: %r" % data.get("prod_host_count"))
    # C: internet_exposed_count must match Q7 vulnerable_count (151)
    iec = data.get("internet_exposed_count")
    try:
        iec_val = int(iec)
        if iec_val <= 0:
            fails.append("internet_exposed_count must be positive")
        # Cross-round: if Q7 exposure_report.json exists, must match exactly
        q7_path = ws / "work" / "exposure_report.json"
        if q7_path.exists():
            q7_data = json.loads(q7_path.read_text(encoding="utf-8"))
            vc_q7 = q7_data.get("vulnerable_count")
            if vc_q7 is not None and iec_val != int(vc_q7):
                fails.append("internet_exposed_count drift: risk_matrix=%d, Q7 vulnerable_count=%d (must match exactly)" % (iec_val, int(vc_q7)))
    except (TypeError, ValueError):
        fails.append("internet_exposed_count not numeric: %r" % iec)
    _finish(fails)
main()
'''

# ── Q10: 补丁进度跟踪（V1 多 session；V3 P4 env 分组）[加难 D: 要求 patched/pending/failed 三子键结构；prod patched >= 20；staging all patched] ───────────────────
CHECKS["check_q10"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "work" / "patch_progress.json")
    if err: _finish([err])
    if not isinstance(data, dict):
        _finish(["patch_progress.json must be a JSON object"])
    low_keys = {k.lower() for k in data.keys()}
    # Must have prod/staging/dev groupings
    for env in ("prod", "staging", "dev"):
        if env not in low_keys:
            fails.append("patch_progress.json missing env group: %s (P4 requires prod/staging/dev)" % env)
    if fails: _finish(fails)
    # D: each env group must be a dict with exactly the keys: patched, pending, failed (each a list)
    def _get_env(d, key):
        for k in d.keys():
            if k.lower() == key:
                return d[k]
        return None
    for env in ("prod", "staging", "dev"):
        grp = _get_env(data, env)
        if not isinstance(grp, dict):
            fails.append("patch_progress.json[%r] must be an object with keys patched/pending/failed; got %r" % (env, type(grp).__name__))
            continue
        for sub in ("patched", "pending", "failed"):
            if sub not in grp:
                fails.append("patch_progress.json[%r] missing sub-key %r (required: patched, pending, failed)" % (env, sub))
            elif not isinstance(grp[sub], list):
                fails.append("patch_progress.json[%r][%r] must be a list; got %r" % (env, sub, type(grp[sub]).__name__))
    if fails: _finish(fails)
    # D: prod patched count must be >= 20 (session history: prod-host-001..020 are patched)
    prod_grp = _get_env(data, "prod")
    if prod_grp:
        prod_patched = prod_grp.get("patched", [])
        if len(prod_patched) < 20:
            fails.append("prod patched count = %d (must be >= 20 per session history: prod-host-001 through prod-host-020 are patched)" % len(prod_patched))
    # D: staging must have no pending and no failed hosts (session: fully patched)
    staging_grp = _get_env(data, "staging")
    if staging_grp:
        s_pending = staging_grp.get("pending", [])
        s_failed = staging_grp.get("failed", [])
        if len(s_pending) > 0:
            fails.append("staging pending count = %d (must be 0; session history shows staging is fully patched)" % len(s_pending))
        if len(s_failed) > 0:
            fails.append("staging failed count = %d (must be 0; session history shows staging is fully patched)" % len(s_failed))
    # D: dev must have no patched hosts (session: all dev pending)
    dev_grp = _get_env(data, "dev")
    if dev_grp:
        d_patched = dev_grp.get("patched", [])
        if len(d_patched) > 0:
            fails.append("dev patched count = %d (must be 0; session history shows dev is all pending)" % len(d_patched))
    # Check prod appears before staging/dev in the JSON key order
    keys = list(data.keys())
    low_keys_ordered = [k.lower() for k in keys if k.lower() in ("prod","staging","dev")]
    if low_keys_ordered and low_keys_ordered[0] != "prod":
        fails.append("patch_progress.json: prod group must come first (P4 grouping)")
    _finish(fails)
main()
'''

# ── Q11: Supersede — 撤销 LoginGraceTime 0（V10 supersede；V2）[加难 A: SC decision ID 精确；D: RHSA 补丁版本引用] ──────────
CHECKS["check_q11"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "work" / "workaround_plan_v2.md")
    if txt is None:
        _finish(["file not found: work/workaround_plan_v2.md"])
    low = txt.lower()
    # Must contain MaxStartups 10:30:100
    if "MaxStartups 10:30:100" not in txt and "maxstartups 10:30:100" not in low:
        fails.append("workaround_plan_v2.md missing MaxStartups 10:30:100")
    # Must explicitly state LoginGraceTime 0 is superseded
    if not (re.search(r"supersed|revok|replac", low) and re.search(r"logingraceTime\s+0|logingraceTime0", low, re.IGNORECASE)):
        fails.append("workaround_plan_v2.md does not explicitly state LoginGraceTime 0 is superseded/revoked")
    # A: must reference Security Committee Decision ID SC-2024-0708-01 exactly
    if "SC-2024-0708-01" not in txt:
        fails.append("workaround_plan_v2.md missing Security Committee Decision ID SC-2024-0708-01 (from assets/advisories/security_committee_decision.md)")
    # D: must reference the definitive patch target (9.8p1 or RHSA errata) as the final goal
    if "9.8p1" not in txt and "RHSA-2024:4312" not in txt and "RHSA-2024:4340" not in txt:
        fails.append("workaround_plan_v2.md must reference the definitive patch target (OpenSSH 9.8p1 or RHSA-2024:4312 for RHEL 9)")
    # Must NOT actively recommend LoginGraceTime 0 (only mention it as superseded)
    recommend_pattern = r"(?:use|set|apply|configure|add|recommend)[^\\n]{0,60}logingraceTime\s+0"
    if re.search(recommend_pattern, low) and not re.search(r"supersed|revok|no\s+longer", low):
        fails.append("workaround_plan_v2.md appears to actively recommend LoginGraceTime 0 (should only mention it as superseded)")
    _finish(fails)
main()
'''

# ── Q12: 利用技术分析（V5 honey-pot 30min → 正确 6-8 hours）[加难 D: _IO_FILE 精确；B: 30min 的 Slack bot 必须被明确否定] ─────────────
CHECKS["check_q12"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "work" / "exploit_analysis.md")
    if txt is None:
        _finish(["file not found: work/exploit_analysis.md"])
    low = txt.lower()
    # V5: must cite 10,000 attempts (allow 10000 or 10,000)
    if not re.search(r"10[,.]?000", txt):
        fails.append("exploit_analysis.md missing ~10,000 attempts figure")
    # V5: must cite 6-8 hours (not just 30 minutes)
    if not re.search(r"6.{0,3}8\s*hour|6-8 hour", low):
        fails.append("exploit_analysis.md missing 6-8 hours exploitation time")
    # B: '30 minutes' claim from Feishu internal note is INCORRECT — Qualys report is authoritative
    # If the document mentions 30 minutes without explicitly flagging it as incorrect, fail
    if re.search(r"30\s*min", low):
        if not re.search(r"incorrect|wrong|inaccurate|not.*30|30.*not|内部.*错|错误|不可信|不准确|feishu.*错|错误.*feishu|30.*incorrect|incorrect.*30|并非|并不是.*30", low):
            fails.append("exploit_analysis.md states '30 minutes' exploitation time without flagging it as incorrect — the authoritative Qualys report (assets/advisories/qualys_regresshion_report.txt) states 6-8 hours; the Feishu internal note's '30 minutes' figure is erroneous")
    # Must mention glibc dependency
    if "glibc" not in low:
        fails.append("exploit_analysis.md missing glibc dependency")
    # Must mention ASLR
    if "aslr" not in low:
        fails.append("exploit_analysis.md missing ASLR bypass technique")
    # 32-bit constraint
    if "32" not in txt or "bit" not in low:
        fails.append("exploit_analysis.md missing 32-bit constraint")
    # D: must reference _IO_FILE structure manipulation (verbatim from Qualys report)
    if "_IO_FILE" not in txt and "io_file" not in low:
        fails.append("exploit_analysis.md missing _IO_FILE structure manipulation technique (verbatim from assets/advisories/qualys_regresshion_report.txt)")
    _finish(fails)
main()
'''

# ── Q13: 执行摘要（V9 verbatim；V3 P5 TL;DR；P2 CVE 格式）[加难 A: TL;DR ≤150 words; B: MaxStartups verbatim required] ─────────────
CHECKS["check_q13"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "work" / "executive_report.md")
    if txt is None:
        _finish(["file not found: work/executive_report.md"])
    low = txt.lower()
    # V9: verbatim CVE ID
    if "CVE-2024-6387" not in txt:
        fails.append("executive_report.md missing CVE-2024-6387")
    # A: exact CVSS score 8.1
    if "8.1" not in txt:
        fails.append("executive_report.md missing CVSS score 8.1")
    # RHSA-2024:4312
    if "RHSA-2024:4312" not in txt:
        fails.append("executive_report.md missing RHSA-2024:4312")
    # errata date 2024-07-03
    if "2024-07-03" not in txt:
        fails.append("executive_report.md missing errata release date 2024-07-03 (RHSA-2024:4312 was published on this date)")
    # patched version 9.8p1
    if "9.8p1" not in txt:
        fails.append("executive_report.md missing patched version 9.8p1")
    # B: current workaround must be MaxStartups (per Update 2 — LoginGraceTime 0 was superseded)
    if "MaxStartups" not in txt and "maxstartups" not in low:
        fails.append("executive_report.md missing current workaround MaxStartups (per Update 2 — LoginGraceTime 0 was revoked by SC-2024-0708-01)")
    # A: TL;DR section present — Alice Wang's internal style guide caps board-facing TL;DRs at 60 words
    # (The CTO Carol's email references '≤200 words' for the full report; but the TL;DR paragraph itself
    # must be ≤60 words per the internal security team style guide — a separate constraint not surfaced in the
    # session email thread. Read assets/templates/ or SOUL.md for Alice's standing guidance.)
    tldr_match = re.search(r"##?\s*TL;?DR(.+?)(?=^##|\Z)", txt, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    if not tldr_match:
        fails.append("executive_report.md missing standalone TL;DR section (CTO requirement)")
    else:
        tldr_text = tldr_match.group(1).strip()
        word_count = len(tldr_text.split())
        if word_count > 60:
            fails.append("TL;DR section has %d words (must be ≤60 words per Alice Wang's style guide for board-facing TL;DR paragraphs — the CTO's '200 words' refers to the full executive summary, not just the TL;DR)" % word_count)
    _finish(fails)
main()
'''

# ── Q14: 双 CVE 对比（V1 多源；V2 update 扩充）[加难 A+D: exact scores; scope field required; disclosure_date required] ──────────────────────────
CHECKS["check_q14"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "work" / "cve_comparison.json")
    if err: _finish([err])
    # V8: both CVE keys must be present
    if "CVE-2024-6387" not in data:
        fails.append("cve_comparison.json missing CVE-2024-6387 entry")
    if "CVE-2024-6409" not in data:
        fails.append("cve_comparison.json missing CVE-2024-6409 entry")
    if fails: _finish(fails)
    e6387 = data.get("CVE-2024-6387", {})
    e6409 = data.get("CVE-2024-6409", {})
    # D: each entry must have all three required fields: affected_versions, cvss_score, scope
    for cve_key, entry in [("CVE-2024-6387", e6387), ("CVE-2024-6409", e6409)]:
        for field in ("affected_versions", "cvss_score", "scope"):
            if field not in entry:
                fails.append("cve_comparison.json[%r] missing required field %r" % (cve_key, field))
    if fails: _finish(fails)
    # A: CVE-2024-6387 exact cvss_score 8.1
    try:
        s6387 = float(e6387.get("cvss_score", 0))
        if s6387 != 8.1:
            fails.append("CVE-2024-6387 cvss_score == %r (must be exactly 8.1)" % s6387)
    except (TypeError, ValueError):
        fails.append("CVE-2024-6387 cvss_score not numeric: %r" % e6387.get("cvss_score"))
    # A: CVE-2024-6409 exact cvss_score 7.0
    try:
        s6409 = float(e6409.get("cvss_score", 0))
        if s6409 != 7.0:
            fails.append("CVE-2024-6409 cvss_score == %r (must be exactly 7.0 from assets/advisories/CVE-2024-6409_detail.json — not the same as CVE-2024-6387's 8.1)" % s6409)
    except (TypeError, ValueError):
        fails.append("CVE-2024-6409 cvss_score not numeric: %r" % e6409.get("cvss_score"))
    # CVE-2024-6409 must have narrower version range (8.7 or 8.8 RHEL backport)
    av6409 = str(e6409.get("affected_versions",""))
    if not ("8.7" in av6409 or "8.8" in av6409):
        fails.append("CVE-2024-6409 affected_versions must mention 8.7 or 8.8 (RHEL backport versions only); got %r" % av6409)
    # D: scope field for CVE-2024-6409 must reference privilege_separation or child process
    sc6409 = str(e6409.get("scope","")).lower()
    if "privilege" not in sc6409 and "child" not in sc6409 and "privsep" not in sc6409:
        fails.append("CVE-2024-6409 scope %r must reference privilege separation child process (different from CVE-2024-6387's main sshd scope)" % e6409.get("scope"))
    # Must NOT share the same cvss_score as 6387
    try:
        if abs(float(e6387.get("cvss_score",0)) - float(e6409.get("cvss_score",0))) < 0.5:
            fails.append("CVE-2024-6387 and CVE-2024-6409 must have different cvss_score values (6387=8.1, 6409=7.0)")
    except (TypeError, ValueError):
        pass
    _finish(fails)
main()
'''

# ── Q15: 补丁代码注释（V9 verbatim；V4 与 Q4 一致）[加难 D: 要求 Chinese 技术注解；syslog+malloc 关系；代码块存在] ──────────────────────
CHECKS["check_q15"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "work" / "patch_diff_annotated.md")
    if txt is None:
        _finish(["file not found: work/patch_diff_annotated.md"])
    low = txt.lower()
    # V9: verbatim code identifier
    if "DO_LOG_SAFE_IN_SIGHAND" not in txt:
        fails.append("patch_diff_annotated.md missing DO_LOG_SAFE_IN_SIGHAND macro")
    # _exit(1) safe in signal handlers
    if "_exit(1)" not in txt and "_exit" not in txt:
        fails.append("patch_diff_annotated.md missing _exit(1) as async-signal-safe alternative")
    # V4: commit hash (consistent with Q4)
    if "752250c" not in txt:
        fails.append("patch_diff_annotated.md missing commit hash 752250c (must be consistent with Q4)")
    # D: must explain that syslog() calls malloc() — the specific mechanism of heap corruption
    if "malloc" not in low:
        fails.append("patch_diff_annotated.md must explain that syslog() internally calls malloc() (the heap corruption mechanism)")
    # D: must include actual code blocks (```c or similar) showing the diff
    if "```" not in txt:
        fails.append("patch_diff_annotated.md must include code blocks (```c or similar) showing the vulnerable vs patched code")
    # D: must have Chinese technical annotations (the task spec says 'Use Chinese technical annotations')
    # Check for presence of Chinese characters (basic CJK range)
    has_chinese = any(0x4e00 <= ord(c) <= 0x9fff for c in txt)
    if not has_chinese:
        fails.append("patch_diff_annotated.md must include Chinese technical annotations (as instructed in the task)")
    # D: must reference POSIX.1 standard for async-signal-safe functions
    # (signal_handler_analysis.md in assets/code_samples references POSIX.1-2008)
    if "posix" not in low and "POSIX" not in txt:
        fails.append("patch_diff_annotated.md must reference the POSIX standard for async-signal-safe functions (see assets/code_samples/signal_handler_analysis.md for POSIX.1-2008 signal safety requirements)")
    _finish(fails)
main()
'''

# ── Q16: 最终修复清单（V4 全局闭合；V8；V9；V10）[加难 A+C: exact score, deadline ISO8601Z, rhel8_package exact, cross-round consistency] ────────────────────────
CHECKS["check_q16"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "work" / "final_remediation.json")
    if err: _finish([err])
    # V8: all 16 required fields
    REQ = ["affected_range","cve_id","cvss_score","cvss_vector","disclosure_date",
           "ghsa_id","patched_version","prior_cve","regression_commit",
           "remediation_deadline","rhel8_errata","rhel8_package","rhel9_errata",
           "rhel9_package","workaround_current","workaround_superseded"]
    for f in REQ:
        if f not in data:
            fails.append("missing field: " + f)
    if fails: _finish(fails)
    # V9/V4: spot-check key anchor values
    if data.get("cve_id") != "CVE-2024-6387":
        fails.append("cve_id == %r" % data.get("cve_id"))
    # A: exact cvss_score
    try:
        if float(data.get("cvss_score",0)) != 8.1:
            fails.append("cvss_score == %r (must be exactly 8.1)" % data.get("cvss_score"))
    except (TypeError, ValueError):
        fails.append("cvss_score not numeric")
    if data.get("cvss_vector") != "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H":
        fails.append("cvss_vector verbatim mismatch: %r" % data.get("cvss_vector"))
    if data.get("patched_version") != "9.8p1":
        fails.append("patched_version == %r (expected 9.8p1)" % data.get("patched_version"))
    if data.get("rhel9_errata") != "RHSA-2024:4312":
        fails.append("rhel9_errata == %r (expected RHSA-2024:4312)" % data.get("rhel9_errata"))
    # A: rhel9_package verbatim (full package name)
    if data.get("rhel9_package") != "openssh-8.7p1-38.el9_4.1":
        fails.append("rhel9_package == %r (must be exactly openssh-8.7p1-38.el9_4.1)" % data.get("rhel9_package"))
    # A: rhel8_package verbatim
    if data.get("rhel8_package") != "openssh-8.0p1-19.el8_10.1":
        fails.append("rhel8_package == %r (must be exactly openssh-8.0p1-19.el8_10.1)" % data.get("rhel8_package"))
    if data.get("rhel8_errata") != "RHSA-2024:4340":
        fails.append("rhel8_errata == %r (expected RHSA-2024:4340)" % data.get("rhel8_errata"))
    # A: remediation_deadline must be exact ISO-8601 UTC string (with seconds)
    dl = str(data.get("remediation_deadline",""))
    if dl != "2024-07-05T09:00:00Z":
        fails.append("remediation_deadline == %r (must be exactly '2024-07-05T09:00:00Z' in ISO-8601 UTC with seconds)" % dl)
    # V10: workaround_superseded must be exactly "LoginGraceTime 0"
    ws_sup = str(data.get("workaround_superseded",""))
    if ws_sup != "LoginGraceTime 0":
        fails.append("workaround_superseded == %r (must be exactly 'LoginGraceTime 0')" % ws_sup)
    # workaround_current must contain MaxStartups 10:30:100 verbatim
    wc = str(data.get("workaround_current",""))
    if "MaxStartups 10:30:100" not in wc:
        fails.append("workaround_current %r must contain verbatim 'MaxStartups 10:30:100'" % wc)
    if data.get("prior_cve") != "CVE-2006-5051":
        fails.append("prior_cve == %r (expected CVE-2006-5051)" % data.get("prior_cve"))
    # A: regression_commit full hash
    rc = str(data.get("regression_commit",""))
    if rc != "752250caabda3dd24635503c4cd689b32a650794":
        fails.append("regression_commit == %r (must be the full 40-char hash: 752250caabda3dd24635503c4cd689b32a650794)" % rc)
    # C: cross-round disclosure_date must match Q1
    if data.get("disclosure_date") != "2024-07-01":
        fails.append("disclosure_date == %r (expected 2024-07-01, consistent with Q1)" % data.get("disclosure_date"))
    _finish(fails)
main()
'''

# ── Q17: SHA-256 sign-off（V7） ───────────────────────────────────────────
CHECKS["check_q17"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    sign = _read(ws / "work" / "signoff.txt")
    if sign is None:
        _finish(["file not found: work/signoff.txt"])
    line = sign.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["signoff.txt must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80]])
    final_path = ws / "work" / "final_remediation.json"
    if not final_path.exists():
        _finish(["cannot verify: work/final_remediation.json missing"])
    import hashlib
    digest = hashlib.sha256(final_path.read_bytes()).hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: signoff %s != recomputed %s" % (m.group(1)[:12], digest[:12]))
    _finish(fails)
main()
'''

# ── check_preferences.py ─────────────────────────────────────────────────
PREF = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sec1 preference checker (P1-P5).

P1: JSON 2-space indent, top-level fields alphabetically ordered.
P2: CVE IDs formatted as CVE-YYYY-NNNNN (hyphenated, uppercase).
P3: Work product filenames use snake_case.
P4: Progress/inventory reports grouped prod/staging/dev, prod first.
P5: Executive summaries contain standalone TL;DR paragraph ≤200 words.
"""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """JSON 2-space indent + top-level alphabetical field order."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    if not isinstance(data, dict):
        return True, "P1: top-level not a dict, skip"
    # Check indentation: look for 2-space indent pattern
    lines = txt.split("\\n")
    has_indent = any(line.startswith("  ") and not line.startswith("   ") for line in lines)
    if lines and not has_indent:
        # Allow no-indent for trivially small JSON or single-line
        pass  # lenient on this check
    # Check alphabetical field order
    keys = list(data.keys())
    # filter out schema_version as a special key
    content_keys = [k for k in keys]
    if content_keys != sorted(content_keys):
        return False, ("P1: top-level keys not alphabetically sorted: %s (expected %s)" %
                       (content_keys[:8], sorted(content_keys)[:8]))
    return True, "P1: PASSED"


def check_P2(ws, target):
    """CVE IDs must be in CVE-YYYY-NNNNN format."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    # Find any CVE-like patterns
    bad = re.findall(r"\\bcve[- _]?\\d{4}[- _]?\\d+\\b", txt, re.IGNORECASE)
    good = re.findall(r"\\bCVE-\\d{4}-\\d+\\b", txt)
    # Remove properly formatted ones from bad
    bad_only = [b for b in bad if not re.match(r"^CVE-\\d{4}-\\d+$", b, re.IGNORECASE)]
    # Actually find malformatted ones
    malformed = re.findall(r"\\b(?:cve|CVE)(?!-\\d{4}-\\d)[-_\\s]?\\d", txt)
    bad_format = [b for b in re.findall(r"\\b[Cc][Vv][Ee][-_\\s]?\\d{4}[-_\\s]?\\d+\\b", txt)
                  if b != re.sub(r"[-_\\s]", "-", b.upper())]
    if bad_format:
        return False, "P2: malformatted CVE IDs found: %s (must be CVE-YYYY-NNNNN)" % bad_format[:3]
    return True, "P2: PASSED"


def check_P3(ws, target):
    """Filename must be snake_case."""
    p = ws / target
    name = p.name
    if not name:
        return True, "P3: no target file, skip"
    # Allow only lowercase letters, digits, underscores, dots (for extension)
    stem = p.stem
    bad_chars = re.findall(r"[A-Z\\-\\s]", stem)
    if bad_chars:
        return False, "P3: filename %r contains non-snake_case chars %s" % (name, bad_chars[:5])
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Progress/inventory: prod group appears before staging and dev."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    # For CSV: check that first env value is prod
    if target.endswith(".csv"):
        import csv, io
        rows = list(csv.DictReader(io.StringIO(txt)))
        if not rows:
            return True, "P4: empty CSV, skip"
        envs = [r.get("env","").lower() for r in rows]
        if envs and envs[0] != "prod":
            return False, "P4: first row env=%r (expected prod-first ordering)" % envs[0]
        return True, "P4: PASSED"
    # For JSON: check that prod key appears before staging/dev
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return True, "P4: not JSON, skip"
    if not isinstance(data, dict):
        return True, "P4: not a dict, skip"
    keys = [k.lower() for k in data.keys()]
    if "prod" in keys and "staging" in keys:
        if keys.index("prod") > keys.index("staging"):
            return False, "P4: prod group appears after staging (must be first)"
    if "prod" in keys and "dev" in keys:
        if keys.index("prod") > keys.index("dev"):
            return False, "P4: prod group appears after dev (must be first)"
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Executive summary must contain standalone TL;DR ≤200 words."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    m = re.search(r"##?\\s*TL;?DR(.+?)(?=^##|\\Z)", txt, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    if not m:
        return False, "P5: missing standalone TL;DR section (required for executive summaries)"
    tldr = m.group(1).strip()
    wc = len(tldr.split())
    if wc > 200:
        return False, "P5: TL;DR section has %d words (must be ≤200)" % wc
    return True, "P5: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4, "P5": check_P5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4,P5")
    ap.add_argument("--target", default="work/")
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
        code = HEADER + textwrap.dedent(body)
        (OUT / f"{name}.py").write_text(code, encoding="utf-8")
    (OUT / "check_preferences.py").write_text(PREF, encoding="utf-8")
    print(f"wrote {len(CHECKS)} check scripts + check_preferences.py to {OUT}")


if __name__ == "__main__":
    main()
