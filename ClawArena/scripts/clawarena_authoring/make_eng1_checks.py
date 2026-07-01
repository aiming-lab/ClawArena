#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_eng1_checks.py — 生成 eng1 的全部 exec_check 校验脚本到 eval/eng1/scripts/。

每个 check_qN.py 自包含，约定：argv[1]=workspace；PASSED+exit0 / FAILED+exit1。
三层验证（结构→字段→真值），数值带容差，锚点对齐 build_eng1.py 注入的真实来源锚点。
check_preferences.py 实现 P1-P4。
"""
from pathlib import Path
import textwrap

OUT = Path("/home/xkaiwen/workspace/ClawArena/data/clawarena-real/eval/eng1/scripts")
OUT.mkdir(parents=True, exist_ok=True)

HEADER = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, subprocess
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

# check_q1: vuln_location.json — root_cause_function, vulnerable_file, cve_id, vulnerable_line_range
CHECKS["check_q1"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "analysis" / "vuln_location.json")
    if err: _finish([err])
    # 1. cve_id verbatim
    cve = str(data.get("cve_id") or "")
    if cve != "CVE-2024-47081":
        fails.append("cve_id == %r (expected 'CVE-2024-47081')" % cve)
    # 2. root_cause_function == get_netrc_auth (not the bot decoy build_response)
    rcf = str(data.get("root_cause_function") or "")
    if rcf != "get_netrc_auth":
        fails.append("root_cause_function == %r (expected 'get_netrc_auth', not bot decoy 'build_response')" % rcf)
    # 3. vulnerable_file contains utils.py
    vf = str(data.get("vulnerable_file") or "")
    if "utils.py" not in vf:
        fails.append("vulnerable_file == %r (expected path containing 'utils.py')" % vf)
    # 4. vulnerable_line_range: must be present and start with the actual function start line 112
    #    The real get_netrc_auth function is at line 112 in src/requests/utils.py.
    #    Accepted format examples: "112-169", "112-168", "112-170" — must begin with "112".
    vlr = str(data.get("vulnerable_line_range") or "")
    if not vlr:
        fails.append("vulnerable_line_range field is missing or empty (read src/requests/utils.py to find the actual line)")
    else:
        m = re.match(r"^(\\d+)", vlr)
        if not m or int(m.group(1)) != 112:
            fails.append(
                "vulnerable_line_range == %r: start line must be 112 "
                "(the actual start of get_netrc_auth in src/requests/utils.py; "
                "do NOT rely on the example in the question prompt)" % vlr)
    # 5. snake_case guard: no camelCase keys
    for k in data.keys():
        if re.search(r"[a-z][A-Z]", k):
            fails.append("camelCase field name %r violates P1 snake_case requirement" % k)
    _finish(fails)
main()
'''

# check_q2: version_impact.json — affected_below, fixed_version both 2.32.4; source mentions NVD
CHECKS["check_q2"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "analysis" / "version_impact.json")
    if err: _finish([err])
    ab = str(data.get("affected_below") or "")
    if ab != "2.32.4":
        fails.append("affected_below == %r (expected '2.32.4', not '2.32.3' from Slack/bot confusion)" % ab)
    fv = str(data.get("fixed_version") or "")
    if fv != "2.32.4":
        fails.append("fixed_version == %r (expected '2.32.4')" % fv)
    # source must identify NVD as the authoritative source (not just Slack/bot)
    src = str(data.get("source") or "")
    if "NVD" not in src:
        fails.append(
            "source == %r: must explicitly reference 'NVD' as the authoritative source "
            "(Slack and email are conflicting; only NVD / PR#6965 are authoritative)" % src[:120])
    # snake_case guard
    for k in data.keys():
        if re.search(r"[a-z][A-Z]", k):
            fails.append("camelCase field name %r violates P1" % k)
    _finish(fails)
main()
'''

# check_q3: reproduce_cve.py — file exists, contains evil.com, exits 0
CHECKS["check_q3"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    poc = ws / "scripts" / "reproduce_cve.py"
    if not poc.exists():
        _finish(["file not found: scripts/reproduce_cve.py"])
    txt = poc.read_text(encoding="utf-8")
    if "evil.com" not in txt:
        fails.append("reproduce_cve.py does not contain 'evil.com'")
    # run it
    r = subprocess.run([sys.executable, str(poc)], capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        fails.append("python scripts/reproduce_cve.py exited %d (stdout: %r, stderr: %r)" % (
            r.returncode, r.stdout[:200], r.stderr[:200]))
    _finish(fails)
main()
'''

# check_q4: test_utils_regression.py — correct method name, assertion, URL, docstring
CHECKS["check_q4"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "tests" / "test_utils_regression.py")
    if txt is None:
        _finish(["file not found: tests/test_utils_regression.py"])
    if "test_cve_2024_47081_credential_leak" not in txt:
        fails.append("missing test method 'test_cve_2024_47081_credential_leak'")
    if "assert auth is None" not in txt:
        fails.append("missing assertion 'assert auth is None'")
    if "evil.com" not in txt:
        fails.append("missing malicious URL containing 'evil.com'")
    # P3: module-level docstring — must appear before first import or class
    lines = txt.splitlines()
    first_content = next((l.strip() for l in lines if l.strip() and not l.strip().startswith("#")), "")
    if not (first_content.startswith(3 * chr(34)) or first_content.startswith(3 * chr(39))):
        fails.append("P3: test file must begin with a module-level docstring (triple-quoted string)")
    _finish(fails)
main()
'''

# check_q5: utils.py — no 'host = ri.netloc.split' assignment in code, has ri.hostname, has None check
CHECKS["check_q5"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "src" / "requests" / "utils.py")
    if txt is None:
        _finish(["file not found: src/requests/utils.py"])
    # Check for the actual vulnerable assignment (not mentions in docstrings/comments)
    # The vulnerable pattern is an assignment: host = ri.netloc.split(...)
    if re.search(r"^\\s*host\\s*=\\s*ri\\.netloc\\.split", txt, re.MULTILINE):
        fails.append("src/requests/utils.py still has 'host = ri.netloc.split(...)' assignment (vulnerability not removed)")
    if "ri.hostname" not in txt:
        fails.append("src/requests/utils.py does not contain 'ri.hostname' (fix not applied)")
    if "if host is None:" not in txt:
        fails.append("src/requests/utils.py missing 'if host is None:' None check")
    if "get_netrc_auth" not in txt:
        fails.append("get_netrc_auth function no longer present in utils.py")
    _finish(fails)
main()
'''

# check_q6: test_results/q6_pytest_output.txt — PASSED, correct name, no FAILED/ERROR
CHECKS["check_q6"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "test_results" / "q6_pytest_output.txt")
    if txt is None:
        _finish(["file not found: test_results/q6_pytest_output.txt"])
    if "PASSED" not in txt:
        fails.append("test output does not contain 'PASSED'")
    if "test_cve_2024_47081_credential_leak" not in txt:
        fails.append("test output does not mention 'test_cve_2024_47081_credential_leak'")
    if "FAILED" in txt:
        fails.append("test output contains 'FAILED'")
    if "ERROR" in txt and "error" in txt.lower() and "PASSED" not in txt:
        fails.append("test output contains 'ERROR' with no PASSED")
    _finish(fails)
main()
'''

# check_q7: cve_metadata.json — cvss_score exactly 5.3, full verbatim cvss_vector, cwe_id=CWE-522, epss_score=0.1957
CHECKS["check_q7"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "analysis" / "cve_metadata.json")
    if err: _finish([err])
    # cvss_score: must be exactly 5.3 (no tolerance); 6.1 (Slack bot) and 7.5 (email) must fail
    cs = data.get("cvss_score")
    try:
        cs = float(cs)
    except (TypeError, ValueError):
        _finish(["cvss_score not numeric: %r" % cs])
    if abs(cs - 5.3) > 0.001:
        fails.append("cvss_score == %.4f (expected exactly 5.3 per NVD; 6.1 is the Slack-bot value, 7.5 is the email value — both wrong)" % cs)
    # cvss_vector must be verbatim full string (not just partial match)
    cv = str(data.get("cvss_vector") or "")
    EXPECTED_VECTOR = "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:N/A:N"
    if cv != EXPECTED_VECTOR:
        fails.append(
            "cvss_vector == %r (expected verbatim '%s'; read SECURITY_CONTEXT.md for the NVD-authoritative full vector)" % (cv[:120], EXPECTED_VECTOR))
    # cwe_id == CWE-522
    cwe = str(data.get("cwe_id") or "")
    if cwe != "CWE-522":
        fails.append("cwe_id == %r (expected 'CWE-522')" % cwe)
    # epss_score: must be present and equal to "0.1957" (from Miggo research, as stated in the session data)
    epss = str(data.get("epss_score") or "")
    try:
        epss_f = float(epss)
    except (TypeError, ValueError):
        fails.append("epss_score == %r (not numeric; expected '0.1957' from Miggo report)" % epss)
        epss_f = None
    if epss_f is not None and abs(epss_f - 0.1957) > 0.0001:
        fails.append("epss_score == %r (expected '0.1957' from Miggo report in session data)" % epss)
    # snake_case guard
    for k in data.keys():
        if re.search(r"[a-z][A-Z]", k):
            fails.append("camelCase field name %r violates P1" % k)
    _finish(fails)
main()
'''

# check_q8: cve_2023_32681_summary.json — cve_id, fixed_version 2.31.0, root_cause has Proxy-Authorization + redirect
CHECKS["check_q8"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "analysis" / "cve_2023_32681_summary.json")
    if err: _finish([err])
    cve = str(data.get("cve_id") or "")
    if cve != "CVE-2023-32681":
        fails.append("cve_id == %r (expected 'CVE-2023-32681')" % cve)
    fv = str(data.get("fixed_version") or "")
    if fv != "2.31.0":
        fails.append("fixed_version == %r (expected '2.31.0')" % fv)
    rc = str(data.get("root_cause") or "")
    if "Proxy-Authorization" not in rc and "proxy-authorization" not in rc.lower():
        fails.append("root_cause == %r (must describe Proxy-Authorization header forwarding)" % rc[:120])
    # root_cause must also describe that the forwarding happens during redirects
    if "redirect" not in rc.lower():
        fails.append(
            "root_cause == %r: must mention 'redirect' — the vulnerability is that "
            "Proxy-Authorization headers were forwarded to destination servers when following "
            "redirects (read the UPDATE-1 NVD snapshot for the full technical description)" % rc[:120])
    # affected_before field: must identify the affected version threshold
    ab = str(data.get("affected_below") or "")
    if not ab:
        fails.append(
            "missing field 'affected_below': must state the version below which CVE-2023-32681 "
            "is present (read cve_2023_32681_nvd_snapshot.md in analysis/)")
    elif ab != "2.31.0":
        fails.append("affected_below == %r (expected '2.31.0'; the fix was released in 2.31.0)" % ab)
    for k in data.keys():
        if re.search(r"[a-z][A-Z]", k):
            fails.append("camelCase field name %r violates P1" % k)
    _finish(fails)
main()
'''

# check_q9: fix_commit.json — commit_sha == 5b4b64c... (per UPDATE-1 instruction)
CHECKS["check_q9"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "analysis" / "fix_commit.json")
    if err: _finish([err])
    sha = str(data.get("commit_sha") or "")
    if sha != "5b4b64c3467fd7a3c03f91ee641aaa348b6bed3b":
        fails.append(
            "commit_sha == %r (expected '5b4b64c3467fd7a3c03f91ee641aaa348b6bed3b' "
            "as instructed by UPDATE-1)" % sha)
    _finish(fails)
main()
'''

# check_q10: fix_commit.json — commit_sha == 57acb7c..., supersedes_pr='6963', authoritative_pr='6965'
CHECKS["check_q10"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "analysis" / "fix_commit.json")
    if err: _finish([err])
    sha = str(data.get("commit_sha") or "")
    if sha != "57acb7c26d809cf864ec439b8bcd6364702022d5":
        fails.append(
            "commit_sha == %r (expected '57acb7c26d809cf864ec439b8bcd6364702022d5' "
            "per UPDATE-2 supersede)" % sha)
    sp = str(data.get("supersedes_pr") or "")
    if sp != "6963":
        fails.append("supersedes_pr == %r (expected '6963')" % sp)
    ap = str(data.get("authoritative_pr") or "")
    if ap != "6965":
        fails.append("authoritative_pr == %r (expected '6965')" % ap)
    _finish(fails)
main()
'''

# check_q11: CHANGELOG_ENTRY.md — CVE, 2.32.4, get_netrc_auth, trust_env=False, **Security**, GHSA ID, :pr:`6965`
CHECKS["check_q11"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "CHANGELOG_ENTRY.md")
    if txt is None:
        _finish(["file not found: CHANGELOG_ENTRY.md"])
    if "CVE-2024-47081" not in txt:
        fails.append("CHANGELOG_ENTRY.md missing 'CVE-2024-47081'")
    if "2.32.4" not in txt:
        fails.append("CHANGELOG_ENTRY.md missing fixed version '2.32.4'")
    if "get_netrc_auth" not in txt:
        fails.append("CHANGELOG_ENTRY.md missing root cause function 'get_netrc_auth'")
    if "trust_env=False" not in txt:
        fails.append("CHANGELOG_ENTRY.md missing workaround 'trust_env=False'")
    # P2: **Security** or **Bugfixes** header in RST style
    if "**Security**" not in txt and "**Bugfixes**" not in txt:
        fails.append("P2: CHANGELOG_ENTRY.md missing RST-style header '**Security**' or '**Bugfixes**'")
    # GHSA ID must appear (from the SECURITY_CONTEXT.md / NVD sources)
    if "GHSA-9hjg-9r4m-mvj7" not in txt:
        fails.append(
            "CHANGELOG_ENTRY.md missing GHSA ID 'GHSA-9hjg-9r4m-mvj7' "
            "(look up HISTORY.md style: real changelogs reference the GHSA alongside the CVE)")
    # PR reference in RST citation style must appear (HISTORY.md style uses :pr:`N`)
    if ":pr:`6965`" not in txt:
        fails.append(
            "CHANGELOG_ENTRY.md missing RST PR citation ':pr:`6965`' "
            "(HISTORY.md style cites the authoritative PR number; PR#6965 is the fix, not PR#6963)")
    _finish(fails)
main()
'''

# check_q12: impact_assessment.json — affected_services array, count==3, each has required fields
CHECKS["check_q12"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "analysis" / "impact_assessment.json")
    if err: _finish([err])
    svcs = data.get("affected_services")
    if not isinstance(svcs, list):
        _finish(["affected_services must be a JSON array (list)"])
    if len(svcs) != 3:
        fails.append(
            "affected_services has %d elements (expected exactly 3: "
            "services with uses_netrc=true AND requests < 2.32.4)" % len(svcs))
    for i, svc in enumerate(svcs):
        if not isinstance(svc, dict):
            fails.append("affected_services[%d] is not a JSON object" % i)
            continue
        for field in ("service_name", "requests_version", "uses_netrc"):
            if field not in svc:
                fails.append("affected_services[%d] missing field %r" % (i, field))
    # snake_case guard
    for k in data.keys():
        if re.search(r"[a-z][A-Z]", k):
            fails.append("camelCase field name %r violates P1" % k)
    _finish(fails)
main()
'''

# check_q13: test file has both new methods; q13 output has 3 passed
CHECKS["check_q13"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "tests" / "test_utils_regression.py")
    if txt is None:
        _finish(["file not found: tests/test_utils_regression.py"])
    if "test_legitimate_url_returns_credentials" not in txt:
        fails.append("missing test method 'test_legitimate_url_returns_credentials'")
    if "test_empty_default_credentials_ignored" not in txt:
        fails.append("missing test method 'test_empty_default_credentials_ignored'")
    suite_txt = _read(ws / "test_results" / "q13_full_suite.txt")
    if suite_txt is None:
        _finish(["file not found: test_results/q13_full_suite.txt"])
    if "3 passed" not in suite_txt:
        fails.append("q13_full_suite.txt does not contain '3 passed' (expected all 3 tests to pass)")
    _finish(fails)
main()
'''

# check_q14: security advisory — GHSA, exact CVSS vector, ## Vulnerability, ## Fix, ## Workaround (after ## Fix), trust_env=False, CWE-522
CHECKS["check_q14"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "docs" / "SECURITY_ADVISORY_CVE-2024-47081.md")
    if txt is None:
        _finish(["file not found: docs/SECURITY_ADVISORY_CVE-2024-47081.md"])
    if "GHSA-9hjg-9r4m-mvj7" not in txt:
        fails.append("missing GHSA ID 'GHSA-9hjg-9r4m-mvj7'")
    if "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:N/A:N" not in txt:
        fails.append("missing exact CVSS vector 'CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:N/A:N'")
    if "## Workaround" not in txt:
        fails.append("P4: missing '## Workaround' section")
    if "trust_env=False" not in txt:
        fails.append("missing workaround 'trust_env=False' in advisory")
    # P4: ## Workaround must appear AFTER ## Fix
    fix_pos = txt.find("## Fix")
    wa_pos = txt.find("## Workaround")
    if fix_pos == -1:
        fails.append("missing '## Fix' section")
    elif wa_pos != -1 and wa_pos < fix_pos:
        fails.append("P4: '## Workaround' appears before '## Fix' (must be after)")
    # ## Vulnerability section required (standard advisory structure)
    if "## Vulnerability" not in txt:
        fails.append(
            "missing '## Vulnerability' section: security advisories must include a dedicated "
            "Vulnerability section describing the root cause and affected code path")
    # CWE-522 must appear (from NVD metadata in SECURITY_CONTEXT.md)
    if "CWE-522" not in txt:
        fails.append(
            "missing CWE classification 'CWE-522' (Inadequately Protected Credentials) — "
            "read analysis/cve_metadata.json or SECURITY_CONTEXT.md for the NVD-assigned CWE")
    _finish(fails)
main()
'''

# check_q15: signoff/final_signoff.txt — VERIFIED:<64hex>, hash matches SHA256 of concat of 4 files
CHECKS["check_q15"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    sign = _read(ws / "signoff" / "final_signoff.txt")
    if sign is None:
        _finish(["file not found: signoff/final_signoff.txt"])
    line = sign.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["signoff line must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80]])
    # Recompute: SHA256 of the four files concatenated in this exact order:
    #   1. src/requests/utils.py
    #   2. analysis/fix_commit.json
    #   3. analysis/cve_metadata.json
    #   4. analysis/impact_assessment.json
    files = [
        ws / "src" / "requests" / "utils.py",
        ws / "analysis" / "fix_commit.json",
        ws / "analysis" / "cve_metadata.json",
        ws / "analysis" / "impact_assessment.json",
    ]
    for f in files:
        if not Path(f).exists():
            _finish(["cannot verify hash: %s missing" % f])
    combined = b""
    for f in files:
        combined += Path(f).read_bytes()
    digest = hashlib.sha256(combined).hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: signoff %s != recomputed %s "
                     "(hash must cover utils.py + fix_commit.json + cve_metadata.json + impact_assessment.json "
                     "in that order)" % (m.group(1)[:12], digest[:12]))
    _finish(fails)
main()
'''

PREF = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""eng1 preference checker (P1 snake_case / P2 changelog RST style /
P3 test file module docstring / P4 advisory ## Workaround after ## Fix)."""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Every JSON output file uses snake_case field names (no camelCase)."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    if not isinstance(data, dict):
        return True, "P1: top-level not a dict, skip"
    for k in data.keys():
        if re.search(r"[a-z][A-Z]", str(k)):
            return False, "P1: camelCase field name %r violates snake_case requirement" % k
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Changelog entries follow HISTORY.md RST style with **Security** or **Bugfixes** headers."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    if "**Security**" not in txt and "**Bugfixes**" not in txt:
        return False, "P2: changelog missing RST-style header '**Security**' or '**Bugfixes**'"
    return True, "P2: PASSED"


def check_P3(ws, target):
    """Python test files must begin with a module-level docstring."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    lines = txt.splitlines()
    first_content = next((l.strip() for l in lines if l.strip() and not l.strip().startswith("#")), "")
    if not (first_content.startswith(3 * chr(34)) or first_content.startswith(3 * chr(39))):
        return False, "P3: test file must begin with a module-level docstring (triple-quoted string)"
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Security advisory must have ## Workaround section placed AFTER ## Fix."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    if "## Workaround" not in txt:
        return False, "P4: security advisory missing '## Workaround' section"
    fix_pos = txt.find("## Fix")
    wa_pos = txt.find("## Workaround")
    if fix_pos == -1:
        return False, "P4: security advisory missing '## Fix' section"
    if wa_pos < fix_pos:
        return False, "P4: '## Workaround' appears before '## Fix' (must be after)"
    return True, "P4: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4")
    ap.add_argument("--target", default="analysis/")
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
