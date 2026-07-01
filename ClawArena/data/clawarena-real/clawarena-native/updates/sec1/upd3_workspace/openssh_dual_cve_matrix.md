# OpenSSH Dual CVE Analysis Matrix
## CVE-2024-6387 vs CVE-2024-6409

### Overview

Two related but distinct signal handler race condition vulnerabilities were identified
in OpenSSH around the same period (2024-07):

---

## CVE-2024-6387 (regreSSHion)

| Field | Value |
|-------|-------|
| CVE ID | CVE-2024-6387 |
| GHSA | GHSA-2x8c-95vh-gfv4 |
| CVSS Score | 8.1 (High) |
| CVSS Vector | CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H |
| Affected Component | sshd main process |
| Affected Versions | 8.5p1 through 9.7p1 |
| Impact | Root RCE (unauthenticated) |
| Disclosure | 2024-07-01 |
| Regression of | CVE-2006-5051 |
| Exploitation | ~10,000 attempts, 6-8 hours lab |
| Root Cause | syslog() in SIGALRM handler (removed DO_LOG_SAFE_IN_SIGHAND guard) |

---

## CVE-2024-6409

| Field | Value |
|-------|-------|
| CVE ID | CVE-2024-6409 |
| CVSS Score | 7.0 (High) |
| CVSS Vector | CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:H |
| Affected Component | sshd privilege separation child process |
| Affected Versions | 8.7 and 8.8 ONLY (RHEL backport-specific) |
| Impact | Child process code execution (reduced privileges) |
| Disclosure | 2024-07-08 |
| Regression of | None (new finding) |
| Root Cause | Signal handler race in privilege-separated child |

---

## Key Differences

| Aspect | CVE-2024-6387 | CVE-2024-6409 |
|--------|--------------|--------------|
| CVSS Score | **8.1** | **7.0** |
| Scope | Main sshd process | Privsep child only |
| Privilege at risk | **root** | Reduced (child) |
| Version range | 8.5p1 – 9.7p1 (wide) | **8.7 and 8.8 only** (narrow) |
| Patch | OpenSSH 9.8p1 / vendor errata | Included in same errata |
| Priority | CRITICAL — patch immediately | HIGH — patch with 6387 |

---

## Important Cautions

1. **Do NOT conflate the two CVEs**: They have different CVSS scores (8.1 vs 7.0),
   different version ranges, and different scopes.

2. **CVE-2024-6409 version range is narrow**: Only versions 8.7 and 8.8 (as shipped
   in RHEL packages) are affected by CVE-2024-6409. This is NOT the full 8.5p1–9.7p1
   range of CVE-2024-6387.

3. **Remediation is the same**: Both are fixed by the same vendor patches
   (RHSA-2024:4312 for RHEL 9, RHSA-2024:4340 for RHEL 8).
