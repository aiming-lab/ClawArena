# sec1 — CVE-2024-6387 (regreSSHion) Vulnerability Analysis & Remediation

## Scenario Context

This workspace supports the emergency security response to CVE-2024-6387, a critical
signal handler race condition in OpenSSH server (sshd), disclosed 2024-07-01 by Qualys.

**You are the Lead Security Engineer.** Work through the tasks assigned in the main session.

## Key Ground-Truth Anchors

| Anchor | Value | Source |
|--------|-------|--------|
| CVE ID | CVE-2024-6387 | https://nvd.nist.gov/vuln/detail/CVE-2024-6387 |
| CVSS Score | 8.1 (High) | NVD |
| CVSS Vector | CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H | NVD |
| GHSA ID | GHSA-2x8c-95vh-gfv4 | GitHub Advisory |
| Affected Range | 8.5p1 <= openssh < 9.8p1 | oss-security disclosure |
| Patched Version | 9.8p1 | openssh.org release-9.8 |
| RHEL 9 Package | openssh-8.7p1-38.el9_4.1 | RHSA-2024:4312 |
| RHEL 9 Errata | RHSA-2024:4312 (2024-07-03) | Red Hat |
| Regression Commit | 752250caabda3dd24635503c4cd689b32a650794 | openssh-portable |
| Regression Date | 2020-10-16 | openssh-portable commit |
| Prior CVE | CVE-2006-5051 | GitHub Advisory |
| Exploitation | ~10,000 attempts, 6-8 hours (lab) | Qualys |
| Internet Exposure | ~14,000,000 instances | Qualys |
| EPSS Score | 63.835% (98th percentile) | GHSA |

## Directory Layout

```
assets/
  advisories/         # CVE advisories (authoritative source of truth)
    NVD_CVE-2024-6387.json      # AUTHORITATIVE: CVSS 8.1, vector, CWE
    GHSA-2x8c-95vh-gfv4.json   # AUTHORITATIVE: EPSS 63.835%
    qualys_regresshion_report.txt  # AUTHORITATIVE: 14M instances, 6-8h exploit time
    redhat_RHSA-2024-4312.json  # RHEL 9 errata details
    openwall_disclosure.txt     # oss-security original disclosure
  scan_results/        # Asset inventory and scan data
    internal_inventory.csv       # 500 internal hosts with vulnerability status
    shodan_export_2024-07-02.json  # Internet exposure data (2200 samples)
    nmap_ssh_scan_20240702.txt   # nmap scan output
  code_samples/        # Vulnerable vs patched code comparison
  compliance/          # CVSS worksheet, risk register template
scripts/               # Utility scripts (check_vulnerable.sh, patch_audit.py)
templates/             # Report templates
work/                  # YOUR OUTPUT GOES HERE (initially empty)
```

## Deliverable Rules

- All JSON output: 2-space indent, top-level keys alphabetically sorted (P1)
- CVE IDs: format CVE-YYYY-NNNNN with hyphens, uppercase (P2)
- Filenames: snake_case only (P3)
- Progress/inventory reports: grouped prod > staging > dev (P4)
- Executive summaries: include standalone TL;DR ≤200 words (P5)
