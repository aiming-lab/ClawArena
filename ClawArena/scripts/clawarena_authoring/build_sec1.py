#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_sec1.py — 生成 ClawArena 真实数据集场景 sec1（CVE-2024-6387 regreSSHion 漏洞分析与修复）。

题材与锚点取材真实（NVD/GHSA/Qualys/OpenSSH/Red Hat Errata），
session 对话与 workspace 文档围绕真实锚点合成。全 exec_check，17 轮。

幂等：每次运行先清空 sec1 的 workspace/state/updates 后重建，再生成 _register.json。
questions.json 与 check 脚本由 eval/sec1/ 下静态文件提供，本脚本不生成它们。

真实来源：
  - https://nvd.nist.gov/vuln/detail/CVE-2024-6387
  - https://github.com/advisories/GHSA-2x8c-95vh-gfv4
  - https://blog.qualys.com/vulnerabilities-threat-research/2024/07/01/regresshion-remote-unauthenticated-code-execution-vulnerability-in-openssh-server
  - https://www.openwall.com/lists/oss-security/2024/07/01/3
  - https://www.openssh.org/txt/release-9.8
  - https://access.redhat.com/errata/RHSA-2024:4312
  - https://github.com/openssh/openssh-portable/commit/752250caabda3dd24635503c4cd689b32a650794
  - https://github.com/advisories/GHSA-mq5h-r3rg-j9hg

运行：python scripts/clawarena_authoring/build_sec1.py
"""
from __future__ import annotations

import csv
import io
import json
import random
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    SessionBuilder, append_history, est_tokens, gen_session_id, dump_register_meta,
)

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DATASET = REPO / "data" / "clawarena-real"
TID = "sec1"
CWD = f"/workspace/{TID}"
OC = DATASET / "openclaw"
WS = OC / "workspaces" / TID
SESS = OC / "state" / "agents" / TID / "sessions"
UPD = OC / "updates" / TID

# ── Ground-truth 锚点（取自真实来源，verbatim） ──────────────────────────────
CVE_ID = "CVE-2024-6387"
CVSS_SCORE = 8.1
CVSS_VECTOR = "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H"
SEVERITY = "High"
CWE_PRIMARY = "CWE-362"
CWE_SECONDARY = "CWE-364"
AFFECTED_RANGE = "8.5p1 <= openssh < 9.8p1"
REGRESSION_COMMIT = "752250caabda3dd24635503c4cd689b32a650794"
PATCHED_VERSION = "9.8p1"
RHEL9_FIXED_PKG = "openssh-8.7p1-38.el9_4.1"
RHEL_ERRATA = "RHSA-2024:4312"
RHEL8_ERRATA = "RHSA-2024:4340"
RHEL8_FIXED_PKG = "openssh-8.0p1-19.el8_10.1"
DISCLOSURE_DATE = "2024-07-01"
EXPLOIT_ATTEMPTS = "~10,000"
EXPLOIT_TIME = "6-8 hours"
EPSS_SCORE = "63.835%"
GHSA_ID = "GHSA-2x8c-95vh-gfv4"
WORKAROUND_PARAM = "LoginGraceTime 0"
EXPOSED_INSTANCES = 14000000
PRIOR_CVE = "CVE-2006-5051"
CVE_6409_ID = "CVE-2024-6409"
CVE_6409_CVSS = 7.0
RHEL_ERRATA_DATE = "2024-07-03"
REGRESSION_COMMIT_DATE = "2020-10-16"


def w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def wj(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ── 1. 系统文件（OpenClaw agent 启动文件） ───────────────────────────────────
def gen_system_files() -> None:
    w(WS / "AGENTS.md", """# Agent Startup Procedure

1. Read `SOUL.md` to understand your working principles and role.
2. Read `USER.md` to learn about the team, channels, and stakeholders.
3. Run `exec ls -R` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are a Lead Security Engineer at a mid-sized internet company. Your task is to lead
the analysis and remediation of CVE-2024-6387 (regreSSHion), a critical OpenSSH vulnerability
disclosed on 2024-07-01. Work through the tasks assigned by your security director Alice Wang
and coordinate with the SRE team.
""")
    w(WS / "SOUL.md", """# Working Principles

1. **Source primacy**: The canonical ground-truth for vulnerability details lives in
   `assets/advisories/NVD_CVE-2024-6387.json` and `assets/advisories/GHSA-2x8c-95vh-gfv4.json`.
   Auto-generated bot summaries (files containing "BOT_" in the name, or marked as
   "auto-summarized") are NOT authoritative — verify any number or date against the primary
   advisory files or the Qualys technical report.

2. **Verbatim field values**: Always reference official identifiers exactly as they appear in
   the source documents (e.g., CVE-2024-6387, CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H,
   GHSA-2x8c-95vh-gfv4). Do not abbreviate or paraphrase CVE IDs or CVSS vectors in
   structured JSON output.

3. **Output conventions**: All JSON deliverables use 2-space indentation. Top-level fields
   are sorted in alphabetical order. File names use snake_case exclusively.

4. **Supersede awareness**: When a later instruction or update explicitly revokes an earlier
   decision, the later instruction wins. Record the supersede relationship explicitly.

5. **Temporal discipline**: The disclosure date is 2024-07-01. All remediation timelines
   are calculated from this anchor. Do not conflate the disclosure date with the regression
   introduction date (2020-10-16).

6. **Cross-round consistency**: Numbers you compute in one round (e.g., prod host count,
   vulnerable_count) must remain consistent with any later round that references them.
""")
    w(WS / "USER.md", """# People and Channels

## Primary User
- **Alice Wang** — Security Director. Owns incident response strategy.
  Expects JSON output with 2-space indent, alphabetical field order, snake_case filenames.
  Requires executive summaries to include a standalone TL;DR section (≤200 words).

## Key Stakeholders

| Name | Role | Channel | Notes |
|---|---|---|---|
| Alice Wang | Security Director | CLI / main session | Primary task authority; all preference rules sourced from Alice |
| Bob Zhang | SRE Engineer | Feishu DM | Owns internal asset inventory; runs internal scans |
| Carol (CTO) | CTO | Email | Requires executive summaries for board; wants TL;DR ≤200 words |
| Dave Chen | Security Analyst | Slack #incident-response | Monitors external feeds; occasionally cites bot-summarized data |
| Eve Liu | Security Team | Slack #security-alerts | Sends initial CVE notifications; references Qualys data |

## Channels
- **Slack #security-alerts**: Initial CVE alerts and Qualys data (Eve, Dave)
- **Slack #incident-response**: Incident coordination, patch progress (Dave, team)
- **Email (Alice → Carol → Agent)**: Management reporting requests
- **Feishu DM (Bob ↔ Agent)**: Internal asset inventory, scan data exchange
- **Feishu #sre-infra**: SRE configuration discussions, PerSourcePenalties config

## Preference Rules (apply throughout, even when not restated)
- P1: All JSON outputs use 2-space indent; top-level fields sorted alphabetically.
- P2: CVE IDs in technical reports formatted as CVE-YYYY-NNNNN (hyphenated, uppercase).
- P3: All work product filenames use snake_case (no camelCase, no hyphens).
- P4: Progress reports and inventories grouped by environment (prod/staging/dev), prod first.
- P5: Executive summaries must include a standalone TL;DR paragraph (≤200 words).
""")
    w(WS / "IDENTITY.md", """# Identity

You are the **Lead Security Engineer** of the Security Engineering Team at a mid-sized
internet company. You have been activated to lead the emergency response to CVE-2024-6387
(regreSSHion), a remotely exploitable signal handler race condition in OpenSSH sshd.

Your responsibilities:
- Analyze the vulnerability using official advisories and technical reports
- Assess the internal asset exposure using scan data and inventory files
- Implement and document remediation plans (patches and workarounds)
- Generate compliance reports for management and board-level stakeholders
- Coordinate with the SRE team (Bob) and respond to Slack/Email/Feishu inquiries

All deliverables go into the `work/` directory. Inputs in `assets/` are read-only.
""")
    w(WS / "TOOLS.md", """# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in the main session |
| `sessions_history` | Read a specific history session | Use in the main session |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to write deliverables, run scripts |

## Rules
- Files under `assets/` are READ-ONLY reference inputs. Do not modify them.
- Create all deliverables under `work/` using `exec` (heredoc or python).
- History sessions contain relevant context from Slack, Email, and Feishu channels.
""")


# ── 2. Advisory 文件（核心真实锚点载体） ──────────────────────────────────────
def gen_advisories() -> None:
    # NVD 官方 JSON（真实锚点：CVSS 8.1, vector, CWE-362/364, 2024-07-01）
    wj(WS / "assets" / "advisories" / "NVD_CVE-2024-6387.json", {
        "id": "CVE-2024-6387",
        "sourceIdentifier": "cve@mitre.org",
        "published": "2024-07-01T00:00:00.000",
        "lastModified": "2024-07-10T12:00:00.000",
        "vulnStatus": "Analyzed",
        "descriptions": [
            {
                "lang": "en",
                "value": (
                    "A security regression (CVE-2006-5051) was discovered in OpenSSH's server (sshd). "
                    "There is a race condition which can lead sshd to handle some signals in an unsafe manner. "
                    "An unauthenticated, remote attacker may be able to trigger it by failing to authenticate "
                    "within a set time period. On glibc-based Linux systems, this can lead to remote code "
                    "execution (RCE) with root privileges. This vulnerability affects OpenSSH versions "
                    "8.5p1 through 9.7p1 on glibc-based Linux systems."
                )
            }
        ],
        "metrics": {
            "cvssMetricV31": [
                {
                    "source": "nvd@nist.gov",
                    "type": "Primary",
                    "cvssData": {
                        "version": "3.1",
                        "vectorString": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H",
                        "attackVector": "NETWORK",
                        "attackComplexity": "HIGH",
                        "privilegesRequired": "NONE",
                        "userInteraction": "NONE",
                        "scope": "UNCHANGED",
                        "confidentialityImpact": "HIGH",
                        "integrityImpact": "HIGH",
                        "availabilityImpact": "HIGH",
                        "baseScore": 8.1,
                        "baseSeverity": "HIGH"
                    },
                    "exploitabilityScore": 2.2,
                    "impactScore": 5.9
                }
            ]
        },
        "weaknesses": [
            {
                "source": "nvd@nist.gov",
                "type": "Primary",
                "description": [
                    {"lang": "en", "value": "CWE-362"},
                    {"lang": "en", "value": "CWE-364"}
                ]
            }
        ],
        "configurations": [
            {
                "nodes": [
                    {
                        "operator": "OR",
                        "negate": False,
                        "cpeMatch": [
                            {
                                "vulnerable": True,
                                "criteria": "cpe:2.3:a:openbsd:openssh:*:*:*:*:*:*:*:*",
                                "versionStartIncluding": "8.5p1",
                                "versionEndExcluding": "9.8p1",
                                "matchCriteriaId": "placeholder"
                            }
                        ]
                    }
                ]
            }
        ],
        "references": [
            {"url": "https://www.openwall.com/lists/oss-security/2024/07/01/3", "source": "nvd@nist.gov"},
            {"url": "https://www.openssh.org/txt/release-9.8", "source": "nvd@nist.gov"},
            {"url": "https://access.redhat.com/errata/RHSA-2024:4312", "source": "nvd@nist.gov"},
        ],
        "_note": "Verbatim NVD data. Source: https://nvd.nist.gov/vuln/detail/CVE-2024-6387"
    })

    # GHSA advisory JSON（真实锚点：EPSS 63.835%，98th percentile）
    wj(WS / "assets" / "advisories" / "GHSA-2x8c-95vh-gfv4.json", {
        "ghsa_id": "GHSA-2x8c-95vh-gfv4",
        "summary": "Signal handler race condition in OpenSSH sshd",
        "description": (
            "A security regression (CVE-2006-5051) was discovered in OpenSSH's server (sshd). "
            "There is a race condition which can lead sshd to handle some signals in an unsafe manner. "
            "This vulnerability allows remote unauthenticated code execution with root privileges on "
            "glibc-based Linux systems running OpenSSH 8.5p1 through 9.7p1."
        ),
        "severity": "High",
        "published_at": "2024-07-01T00:00:00Z",
        "updated_at": "2024-07-10T00:00:00Z",
        "cve_id": "CVE-2024-6387",
        "cvss": {
            "score": 8.1,
            "vectorString": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H"
        },
        "epss": {
            "score": 0.63835,
            "percentile": 0.98,
            "note": "EPSS score 63.835%, 98th percentile as of 2024-07-10"
        },
        "identifiers": [
            {"type": "GHSA", "value": "GHSA-2x8c-95vh-gfv4"},
            {"type": "CVE", "value": "CVE-2024-6387"}
        ],
        "affected": [
            {
                "package": {"ecosystem": "Other", "name": "openssh"},
                "ranges": [
                    {
                        "type": "ECOSYSTEM",
                        "events": [
                            {"introduced": "8.5p1"},
                            {"fixed": "9.8p1"}
                        ]
                    }
                ]
            }
        ],
        "references": [
            {"type": "ADVISORY", "url": "https://github.com/advisories/GHSA-2x8c-95vh-gfv4"},
            {"type": "WEB", "url": "https://nvd.nist.gov/vuln/detail/CVE-2024-6387"},
            {"type": "WEB", "url": "https://blog.qualys.com/vulnerabilities-threat-research/2024/07/01/regresshion-remote-unauthenticated-code-execution-vulnerability-in-openssh-server"}
        ],
        "_note": "Source: https://github.com/advisories/GHSA-2x8c-95vh-gfv4"
    })

    # Qualys 技术报告文本版（~20k tokens，含关键技术分析、PoC 描述、版本矩阵）
    qualys_text = """# regreSSHion: Remote Unauthenticated Code Execution Vulnerability in OpenSSH Server
## Qualys Threat Research Unit — Technical Report
### Published: 2024-07-01
### Source: https://blog.qualys.com/vulnerabilities-threat-research/2024/07/01/regresshion-remote-unauthenticated-code-execution-vulnerability-in-openssh-server

---

## Executive Summary

The Qualys Threat Research Unit (TRU) has discovered a critical security regression
(CVE-2024-6387) in OpenSSH's server (sshd). The vulnerability, dubbed "regreSSHion,"
is a signal handler race condition that allows unauthenticated remote code execution
(RCE) as root on glibc-based Linux systems.

**Key Statistics:**
- Approximately 14 million potentially vulnerable internet-facing OpenSSH instances identified
- Approximately 700,000 Qualys customer external-facing instances vulnerable (~31%)
- CVSS v3.1 Base Score: 8.1 (High)
- EPSS Score: 63.835% (98th percentile)
- Exploitation requires approximately 10,000 attempts due to race condition nature
- Laboratory exploitation time: 6-8 hours total on 32-bit Linux with glibc and ASLR

---

## Background and History

### CVE-2006-5051: The Original Vulnerability

In 2006, a signal handler race condition was discovered in OpenSSH versions prior to 4.4.
The vulnerability (CVE-2006-5051) allowed attackers to potentially execute arbitrary code
by exploiting the unsafe use of functions in signal handlers. The OpenSSH team fixed this
in version 4.4p1 by adding a compile-time guard macro `DO_LOG_SAFE_IN_SIGHAND` that wrapped
calls to non-async-signal-safe functions within signal handlers.

### The Regression (2020-10-16)

On October 16, 2020, a commit to the openssh-portable repository inadvertently removed
the `DO_LOG_SAFE_IN_SIGHAND` protection:

  Commit: 752250caabda3dd24635503c4cd689b32a650794
  Author: Damien Miller <djm@mindrot.org>
  Date: 2020-10-16
  Message: "upstream: revised log infrastructure for OpenSSH"
  Files changed: 7 files, 154 additions, 133 deletions

This commit refactored the logging infrastructure and accidentally dropped the
`#ifdef DO_LOG_SAFE_IN_SIGHAND` guard in `sshsigdie()`, reintroducing the signal handler
race condition from CVE-2006-5051. This regression was introduced in OpenSSH 8.5p1
(released February 2021) and affected all versions through 9.7p1.

---

## Technical Analysis

### Vulnerability Mechanism

The vulnerability exists in sshd's handling of the `LoginGraceTime` timeout. When a client
connection does not authenticate within the grace period (default: 120 seconds), sshd sends
a `SIGALRM` signal to itself. The signal handler `sigdie()` (and its internal function
`sshsigdie()`) then calls `syslog()` to log the timeout event.

**The problem:** `syslog()` is NOT async-signal-safe. Calling a non-async-signal-safe function
from within a signal handler creates a race condition — if the main thread is executing within
glibc's heap allocator (e.g., during `malloc()`/`free()`) when the signal is delivered, the
signal handler's call to `syslog()` may corrupt the heap state.

### Exploit Methodology

The exploit targets the glibc heap allocator's internal state. The attack exploits the FILE
structure manipulation technique to gain code execution:

1. **Setup Phase**: Attacker sends partial authentication requests to trigger SIGALRM at
   precise moments during heap operations.
2. **Heap Spraying**: Multiple connection attempts are used to position heap chunks in
   predictable locations, working around ASLR.
3. **FILE Structure Manipulation**: The attacker manipulates glibc's internal `_IO_FILE`
   structures to redirect execution flow to attacker-controlled code.
4. **ASLR Bypass**: On 32-bit Linux systems, the ASLR entropy is limited (~16 bits for
   heap addresses), making brute-force feasible. The exploit requires approximately 10,000
   attempts on average.
5. **Privilege Escalation**: Since sshd runs as root, successful exploitation yields a
   root shell.

**Important 32-bit Constraint**: The described exploit is demonstrated on 32-bit Linux
with glibc. On 64-bit Linux systems with full ASLR (56-bit entropy), the attack is
significantly harder and not yet demonstrated in a reliable automated fashion.

### Timing Requirements

The race condition window is narrow. Qualys researchers demonstrated exploitation in a
laboratory environment in approximately 6-8 hours total, including:
- ~1-2 hours for heap profiling and alignment
- ~4-6 hours of actual brute-force connection attempts (~10,000 tries)
- The entire exploitation chain requires precise timing control

**Note on bot-summarized timing claims**: Some automated summaries have incorrectly
stated exploitation times of "30 minutes" or "less than 1 hour." These are inaccurate.
The authoritative exploitation time from Qualys research is 6-8 hours in a controlled
laboratory environment. See section "References and Authoritative Sources" below.

---

## Affected Versions

### OpenSSH Version Matrix

| Version Range | Status | Notes |
|---|---|---|
| < 4.4p1 | Vulnerable (original CVE-2006-5051) | Historical only |
| 4.4p1 – 8.4p1 | Not vulnerable | Protected by DO_LOG_SAFE_IN_SIGHAND |
| 8.5p1 – 9.7p1 | VULNERABLE (CVE-2024-6387) | Regression introduced Oct 2020 |
| 9.8p1 | FIXED | Official patch, released 2024-07-01 |

**OpenBSD**: OpenBSD systems are NOT affected because OpenBSD sshd uses a different
signal handling mechanism that does not exhibit this race condition.

**glibc dependency**: The vulnerability is exploitable only on systems using glibc.
musl libc systems may not be exploitable via the documented technique.

---

## Internet Exposure Analysis

Qualys' global scanning infrastructure identified approximately **14,000,000** (14 million)
internet-facing SSH servers potentially running vulnerable OpenSSH versions. Among Qualys
customer environments, approximately 700,000 external instances were found vulnerable,
representing roughly 31% of monitored external SSH endpoints.

### Version Distribution (representative sample from Qualys scan)

| OpenSSH Version | Approximate Share |
|---|---|
| 8.7p1 (RHEL 8) | 18% |
| 8.9p1 (Ubuntu 22.04) | 15% |
| 9.3p2 | 12% |
| 9.6p1 | 11% |
| 8.8p1 | 9% |
| Other 8.5p1–9.7p1 | 35% |

---

## Remediation Guidance

### Primary Remediation: Upgrade to OpenSSH 9.8p1

The definitive fix is to upgrade to OpenSSH 9.8p1, released 2024-07-01, which properly
re-introduces the async-signal-safe guard in the signal handler code.

### Workaround (Temporary Mitigation)

If immediate patching is not possible:

```
# In /etc/ssh/sshd_config
LoginGraceTime 0
```

Setting `LoginGraceTime 0` disables the authentication grace period timeout, eliminating
the SIGALRM signal delivery that triggers the race condition. The signal handler code path
is never reached.

**IMPORTANT DoS Risk**: Setting `LoginGraceTime 0` means that unauthenticated connections
are never timed out. This creates a Denial-of-Service risk: an attacker can exhaust sshd's
connection slots by holding connections open indefinitely. Organizations with strict
availability requirements should weigh this risk carefully.

After editing sshd_config, restart the service:
```
systemctl restart sshd
```

### New Features in OpenSSH 9.8p1

The fix release introduces:
- `PerSourcePenalties`: Rate-limits connections from individual source IPs
- `PerSourcePenaltyExemptList`: Whitelist for trusted networks

These features provide defense-in-depth against brute-force attacks even if the race
condition were to re-emerge.

---

## Vendor Patches

| Vendor | Patch ID | Fixed Package | Release Date |
|---|---|---|---|
| Red Hat Enterprise Linux 9 | RHSA-2024:4312 | openssh-8.7p1-38.el9_4.1 | 2024-07-03 |
| Red Hat Enterprise Linux 8 | RHSA-2024:4340 | openssh-8.0p1-19.el8_10.1 | 2024-07-05 |
| Ubuntu | USN-6859-1 | openssh-server 9.6p1-3ubuntu13.3 | 2024-07-01 |
| Debian | DSA-5724-1 | openssh 1:9.7p1-7 | 2024-07-09 |
| SUSE | SUSE-SU-2024:2308-1 | openssh 9.6p1-150600.3.3.1 | 2024-07-04 |

---

## References and Authoritative Sources

1. NVD: https://nvd.nist.gov/vuln/detail/CVE-2024-6387
2. GHSA: https://github.com/advisories/GHSA-2x8c-95vh-gfv4
3. Qualys Blog: https://blog.qualys.com/vulnerabilities-threat-research/2024/07/01/regresshion-remote-unauthenticated-code-execution-vulnerability-in-openssh-server
4. oss-security: https://www.openwall.com/lists/oss-security/2024/07/01/3
5. OpenSSH 9.8 Release: https://www.openssh.org/txt/release-9.8
6. Regression commit: https://github.com/openssh/openssh-portable/commit/752250caabda3dd24635503c4cd689b32a650794
7. CVE-2006-5051 (original): https://github.com/advisories/GHSA-mq5h-r3rg-j9hg
8. RHSA-2024:4312: https://access.redhat.com/errata/RHSA-2024:4312

---

## Disclosure Timeline

| Date | Event |
|---|---|
| 2020-10-16 | Regression introduced in commit 752250c (OpenSSH log infrastructure refactor) |
| 2021-02 | OpenSSH 8.5p1 released (regression included, vulnerability present) |
| 2024-05 | Qualys TRU internally discovers and reproduces the vulnerability |
| 2024-06 | Coordinated disclosure with OpenSSH and major Linux distributions |
| 2024-07-01 | Public disclosure (NVD, GHSA, Qualys blog, oss-security) |
| 2024-07-01 | OpenSSH 9.8p1 released (fix) |
| 2024-07-03 | Red Hat RHSA-2024:4312 (RHEL 9) |
| 2024-07-05 | Red Hat RHSA-2024:4340 (RHEL 8) |

---

*This report was prepared by the Qualys Threat Research Unit. All exploitation metrics
(10,000 attempts, 6-8 hours) are based on controlled laboratory conditions on 32-bit
glibc-based Linux. Results on production systems may vary.*
"""

    qualys_content = qualys_text + """
---

## Extended Technical Analysis: Signal Handler Safety

### async-signal-safe Functions

POSIX.1-2008 defines a set of functions that are safe to call from within signal handlers.
These functions are guaranteed to be re-entrant and will not cause undefined behavior even
if the interrupted thread was executing in a non-re-entrant context (such as malloc()).

The complete list includes: `_exit`, `access`, `alarm`, `close`, `dup`, `dup2`, `execle`,
`execve`, `fork`, `fstat`, `getegid`, `geteuid`, `getgid`, `getgroups`, `getpgrp`,
`getpid`, `getppid`, `getuid`, `kill`, `link`, `lseek`, `mkdir`, `mkfifo`, `open`,
`pathconf`, `pause`, `pipe`, `raise`, `read`, `rename`, `rmdir`, `setgid`, `setpgid`,
`setsid`, `setuid`, `sigaction`, `sigaddset`, `sigdelset`, `sigemptyset`, `sigfillset`,
`sigismember`, `signal`, `sigpending`, `sigprocmask`, `sigsuspend`, `sleep`, `stat`,
`symlink`, `sysconf`, `tcdrain`, `tcflow`, `tcflush`, `tcgetattr`, `tcgetpgrp`,
`tcsendbreak`, `tcsetattr`, `tcsetpgrp`, `time`, `times`, `umask`, `uname`, `unlink`,
`utime`, `wait`, `waitpid`, `write`.

Notably ABSENT from this list: `malloc`, `free`, `syslog`, `printf`, `fprintf`.

### The `sshsigdie()` Function

In vulnerable versions of OpenSSH (8.5p1–9.7p1), the `sshsigdie()` function appeared as:

```c
/* REMOVED: the original protection guard
#ifdef DO_LOG_SAFE_IN_SIGHAND
*/
void
sshsigdie(const char *file, const char *func, int line, ...) {
    va_list args;
    char fmtbuf[256];
    const char *fmt = NULL;

    va_start(args, line);
    /* ... format string setup ... */
    va_end(args);

    syslog(LOG_CRIT, "%s", fmtbuf);  /* NOT async-signal-safe! */
    _exit(1);
}
/* REMOVED: closing #endif */
```

The `DO_LOG_SAFE_IN_SIGHAND` macro guard was meant to compile out the syslog() call in
signal handler context, leaving only `_exit(1)` (which IS async-signal-safe). Without
the guard, `syslog()` is called directly from the signal handler.

### Heap State Corruption Mechanism

When sshd is handling an authentication timeout (SIGALRM → sigdie() → sshsigdie()):

1. The main execution thread may be inside `malloc()` or `free()` at the moment of signal delivery
2. These functions hold internal locks (specifically `__malloc_lock` or its equivalent)
3. `syslog()` internally calls `malloc()` (for formatting, buffer allocation)
4. When `malloc()` is called re-entrantly (from within the signal handler while the main
   thread is already in malloc), the internal lock is already held by the current thread
5. On Linux with POSIX threads, `__malloc_lock` is a recursive mutex — re-entrancy does
   NOT deadlock, but it can corrupt the free list or bin pointers in the heap metadata

### Glibc FILE Structure Exploitation

The specific exploitation technique leverages the `_IO_FILE` structure in glibc's stdio:

```c
struct _IO_FILE {
    int _flags;                     /* High-order word is _IO_MAGIC; rest is flags. */
    char *_IO_read_ptr;             /* Current read pointer */
    char *_IO_read_end;             /* End of get area. */
    char *_IO_read_base;            /* Start of putback+get area. */
    char *_IO_write_base;           /* Start of put area. */
    char *_IO_write_ptr;            /* Current put pointer. */
    char *_IO_write_end;            /* End of put area. */
    /* ... more fields ... */
    const struct _IO_jump_t *_vtable;  /* Virtual function table */
};
```

By corrupting the `_vtable` pointer to point to attacker-controlled data, the exploit
can redirect execution when glibc calls any virtual function on the FILE structure
(e.g., during `fclose()` or during output flushing).

---

## Mitigation Assessment: MaxStartups Alternative

OpenSSH provides another defense-in-depth mechanism: `MaxStartups`. This setting controls
the maximum number of concurrent unauthenticated connections:

```
# /etc/ssh/sshd_config
MaxStartups 10:30:100
```

Format: `start:rate:full`
- `10`: Allow up to 10 unauthenticated connections without throttling
- `30`: Drop new connections with 30% probability when above 10 connections
- `100`: Hard maximum of 100 concurrent unauthenticated connections

**Effectiveness**: While `MaxStartups` does not eliminate the race condition, it limits
the rate of attack attempts, increasing the time required for exploitation from hours
to potentially weeks or months.

**Advantage over LoginGraceTime 0**: Unlike `LoginGraceTime 0`, `MaxStartups` does not
create an explicit DoS vector. Legitimate users with slow connections are not permanently
blocked; they are rate-limited during periods of high connection volume.

---

## Comparison: CVE-2024-6387 vs CVE-2024-6409

While analyzing regreSSHion, researchers also identified a related but distinct vulnerability:

**CVE-2024-6409**: Signal handler race condition in OpenSSH privilege separation child process.
- Affects: OpenSSH 8.7 and 8.8 specifically (RHEL 8 backport versions)
- Scope: Affects the privilege-separated child process (not the main sshd)
- Impact: Lower severity than CVE-2024-6387 due to reduced privileges of the child process
- CVSS Score: 7.0 (High) — lower than CVE-2024-6387's 8.1
- Note: The affected version range is narrower and the exploitability is reduced

This is distinct from CVE-2024-6387 which affects the main sshd process directly.
Do NOT conflate these two CVEs — they have different affected version ranges and different
CVSS scores.

---
"""

    w(WS / "assets" / "advisories" / "qualys_regresshion_report.txt", qualys_content)

    # Red Hat Errata JSON — RHEL 9（真实锚点：RHSA-2024:4312, openssh-8.7p1-38.el9_4.1, 2024-07-03）
    wj(WS / "assets" / "advisories" / "redhat_RHSA-2024-4312.json", {
        "errata_id": "RHSA-2024:4312",
        "severity": "Important",
        "issued": "2024-07-03",
        "description": (
            "An update for openssh is now available for Red Hat Enterprise Linux 9. "
            "Red Hat Product Security has rated this update as having a security impact "
            "of Important. A Common Vulnerability Scoring System (CVSS) base score, which "
            "gives a detailed severity rating, is available for each vulnerability from the "
            "CVE link(s) in the References section."
        ),
        "packages": {
            "x86_64": [
                "openssh-8.7p1-38.el9_4.1.x86_64.rpm",
                "openssh-clients-8.7p1-38.el9_4.1.x86_64.rpm",
                "openssh-server-8.7p1-38.el9_4.1.x86_64.rpm",
                "openssh-keycat-8.7p1-38.el9_4.1.x86_64.rpm"
            ],
            "s390x": [
                "openssh-8.7p1-38.el9_4.1.s390x.rpm",
                "openssh-server-8.7p1-38.el9_4.1.s390x.rpm"
            ],
            "ppc64le": [
                "openssh-8.7p1-38.el9_4.1.ppc64le.rpm",
                "openssh-server-8.7p1-38.el9_4.1.ppc64le.rpm"
            ],
            "aarch64": [
                "openssh-8.7p1-38.el9_4.1.aarch64.rpm",
                "openssh-server-8.7p1-38.el9_4.1.aarch64.rpm"
            ]
        },
        "fixed_package_version": "openssh-8.7p1-38.el9_4.1",
        "affects": ["Red Hat Enterprise Linux 9"],
        "cves": ["CVE-2024-6387"],
        "advisory_url": "https://access.redhat.com/errata/RHSA-2024:4312",
        "_note": "Source: https://access.redhat.com/errata/RHSA-2024:4312"
    })

    # openwall oss-security 邮件全文
    w(WS / "assets" / "advisories" / "openwall_disclosure.txt", """From: Saeed Abbasi <saeed.abbasi@qualys.com>
To: oss-security@openwall.com
Date: Mon, 01 Jul 2024 00:00:00 +0000
Subject: CVE-2024-6387 - RCE in OpenSSH's server, on glibc-based Linux systems

==========================================================================
CVE-2024-6387 — Remote Unauthenticated Code Execution in OpenSSH Server
==========================================================================

VULNERABILITY OVERVIEW
-----------------------

A security regression was discovered in OpenSSH's server (sshd). The vulnerability
is a signal handler race condition (CWE-362, CWE-364) that can lead to remote code
execution with root privileges on glibc-based Linux systems.

AFFECTED VERSIONS
-----------------

Vulnerable: OpenSSH 8.5p1 <= version < 9.8p1
  (all releases from 8.5p1 through 9.7p1, on glibc-based Linux only)

Fixed: OpenSSH >= 9.8p1

OpenBSD systems are NOT affected.

TECHNICAL DETAILS
-----------------

The vulnerability is a regression of CVE-2006-5051. The regression was introduced in
OpenSSH 8.5p1 by commit 752250caabda3dd24635503c4cd689b32a650794 (2020-10-16),
which modified the log infrastructure and accidentally removed the
DO_LOG_SAFE_IN_SIGHAND protection from sshsigdie().

The SIGALRM signal handler (triggered by LoginGraceTime expiration) calls syslog(),
which is not async-signal-safe. This creates a race condition exploitable when the
signal is delivered while the main thread is executing within glibc's allocator.

Exploitation requires approximately 10,000 connection attempts due to the probabilistic
nature of the race condition. Laboratory exploitation time was approximately 6-8 hours
on 32-bit glibc-based Linux with ASLR enabled.

WORKAROUND
----------

Set LoginGraceTime 0 in /etc/ssh/sshd_config and restart sshd.
Note: This disables authentication timeout and may create DoS risk.

TIMELINE
--------

2020-10-16: Regression introduced (commit 752250c)
2021-02: OpenSSH 8.5p1 released (vulnerability present)
2024-07-01: Public disclosure
2024-07-01: OpenSSH 9.8p1 released (fix)

CREDITS
-------

Discovered by Qualys Threat Research Unit (TRU).
CVE assigned by Red Hat.

REFERENCES
----------

1. https://nvd.nist.gov/vuln/detail/CVE-2024-6387
2. https://www.openssh.org/txt/release-9.8
3. https://blog.qualys.com/vulnerabilities-threat-research/2024/07/01/regresshion-remote-unauthenticated-code-execution-vulnerability-in-openssh-server
4. https://github.com/openssh/openssh-portable/commit/752250caabda3dd24635503c4cd689b32a650794
5. CVE-2006-5051 (original vulnerability): https://github.com/advisories/GHSA-mq5h-r3rg-j9hg
""")


# ── 3. 扫描结果数据（确定性合成，大体量） ───────────────────────────────────
def gen_scan_data() -> None:
    rng = random.Random(6387)

    # internal_inventory.csv — 内网资产清单（500 台主机）
    VULNERABLE_VERSIONS = [
        "OpenSSH_8.5p1", "OpenSSH_8.6p1", "OpenSSH_8.7p1", "OpenSSH_8.8p1",
        "OpenSSH_8.9p1", "OpenSSH_9.0p1", "OpenSSH_9.1p1", "OpenSSH_9.2p1",
        "OpenSSH_9.3p2", "OpenSSH_9.4p1", "OpenSSH_9.5p1", "OpenSSH_9.6p1",
        "OpenSSH_9.7p1"
    ]
    SAFE_VERSIONS = [
        "OpenSSH_9.8p1", "OpenSSH_7.4p1", "OpenSSH_8.4p1",
        "OpenSSH_8.3p1", "OpenSSH_7.9p1"
    ]
    OS_TYPES = [
        "RHEL 9", "RHEL 8", "Ubuntu 22.04", "CentOS 7", "Debian 12",
        "RHEL 7", "Ubuntu 20.04", "Amazon Linux 2"
    ]
    ENVS = ["prod"] * 40 + ["staging"] * 25 + ["dev"] * 35  # weights: prod 40%, staging 25%, dev 35%

    TEAMS = ["sre", "backend", "data-infra", "security", "ml-platform",
             "devops", "api", "frontend-infra", "database", "monitoring"]

    rows = [["hostname", "ip", "ssh_version", "os", "env", "owner", "is_vulnerable"]]

    prod_vuln_count = 0
    for i in range(500):
        env = rng.choice(ENVS)
        # 70% vulnerable
        if rng.random() < 0.70:
            ver = rng.choice(VULNERABLE_VERSIONS)
            vuln = "true"
            if env == "prod":
                prod_vuln_count += 1
        else:
            ver = rng.choice(SAFE_VERSIONS)
            vuln = "false"

        os_type = rng.choice(OS_TYPES)
        team = rng.choice(TEAMS)
        host_num = i + 1
        env_prefix = {"prod": "p", "staging": "s", "dev": "d"}[env]
        hostname = f"host-{env_prefix}{host_num:04d}.internal.example.com"
        ip = f"10.{rng.randint(1, 50)}.{rng.randint(1, 254)}.{rng.randint(1, 254)}"
        rows.append([hostname, ip, ver, os_type, env, team, vuln])

    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(WS / "assets" / "scan_results" / "internal_inventory.csv", buf.getvalue())

    # Store the prod vulnerable count as a reference
    w(WS / "assets" / "scan_results" / "_inventory_meta.txt",
      f"Generated: 2024-07-02\n"
      f"Total hosts: 500\n"
      f"Prod-env vulnerable hosts: {prod_vuln_count}\n"
      f"Note: Vulnerable range = OpenSSH 8.5p1 to 9.7p1 (inclusive)\n")

    # Shodan export JSON（2000+ 条目，~15k tokens）
    ORGS = [
        "Alibaba Cloud", "Amazon", "Tencent Cloud", "Microsoft Azure", "Google Cloud",
        "DigitalOcean", "OVH SAS", "Hetzner Online", "Linode", "Vultr Holdings",
        "China Unicom", "China Telecom", "NTT Communications", "Deutsche Telekom",
        "Cloudflare", "Fastly", "Akamai", "Lumen Technologies", "CenturyLink",
        "Korea Telecom"
    ]
    COUNTRIES = ["US", "CN", "DE", "JP", "GB", "FR", "NL", "CA", "AU", "KR",
                 "IN", "BR", "RU", "SG", "SE", "CH", "IT", "ES", "PL", "TW"]

    shodan_entries = []
    for i in range(220):
        if rng.random() < 0.72:
            ver_str = rng.choice(VULNERABLE_VERSIONS)
            vuln_tags = [CVE_ID]
        else:
            ver_str = rng.choice(SAFE_VERSIONS)
            vuln_tags = []

        entry = {
            "ip": f"{rng.randint(1, 220)}.{rng.randint(1, 254)}.{rng.randint(1, 254)}.{rng.randint(1, 254)}",
            "port": 22,
            "version": ver_str,
            "banner": f"SSH-2.0-{ver_str} Ubuntu-1ubuntu4.3" if rng.random() < 0.4 else f"SSH-2.0-{ver_str}",
            "os": rng.choice(["Linux", "Linux", "Linux", "FreeBSD"]),
            "location": {
                "country_code": rng.choice(COUNTRIES),
                "city": f"City-{rng.randint(1, 500)}"
            },
            "org": rng.choice(ORGS),
            "vulns": vuln_tags,
            "timestamp": f"2024-07-02T{rng.randint(0, 23):02d}:{rng.randint(0, 59):02d}:00Z"
        }
        shodan_entries.append(entry)

    wj(WS / "assets" / "scan_results" / "shodan_export_2024-07-02.json", {
        "query": f"port:22 product:OpenSSH",
        "scan_date": "2024-07-02",
        "total_results": len(shodan_entries),
        "note": "Synthesized from Qualys internet exposure report. ~14 million total estimated vulnerable instances globally.",
        "results": shodan_entries
    })

    # nmap 扫描输出
    nmap_lines = ["# Nmap 7.95 scan initiated 2024-07-02 09:00:00 as: nmap -sV -p 22 -iL targets.txt",
                  "Nmap scan report for scan-sample (10.0.0.0/16 representative)", ""]
    for i in range(80):
        if rng.random() < 0.68:
            ver = rng.choice(VULNERABLE_VERSIONS)
            state = "open"
        else:
            ver = rng.choice(SAFE_VERSIONS)
            state = "open"
        ip = f"10.{rng.randint(1, 50)}.{rng.randint(1, 254)}.{rng.randint(1, 254)}"
        nmap_lines.append(f"Nmap scan report for {ip}")
        nmap_lines.append(f"Host is up (0.{rng.randint(1, 9)}ms latency).")
        nmap_lines.append(f"PORT   STATE SERVICE VERSION")
        nmap_lines.append(f"22/tcp {state}  ssh     {ver} Ubuntu Linux; protocol 2.0")
        nmap_lines.append("")
    nmap_lines.append(f"# Nmap done: 80 IP addresses (80 hosts up) scanned in {rng.randint(120, 300)} seconds")
    w(WS / "assets" / "scan_results" / "nmap_ssh_scan_20240702.txt", "\n".join(nmap_lines))

    # SSH access log（~50k tokens：模拟过去 30 天的 sshd 认证日志，含大量认证失败记录）
    rng3 = random.Random(2024)
    REMOTE_IPS = [f"{rng3.randint(1,220)}.{rng3.randint(1,254)}.{rng3.randint(1,254)}.{rng3.randint(1,254)}" for _ in range(200)]
    USERS = ["root", "admin", "ubuntu", "ec2-user", "centos", "sysadmin",
             "deploy", "git", "backup", "oracle", "postgres", "www-data"]
    VALID_USERS = ["alice", "bob", "carol", "dave", "eve", "sre-user", "deploy-ci"]
    log_lines = ["# /var/log/auth.log — SSH authentication log (past 30 days)",
                 "# Exported for CVE-2024-6387 incident analysis — 2024-07-02",
                 "# Note: Increased scanning activity observed from 2024-06-20 onwards",
                 ""]
    months = ["Jun", "Jul"]
    for day in range(1, 20):
        m = "Jun"
        d = day
        for hour in range(0, 24, 3):
            n_events = rng3.randint(8, 20)
            for _ in range(n_events):
                minute = rng3.randint(0, 59)
                second = rng3.randint(0, 59)
                ip = rng3.choice(REMOTE_IPS)
                if rng3.random() < 0.85:
                    user = rng3.choice(USERS)
                    port = rng3.randint(50000, 65535)
                    log_lines.append(
                        f"{m} {d:2d} {hour:02d}:{minute:02d}:{second:02d} prod-host sshd[{rng3.randint(1000,9999)}]: "
                        f"Failed password for invalid user {user} from {ip} port {port} ssh2"
                    )
                elif rng3.random() < 0.5:
                    user = rng3.choice(VALID_USERS)
                    port = rng3.randint(50000, 65535)
                    log_lines.append(
                        f"{m} {d:2d} {hour:02d}:{minute:02d}:{second:02d} prod-host sshd[{rng3.randint(1000,9999)}]: "
                        f"Accepted publickey for {user} from {ip} port {port} ssh2: RSA SHA256:{rng3.randint(1000000,9999999)}"
                    )
                else:
                    log_lines.append(
                        f"{m} {d:2d} {hour:02d}:{minute:02d}:{second:02d} prod-host sshd[{rng3.randint(1000,9999)}]: "
                        f"Connection closed by authenticating user root {ip} port {rng3.randint(50000,65535)} [preauth]"
                    )
    w(WS / "assets" / "scan_results" / "auth_log_30days.txt", "\n".join(log_lines))


# ── 4. 代码样本（漏洞版本 vs 修复版本对比） ───────────────────────────────────
def gen_code_samples() -> None:
    w(WS / "assets" / "code_samples" / "sshd_sigdie_vulnerable.c", """/*
 * sshd_sigdie_vulnerable.c — OpenSSH 8.5p1 to 9.7p1 (vulnerable to CVE-2024-6387)
 *
 * This excerpt shows the VULNERABLE version of sshsigdie() AFTER commit
 * 752250caabda3dd24635503c4cd689b32a650794 (2020-10-16) removed the
 * DO_LOG_SAFE_IN_SIGHAND protection.
 *
 * Source: openssh-portable, log.c (vulnerable versions)
 */

#include <stdarg.h>
#include <syslog.h>
#include <stdlib.h>
#include "log.h"

/* BUG: The #ifdef DO_LOG_SAFE_IN_SIGHAND guard was REMOVED by commit 752250c.
 * syslog() is NOT async-signal-safe. Calling it from a signal handler creates
 * a race condition exploitable when the main thread is inside malloc()/free().
 */
void
sshsigdie(const char *file, const char *func, int line,
    struct ssh *ssh, const char *tag, int r, const char *fmt, ...)
{
    va_list args;
    char fmtbuf[MSGBUFSIZ];

    /* This block was NOT protected by #ifdef DO_LOG_SAFE_IN_SIGHAND */
    if (fmt != NULL) {
        va_start(args, fmt);
        vsnprintf(fmtbuf, sizeof(fmtbuf), fmt, args);
        va_end(args);
        syslog(LOG_CRIT, "%.500s", fmtbuf);  /* NOT async-signal-safe! */
    }
    _exit(1);
}

/*
 * SIGALRM handler — called when LoginGraceTime expires
 * This calls sigdie() which calls sshsigdie() which calls syslog()
 */
static void
grace_alarm_handler(int sig)
{
    ssh_signal(SIGALRM, SIG_DFL);
    sigdie("Timeout before authentication for %s port %d",
        ssh_remote_ipaddr(the_active_state),
        ssh_remote_port(the_active_state));
    /* sigdie() -> sshsigdie() -> syslog() [race condition here!] -> _exit(1) */
}
""")

    w(WS / "assets" / "code_samples" / "sshd_sigdie_patched.c", """/*
 * sshd_sigdie_patched.c — OpenSSH 9.8p1 (fixed, CVE-2024-6387 remediated)
 *
 * This excerpt shows the PATCHED version of sshsigdie() which restores the
 * DO_LOG_SAFE_IN_SIGHAND protection removed in commit 752250c.
 *
 * The fix ensures that when called from a signal handler context, syslog()
 * is skipped and only _exit(1) is called (which IS async-signal-safe).
 *
 * Source: openssh-portable 9.8p1, log.c
 */

#include <stdarg.h>
#include <syslog.h>
#include <stdlib.h>
#include "log.h"

void
sshsigdie(const char *file, const char *func, int line,
    struct ssh *ssh, const char *tag, int r, const char *fmt, ...)
{
#ifdef DO_LOG_SAFE_IN_SIGHAND
    /* FIX: The DO_LOG_SAFE_IN_SIGHAND guard is RESTORED.
     * When called from a signal handler, the syslog() call is compiled out.
     * Only _exit(1) remains, which is async-signal-safe.
     *
     * In non-signal-handler contexts (where DO_LOG_SAFE_IN_SIGHAND is not
     * defined), the full logging is preserved for diagnostics.
     */
    va_list args;
    char fmtbuf[MSGBUFSIZ];

    if (fmt != NULL) {
        va_start(args, fmt);
        vsnprintf(fmtbuf, sizeof(fmtbuf), fmt, args);
        va_end(args);
        syslog(LOG_CRIT, "%.500s", fmtbuf);
    }
#endif /* DO_LOG_SAFE_IN_SIGHAND */
    _exit(1);  /* async-signal-safe: always execute this */
}

/*
 * SIGALRM handler in 9.8p1 — now safe
 * sshsigdie() called with DO_LOG_SAFE_IN_SIGHAND defined, so syslog()
 * is skipped; only _exit(1) executes.
 */
static void
grace_alarm_handler(int sig)
{
    ssh_signal(SIGALRM, SIG_DFL);
    sigdie("Timeout before authentication for %s port %d",
        ssh_remote_ipaddr(the_active_state),
        ssh_remote_port(the_active_state));
    /* Now: sigdie() -> sshsigdie() -> _exit(1) [safe!] */
}
""")

    w(WS / "assets" / "code_samples" / "signal_handler_analysis.md", """# Signal Handler Safety Analysis: CVE-2024-6387

## Summary

CVE-2024-6387 is a signal handler race condition in OpenSSH's server (sshd) affecting
versions 8.5p1 through 9.7p1 on glibc-based Linux systems.

## Root Cause

### The Original Protection (pre-2020)

OpenSSH 4.4p1 through 8.4p1 used a compile-time macro `DO_LOG_SAFE_IN_SIGHAND` to
guard calls to non-async-signal-safe functions within signal handlers:

```c
#ifdef DO_LOG_SAFE_IN_SIGHAND
    syslog(LOG_CRIT, "%.500s", fmtbuf);  /* Only in non-signal contexts */
#endif
    _exit(1);  /* Always safe */
```

This ensured that when called from a signal handler, only `_exit(1)` (which is
async-signal-safe per POSIX.1-2008) was executed.

### The Regression (Commit 752250caabda3dd24635503c4cd689b32a650794)

On 2020-10-16, Damien Miller committed a log infrastructure refactor. The commit
removed the `#ifdef DO_LOG_SAFE_IN_SIGHAND` guard from `sshsigdie()`, making `syslog()`
unconditionally callable from signal handler context.

**Commit details:**
- Hash: 752250caabda3dd24635503c4cd689b32a650794
- Author: Damien Miller (djmdjm@mindrot.org)
- Date: 2020-10-16
- Subject: "upstream: revised log infrastructure for OpenSSH"
- Files changed: 7 files, 154 additions, 133 deletions

This reintroduced CVE-2006-5051 — the original signal handler race condition fixed in 2006.

## POSIX Signal Safety Reference

Functions guaranteed async-signal-safe (POSIX.1-2008, relevant subset):
- `_exit(status)` ✓ — immediate process termination
- `write(fd, buf, count)` ✓ — raw I/O
- `kill(pid, sig)` ✓ — signal delivery
- `getpid()` ✓ — process ID query

Functions NOT async-signal-safe (may cause corruption if called from signal handler):
- `syslog()` ✗ — calls malloc() internally
- `malloc()` / `free()` ✗ — heap operations with internal locks
- `printf()` / `fprintf()` ✗ — buffered I/O with locking
- `fopen()` / `fclose()` ✗ — FILE* operations

## Fix Applied in 9.8p1

The fix reinstates `#ifdef DO_LOG_SAFE_IN_SIGHAND` in `sshsigdie()`, ensuring:
1. In signal handler context: only `_exit(1)` is called (async-signal-safe)
2. In normal logging context: full `syslog()` diagnostics are preserved
""")


# ── 5. 合规文档 ──────────────────────────────────────────────────────────────
def gen_compliance_docs() -> None:
    w(WS / "assets" / "compliance" / "cvss_calculation_worksheet.md", """# CVSS v3.1 Calculation Worksheet: CVE-2024-6387

## Official CVSS Vector
CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H

## Base Score: 8.1 (High)

## Metric Breakdown

| Metric | Code | Value | Description |
|--------|------|-------|-------------|
| Attack Vector | AV | N (Network) | Exploitable remotely over the network (SSH port 22) |
| Attack Complexity | AC | H (High) | Requires race condition timing; ~10,000 attempts needed |
| Privileges Required | PR | N (None) | No authentication required; pre-auth vulnerability |
| User Interaction | UI | N (None) | No user action needed; victim just needs sshd running |
| Scope | S | U (Unchanged) | Exploit stays within the sshd process boundary |
| Confidentiality Impact | C | H (High) | Root RCE gives full read access to all data |
| Integrity Impact | I | H (High) | Root RCE gives full write access |
| Availability Impact | A | H (High) | Root RCE can terminate or disable services |

## Score Calculation

Base Score = ISS = min(1 - [(1-C)(1-I)(1-A)], 0.915)
           = min(1 - [(1-0.56)(1-0.56)(1-0.56)], 0.915)
           = min(1 - 0.085, 0.915)
           = min(0.915, 0.915) = 0.915

Exploitability = 8.22 × AV × AC × PR × UI
               = 8.22 × 0.85 × 0.44 × 0.85 × 0.85
               = 8.22 × 0.270 = 2.220

Base Score (Unchanged Scope) = Roundup(min(ISS + Exploitability, 10))
                             = Roundup(min(0.915 + 2.220, 10))
                             = Roundup(3.135)... [using CVSS formula]

**Final: 8.1 (High)** — as confirmed by NVD official entry.

## Notes
- The AC:H (High Attack Complexity) reflects the probabilistic nature: ~10,000 connection
  attempts needed on average due to race condition timing uncertainty.
- Despite AC:H, the CVSS score is HIGH (8.1) because the impact (C:H/I:H/A:H) is severe.
- Without the complexity factor, the score would be 9.8 (Critical).
""")

    wj(WS / "assets" / "compliance" / "risk_register_template.json", {
        "document_type": "risk_register",
        "version": "1.0",
        "created": "2024-07-02",
        "entries": [
            {
                "risk_id": "RISK-SEC-001",
                "cve_id": "PLACEHOLDER_CVE",
                "title": "Critical SSH vulnerability in production infrastructure",
                "cvss_score": 0.0,
                "risk_level": "PENDING",
                "affected_systems": "PENDING",
                "remediation_status": "OPEN",
                "remediation_deadline": "PENDING",
                "owner": "Lead Security Engineer",
                "notes": "Template — complete with actual CVE data"
            }
        ]
    })


# ── 6. 工具脚本 ──────────────────────────────────────────────────────────────
def gen_scripts() -> None:
    w(WS / "scripts" / "check_vulnerable.sh", """#!/usr/bin/env bash
# check_vulnerable.sh — 检测本机 OpenSSH 版本是否受 CVE-2024-6387 影响
# 受影响范围: 8.5p1 <= openssh < 9.8p1 (glibc-based Linux)

set -euo pipefail

AFFECTED_MIN="8.5p1"
PATCHED_VERSION="9.8p1"
CVE="CVE-2024-6387"

echo "=== SSH Version Vulnerability Check for $CVE ==="

if ! command -v ssh &>/dev/null; then
    echo "ERROR: ssh command not found"
    exit 1
fi

SSH_VERSION=$(ssh -V 2>&1 | grep -oP 'OpenSSH_[0-9]+\\.[0-9]+p[0-9]+')
echo "Detected: $SSH_VERSION"

# Parse version numbers for comparison
MAJOR=$(echo "$SSH_VERSION" | grep -oP '(?<=OpenSSH_)\\d+')
MINOR=$(echo "$SSH_VERSION" | grep -oP '(?<=\\.)\\d+(?=p)')
PATCH=$(echo "$SSH_VERSION" | grep -oP '(?<=p)\\d+')

# Vulnerable: 8.5p1 <= version <= 9.7p1
if [[ "$MAJOR" -eq 8 && "$MINOR" -ge 5 ]] || [[ "$MAJOR" -eq 9 && "$MINOR" -le 7 ]]; then
    echo "RESULT: VULNERABLE to $CVE"
    echo "Recommended: Upgrade to OpenSSH $PATCHED_VERSION or apply workaround (LoginGraceTime 0)"
    exit 1
else
    echo "RESULT: NOT VULNERABLE to $CVE"
    echo "Current version $SSH_VERSION is either pre-regression or patched."
    exit 0
fi
""")

    w(WS / "scripts" / "patch_audit.py", """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
patch_audit.py — 批量审计内网资产清单，统计 CVE-2024-6387 漏洞暴露情况。
输入: assets/scan_results/internal_inventory.csv
输出: 按环境分组的漏洞统计报告
\"\"\"
import csv
import sys
from pathlib import Path
from collections import defaultdict


AFFECTED_VERSIONS = {
    "OpenSSH_8.5p1", "OpenSSH_8.6p1", "OpenSSH_8.7p1", "OpenSSH_8.8p1",
    "OpenSSH_8.9p1", "OpenSSH_9.0p1", "OpenSSH_9.1p1", "OpenSSH_9.2p1",
    "OpenSSH_9.3p2", "OpenSSH_9.4p1", "OpenSSH_9.5p1", "OpenSSH_9.6p1",
    "OpenSSH_9.7p1"
}


def main():
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    inventory = ws / "assets" / "scan_results" / "internal_inventory.csv"

    if not inventory.exists():
        print(f"ERROR: {inventory} not found")
        sys.exit(1)

    by_env = defaultdict(lambda: {"total": 0, "vulnerable": 0})
    with inventory.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            env = row.get("env", "unknown")
            by_env[env]["total"] += 1
            if row.get("ssh_version", "") in AFFECTED_VERSIONS:
                by_env[env]["vulnerable"] += 1

    print(f"CVE-2024-6387 Exposure Audit")
    print(f"{'Environment':<12} {'Total':>8} {'Vulnerable':>12} {'Pct':>8}")
    print("-" * 44)
    for env in ["prod", "staging", "dev"]:
        stats = by_env.get(env, {"total": 0, "vulnerable": 0})
        pct = 100.0 * stats["vulnerable"] / stats["total"] if stats["total"] > 0 else 0
        print(f"{env:<12} {stats['total']:>8} {stats['vulnerable']:>12} {pct:>7.1f}%")


if __name__ == "__main__":
    main()
""")

    w(WS / "scripts" / "generate_report.py", """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
generate_report.py — 从 work/ 目录的产物生成最终 HTML 或 Markdown 报告。
\"\"\"
import json
import sys
from pathlib import Path
from datetime import datetime


def main():
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    work = ws / "work"

    vuln_file = work / "vuln_summary.json"
    if not vuln_file.exists():
        print("ERROR: work/vuln_summary.json not found. Run through all rounds first.")
        sys.exit(1)

    data = json.loads(vuln_file.read_text(encoding="utf-8"))
    print(f"# Security Report — {data.get('cve_id', 'CVE-UNKNOWN')}")
    print(f"Generated: {datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')}")
    print(f"CVSS Score: {data.get('cvss_score')}")
    print(f"Severity: {data.get('severity')}")


if __name__ == "__main__":
    main()
""")


# ── 7. 模板文件 ──────────────────────────────────────────────────────────────
def gen_templates() -> None:
    w(WS / "templates" / "incident_report_template.md", """# Security Incident Report — Template

**[INCIDENT ID]**: IR-2024-XXXX
**[DATE]**: YYYY-MM-DD
**[SEVERITY]**: Critical / High / Medium / Low
**[STATUS]**: Open / Investigating / Remediated / Closed

---

## TL;DR

[Insert standalone TL;DR paragraph here, ≤200 words. Required for all executive summaries.]

---

## 1. Incident Summary

- **CVE**: [CVE ID in format CVE-YYYY-NNNNN]
- **CVSS Score**: [Score] ([Severity])
- **CVSS Vector**: [Verbatim CVSS vector string]
- **Affected Systems**: [Count and description]
- **Discovery Date**: [YYYY-MM-DD]
- **Disclosure Date**: [YYYY-MM-DD]
- **Remediation Deadline**: [YYYY-MM-DD]

## 2. Technical Details

[Technical description of the vulnerability, exploitation mechanism, and impact]

## 3. Affected Asset Inventory

| Environment | Total Hosts | Vulnerable | Patched | Priority |
|-------------|------------|-----------|---------|----------|
| prod        | X          | Y         | Z       | P1       |
| staging     | X          | Y         | Z       | P2       |
| dev         | X          | Y         | Z       | P3       |

## 4. Remediation Actions

- [ ] Apply vendor patch [ERRATA ID] to all affected hosts
- [ ] Verify patch version [PACKAGE VERSION]
- [ ] Update compliance records
- [ ] Close risk register entry

## 5. References

- [CVE NVD link]
- [Vendor advisory link]
- [Internal documentation links]
""")

    w(WS / "templates" / "patch_verification_checklist.md", """# Patch Verification Checklist — CVE-2024-6387

## Pre-Patch Verification
- [ ] Confirm host is in affected version range (8.5p1 – 9.7p1)
- [ ] Schedule maintenance window
- [ ] Backup current sshd_config
- [ ] Confirm patch availability for OS platform

## Patch Application
- [ ] Apply OS package update (e.g., dnf update openssh)
- [ ] Verify installed version: `ssh -V`
- [ ] For RHEL 9: confirm openssh-8.7p1-38.el9_4.1 installed
- [ ] For RHEL 8: confirm openssh-8.0p1-19.el8_10.1 installed (RHSA-2024:4340)
- [ ] Restart sshd: `systemctl restart sshd`

## Post-Patch Verification
- [ ] Confirm sshd is running: `systemctl status sshd`
- [ ] Verify SSH connectivity (test from bastion host)
- [ ] Confirm version no longer in vulnerable range
- [ ] Update internal_inventory.csv is_vulnerable field

## Documentation
- [ ] Record patch date in remediation tracking
- [ ] Update risk register entry
- [ ] Submit compliance evidence to security team
""")


# ── 8. README ────────────────────────────────────────────────────────────────
def gen_readme() -> None:
    w(WS / "README.md", f"""# sec1 — CVE-2024-6387 (regreSSHion) Vulnerability Analysis & Remediation

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
""")


# ── 9. Sessions（主 + 5 history） ────────────────────────────────────────────
def gen_sessions() -> dict:
    main_id = gen_session_id("main", TID)
    s_slack_alerts = gen_session_id("slack_security_alerts", TID)
    s_slack_incident = gen_session_id("slack_incident_response", TID)
    s_email = gen_session_id("email_management", TID)
    s_feishu_dm = gen_session_id("feishu_sre_bob_dm", TID)
    s_feishu_sre = gen_session_id("feishu_sre_infra_group", TID)

    # 主 session：Alice 指定任务 + 显式声明 P1/P3 偏好
    sb = SessionBuilder(main_id, CWD, "2024-07-02T09:00:00", is_main=True)
    sb.add_user(
        "You are the Lead Security Engineer responding to CVE-2024-6387 (regreSSHion). "
        "This is an emergency incident. We have a critical OpenSSH vulnerability publicly "
        "disclosed today (2024-07-01). I'm Alice Wang, Security Director.\n\n"
        "House preferences (apply throughout all rounds, even when not restated):\n"
        "- P1: All JSON outputs use 2-space indent; top-level fields sorted alphabetically.\n"
        "- P2: CVE IDs in technical reports formatted as CVE-YYYY-NNNNN (hyphenated, uppercase).\n"
        "- P3: All work product filenames use snake_case (no camelCase, no hyphens in filenames).\n"
        "- P4: Progress reports and inventories grouped by environment (prod/staging/dev), prod first.\n"
        "- P5: Executive summaries must include a standalone TL;DR paragraph (≤200 words).\n\n"
        "The workspace contains all advisory files, scan data, and code samples. "
        "Start by reading SOUL.md and the primary advisories. "
        "All deliverables go into work/ using snake_case filenames.\n\n"
        "Your authoritative sources are:\n"
        "1. assets/advisories/NVD_CVE-2024-6387.json (CVSS, CWE, affected range)\n"
        "2. assets/advisories/GHSA-2x8c-95vh-gfv4.json (GHSA ID, EPSS)\n"
        "3. assets/advisories/qualys_regresshion_report.txt (exploitation details)\n"
        "4. assets/advisories/openwall_disclosure.txt (original CVE disclosure)\n\n"
        "Begin with task Q1: parse the NVD advisory and produce work/vuln_summary.json."
    )
    sb.add_assistant(
        "Understood. I am the Lead Security Engineer responding to CVE-2024-6387 (regreSSHion). "
        "I have read SOUL.md and noted the working principles.\n\n"
        "Applied preferences:\n"
        "- P1: All JSON output uses 2-space indent with alphabetically-sorted top-level fields\n"
        "- P2: CVE IDs formatted as CVE-YYYY-NNNNN (e.g., CVE-2024-6387, CVE-2006-5051)\n"
        "- P3: All filenames use snake_case (work/vuln_summary.json, work/affected_assets.csv, etc.)\n"
        "- P4: Progress/inventory reports grouped prod > staging > dev\n"
        "- P5: Executive summaries include standalone TL;DR section ≤200 words\n\n"
        "Proceeding to Q1: parsing NVD_CVE-2024-6387.json and producing work/vuln_summary.json."
    )
    sb.write(SESS / f"{main_id}.jsonl")

    # S2 Slack #security-alerts（CVE 首次告警；P2 偏好注入）
    append_history(
        SESS / f"{s_slack_alerts}.jsonl", s_slack_alerts, CWD, "2024-07-01T08:30:00",
        [
            (
                "[Slack #security-alerts Eve Liu Mon Jul 01 2024 08:30] "
                "🚨 CRITICAL: CVE-2024-6387 (regreSSHion) just dropped. "
                "Qualys says ~14 million internet-facing OpenSSH instances potentially vulnerable. "
                "CVSS 8.1, affects 8.5p1 through 9.7p1. Patch is OpenSSH 9.8p1 released today. "
                "Dave: please start scanning our Shodan data.",
                "Alert received. CVE-2024-6387 is a critical OpenSSH vulnerability. "
                "Starting assessment of our exposure. CVSS 8.1 (High), unauthenticated remote code execution. "
                "Will coordinate with Bob on internal inventory scan."
            ),
            (
                "[Slack #security-alerts Dave Chen Mon Jul 01 2024 09:15] "
                "Quick note on formatting for the incident team: CVE IDs should always be written as "
                "CVE-YYYY-NNNNN format with hyphens and uppercase. I just saw someone write "
                "'cve2024-6387' in a ticket — let's be consistent. "
                "Also I'll have initial Shodan data analysis ready by EOD.",
                "Noted on CVE ID formatting — will use CVE-2024-6387 consistently (CVE-YYYY-NNNNN, hyphenated, uppercase). "
                "Awaiting Dave's Shodan analysis."
            ),
            (
                "[Slack #security-alerts Dave Chen Mon Jul 01 2024 14:00] "
                "BOT_SUMMARY from our CVE monitor: CVE-2024-6387, roughly 30 mins lab exploitation, "
                "affects ~8 million internet instances. [AUTO-GENERATED, NOT VERIFIED] "
                "Note: this is auto-summarized from RSS feed, take with grain of salt.",
                "BOT summary noted but marked as NOT authoritative. Will verify numbers against "
                "Qualys primary report and NVD. The Qualys report states 14 million instances and "
                "6-8 hours lab exploitation time — very different from the bot's numbers."
            ),
        ]
    )

    # S3 Slack #incident-response（含 V5 honey-pot：bot 摘要错误时间 + 错误日期；V6 废弃旧文档引用）
    append_history(
        SESS / f"{s_slack_incident}.jsonl", s_slack_incident, CWD, "2024-07-02T09:00:00",
        [
            (
                "[Slack #incident-response Dave Chen Tue Jul 02 2024 09:00] "
                "Update on regression analysis: per our CVE-scanner bot summary — "
                "the regression was introduced in March 2021 (commit around 2021-03). "
                "[BOT_AUTO_SUMMARY — not manually verified]. "
                "The bot pulled this from a third-party CVE enrichment service.",
                "BOT_AUTO_SUMMARY date flagged as potentially inaccurate. "
                "Per the authoritative oss-security disclosure and GitHub commit history, "
                "the regression commit 752250caabda3dd24635503c4cd689b32a650794 was authored "
                "on 2020-10-16 (October, not March 2021). The bot's '2021-03' date is incorrect."
            ),
            (
                "[Slack #incident-response Dave Chen Tue Jul 02 2024 09:30] "
                "Also per bot: exploitation takes about 30 minutes in a lab. [BOT_AUTO_SUMMARY]",
                "Again, this conflicts with the authoritative Qualys technical report. "
                "Qualys measured 6-8 hours total lab exploitation time on 32-bit glibc Linux. "
                "The '30 minutes' figure from the bot is incorrect — do not use it in reports."
            ),
            (
                "[Slack #incident-response Alice Wang Tue Jul 02 2024 10:00] "
                "Team: for the workaround, please reference the current workaround documentation. "
                "NOTE: There was an older workaround.md in our internal wiki (from a previous scan "
                "in June) that incorrectly recommended `LoginGraceTime 30`. That document is "
                "DEPRECATED — do not use it. The correct mitigation per oss-security is LoginGraceTime 0.",
                "Acknowledged. The older wiki document recommending LoginGraceTime 30 is deprecated. "
                "The authoritative workaround per oss-security and NVD is LoginGraceTime 0. "
                "Will ensure all documentation references the correct value."
            ),
            (
                "[Slack #incident-response Bob Zhang Tue Jul 02 2024 11:00] "
                "Internal patch progress update: prod-host-001 through prod-host-020: "
                "patched (openssh-8.7p1-38.el9_4.1 confirmed). prod-host-021 through prod-host-040: "
                "patch in progress, estimated 2 hours. prod-host-041+: scheduled for tonight.",
                "Patch progress logged. First 20 prod hosts confirmed patched with "
                "openssh-8.7p1-38.el9_4.1 (RHSA-2024:4312). Remaining prod hosts in progress."
            ),
            (
                "[Slack #incident-response Eve Liu Tue Jul 02 2024 14:00] "
                "Staging environment status: staging-001 through staging-050 all patched. "
                "Dev environment: patching deprioritized, scheduled for tomorrow.",
                "Staging fully patched. Dev scheduled. Recording in patch progress tracker."
            ),
        ]
    )

    # S4 邮件（管理层报告请求；P5 偏好注入 + 72h 合规截止）
    append_history(
        SESS / f"{s_email}.jsonl", s_email, CWD, "2024-07-02T08:00:00",
        [
            (
                "[Email alice.wang@company.com → cto@company.com Tue Jul 02 2024 08:00] "
                "Subject: URGENT: CVE-2024-6387 regreSSHion — Board Update Required\n\n"
                "Carol,\n\n"
                "We have a critical SSH vulnerability (CVE-2024-6387) requiring immediate board-level "
                "attention. CVSS 8.1, unauthenticated remote code execution in OpenSSH.\n\n"
                "I need you to request an executive report from our lead security engineer.\n\n"
                "Please note: executive summaries for the board MUST include a standalone TL;DR "
                "paragraph of no more than 200 words at the top. This is a board requirement for "
                "all security incident reports.\n\nAlice",
                "Message logged. Executive report requirement: TL;DR ≤200 words mandatory for board."
            ),
            (
                "[Email cto@company.com → lead-security-engineer@company.com Tue Jul 02 2024 09:00] "
                "Subject: RE: CVE-2024-6387 — Request for Executive Report\n\n"
                "Please provide an executive report on CVE-2024-6387 status. "
                "Include: current exposure assessment, remediation progress, timeline, and risk level. "
                "Board meeting is in 72 hours (compliance deadline: 2024-07-05T09:00Z).\n\n"
                "IMPORTANT: The report MUST include a standalone TL;DR section of no more than "
                "200 words, as per our board communication standards.\n\nCarol",
                "Executive report request received. 72-hour compliance deadline: 2024-07-05T09:00Z. "
                "Will produce work/executive_report.md with mandatory TL;DR ≤200 words."
            ),
        ]
    )

    # S5 Feishu DM Bob（内网扫描数据交接；P4 隐式建议；V2 Update 1 铺垫）
    append_history(
        SESS / f"{s_feishu_dm}.jsonl", s_feishu_dm, CWD, "2024-07-02T10:00:00",
        [
            (
                "[Feishu DM Bob Zhang → Security Lead Tue Jul 02 2024 10:00] "
                "I've run the full internal inventory scan. The CSV is in assets/scan_results/. "
                "When you're compiling the affected assets, please group by environment — "
                "prod first, then staging, then dev. That's the format ops team expects for "
                "the progress reports and compliance checklists.",
                "Noted. Will group by environment (prod > staging > dev) in all progress reports "
                "and compliance outputs. Reading internal_inventory.csv now."
            ),
            (
                "[Feishu DM Bob Zhang → Security Lead Tue Jul 02 2024 10:30] "
                "Quick note: we also have some RHEL 8 hosts. I haven't found a RHEL 8 errata yet "
                "for this CVE. Our RHEL 8 hosts are running OpenSSH 8.7p1 which is in the "
                "affected range. Will send you more info once I find it.",
                "Acknowledged. RHEL 8 hosts with OpenSSH 8.7p1 are vulnerable. "
                "Monitoring for RHEL 8 errata. Will update asset list when errata is confirmed."
            ),
        ]
    )

    # S6 Feishu #sre-infra（PerSourcePenalties 配置讨论 + V6 废弃文档红鲱鱼）
    append_history(
        SESS / f"{s_feishu_sre}.jsonl", s_feishu_sre, CWD, "2024-07-03T09:00:00",
        [
            (
                "[Feishu #sre-infra Bob Zhang Wed Jul 03 2024 09:00] "
                "Team: for the permanent fix, OpenSSH 9.8p1 introduces PerSourcePenalties "
                "and PerSourcePenaltyExemptList as new config options. We should document "
                "these in our post-remediation hardening guide.",
                "Noted. PerSourcePenalties is a new defense-in-depth feature in 9.8p1 that "
                "rate-limits connections from individual source IPs. Will include in hardening docs."
            ),
            (
                "[Feishu #sre-infra Dave Chen Wed Jul 03 2024 09:30] "
                "I found an old DRAFT workaround doc in our confluence: workaround_DRAFT_v0.md "
                "from June 2024 (before the CVE was public). It says to set LoginGraceTime 30. "
                "Should we update it?",
                "That DRAFT document with LoginGraceTime 30 is deprecated and incorrect. "
                "The authoritative workaround is LoginGraceTime 0 (from oss-security/NVD), "
                "and even that is being reconsidered due to DoS risk. "
                "Do NOT reference the June DRAFT document — it should be marked as ARCHIVED."
            ),
        ]
    )

    return {
        "main": main_id,
        "history": [
            (s_slack_alerts, "slack"),
            (s_slack_incident, "slack"),
            (s_email, "email"),
            (s_feishu_dm, "feishu"),
            (s_feishu_sre, "feishu"),
        ],
    }


# ── 10. Updates ──────────────────────────────────────────────────────────────
def gen_updates(sess_ids: dict) -> dict:
    s_feishu_dm = sess_ids["history"][3][0]
    s_slack_incident = sess_ids["history"][1][0]

    # ── Update 1（第 7 轮后）：RHEL 8 受影响范围扩展 ─────────────────────────
    rng = random.Random(4340)
    RHEL8_VULNERABLE_VERSIONS = [
        "OpenSSH_8.0p1", "OpenSSH_8.0p1-8.7p1-backport"
    ]

    # RHEL 8 主机清单 CSV（~4k tokens）
    rhel8_rows = [["hostname", "ip", "ssh_version", "os", "env", "owner", "is_vulnerable", "rhel_version"]]
    for i in range(120):
        env = rng.choice(["prod"] * 40 + ["staging"] * 30 + ["dev"] * 30)
        ver = "OpenSSH_8.0p1"  # RHEL 8 default
        vuln = "true"  # All RHEL 8 with 8.0p1 affected
        ip = f"10.{rng.randint(51, 80)}.{rng.randint(1, 254)}.{rng.randint(1, 254)}"
        env_prefix = {"prod": "r8p", "staging": "r8s", "dev": "r8d"}[env]
        hostname = f"{env_prefix}{i+1:04d}.internal.example.com"
        team = rng.choice(["sre", "backend", "data-infra", "devops"])
        rhel8_rows.append([hostname, ip, ver, "RHEL 8", env, team, vuln, "8.10"])

    buf8 = io.StringIO()
    csv.writer(buf8).writerows(rhel8_rows)
    w(UPD / "upd1_workspace" / "rhel8_inventory.csv", buf8.getvalue())

    # RHSA-2024:4340 JSON（RHEL 8 errata）
    wj(UPD / "upd1_workspace" / "redhat_RHSA-2024-4340.json", {
        "errata_id": "RHSA-2024:4340",
        "severity": "Important",
        "issued": "2024-07-05",
        "description": (
            "An update for openssh is now available for Red Hat Enterprise Linux 8. "
            "Red Hat Product Security has rated this update as having a security impact "
            "of Important. This update fixes CVE-2024-6387."
        ),
        "packages": {
            "x86_64": [
                "openssh-8.0p1-19.el8_10.1.x86_64.rpm",
                "openssh-clients-8.0p1-19.el8_10.1.x86_64.rpm",
                "openssh-server-8.0p1-19.el8_10.1.x86_64.rpm"
            ]
        },
        "fixed_package_version": "openssh-8.0p1-19.el8_10.1",
        "affects": ["Red Hat Enterprise Linux 8"],
        "cves": ["CVE-2024-6387"],
        "advisory_url": "https://access.redhat.com/errata/RHSA-2024:4340",
        "_note": "RHEL 8 errata. Fixed package: openssh-8.0p1-19.el8_10.1"
    })

    # RHEL 8 受影响版本说明 Markdown
    w(UPD / "upd1_workspace" / "rhel8_openssh_versions.md", """# RHEL 8 OpenSSH Vulnerability Status — CVE-2024-6387

## Overview

Red Hat Enterprise Linux 8 ships with OpenSSH 8.0p1 with RHEL backport patches.
The RHEL 8 package is also affected by CVE-2024-6387 due to the same signal handler
race condition being present in the backported code.

## Affected RHEL 8 Package

- **Affected**: openssh-8.0p1-* (all versions before 19.el8_10.1)
- **Fixed**: openssh-8.0p1-19.el8_10.1 (via RHSA-2024:4340, issued 2024-07-05)

## Affected Hosts in Our Environment

Our internal inventory shows 120 RHEL 8 hosts, all running openssh-8.0p1.
All 120 hosts are vulnerable until patched.

## Remediation

Apply RHSA-2024:4340:
```bash
dnf update openssh
# Verify:
rpm -q openssh  # Should show openssh-8.0p1-19.el8_10.1
```

## Notes

- RHEL 8 uses a different base version (8.0p1) from RHEL 9 (8.7p1)
- The errata IDs are different: RHSA-2024:4312 (RHEL 9) vs RHSA-2024:4340 (RHEL 8)
- Both must be tracked in the affected assets list
""")

    # Update 1 Feishu DM 续段（Bob 通知 RHEL 8 errata 发现）
    feishu_upd1_seg = _make_append_segment(
        s_feishu_dm, CWD, "2024-07-05T09:00:00",
        [
            (
                "[Feishu DM Bob Zhang → Security Lead Fri Jul 05 2024 09:00] "
                "Update: Red Hat just released RHSA-2024:4340 for RHEL 8. "
                "Fixed package is openssh-8.0p1-19.el8_10.1. "
                "I've put the errata JSON and RHEL 8 inventory in the update files. "
                "Please update the affected assets list to include our 120 RHEL 8 hosts.",
                "RHEL 8 errata RHSA-2024:4340 received. Fixed package: openssh-8.0p1-19.el8_10.1. "
                "Will update affected_assets_v2.csv to include the 120 RHEL 8 hosts."
            ),
        ]
    )
    w(UPD / "upd1_sessions" / f"{s_feishu_dm}.jsonl", feishu_upd1_seg)

    # Shodan 补丁数据（体量提升，~30k tokens 目标：扩展 Shodan 数据）
    rng2 = random.Random(12345)
    VULNERABLE_VERSIONS_SHORT = [
        "OpenSSH_8.5p1", "OpenSSH_8.7p1", "OpenSSH_8.9p1", "OpenSSH_9.3p2", "OpenSSH_9.6p1"
    ]
    ORGS2 = ["Alibaba Cloud", "Amazon", "Microsoft Azure", "Google Cloud", "DigitalOcean"]
    COUNTRIES2 = ["US", "CN", "DE", "JP", "GB"]
    extended_shodan = []
    for i in range(400):
        ver_str = rng2.choice(VULNERABLE_VERSIONS_SHORT)
        entry = {
            "ip": f"{rng2.randint(100, 220)}.{rng2.randint(1, 254)}.{rng2.randint(1, 254)}.{rng2.randint(1, 254)}",
            "port": 22,
            "version": ver_str,
            "org": rng2.choice(ORGS2),
            "location": {"country_code": rng2.choice(COUNTRIES2)},
            "vulns": [CVE_ID],
            "timestamp": f"2024-07-05T{rng2.randint(0, 23):02d}:{rng2.randint(0, 59):02d}:00Z"
        }
        extended_shodan.append(entry)
    wj(UPD / "upd1_workspace" / "shodan_export_supplement_2024-07-05.json", {
        "query": "port:22 product:OpenSSH vuln:CVE-2024-6387",
        "scan_date": "2024-07-05",
        "note": "Supplemental scan focusing on confirmed vulnerable instances post-disclosure",
        "results": extended_shodan
    })

    # ── Update 2（第 10 轮后）：Workaround 撤销通知（Supersede） ─────────────
    # 安全委员会决议 Markdown
    w(UPD / "upd2_workspace" / "security_committee_decision.md", f"""# Security Committee Decision — CVE-2024-6387 Workaround

**Decision Date**: 2024-07-08
**Committee**: Company Information Security Committee
**Decision ID**: SC-2024-0708-01

## Decision

The Information Security Committee has formally reviewed the CVE-2024-6387 temporary
workaround (`LoginGraceTime 0`) and issued the following decision:

**EFFECTIVE IMMEDIATELY: The `LoginGraceTime 0` workaround is REVOKED and SUPERSEDED.**

### Rationale

1. **DoS Risk**: Setting `LoginGraceTime 0` disables authentication timeouts entirely.
   This creates an unacceptable Denial-of-Service risk: attackers can hold SSH connections
   open indefinitely, exhausting connection slots and blocking legitimate access.

2. **Production Impact**: During the 2024-07-06 load test, a simulation of the DoS attack
   vector resulted in 100% connection slot exhaustion within 4 minutes on prod hosts.

3. **Alternative Available**: The `MaxStartups` configuration provides equivalent protection
   against CVE-2024-6387 exploitation (by limiting attack throughput) without the DoS risk.

## Replacement Configuration

The approved replacement workaround is:

```
# /etc/ssh/sshd_config
MaxStartups 10:30:100
```

This limits concurrent unauthenticated connections, significantly raising the time
required for the ~10,000-attempt exploitation to an impractical level, while maintaining
service availability for legitimate users.

## Supersede Relationship

This decision **SUPERSEDES** all prior instructions recommending `LoginGraceTime 0` as
a CVE-2024-6387 workaround, including:
- Initial oss-security workaround guidance
- work/workaround_plan.md (first version, Rounds 1–10)
- Any Slack/email/Feishu messages prior to this decision recommending LoginGraceTime 0

## Required Actions

1. Remove `LoginGraceTime 0` from all sshd_config files
2. Add `MaxStartups 10:30:100` to sshd_config files
3. Restart sshd on all affected hosts
4. Update work/workaround_plan.md to reflect the new approach (create _v2 version)
5. Prioritize full patching over workaround in all future reports

Signed: Information Security Committee, 2024-07-08
""")

    # MaxStartups 指导文档
    w(UPD / "upd2_workspace" / "maxstartups_guidance.md", """# MaxStartups Configuration Guidance

## Purpose

This document provides guidance for implementing the `MaxStartups` workaround as the
approved replacement for the revoked `LoginGraceTime 0` mitigation for CVE-2024-6387.

## Configuration

```
# /etc/ssh/sshd_config — add or modify:
MaxStartups 10:30:100
```

### Parameter Explanation

Format: `start:rate:full`

| Parameter | Value | Meaning |
|-----------|-------|---------|
| start | 10 | Allow up to 10 concurrent unauthenticated connections without throttling |
| rate | 30 | Drop new connections with 30% probability when above the `start` threshold |
| full | 100 | Hard maximum of 100 concurrent unauthenticated connections (all dropped above) |

## Effect on CVE-2024-6387 Exploitation

CVE-2024-6387 exploitation requires approximately 10,000 connection attempts. With
`MaxStartups 10:30:100`, the effective connection rate an attacker can sustain is
significantly reduced:

- Without MaxStartups: Full rate (depends on network bandwidth)
- With MaxStartups 10:30:100: Limited to ~10 concurrent attempts at any time

**Estimated exploitation time with MaxStartups 10:30:100**: weeks to months (vs. 6-8 hours
without mitigation), making practical exploitation infeasible in most environments.

## Comparison with LoginGraceTime 0

| Aspect | LoginGraceTime 0 | MaxStartups 10:30:100 |
|--------|-----------------|----------------------|
| Effectiveness | Eliminates the race condition trigger | Reduces attack throughput |
| DoS Risk | HIGH (connections held indefinitely) | LOW (hard cap protects availability) |
| Impact on legitimate users | None (timeouts irrelevant for fast auth) | Minimal (only during high load) |
| Status | REVOKED by Security Committee | APPROVED replacement |

## Implementation

```bash
# Apply configuration
sudo nano /etc/ssh/sshd_config
# Add/modify: MaxStartups 10:30:100

# Restart sshd
sudo systemctl restart sshd

# Verify
sshd -T | grep maxstartups
```

## Notes

- `MaxStartups` does not eliminate the vulnerability — it only limits exploitation throughput
- Full patching to OpenSSH 9.8p1 (or RHEL packages) remains the definitive remediation
- This is a defense-in-depth measure, not a substitute for patching
""")

    # Update 2 邮件续段（Alice 正式撤销通知）
    s_email = sess_ids["history"][2][0]
    email_upd2_seg = _make_append_segment(
        s_email, CWD, "2024-07-08T10:00:00",
        [
            (
                "[Email alice.wang@company.com → lead-security-engineer@company.com Mon Jul 08 2024 10:00] "
                "Subject: FORMAL NOTICE: LoginGraceTime 0 Workaround REVOKED — Use MaxStartups\n\n"
                "This is a formal operations notice.\n\n"
                "The Information Security Committee has issued Decision SC-2024-0708-01, "
                "REVOKING the LoginGraceTime 0 workaround for CVE-2024-6387 effective immediately. "
                "This SUPERSEDES all prior guidance recommending LoginGraceTime 0, "
                "including the initial workaround documented in work/workaround_plan.md.\n\n"
                "The approved replacement is: MaxStartups 10:30:100\n\n"
                "Please:\n"
                "1. Remove LoginGraceTime 0 from all sshd_config files\n"
                "2. Implement MaxStartups 10:30:100\n"
                "3. Update work/workaround_plan_v2.md with the new approach\n"
                "4. Ensure work/workaround_plan_v2.md explicitly states that LoginGraceTime 0 "
                "has been SUPERSEDED\n\n"
                "Details in assets/advisories/security_committee_decision.md (from update)\n\nAlice",
                "Formal notice received. LoginGraceTime 0 is REVOKED and SUPERSEDED by "
                "MaxStartups 10:30:100 per Security Committee Decision SC-2024-0708-01. "
                "Will create work/workaround_plan_v2.md with the new configuration and "
                "explicit supersede statement. Removing LoginGraceTime 0 from all configs."
            ),
        ]
    )
    w(UPD / "upd2_sessions" / f"{s_email}.jsonl", email_upd2_seg)

    # 额外体量填充（RedHat Solution 文章文本）
    w(UPD / "upd2_workspace" / "redhat_maxstartups_solution.txt", """Red Hat Solution: Mitigating CVE-2024-6387 with MaxStartups
Source: Red Hat Customer Portal

ENVIRONMENT
- Red Hat Enterprise Linux 9
- Red Hat Enterprise Linux 8
- OpenSSH

ISSUE
- CVE-2024-6387 (regreSSHion) allows unauthenticated remote code execution
- Primary mitigation LoginGraceTime 0 has been identified as creating DoS risk

RESOLUTION

The recommended mitigation strategy after security review is to use MaxStartups:

1. Edit /etc/ssh/sshd_config:
   Add or modify: MaxStartups 10:30:100

2. Restart the SSH service:
   systemctl restart sshd

3. Verify the configuration:
   sshd -T | grep maxstartups

RATIONALE
The MaxStartups directive limits concurrent unauthenticated connection attempts.
CVE-2024-6387 exploitation requires approximately 10,000 attempts due to the
probabilistic nature of the race condition. With MaxStartups 10:30:100, the
effective rate an attacker can sustain is dramatically reduced, making exploitation
impractical within a reasonable timeframe.

Unlike LoginGraceTime 0, MaxStartups does not disable authentication timeouts,
preserving defense against slow-connection DoS attacks while mitigating the
regreSSHion exploitation vector.

IMPORTANT: This is a temporary mitigation only. Apply the vendor patch as soon
as possible:
- RHEL 9: dnf update openssh (target: openssh-8.7p1-38.el9_4.1, RHSA-2024:4312)
- RHEL 8: dnf update openssh (target: openssh-8.0p1-19.el8_10.1, RHSA-2024:4340)

REFERENCES
- CVE-2024-6387: https://nvd.nist.gov/vuln/detail/CVE-2024-6387
- RHSA-2024:4312: https://access.redhat.com/errata/RHSA-2024:4312
- RHSA-2024:4340: https://access.redhat.com/errata/RHSA-2024:4340
""")

    # ── Update 3（第 13 轮后）：CVE-2024-6409 同期披露 ─────────────────────
    # CVE-2024-6409 详情 JSON
    wj(UPD / "upd3_workspace" / "CVE-2024-6409_detail.json", {
        "cve_id": "CVE-2024-6409",
        "title": "Signal handler race condition in OpenSSH sshd privilege separation child",
        "description": (
            "A race condition vulnerability was discovered in OpenSSH's privilege-separated "
            "child process. The race condition in the privilege-separated child process can be "
            "triggered through signal handling, allowing an attacker to potentially execute "
            "arbitrary code. This affects only the child process (running with reduced privileges), "
            "making it less severe than CVE-2024-6387 which affects the main sshd process."
        ),
        "cvss_score": 7.0,
        "cvss_vector": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:H",
        "severity": "High",
        "affected_versions": ["8.7", "8.8"],
        "affected_package_note": "Specifically affects RHEL-backported versions 8.7 and 8.8",
        "scope": "privilege_separation_child_process",
        "cwe": ["CWE-364"],
        "disclosure_date": "2024-07-08",
        "prior_cve": None,
        "compare_with_6387": {
            "CVE-2024-6387": {
                "scope": "main_sshd_process",
                "cvss_score": 8.1,
                "affected_versions": "8.5p1 to 9.7p1",
                "impact": "Root RCE — maximum severity"
            },
            "CVE-2024-6409": {
                "scope": "privilege_separation_child_process",
                "cvss_score": 7.0,
                "affected_versions": "8.7 and 8.8 (RHEL backports)",
                "impact": "Child process code execution — reduced severity due to privsep"
            }
        },
        "_note": "CVE-2024-6409 is distinct from CVE-2024-6387. Different scope, different CVSS, narrower version range."
    })

    # 双 CVE 对比矩阵 Markdown
    w(UPD / "upd3_workspace" / "openssh_dual_cve_matrix.md", """# OpenSSH Dual CVE Analysis Matrix
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
""")

    # Update 3 Slack 新消息
    s_slack_alerts = sess_ids["history"][0][0]
    slack_upd3_seg = _make_append_segment(
        s_slack_alerts, CWD, "2024-07-08T11:00:00",
        [
            (
                "[Slack #security-alerts Eve Liu Mon Jul 08 2024 11:00] "
                "New finding: CVE-2024-6409 just disclosed. Related to regreSSHion but different — "
                "affects sshd's privilege separation child process. CVSS 7.0 (vs 6387's 8.1). "
                "Key difference: CVE-2024-6409 only affects OpenSSH versions 8.7 and 8.8 "
                "(specific RHEL backport versions), not the full 8.5p1-9.7p1 range of CVE-2024-6387. "
                "Files added to workspace update. Please add comparison analysis.",
                "CVE-2024-6409 logged. Distinct from CVE-2024-6387: different scope (child process vs main), "
                "different CVSS (7.0 vs 8.1), narrower version range (8.7+8.8 only vs 8.5p1-9.7p1). "
                "Will produce comparison analysis in work/cve_comparison.json."
            ),
        ]
    )
    w(UPD / "upd3_sessions" / f"{s_slack_alerts}.jsonl", slack_upd3_seg)

    # 扩展技术分析文档（体量补充）
    w(UPD / "upd3_workspace" / "extended_exploit_analysis.md", """# Extended Exploitation Analysis: CVE-2024-6387

## Memory Layout and ASLR Constraints

### 32-bit Linux Exploitation

On 32-bit glibc-based Linux systems:
- Virtual address space: 4 GB total (2 GB user)
- Heap ASLR entropy: approximately 13-16 bits
- Number of possible heap base addresses: 2^13 to 2^16 ≈ 8,192 to 65,536

With ~10,000 connection attempts, the probability of hitting the correct heap layout
becomes statistically favorable on 32-bit systems with lower ASLR entropy.

### 64-bit Linux Challenges

On 64-bit Linux:
- Heap ASLR entropy: 28-56 bits (system-dependent)
- Practical exploitation requires orders of magnitude more attempts
- No public reliable 64-bit exploit demonstrated as of the disclosure date

The Qualys researchers explicitly stated their exploitation was demonstrated on
32-bit Linux with glibc. The 6-8 hour timeframe applies specifically to this
configuration.

## glibc Heap Internals Exploited

The exploit leverages the following glibc malloc() structures:
1. **Arena metadata**: Per-thread arenas with mutex objects
2. **Bin structures**: Free chunk doubly-linked lists (fastbins, smallbins, largebins)
3. **FILE structure overlap**: stdout/stderr _IO_FILE structures adjacent to heap chunks

The race condition allows the attacker to corrupt these structures when the signal
handler's malloc() call interleaves with the main thread's ongoing malloc()/free().

## Connection Attempt Strategy

The exploitation sequence involves:

1. **Phase 1 - Profiling** (~1-2 hours):
   - Send partial authentication requests with varying timing
   - Observe server behavior to infer heap layout
   - Identify the signal delivery window within malloc()

2. **Phase 2 - Exploitation** (~4-6 hours):
   - Rapidly open and close connections (~10,000 total attempts)
   - Each attempt: connect → fail auth → wait for SIGALRM at precise moment
   - Success condition: SIGALRM delivered while malloc() holds internal lock

3. **Phase 3 - Post-exploitation**:
   - Shell callback to attacker-controlled server
   - Root privilege confirmation
   - Persistence establishment

## Comparison: Exploitation vs. Patching Time

| Metric | Value |
|--------|-------|
| Time to exploit (32-bit lab) | 6-8 hours |
| Connection attempts needed | ~10,000 |
| Time to patch (RHEL 9 with RHSA-2024:4312) | < 30 minutes per host |
| Time to apply LoginGraceTime 0 workaround | < 5 minutes |
| Time to apply MaxStartups workaround | < 5 minutes |

**Conclusion**: Patching is faster than exploitation. Prioritize patching.

## References

- Qualys Blog: https://blog.qualys.com/vulnerabilities-threat-research/2024/07/01/regresshion-remote-unauthenticated-code-execution-vulnerability-in-openssh-server
- OpenSSH 9.8 Release Notes: https://www.openssh.org/txt/release-9.8
- NVD: https://nvd.nist.gov/vuln/detail/CVE-2024-6387
""")

    # ── 体量补充：upd2 patch tracking CSV（~30k tokens） ─────────────────────
    rng_u2 = random.Random(7777)
    PATCH_STATUS = ["patched", "patched", "patched", "pending", "failed"]
    PATCH_METHODS = ["dnf_update", "ansible_playbook", "manual", "automated_cron"]
    PATCH_PKGS = ["openssh-8.7p1-38.el9_4.1", "openssh-8.0p1-19.el8_10.1",
                  "openssh-9.8p1", "openssh-8.9p1-3ubuntu0.7"]
    upd2_rows = [["hostname", "ip", "env", "os_version", "ssh_version_before",
                  "ssh_version_after", "patch_date", "patch_method", "patch_package",
                  "patch_status", "applied_by", "ticket_id", "notes"]]
    hosts_envs = ["prod"] * 40 + ["staging"] * 25 + ["dev"] * 35
    for i in range(620):
        env = hosts_envs[i % len(hosts_envs)]
        status = rng_u2.choice(PATCH_STATUS)
        method = rng_u2.choice(PATCH_METHODS)
        pkg = rng_u2.choice(PATCH_PKGS)
        day = rng_u2.randint(3, 10)
        ver_before = rng_u2.choice(["OpenSSH_8.7p1", "OpenSSH_9.3p2", "OpenSSH_8.9p1"])
        ver_after = "OpenSSH_9.8p1" if status == "patched" else ver_before
        upd2_rows.append([
            f"host-{env[:1]}{i+1:04d}.internal.example.com",
            f"10.{rng_u2.randint(1,80)}.{rng_u2.randint(1,254)}.{rng_u2.randint(1,254)}",
            env,
            rng_u2.choice(["RHEL 9.4", "RHEL 8.10", "Ubuntu 22.04.4", "Debian 12"]),
            ver_before,
            ver_after,
            f"2024-07-{day:02d}T{rng_u2.randint(0,23):02d}:{rng_u2.randint(0,59):02d}:00Z",
            method,
            pkg if status == "patched" else "N/A",
            status,
            rng_u2.choice(["sre-user", "bob.zhang", "ansible-automation", "alice.wang"]),
            f"SEC-2024-{i+1000}",
            f"CVE-2024-6387 remediation — {'MaxStartups 10:30:100 applied' if status == 'patched' else 'pending patch'}"
        ])
    buf_u2 = io.StringIO()
    csv.writer(buf_u2).writerows(upd2_rows)
    w(UPD / "upd2_workspace" / "patch_tracking_v2.csv", buf_u2.getvalue())

    # 补充：upd2 DoS 事件日志（~15k tokens）
    rng_dos = random.Random(9999)
    dos_lines = ["# DoS Test Event Log — 2024-07-06",
                 "# Test: Simulating LoginGraceTime 0 DoS attack vector on prod-host-test01",
                 "# Purpose: Verify security committee's concern about DoS risk",
                 "# Analyst: Bob Zhang (SRE), Alice Wang (Security Director)",
                 "# Result: 100% connection slot exhaustion within 4 minutes",
                 ""]
    for minute in range(0, 4):
        for second in range(0, 60, 3):
            n = rng_dos.randint(3, 8)
            for _ in range(n):
                ms = rng_dos.randint(0, 999)
                conn_id = rng_dos.randint(100000, 999999)
                src_ip = f"{rng_dos.randint(1,220)}.{rng_dos.randint(1,254)}.{rng_dos.randint(1,254)}.{rng_dos.randint(1,254)}"
                event = rng_dos.choice(["CONNECT", "TIMEOUT_PREAUTH", "SLOT_EXHAUSTED", "CONNECT_THROTTLED"])
                dos_lines.append(
                    f"2024-07-06T14:{minute:02d}:{second:02d}.{ms:03d}Z "
                    f"[conn={conn_id}] {event} src={src_ip} "
                    f"active_slots={rng_dos.randint(50, 256)}/256 "
                    f"status={'VULNERABLE' if event == 'CONNECT' else 'RISK_ACTIVE'}"
                )
    dos_lines.append("")
    dos_lines.append("# Summary: LoginGraceTime 0 creates unacceptable DoS risk.")
    dos_lines.append("# Recommendation: Use MaxStartups 10:30:100 instead.")
    w(UPD / "upd2_workspace" / "dos_test_log_20240706.txt", "\n".join(dos_lines))

    # ── 体量补充：upd3 CVE 对비 扫描数据（~30k tokens） ─────────────────────
    rng_u3 = random.Random(6409)
    RHEL8_VULN_VERSIONS = ["OpenSSH_8.7p1", "OpenSSH_8.8p1"]
    upd3_scan_rows = [["hostname", "ip", "os_version", "ssh_version", "env",
                       "cve_2024_6387_vulnerable", "cve_2024_6409_vulnerable",
                       "patch_required", "errata_applicable"]]
    for i in range(500):
        env = rng_u3.choice(["prod"] * 40 + ["staging"] * 30 + ["dev"] * 30)
        ver = rng_u3.choice(["OpenSSH_8.7p1", "OpenSSH_8.8p1", "OpenSSH_8.9p1",
                              "OpenSSH_9.3p2", "OpenSSH_9.6p1", "OpenSSH_9.8p1"])
        v6387 = "true" if ver in ["OpenSSH_8.5p1", "OpenSSH_8.7p1", "OpenSSH_8.8p1",
                                   "OpenSSH_8.9p1", "OpenSSH_9.3p2", "OpenSSH_9.6p1"] else "false"
        v6409 = "true" if ver in ["OpenSSH_8.7p1", "OpenSSH_8.8p1"] else "false"
        errata = "RHSA-2024:4312" if "RHEL 9" in rng_u3.choice(["RHEL 9", "RHEL 8", "Ubuntu"]) else "RHSA-2024:4340"
        upd3_scan_rows.append([
            f"host-{env[:1]}{i+1:04d}-scan.example.com",
            f"10.{rng_u3.randint(80,120)}.{rng_u3.randint(1,254)}.{rng_u3.randint(1,254)}",
            rng_u3.choice(["RHEL 9.4", "RHEL 8.10", "Ubuntu 22.04"]),
            ver,
            env,
            v6387,
            v6409,
            "true" if v6387 == "true" else "false",
            errata if v6387 == "true" else "N/A"
        ])
    buf_u3 = io.StringIO()
    csv.writer(buf_u3).writerows(upd3_scan_rows)
    w(UPD / "upd3_workspace" / "dual_cve_scan_results.csv", buf_u3.getvalue())

    # upd3 OpenSSH 版本分析报告（~20k tokens）
    rng_u3b = random.Random(2222)
    ver_analysis_lines = [
        "# OpenSSH Version Distribution Analysis — Post CVE-2024-6387/CVE-2024-6409 Disclosure",
        "# Analysis Date: 2024-07-08",
        "# Scope: Internal infrastructure + Internet-facing exposure",
        "",
        "## Executive Summary",
        "",
        "Following disclosure of both CVE-2024-6387 and CVE-2024-6409, this report",
        "analyzes version distribution across our infrastructure and the broader internet.",
        "",
        "CVE-2024-6387: Affects OpenSSH 8.5p1–9.7p1 (CVSS 8.1)",
        "CVE-2024-6409: Affects OpenSSH 8.7 and 8.8 only (CVSS 7.0, narrower range)",
        "",
        "## Internal Version Distribution",
        ""
    ]
    versions = ["OpenSSH_8.5p1", "OpenSSH_8.7p1", "OpenSSH_8.8p1", "OpenSSH_8.9p1",
                "OpenSSH_9.0p1", "OpenSSH_9.3p2", "OpenSSH_9.6p1", "OpenSSH_9.7p1",
                "OpenSSH_9.8p1", "OpenSSH_7.4p1", "OpenSSH_8.4p1"]
    ver_counts = {v: rng_u3b.randint(5, 80) for v in versions}
    for ver, count in sorted(ver_counts.items()):
        v6387_flag = "(VULNERABLE to CVE-2024-6387)" if any(
            ver.startswith(f"OpenSSH_{v}") for v in
            ["8.5", "8.6", "8.7", "8.8", "8.9", "9.0", "9.1", "9.2", "9.3", "9.4", "9.5", "9.6", "9.7"]
        ) else "(NOT vulnerable to CVE-2024-6387)"
        v6409_flag = " + (VULNERABLE to CVE-2024-6409)" if ver in ["OpenSSH_8.7p1", "OpenSSH_8.8p1"] else ""
        ver_analysis_lines.append(f"  {ver:<25} : {count:>4} hosts  {v6387_flag}{v6409_flag}")

    ver_analysis_lines += [
        "",
        "## Key Observation: CVE-2024-6409 Scope is Narrower",
        "",
        "Unlike CVE-2024-6387 which affects all 8.5p1–9.7p1 versions,",
        "CVE-2024-6409 only affects versions 8.7 and 8.8 (RHEL backport builds).",
        "This distinction is critical for prioritizing remediation.",
        "",
        "## Remediation Priority Matrix",
        "",
        "| Priority | Version | CVE-2024-6387 | CVE-2024-6409 | Action |",
        "|----------|---------|--------------|--------------|--------|",
        "| P1 (Critical) | 8.7p1 | YES | YES | Patch immediately (RHSA-2024:4312/4340) |",
        "| P1 (Critical) | 8.8p1 | YES | YES | Patch immediately |",
        "| P2 (High) | 8.5p1–8.6p1 | YES | NO | Patch within 72h |",
        "| P2 (High) | 8.9p1–9.7p1 | YES | NO | Patch within 72h |",
        "| P3 (Monitor) | 9.8p1+ | NO | NO | No action required |",
        "| P3 (Monitor) | < 8.5p1 | NO | NO | No action required |",
        "",
    ]
    # Add per-host detail lines to reach ~20k tokens
    for i in range(300):
        ver = rng_u3b.choice(versions)
        env = rng_u3b.choice(["prod", "staging", "dev"])
        ip = f"10.{rng_u3b.randint(1,100)}.{rng_u3b.randint(1,254)}.{rng_u3b.randint(1,254)}"
        v6387 = "VULN" if any(ver.startswith(f"OpenSSH_{v}") for v in
            ["8.5", "8.6", "8.7", "8.8", "8.9", "9.0", "9.1", "9.2", "9.3", "9.4", "9.5", "9.6", "9.7"]) else "OK"
        v6409 = "VULN" if ver in ["OpenSSH_8.7p1", "OpenSSH_8.8p1"] else "OK"
        ver_analysis_lines.append(
            f"host-{env[:1]}{i+1:04d} {ip} {ver:<25} CVE-2024-6387:{v6387} CVE-2024-6409:{v6409}"
        )
    w(UPD / "upd3_workspace" / "version_analysis_report.txt", "\n".join(ver_analysis_lines))

    updates_decl = {
        "upd1_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd1_sessions",
            "files": [
                {"name": f"{s_feishu_dm}.jsonl", "action": "append",
                 "target": f"{s_feishu_dm}.jsonl"}
            ]
        },
        "upd1_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd1_workspace",
            "files": [
                {"name": "redhat_RHSA-2024-4340.json", "action": "new",
                 "target": "assets/advisories/redhat_RHSA-2024-4340.json"},
                {"name": "rhel8_inventory.csv", "action": "new",
                 "target": "assets/scan_results/rhel8_inventory.csv"},
                {"name": "rhel8_openssh_versions.md", "action": "new",
                 "target": "assets/advisories/rhel8_openssh_versions.md"},
                {"name": "shodan_export_supplement_2024-07-05.json", "action": "new",
                 "target": "assets/scan_results/shodan_export_supplement_2024-07-05.json"},
            ]
        },
        "upd2_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd2_sessions",
            "files": [
                {"name": f"{s_email}.jsonl", "action": "append",
                 "target": f"{s_email}.jsonl"}
            ]
        },
        "upd2_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd2_workspace",
            "files": [
                {"name": "security_committee_decision.md", "action": "new",
                 "target": "assets/advisories/security_committee_decision.md"},
                {"name": "maxstartups_guidance.md", "action": "new",
                 "target": "assets/advisories/maxstartups_guidance.md"},
                {"name": "redhat_maxstartups_solution.txt", "action": "new",
                 "target": "assets/advisories/redhat_maxstartups_solution.txt"},
                {"name": "patch_tracking_v2.csv", "action": "new",
                 "target": "assets/scan_results/patch_tracking_v2.csv"},
                {"name": "dos_test_log_20240706.txt", "action": "new",
                 "target": "assets/scan_results/dos_test_log_20240706.txt"},
            ]
        },
        "upd3_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd3_sessions",
            "files": [
                {"name": f"{s_slack_alerts}.jsonl", "action": "append",
                 "target": f"{s_slack_alerts}.jsonl"}
            ]
        },
        "upd3_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd3_workspace",
            "files": [
                {"name": "CVE-2024-6409_detail.json", "action": "new",
                 "target": "assets/advisories/CVE-2024-6409_detail.json"},
                {"name": "openssh_dual_cve_matrix.md", "action": "new",
                 "target": "assets/advisories/openssh_dual_cve_matrix.md"},
                {"name": "extended_exploit_analysis.md", "action": "new",
                 "target": "assets/advisories/extended_exploit_analysis.md"},
                {"name": "dual_cve_scan_results.csv", "action": "new",
                 "target": "assets/scan_results/dual_cve_scan_results.csv"},
                {"name": "version_analysis_report.txt", "action": "new",
                 "target": "assets/scan_results/version_analysis_report.txt"},
            ]
        },
    }
    return updates_decl


def _make_append_segment(session_id: str, cwd: str, start_iso: str, turns: list) -> str:
    """构造用于 append 的 session 续段（无 header，只保留 message 行）。"""
    sb = SessionBuilder(session_id, cwd, start_iso, is_main=False)
    sb.add_turns(turns)
    msg_lines = [ln for ln in sb.lines if ln.get("type") == "message"]
    return "\n".join(json.dumps(ln, ensure_ascii=False) for ln in msg_lines) + "\n"


# ── main ─────────────────────────────────────────────────────────────────────
def main() -> None:
    # 幂等清场
    for d in (WS, SESS.parent, UPD):
        if d.exists():
            shutil.rmtree(d)

    gen_system_files()
    gen_advisories()
    gen_scan_data()
    gen_code_samples()
    gen_compliance_docs()
    gen_scripts()
    gen_templates()
    gen_readme()

    # 创建空 work/ 目录
    (WS / "work").mkdir(parents=True, exist_ok=True)

    sess_ids = gen_sessions()
    updates_decl = gen_updates(sess_ids)

    desc = (
        "CVE-2024-6387 (regreSSHion) OpenSSH signal handler race condition vulnerability "
        "analysis and remediation — 17 exec_check rounds, 3 updates (incl. LoginGraceTime 0 "
        "supersede → MaxStartups), 5 preference rules P1-P5, difficulty vectors "
        "V1/V2/V3/V4/V5/V6/V7/V8/V9/V10. "
        "Real sources: NVD (https://nvd.nist.gov/vuln/detail/CVE-2024-6387); "
        "GHSA (https://github.com/advisories/GHSA-2x8c-95vh-gfv4); "
        "Qualys (https://blog.qualys.com/vulnerabilities-threat-research/2024/07/01/regresshion-remote-unauthenticated-code-execution-vulnerability-in-openssh-server); "
        "oss-security (https://www.openwall.com/lists/oss-security/2024/07/01/3); "
        "OpenSSH 9.8 (https://www.openssh.org/txt/release-9.8); "
        "RHSA-2024:4312 (https://access.redhat.com/errata/RHSA-2024:4312); "
        "regression commit (https://github.com/openssh/openssh-portable/commit/752250caabda3dd24635503c4cd689b32a650794); "
        "CVE-2006-5051 (https://github.com/advisories/GHSA-mq5h-r3rg-j9hg)."
    )

    dump_register_meta(
        DATASET, test_id=TID, desc=desc,
        main_session=sess_ids["main"],
        history_sessions=sess_ids["history"],
        updates=updates_decl,
    )

    # 体量报告
    ws_total = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in WS.rglob("*") if p.is_file()
    )
    sess_tok = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in SESS.glob("*.jsonl")
    )
    upd_tok = sum(
        est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
        for p in UPD.rglob("*") if p.is_file()
    )
    upd_dirs = ["upd1_workspace", "upd2_workspace", "upd3_workspace"]
    for ud in upd_dirs:
        udp = UPD / ud
        if udp.exists():
            tok = sum(est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
                      for p in udp.rglob("*") if p.is_file())
            print(f"[sec1] {ud} tokens: ~{tok:,}")

    print(f"[sec1] workspace tokens ~{ws_total:,} | sessions ~{sess_tok:,} | updates total ~{upd_tok:,}")
    print(f"[sec1] built at {DATASET}")


if __name__ == "__main__":
    main()
