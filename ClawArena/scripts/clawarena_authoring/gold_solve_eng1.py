#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gold_solve_eng1.py — eng1 可解性审计（金标自检）。

在 workspace 的临时副本上模拟 update 生效后的状态，写出每一轮的「正确产物」，
然后运行全部 check_qN.py + 对应 preference，断言正解全部 PASS。
再做一组反例（错误产物）抽样，断言 check 能 FAIL（不过松）。

用途：证明每个 ground-truth 可由真实数据解出、check 不过严也不过松。
运行：python scripts/clawarena_authoring/gold_solve_eng1.py
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DS = REPO / "data" / "clawarena-real"
WS_SRC = DS / "openclaw" / "workspaces" / "eng1"
UPD = DS / "openclaw" / "updates" / "eng1"
SCRIPTS = DS / "eval" / "eng1" / "scripts"
GOLD = Path("/home/xkaiwen/.claude/jobs/579de28f/tmp/eng1_gold_ws")

# Ground-truth anchors (from real sources, verbatim)
CVE_ID = "CVE-2024-47081"
GHSA_ID = "GHSA-9hjg-9r4m-mvj7"
AFFECTED_BELOW = "2.32.4"
FIXED_VERSION = "2.32.4"
ROOT_CAUSE_FUNC = "get_netrc_auth"
VULN_CODE = "ri.netloc.split(':')[0]"
FIX_CODE = "ri.hostname"
MALICIOUS_URL = "http://example.com:@evil.com/"
CVSS_SCORE = 5.3
CVSS_VECTOR = "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:N/A:N"
CWE_ID = "CWE-522"
COMMIT_SHA_PR6965 = "57acb7c26d809cf864ec439b8bcd6364702022d5"
COMMIT_SHA_PR6963 = "5b4b64c3467fd7a3c03f91ee641aaa348b6bed3b"
CVE_2023_FIXED = "2.31.0"
AFFECTED_SERVICES_NETRC_COUNT = 3


def prep_workspace() -> Path:
    if GOLD.exists():
        shutil.rmtree(GOLD)
    shutil.copytree(WS_SRC, GOLD)
    # 应用 update workspace 文件
    upd1 = UPD / "upd1"
    upd2 = UPD / "upd2"
    (GOLD / "analysis").mkdir(exist_ok=True)
    (GOLD / "sessions").mkdir(exist_ok=True)
    shutil.copy(upd1 / "cve_2023_32681_nvd_snapshot.md",
                GOLD / "analysis" / "cve_2023_32681_nvd_snapshot.md")
    shutil.copy(upd1 / "slack_update1_messages.md",
                GOLD / "sessions" / "slack_update1_messages.md")
    shutil.copy(upd2 / "pr6965_review_snapshot.md",
                GOLD / "analysis" / "pr6965_review_snapshot.md")
    shutil.copy(upd2 / "erratum_email.md",
                GOLD / "sessions" / "erratum_email.md")
    shutil.copy(upd2 / "erratum_slack.md",
                GOLD / "sessions" / "erratum_slack.md")
    return GOLD


def _w(p: Path, t: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8")


def _wj(p: Path, o) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _patch_utils_py(ws: Path) -> None:
    """Apply the CVE-2024-47081 fix to utils.py: replace netloc.split with ri.hostname."""
    utils_path = ws / "src" / "requests" / "utils.py"
    txt = utils_path.read_text(encoding="utf-8")
    # Replace the vulnerable line with the fix
    txt = txt.replace(
        '        host = ri.netloc.split(":")[0]',
        '        host = ri.hostname\n        if host is None:\n            return None'
    )
    utils_path.write_text(txt, encoding="utf-8")


def solve(ws: Path) -> None:
    """Write all gold-standard deliverables to the workspace."""
    analysis = ws / "analysis"
    analysis.mkdir(exist_ok=True)
    test_results = ws / "test_results"
    test_results.mkdir(exist_ok=True)
    docs = ws / "docs"
    docs.mkdir(exist_ok=True)
    signoff = ws / "signoff"
    signoff.mkdir(exist_ok=True)
    tests = ws / "tests"
    tests.mkdir(exist_ok=True)

    # ── Q1: vuln_location.json ────────────────────────────────────────────────
    # vulnerable_line_range must start at 112 (actual start of get_netrc_auth)
    _wj(analysis / "vuln_location.json", {
        "cve_id": CVE_ID,
        "root_cause_function": ROOT_CAUSE_FUNC,
        "vulnerable_file": "src/requests/utils.py",
        "vulnerable_line_range": "112-169",
    })

    # ── Q2: version_impact.json ───────────────────────────────────────────────
    # source must contain "NVD" verbatim (check_q2 now enforces this)
    _wj(analysis / "version_impact.json", {
        "affected_below": AFFECTED_BELOW,
        "fixed_version": FIXED_VERSION,
        "source": "NVD (https://nvd.nist.gov/vuln/detail/CVE-2024-47081) and PR#6965 (sethmlarson)",
    })

    # ── Q3: reproduce_cve.py ──────────────────────────────────────────────────
    # This script MUST exit 0 proving the vulnerability exists — we implement
    # the vulnerable logic directly (no importing from requests to avoid circular imports)
    _w(ws / "scripts" / "reproduce_cve.py", '''\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PoC script for CVE-2024-47081: demonstrates credential leak via crafted URL.

This script directly implements the vulnerable hostname extraction logic to
demonstrate that ri.netloc.split(\':\')[0] incorrectly returns \'example.com\'
for the malicious URL http://example.com:@evil.com/, while the actual target
is evil.com.
"""
import os
import sys
import tempfile
from urllib.parse import urlparse
from netrc import netrc


def vulnerable_get_host(url):
    """Vulnerable hostname extraction (CVE-2024-47081 root cause).

    Replicates the logic from get_netrc_auth in src/requests/utils.py
    before the fix: uses ri.netloc.split(\':\')[0] instead of ri.hostname.
    """
    ri = urlparse(url)
    # VULNERABLE CODE: using netloc.split(\':\')[0] to extract host
    # For http://example.com:@evil.com/ this gives \'example.com\' NOT \'evil.com\'
    host = ri.netloc.split(":")[0]
    return host


def main():
    # Create a temporary netrc file with credentials for example.com
    with tempfile.NamedTemporaryFile(mode="w", suffix=".netrc", delete=False) as f:
        f.write("machine example.com login aaaa password bbbb\\n")
        netrc_path = f.name

    try:
        # Demonstrate the vulnerability: the malicious URL
        malicious_url = "http://example.com:@evil.com/"
        host = vulnerable_get_host(malicious_url)

        # Verify the bug: netloc.split gives example.com, NOT evil.com
        assert host == "example.com", f"Expected example.com, got {host!r}"

        # Check what urlparse.hostname gives (the correct fix):
        ri = urlparse(malicious_url)
        correct_host = ri.hostname
        assert correct_host == "evil.com", f"Expected evil.com from ri.hostname, got {correct_host!r}"

        # Demonstrate that netrc lookup with the vulnerable host leaks credentials
        netrc_ = netrc(netrc_path)
        auth = netrc_.authenticators(host)  # host = "example.com" (wrong!)

        assert auth is not None, "Credentials not found in netrc for example.com (unexpected)"
        print(f"[VULNERABILITY CONFIRMED] evil.com URL triggers example.com lookup")
        print(f"Vulnerable host extracted: {host!r} (should be {correct_host!r})")
        print(f"Leaked credentials: login={auth[0]!r}, password={auth[2]!r}")
        print(f"Target URL evil.com would receive credentials for example.com")
        print(f"PoC URL: {malicious_url}")
        sys.exit(0)
    finally:
        os.unlink(netrc_path)


if __name__ == "__main__":
    main()
''')

    # ── Q4: test_utils_regression.py (pre-fix version — but check only validates structure) ──
    _w(tests / "test_utils_regression.py", '''\
"""
Regression test suite for CVE-2024-47081 in psf/requests.

This module contains regression tests for the credential-leakage vulnerability
in get_netrc_auth (src/requests/utils.py). Tests verify that the patched version
correctly handles crafted URLs and does not leak credentials to attacker-controlled hosts.

Real test anchors sourced from:
  https://raw.githubusercontent.com/psf/requests/main/tests/test_utils.py
"""
import os
import sys
import tempfile
import importlib.util
import pytest
from pathlib import Path

# Import get_netrc_auth directly from the module file to avoid circular import issues
_utils_path = Path(__file__).parent.parent / "src" / "requests" / "utils.py"
_spec = importlib.util.spec_from_file_location("requests_utils", _utils_path)
_utils_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_utils_mod)
get_netrc_auth = _utils_mod.get_netrc_auth


def _make_netrc(tmp_path, content):
    """Helper to create a temporary netrc file and set NETRC env var."""
    netrc_file = tmp_path / ".netrc"
    netrc_file.write_text(content)
    old = os.environ.get("NETRC")
    os.environ["NETRC"] = str(netrc_file)
    return old


def _restore_netrc(old):
    if old is None:
        os.environ.pop("NETRC", None)
    else:
        os.environ["NETRC"] = old


class TestCVE202447081:
    """Regression tests for CVE-2024-47081 (get_netrc_auth credential leak)."""

    def test_cve_2024_47081_credential_leak(self, tmp_path):
        """Verify that the patched get_netrc_auth does NOT leak credentials via crafted URL.

        The malicious URL http://example.com:@evil.com/ should return None (no credentials)
        after the fix is applied, because ri.hostname correctly identifies evil.com as the
        target host, for which no netrc entry exists.

        Source: https://raw.githubusercontent.com/psf/requests/main/tests/test_utils.py
        test_not_vulnerable_to_bad_url_parsing
        """
        old = _make_netrc(tmp_path, "machine example.com login aaaa password bbbb\\n")
        try:
            auth = get_netrc_auth("http://example.com:@evil.com/")
            assert auth is None, (
                f"Credential leak detected! auth={auth!r} was returned for "
                "http://example.com:@evil.com/ — patch may not have been applied."
            )
        finally:
            _restore_netrc(old)

    def test_legitimate_url_returns_credentials(self, tmp_path):
        """Normal URL returns correct credentials from netrc.

        Source: https://raw.githubusercontent.com/psf/requests/main/tests/test_utils.py
        test_works — assert auth == ("aaaa", "bbbb")
        """
        old = _make_netrc(tmp_path, "machine example.com login aaaa password bbbb\\n")
        try:
            auth = get_netrc_auth("http://example.com/")
            assert auth == ("aaaa", "bbbb"), f"Expected ('aaaa', 'bbbb'), got {auth!r}"
        finally:
            _restore_netrc(old)

    def test_empty_default_credentials_ignored(self, tmp_path):
        """URL with no matching netrc entry returns None.

        Source: https://raw.githubusercontent.com/psf/requests/main/tests/test_utils.py
        test_empty_default_credentials_ignored
        """
        old = _make_netrc(tmp_path, "machine example.com login aaaa password bbbb\\n")
        try:
            auth = get_netrc_auth("http://other.example.org/path")
            assert auth is None, f"Expected None for unknown host, got {auth!r}"
        finally:
            _restore_netrc(old)
''')

    # ── Q5: Apply the fix to utils.py ─────────────────────────────────────────
    _patch_utils_py(ws)

    # ── Q6: run Q4 test, save output ──────────────────────────────────────────
    test_file = tests / "test_utils_regression.py"
    r = subprocess.run(
        [sys.executable, "-m", "pytest", str(test_file), "-v", "--tb=short"],
        capture_output=True, text=True, cwd=str(ws), timeout=60
    )
    q6_output = r.stdout + r.stderr
    _w(test_results / "q6_pytest_output.txt", q6_output)

    # ── Q7: cve_metadata.json ─────────────────────────────────────────────────
    _wj(analysis / "cve_metadata.json", {
        "cvss_score": CVSS_SCORE,
        "cvss_vector": CVSS_VECTOR,
        "cwe_id": CWE_ID,
        "epss_score": "0.1957",
    })

    # ── Q8: cve_2023_32681_summary.json ───────────────────────────────────────
    # root_cause must mention both Proxy-Authorization AND redirect (check_q8 enforces both)
    # affected_below field must now be present (new requirement)
    _wj(analysis / "cve_2023_32681_summary.json", {
        "cve_id": "CVE-2023-32681",
        "fixed_version": CVE_2023_FIXED,
        "affected_below": CVE_2023_FIXED,
        "root_cause": (
            "The Proxy-Authorization header was inadvertently forwarded to destination "
            "servers when following redirects through an HTTPS proxy. The vulnerability "
            "occurred because the redirect handling logic in requests/sessions.py failed "
            "to strip Proxy-Authorization headers before forwarding requests to the "
            "destination server after the tunnel was established. Fixed in requests 2.31.0."
        ),
    })

    # ── Q9: fix_commit.json (UPDATE-1 instruction: PR#6963 SHA) ───────────────
    # This is written first; check_q9 runs separately before Q10 overwrites it
    _wj(analysis / "fix_commit.json", {
        "commit_sha": COMMIT_SHA_PR6963,
        "pr": "6963",
        "note": "Per UPDATE-1 instruction from Alice (to be corrected by UPDATE-2)",
    })

    # ── Q11: CHANGELOG_ENTRY.md ───────────────────────────────────────────────
    # Must contain: CVE ID, 2.32.4, get_netrc_auth, trust_env=False, **Security**,
    #               GHSA ID (GHSA-9hjg-9r4m-mvj7), :pr:`6965` RST citation
    _w(ws / "CHANGELOG_ENTRY.md", f"""\
## {FIXED_VERSION} (2025-06-10)

**Security**

- Fixed {CVE_ID} ({GHSA_ID}): ``{ROOT_CAUSE_FUNC}`` used
  ``ri.netloc.split(':')[0]`` to extract the hostname for .netrc lookup.
  A crafted URL like ``http://example.com:@evil.com/`` would cause credentials
  for ``example.com`` to be sent to ``evil.com``. Fixed by using ``ri.hostname``
  instead. Users who cannot upgrade immediately should set ``trust_env=False``
  on their Session objects as a workaround. (:issue:`6964`, :pr:`6965`)
""")

    # ── Q12: impact_assessment.json ───────────────────────────────────────────
    # Read affected_services.json and filter for uses_netrc=True AND version < 2.32.4
    svc_data = json.loads((ws / "analysis" / "affected_services.json").read_text())
    affected = []
    for svc in svc_data["services"]:
        if svc.get("uses_netrc") is True and svc.get("requests_version") is not None:
            ver = svc["requests_version"]
            parts = ver.split(".")
            try:
                major, minor, patch_ = int(parts[0]), int(parts[1]), int(parts[2])
                if (major, minor, patch_) < (2, 32, 4):
                    affected.append({
                        "service_name": svc["service_name"],
                        "requests_version": svc["requests_version"],
                        "uses_netrc": svc["uses_netrc"],
                    })
            except (ValueError, IndexError):
                pass
    _wj(analysis / "impact_assessment.json", {
        "affected_services": affected,
        "count": len(affected),
    })

    # ── Q13: extended test file + run full suite ───────────────────────────────
    # The test file already has all 3 tests (written in Q4 step above)
    # Just run the full suite
    r13 = subprocess.run(
        [sys.executable, "-m", "pytest", str(tests / "test_utils_regression.py"), "-v", "--tb=short"],
        capture_output=True, text=True, cwd=str(ws), timeout=60
    )
    _w(test_results / "q13_full_suite.txt", r13.stdout + r13.stderr)

    # ── Q14: security advisory ────────────────────────────────────────────────
    # Must contain: GHSA ID, exact CVSS vector, ## Vulnerability section,
    #               ## Fix section, ## Workaround after ## Fix, trust_env=False, CWE-522
    _w(docs / "SECURITY_ADVISORY_CVE-2024-47081.md", f"""\
# Security Advisory: {CVE_ID}

## Summary

A credential-leakage vulnerability has been identified in the psf/requests library.

| Field | Value |
|-------|-------|
| CVE | {CVE_ID} |
| GHSA | {GHSA_ID} |
| CVSS Score | {CVSS_SCORE} (MEDIUM) |
| CVSS Vector | `{CVSS_VECTOR}` |
| CWE | {CWE_ID} |
| Affected | requests < {AFFECTED_BELOW} |
| Fixed | requests == {FIXED_VERSION} |

## Vulnerability

The `{ROOT_CAUSE_FUNC}` function in `src/requests/utils.py` used
`ri.netloc.split(':')[0]` to extract the hostname for `.netrc` credential lookup.
A crafted URL like `http://example.com:@evil.com/` would cause credentials stored
for `example.com` to be sent to `evil.com`.

CWE classification: {CWE_ID} (Inadequately Protected Credentials).

## Fix

Upgrade to requests >= {FIXED_VERSION}. The fix replaces `ri.netloc.split(':')[0]`
with `ri.hostname`, which correctly handles userinfo in URLs.

Official fix: PR#6965 (commit `{COMMIT_SHA_PR6965}`, author: sethmlarson).
GHSA: `{GHSA_ID}`.

## Workaround

If you cannot upgrade immediately, set `trust_env=False` on all Session objects
to disable `.netrc` file reading:

```python
import requests
s = requests.Session()
s.trust_env = False
```
""")

    # ── Q15: SHA-256 sign-off ─────────────────────────────────────────────────
    # Now hashes 4 files: utils.py + fix_commit.json + cve_metadata.json + impact_assessment.json
    files_for_hash = [
        ws / "src" / "requests" / "utils.py",
        ws / "analysis" / "fix_commit.json",
        ws / "analysis" / "cve_metadata.json",
        ws / "analysis" / "impact_assessment.json",
    ]
    combined = b""
    for f in files_for_hash:
        combined += f.read_bytes()
    digest = hashlib.sha256(combined).hexdigest()
    _w(signoff / "final_signoff.txt", f"VERIFIED:{digest}\n")


# ─────────────────────────────────────────────────────────────────────────────
# Run checks
# ─────────────────────────────────────────────────────────────────────────────
EVAL_CMDS_PRE_Q10 = {
    "q1": ["check_q1.py"],
    "q2": ["check_q2.py"],
    "q3": ["check_q3.py"],
    "q4": ["check_q4.py", ("pref", "P3", "tests/test_utils_regression.py")],
    "q5": ["check_q5.py"],
    "q6": ["check_q6.py"],
    "q7": ["check_q7.py", ("pref", "P1", "analysis/cve_metadata.json")],
    "q8": ["check_q8.py", ("pref", "P1", "analysis/cve_2023_32681_summary.json")],
    "q9": ["check_q9.py"],  # Must run BEFORE q10 overwrites fix_commit.json
}

EVAL_CMDS_POST_Q10 = {
    "q10": ["check_q10.py"],
    "q11": ["check_q11.py", ("pref", "P2", "CHANGELOG_ENTRY.md")],
    "q12": ["check_q12.py", ("pref", "P1", "analysis/impact_assessment.json")],
    "q13": ["check_q13.py", ("pref", "P3", "tests/test_utils_regression.py")],
    "q14": ["check_q14.py", ("pref", "P4", "docs/SECURITY_ADVISORY_CVE-2024-47081.md")],
    "q15": ["check_q15.py"],
}


def run_check(item, ws: Path) -> tuple[bool, str]:
    if isinstance(item, tuple):
        _, rules, target = item
        cmd = [sys.executable, str(SCRIPTS / "check_preferences.py"),
               str(ws), "--rules", rules, "--target", target]
    else:
        cmd = [sys.executable, str(SCRIPTS / item), str(ws)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    last = (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout or r.stderr) else ""
    return r.returncode == 0, last


def main():
    ws = prep_workspace()
    solve(ws)

    print("=== GOLD SOLUTION: every check must PASS ===")
    n_pass = n_fail = 0

    # Phase 1: run q1-q9 BEFORE overwriting fix_commit.json with q10 value
    for q, items in EVAL_CMDS_PRE_Q10.items():
        for it in items:
            ok, last = run_check(it, ws)
            tag = f"pref {it[1]}" if isinstance(it, tuple) else "main"
            status = "PASS" if ok else "FAIL"
            print(f"  [{status}] {q} ({tag}): {last}")
            if ok:
                n_pass += 1
            else:
                n_fail += 1

    # Transition: overwrite fix_commit.json with the UPDATE-2 corrected value
    analysis = ws / "analysis"
    _wj(analysis / "fix_commit.json", {
        "commit_sha": COMMIT_SHA_PR6965,
        "supersedes_pr": "6963",
        "authoritative_pr": "6965",
        "note": "UPDATE-2 correction: PR#6963 (5b4b64c3...) superseded by PR#6965 (sethmlarson)",
    })

    # Recompute and update Q15 signoff after fix_commit.json changes
    # 4-file hash: utils.py + fix_commit.json + cve_metadata.json + impact_assessment.json
    files_for_hash = [
        ws / "src" / "requests" / "utils.py",
        ws / "analysis" / "fix_commit.json",
        ws / "analysis" / "cve_metadata.json",
        ws / "analysis" / "impact_assessment.json",
    ]
    combined = b""
    for f in files_for_hash:
        combined += f.read_bytes()
    digest = hashlib.sha256(combined).hexdigest()
    _w(ws / "signoff" / "final_signoff.txt", f"VERIFIED:{digest}\n")

    # Phase 2: run q10-q15 with updated fix_commit.json
    for q, items in EVAL_CMDS_POST_Q10.items():
        for it in items:
            ok, last = run_check(it, ws)
            tag = f"pref {it[1]}" if isinstance(it, tuple) else "main"
            status = "PASS" if ok else "FAIL"
            print(f"  [{status}] {q} ({tag}): {last}")
            if ok:
                n_pass += 1
            else:
                n_fail += 1

    print(f"gold: {n_pass} checks PASSED, {n_fail} FAILED")

    # ── 反例抽样（≥4 个，each must FAIL）─────────────────────────────────────
    print("\n=== NEGATIVE PROBES: each must FAIL ===")
    probes = 0
    caught = 0

    # 1a. q1 bot decoy: wrong root_cause_function (build_response)
    _wj(ws / "analysis" / "vuln_location.json", {
        "cve_id": "CVE-2024-47081",
        "root_cause_function": "build_response",   # BOT DECOY
        "vulnerable_file": "src/requests/adapters.py",
        "vulnerable_line_range": "112-169",
    })
    ok, _ = run_check("check_q1.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q1 bot-decoy build_response -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 1b. q1 wrong line number (question prompt decoy 180-217 instead of real 112-169)
    _wj(ws / "analysis" / "vuln_location.json", {
        "cve_id": "CVE-2024-47081",
        "root_cause_function": "get_netrc_auth",
        "vulnerable_file": "src/requests/utils.py",
        "vulnerable_line_range": "180-217",   # DECOY from question prompt
    })
    ok, _ = run_check("check_q1.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q1 decoy line range 180-217 (should be 112-169) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore correct q1 for later checks
    _wj(ws / "analysis" / "vuln_location.json", {
        "cve_id": "CVE-2024-47081",
        "root_cause_function": "get_netrc_auth",
        "vulnerable_file": "src/requests/utils.py",
        "vulnerable_line_range": "112-169",
    })

    # 2a. q2 wrong affected range 2.32.3 instead of 2.32.4 (Bob/Slack confusion)
    _wj(ws / "analysis" / "version_impact.json", {
        "affected_below": "2.32.3",   # WRONG (Slack confusion)
        "fixed_version": "2.32.3",
        "source": "Slack bot",
    })
    ok, _ = run_check("check_q2.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q2 wrong version 2.32.3 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 2b. q2 correct version but source missing NVD
    _wj(ws / "analysis" / "version_impact.json", {
        "affected_below": "2.32.4",
        "fixed_version": "2.32.4",
        "source": "GitHub PR#6965 and security email",   # WRONG: no "NVD" mentioned
    })
    ok, _ = run_check("check_q2.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q2 missing 'NVD' in source -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore correct q2
    _wj(ws / "analysis" / "version_impact.json", {
        "affected_below": "2.32.4",
        "fixed_version": "2.32.4",
        "source": "NVD (https://nvd.nist.gov/vuln/detail/CVE-2024-47081) and PR#6965 (sethmlarson)",
    })

    # 3a. q7 CVSS 6.1 (bot decoy score)
    _wj(ws / "analysis" / "cve_metadata.json", {
        "cvss_score": 6.1,   # BOT DECOY
        "cvss_vector": "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:N/A:N",
        "cwe_id": "CWE-522",
        "epss_score": "0.1957",
    })
    ok, _ = run_check("check_q7.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q7 bot-decoy CVSS 6.1 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 3b. q7 partial cvss_vector (not full verbatim string)
    _wj(ws / "analysis" / "cve_metadata.json", {
        "cvss_score": 5.3,
        "cvss_vector": "AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:N/A:N",   # missing CVSS:3.1/ prefix
        "cwe_id": "CWE-522",
        "epss_score": "0.1957",
    })
    ok, _ = run_check("check_q7.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q7 partial cvss_vector (no CVSS:3.1/ prefix) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 3c. q7 wrong epss_score
    _wj(ws / "analysis" / "cve_metadata.json", {
        "cvss_score": 5.3,
        "cvss_vector": "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:N/A:N",
        "cwe_id": "CWE-522",
        "epss_score": "0.05",   # WRONG
    })
    ok, _ = run_check("check_q7.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q7 wrong epss_score 0.05 (should be 0.1957) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore correct cve_metadata for q15 hash reuse
    _wj(ws / "analysis" / "cve_metadata.json", {
        "cvss_score": 5.3,
        "cvss_vector": "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:N/A:N",
        "cwe_id": "CWE-522",
        "epss_score": "0.1957",
    })

    # 4. q10 old SHA (PR#6963) — should fail because UPDATE-2 superseded it
    _wj(ws / "analysis" / "fix_commit.json", {
        "commit_sha": "5b4b64c3467fd7a3c03f91ee641aaa348b6bed3b",   # WRONG (pre-supersede)
        "pr": "6963",
    })
    ok, _ = run_check("check_q10.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q10 old PR#6963 SHA (pre-supersede) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 5. q15 placeholder hash
    _w(ws / "signoff" / "final_signoff.txt", "VERIFIED:" + "0" * 64 + "\n")
    ok, _ = run_check("check_q15.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q15 placeholder hash -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 6. q12 wrong count (4 instead of 3)
    _wj(ws / "analysis" / "impact_assessment.json", {
        "affected_services": [
            {"service_name": "a", "requests_version": "2.32.3", "uses_netrc": True},
            {"service_name": "b", "requests_version": "2.31.0", "uses_netrc": True},
            {"service_name": "c", "requests_version": "2.32.3", "uses_netrc": True},
            {"service_name": "d", "requests_version": "2.28.2", "uses_netrc": True},  # extra
        ],
        "count": 4,
    })
    ok, _ = run_check("check_q12.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q12 wrong count (4 instead of 3) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 7. q8 missing redirect in root_cause
    _wj(ws / "analysis" / "cve_2023_32681_summary.json", {
        "cve_id": "CVE-2023-32681",
        "fixed_version": "2.31.0",
        "affected_below": "2.31.0",
        "root_cause": "Proxy-Authorization header was forwarded to destination servers.",  # missing 'redirect'
    })
    ok, _ = run_check("check_q8.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q8 missing 'redirect' in root_cause -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 8. q11 missing GHSA or :pr:`6965`
    (ws / "CHANGELOG_ENTRY.md").write_text(
        "## 2.32.4\n\n**Security**\n\n- Fixed CVE-2024-47081: get_netrc_auth leak. "
        "Use trust_env=False as workaround. (:issue:`6964`)\n",
        encoding="utf-8"
    )
    ok, _ = run_check("check_q11.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q11 missing GHSA + :pr:`6965` -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 9. q14 missing ## Vulnerability section
    (ws / "docs" / "SECURITY_ADVISORY_CVE-2024-47081.md").write_text(
        "# Security Advisory: CVE-2024-47081\n\n"
        "GHSA-9hjg-9r4m-mvj7\n"
        "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:N/A:N\n"
        "CWE-522\n"
        "## Fix\nUpgrade to 2.32.4.\n"
        "## Workaround\nSet trust_env=False.\n",
        encoding="utf-8"
    )
    ok, _ = run_check("check_q14.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q14 missing ## Vulnerability section -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # 10. q15 old 3-file hash (should fail because 4 files now required)
    files_old_3 = [
        ws / "src" / "requests" / "utils.py",
        ws / "analysis" / "fix_commit.json",
        ws / "analysis" / "cve_metadata.json",
    ]
    combined_old = b""
    for f in files_old_3:
        combined_old += f.read_bytes()
    old_digest = hashlib.sha256(combined_old).hexdigest()
    _w(ws / "signoff" / "final_signoff.txt", f"VERIFIED:{old_digest}\n")
    ok, _ = run_check("check_q15.py", ws)
    probes += 1; caught += (not ok)
    print(f"  q15 old 3-file hash (missing impact_assessment.json) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    print(f"negatives: {caught}/{probes} correctly caught")

    if n_fail == 0 and caught == probes:
        print("\nAUDIT OK: gold solution all-PASS and all negative probes caught.")
    else:
        print("\nAUDIT PROBLEM: see failures above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
