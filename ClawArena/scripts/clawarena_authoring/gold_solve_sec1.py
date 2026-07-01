#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gold_solve_sec1.py — sec1 可解性审计（金标自检）。

在 workspace 临时副本上模拟 update 生效后的状态，写出每一轮的正确产物，
然后运行全部 check_qN.py + preference，断言正解全部 PASS。
再做反例断言，确认 check 能 FAIL（不过松）。

运行：python scripts/clawarena_authoring/gold_solve_sec1.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DS = REPO / "data" / "clawarena-real"
WS_SRC = DS / "openclaw" / "workspaces" / "sec1"
UPD = DS / "openclaw" / "updates" / "sec1"
SCRIPTS = DS / "eval" / "sec1" / "scripts"
GOLD = Path("/home/xkaiwen/.claude/jobs/579de28f/tmp/sec1_gold_ws")

# ── Ground-truth anchors ─────────────────────────────────────────────────
CVE_ID = "CVE-2024-6387"
CVSS_SCORE = 8.1
CVSS_VECTOR = "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H"
SEVERITY = "High"
GHSA_ID = "GHSA-2x8c-95vh-gfv4"
AFFECTED_RANGE = "8.5p1 <= openssh < 9.8p1"
DISCLOSURE_DATE = "2024-07-01"
CWE_IDS = ["CWE-362", "CWE-364"]
REGRESSION_COMMIT = "752250caabda3dd24635503c4cd689b32a650794"
PATCHED_VERSION = "9.8p1"
RHEL9_PKG = "openssh-8.7p1-38.el9_4.1"
RHEL9_ERRATA = "RHSA-2024:4312"
RHEL8_PKG = "openssh-8.0p1-19.el8_10.1"
RHEL8_ERRATA = "RHSA-2024:4340"
PRIOR_CVE = "CVE-2006-5051"

VULN_VERSIONS = {
    "OpenSSH_8.5p1", "OpenSSH_8.6p1", "OpenSSH_8.7p1", "OpenSSH_8.8p1",
    "OpenSSH_8.9p1", "OpenSSH_9.0p1", "OpenSSH_9.1p1", "OpenSSH_9.2p1",
    "OpenSSH_9.3p2", "OpenSSH_9.4p1", "OpenSSH_9.5p1", "OpenSSH_9.6p1",
    "OpenSSH_9.7p1"
}


def _w(p: Path, t: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8")


def _wj(p: Path, o) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def prep_workspace() -> Path:
    if GOLD.exists():
        shutil.rmtree(GOLD)
    shutil.copytree(WS_SRC, GOLD)
    # Apply all 3 updates (workspace files only — sessions are metadata)
    for upd_name, target_path in [
        ("upd1_workspace/redhat_RHSA-2024-4340.json",
         "assets/advisories/redhat_RHSA-2024-4340.json"),
        ("upd1_workspace/rhel8_inventory.csv",
         "assets/scan_results/rhel8_inventory.csv"),
        ("upd1_workspace/rhel8_openssh_versions.md",
         "assets/advisories/rhel8_openssh_versions.md"),
        ("upd1_workspace/shodan_export_supplement_2024-07-05.json",
         "assets/scan_results/shodan_export_supplement_2024-07-05.json"),
        ("upd2_workspace/security_committee_decision.md",
         "assets/advisories/security_committee_decision.md"),
        ("upd2_workspace/maxstartups_guidance.md",
         "assets/advisories/maxstartups_guidance.md"),
        ("upd2_workspace/redhat_maxstartups_solution.txt",
         "assets/advisories/redhat_maxstartups_solution.txt"),
        ("upd2_workspace/patch_tracking_v2.csv",
         "assets/scan_results/patch_tracking_v2.csv"),
        ("upd2_workspace/dos_test_log_20240706.txt",
         "assets/scan_results/dos_test_log_20240706.txt"),
        ("upd3_workspace/CVE-2024-6409_detail.json",
         "assets/advisories/CVE-2024-6409_detail.json"),
        ("upd3_workspace/openssh_dual_cve_matrix.md",
         "assets/advisories/openssh_dual_cve_matrix.md"),
        ("upd3_workspace/extended_exploit_analysis.md",
         "assets/advisories/extended_exploit_analysis.md"),
        ("upd3_workspace/dual_cve_scan_results.csv",
         "assets/scan_results/dual_cve_scan_results.csv"),
        ("upd3_workspace/version_analysis_report.txt",
         "assets/scan_results/version_analysis_report.txt"),
    ]:
        src = UPD / upd_name
        dst = GOLD / target_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, dst)
    return GOLD


def load_inventory(ws: Path) -> list[dict]:
    """Load internal_inventory.csv."""
    with (ws / "assets" / "scan_results" / "internal_inventory.csv").open() as fh:
        return list(csv.DictReader(fh))


def load_rhel8_inventory(ws: Path) -> list[dict]:
    """Load rhel8_inventory.csv."""
    p = ws / "assets" / "scan_results" / "rhel8_inventory.csv"
    if not p.exists():
        return []
    with p.open() as fh:
        return list(csv.DictReader(fh))


def load_shodan(ws: Path) -> list[dict]:
    """Load shodan_export_2024-07-02.json results."""
    data = json.loads((ws / "assets" / "scan_results" / "shodan_export_2024-07-02.json").read_text())
    return data.get("results", [])


def solve(ws: Path) -> None:
    work = ws / "work"
    work.mkdir(exist_ok=True)

    inventory = load_inventory(ws)
    rhel8_inv = load_rhel8_inventory(ws)
    shodan = load_shodan(ws)

    # ── Q1: vuln_summary.json ─────────────────────────────────────────────
    _wj(work / "vuln_summary.json", {
        "affected_range": AFFECTED_RANGE,
        "cve_id": CVE_ID,
        "cvss_score": CVSS_SCORE,
        "cvss_vector": CVSS_VECTOR,
        "cwe_ids": CWE_IDS,
        "disclosure_date": DISCLOSURE_DATE,
        "ghsa_id": GHSA_ID,
        "severity": SEVERITY,
    })

    # ── Q2: affected_assets.csv ───────────────────────────────────────────
    vuln_rows = [r for r in inventory if r.get("ssh_version", "") in VULN_VERSIONS]
    # Sort: prod first, then staging, then dev
    env_order = {"prod": 0, "staging": 1, "dev": 2}
    vuln_rows.sort(key=lambda r: (env_order.get(r.get("env", "dev"), 3)))

    q2_path = work / "affected_assets.csv"
    with q2_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["hostname", "ip", "ssh_version", "env", "owner", "is_vulnerable"])
        writer.writeheader()
        for r in vuln_rows:
            writer.writerow({
                "hostname": r["hostname"],
                "ip": r["ip"],
                "ssh_version": r["ssh_version"],
                "env": r["env"],
                "owner": r.get("owner", ""),
                "is_vulnerable": "true",
            })

    prod_vuln_count = sum(1 for r in vuln_rows if r.get("env", "").lower() == "prod")

    # ── Q3: cvss_breakdown.md ─────────────────────────────────────────────
    _w(work / "cvss_breakdown.md", f"""# CVSS v3.1 向量分解说明：{CVE_ID}

## CVSS 向量（Verbatim）

```
{CVSS_VECTOR}
```

## 基础评分：{CVSS_SCORE}（High）

## 各项指标说明

| 指标代码 | 含义 | 说明 |
|----------|------|------|
| AV:N | Attack Vector: Network（网络攻击向量） | 漏洞可通过网络（SSH port 22）远程利用，无需本地访问 |
| AC:H | Attack Complexity: High（高攻击复杂度） | 利用需要竞态条件时序精确控制；平均需约 10,000 次连接尝试 |
| PR:N | Privileges Required: None（无需权限） | 攻击者无需任何认证即可触发漏洞（pre-auth 漏洞） |
| UI:N | User Interaction: None（无需用户交互） | 受害方只需运行 sshd，无需用户主动操作 |
| S:U  | Scope: Unchanged（影响范围不变） | 漏洞利用局限于 sshd 进程范围内 |
| C:H  | Confidentiality: High（机密性影响高） | Root RCE 可读取系统全部数据 |
| I:H  | Integrity: High（完整性影响高） | Root RCE 可修改系统全部数据 |
| A:H  | Availability: High（可用性影响高） | Root RCE 可终止或禁用服务 |

## CVSS 评分计算（参考 assets/compliance/cvss_calculation_worksheet.md）

根据 CVSS v3.1 工作表计算：

- ISS（Impact Sub-Score）= 0.915（三项影响均为 High）
- Exploitability = 2.220（基于 AV:N × AC:H × PR:N × UI:N 参数）
- Base Score = Roundup(min(ISS + Exploitability, 10)) = Roundup(min(0.915 + 2.220, 10)) = **{CVSS_SCORE}**

## 评分注意事项

- AC:H（高复杂度）反映了竞态条件的概率性，虽然提高了利用门槛，但由于 C/I/A 均为 High，最终评分仍达 {CVSS_SCORE}
- 若 AC 为 Low，评分将达 9.8（Critical）
- NVD 官方来源：https://nvd.nist.gov/vuln/detail/{CVE_ID}
""")

    # ── Q4: regression_analysis.md ───────────────────────────────────────
    _w(work / "regression_analysis.md", f"""# 历史回归溯源分析：{CVE_ID} (regreSSHion)

## 摘要

CVE-2024-6387 是 CVE-2006-5051 的回归版本。2020 年 10 月，一次日志基础设施重构提交意外移除了
保护信号处理器的编译宏，导致 2006 年修复的漏洞重新引入到 OpenSSH 代码中。

## 原始漏洞：CVE-2006-5051（2006 年）

2006 年，OpenSSH 4.4 以下版本中发现信号处理器竞态条件漏洞（CVE-2006-5051）。
OpenSSH 团队在 4.4p1 版本中通过引入编译宏 `DO_LOG_SAFE_IN_SIGHAND` 修复：
该宏在信号处理器上下文中屏蔽了非异步信号安全函数（如 syslog()）的调用。

## 回归引入：Commit 752250caabda3dd24635503c4cd689b32a650794

- **Commit Hash**: `752250caabda3dd24635503c4cd689b32a650794`（简称 752250c）
- **作者**: Damien Miller (djm@mindrot.org)
- **日期**: **2020-10-16**
- **提交说明**: "upstream: revised log infrastructure for OpenSSH"
- **变更范围**: 7 个文件，154 处新增，133 处删除

该提交在重构 OpenSSH 日志基础设施时，意外移除了 `sshsigdie()` 函数中的
`#ifdef DO_LOG_SAFE_IN_SIGHAND` 保护块，使得 `syslog()` 可以在信号处理器
（SIGALRM handler）上下文中被直接调用——而 `syslog()` 并非异步信号安全函数。

**重要说明**：某自动摘要工具错误地将回归引入时间标注为 2021-03，此为不准确信息。
根据 oss-security 原始披露和 GitHub commit 记录，正确日期为 **2020-10-16**（2020 年 10 月）。

## 从 8.5p1 到 9.7p1 的影响

该回归在 OpenSSH 8.5p1（2021 年 2 月发布）中进入生产版本，影响所有后续版本直至 9.7p1。

## 修复：9.8p1（2024-07-01 发布）

OpenSSH 9.8p1 重新引入 `DO_LOG_SAFE_IN_SIGHAND` 保护宏，确保 SIGALRM 信号处理器
中只调用 `_exit(1)`（异步信号安全），不再调用 `syslog()`。

## 参考来源

- oss-security 披露: https://www.openwall.com/lists/oss-security/2024/07/01/3
- Regression commit: https://github.com/openssh/openssh-portable/commit/{REGRESSION_COMMIT}
- CVE-2006-5051: https://github.com/advisories/GHSA-mq5h-r3rg-j9hg
""")

    # ── Q5: workaround_plan.md ────────────────────────────────────────────
    _w(work / "workaround_plan.md", f"""# 临时缓解方案工单 — {CVE_ID} (regreSSHion)

**工单编号**: INC-2024-0702-001
**状态**: ACTIVE（已被 Update 2 撤销，见 workaround_plan_v2.md）
**日期**: 2024-07-02
**负责人**: Lead Security Engineer

---

## 背景

{CVE_ID} 是 OpenSSH sshd 的信号处理器竞态条件漏洞。在正式补丁部署前，
需要立即实施临时缓解措施。

---

## 临时缓解配置

在所有受影响主机的 `/etc/ssh/sshd_config` 中添加：

```
LoginGraceTime 0
```

---

## ⚠️ DoS 风险警告（CRITICAL）

将 `LoginGraceTime` 设为 0 会**完全禁用认证超时**。这意味着：
- 未经认证的连接将永远不会超时断开
- 攻击者可通过持续占用连接槽发起 Denial-of-Service（拒绝服务）攻击
- 在高并发场景下，可能导致合法用户无法连接

**风险评估**：DoS 风险等级 Medium（低于漏洞本身的 High 级别 RCE 风险）。
在正式补丁部署前，此 DoS 风险被认为可接受，但需持续监控。

---

## 实施步骤

1. 备份配置：`cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak.$(date +%Y%m%d)`
2. 编辑配置：`sudo nano /etc/ssh/sshd_config`，添加 `LoginGraceTime 0`
3. 重启服务：`systemctl restart sshd`
4. 验证：`sshd -T | grep logingracetime`（应返回 `logingracetime 0`）
5. 记录完成时间并更新工单

---

## 注意事项

- 旧版 Feishu 文档（workaround_DRAFT_v0.md from June 2024）中有 `LoginGraceTime 30` 的记录，
  该文档为**已废弃的草稿**，配置值 30 是错误的——正确值应为 **0**。
- 本临时缓解方案不替代正式补丁。请尽快按照 RHSA-2024:4312 升级 openssh。

---

## 参考

- oss-security 原始披露: https://www.openwall.com/lists/oss-security/2024/07/01/3
- NVD: https://nvd.nist.gov/vuln/detail/{CVE_ID}
""")

    # ── Q6: check_rhel_patch.sh ───────────────────────────────────────────
    script_content = f"""#!/usr/bin/env bash
# check_rhel_patch.sh — 验证 RHSA-2024:4312 修复包是否已安装
# CVE-2024-6387 (regreSSHion) — RHEL 9 补丁验证脚本
# Errata: RHSA-2024:4312
# Fixed package: openssh-8.7p1-38.el9_4.1

set -euo pipefail

ERRATA="RHSA-2024:4312"
FIXED_PKG="openssh-8.7p1-38.el9_4.1"
CVE="{CVE_ID}"

echo "=== RHEL Patch Verification for $CVE ($ERRATA) ==="
echo "Expected fixed package: $FIXED_PKG"

if ! command -v rpm &>/dev/null; then
    echo "WARNING: rpm command not found (non-RHEL system)"
    echo "Manual verification required: check openssh version >= 9.8p1"
    # Fall back to ssh -V check
    if command -v ssh &>/dev/null; then
        SSH_VER=$(ssh -V 2>&1 | grep -oP 'OpenSSH_[0-9]+\\.[0-9]+p[0-9]+' || echo "unknown")
        echo "Detected SSH version: $SSH_VER"
        if [[ "$SSH_VER" == "OpenSSH_9.8p1" ]] || [[ "$SSH_VER" > "OpenSSH_9.8" ]]; then
            echo "PASS: patched version detected"
            exit 0
        else
            echo "FAIL: version $SSH_VER is in vulnerable range or undetectable"
            exit 1
        fi
    fi
    echo "FAIL: cannot determine patch status"
    exit 1
fi

# Check installed openssh package version
INSTALLED=$(rpm -q openssh 2>/dev/null || echo "not_installed")
echo "Installed: $INSTALLED"

if [[ "$INSTALLED" == "openssh-8.7p1-38.el9_4.1"* ]]; then
    echo "PASS: $ERRATA fix is installed ($INSTALLED)"
    exit 0
elif [[ "$INSTALLED" == "not_installed" ]]; then
    echo "FAIL: openssh package not found"
    exit 1
else
    echo "FAIL: installed version $INSTALLED does not meet $ERRATA requirement ($FIXED_PKG)"
    echo "Run: dnf update openssh  # to install the fix"
    exit 1
fi
"""
    q6_path = work / "check_rhel_patch.sh"
    _w(q6_path, script_content)
    # Make executable
    current = q6_path.stat().st_mode
    q6_path.chmod(current | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    # ── Q7: exposure_report.json ──────────────────────────────────────────
    total_scanned = len(shodan)
    vulnerable = [e for e in shodan if CVE_ID in e.get("vulns", [])]
    vuln_count = len(vulnerable)

    ver_dist: dict = defaultdict(int)
    for e in vulnerable:
        ver_dist[e.get("version", "unknown")] += 1

    # Top 5 orgs by vulnerable count
    org_counts: dict = defaultdict(int)
    for e in vulnerable:
        org_counts[e.get("org", "unknown")] += 1
    top5 = sorted(org_counts.items(), key=lambda x: -x[1])[:5]
    top5_orgs = [org for org, _ in top5]

    _wj(work / "exposure_report.json", {
        "internet_exposed_global_estimate": 14000000,
        "top_5_exposed_orgs": top5_orgs,
        "total_scanned": total_scanned,
        "version_distribution": dict(ver_dist),
        "vulnerable_count": vuln_count,
    })

    # ── Q8: affected_assets_v2.csv (with RHEL 8) ─────────────────────────
    q8_path = work / "affected_assets_v2.csv"
    with q8_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["hostname", "ip", "ssh_version", "env", "owner", "is_vulnerable",
                         "errata_note"])
        # Existing Q2 rows
        for r in vuln_rows:
            writer.writerow([r["hostname"], r["ip"], r["ssh_version"], r["env"],
                             r.get("owner", ""), "true", RHEL9_ERRATA])
        # RHEL 8 rows
        for r in rhel8_inv:
            if r.get("is_vulnerable", "").lower() == "true":
                writer.writerow([r["hostname"], r["ip"], r.get("ssh_version", "OpenSSH_8.0p1"),
                                 r["env"], r.get("owner", ""), "true", RHEL8_ERRATA])

    # ── Q9: risk_matrix.json ──────────────────────────────────────────────
    # estimated_exposure_hours: 2024-07-02 09:00 - 2024-07-01 00:00 = ~33 hours
    _wj(work / "risk_matrix.json", {
        "cve_id": CVE_ID,
        "cvss_score": CVSS_SCORE,
        "estimated_exposure_hours": 33,
        "internet_exposed_count": vuln_count,
        "prod_host_count": prod_vuln_count,
        "remediation_priority": "P1",
        "risk_level": "HIGH",
    })

    # ── Q10: patch_progress.json ──────────────────────────────────────────
    _wj(work / "patch_progress.json", {
        "prod": {
            "patched": [f"prod-host-{i:03d}" for i in range(1, 21)],
            "pending": [f"prod-host-{i:03d}" for i in range(21, 41)],
            "failed": [],
        },
        "staging": {
            "patched": [f"staging-{i:03d}" for i in range(1, 51)],
            "pending": [],
            "failed": [],
        },
        "dev": {
            "patched": [],
            "pending": ["all dev hosts"],
            "failed": [],
        },
    })

    # ── Q11: workaround_plan_v2.md ────────────────────────────────────────
    _w(work / "workaround_plan_v2.md", f"""# 更新缓解方案 v2 — {CVE_ID} (regreSSHion)

**工单编号**: INC-2024-0702-001 (修订版)
**决策编号**: SC-2024-0708-01
**状态**: ACTIVE（替代已撤销的 workaround_plan.md v1）
**日期**: 2024-07-08
**负责人**: Lead Security Engineer

---

## ⚠️ 重要变更：LoginGraceTime 0 已被撤销（SUPERSEDED）

根据信息安全委员会决议 **SC-2024-0708-01**，`LoginGraceTime 0` 方案因存在
不可接受的 Denial-of-Service（拒绝服务）风险，已被**正式撤销并废止**。

- **已废止方案**: `LoginGraceTime 0`（已从所有 sshd_config 文件中移除）
- **已废止原因**: 禁用认证超时导致连接槽可被恶意占用，触发 DoS 攻击

**此文档 SUPERSEDES（取代）** work/workaround_plan.md 第一版中所有关于
`LoginGraceTime 0` 的指导内容。

---

## 当前批准缓解方案：MaxStartups 限制

### 配置内容

在所有受影响主机的 `/etc/ssh/sshd_config` 中添加或修改：

```
MaxStartups 10:30:100
```

### 参数说明

| 参数 | 值 | 含义 |
|------|-----|------|
| start | 10 | 最多允许 10 个未认证连接同时存在（无限流） |
| rate  | 30 | 超过 10 个时，以 30% 概率拒绝新连接 |
| full  | 100 | 硬性上限：超过 100 个全部拒绝 |

### 有效性

CVE-2024-6387 利用需要约 10,000 次连接尝试。`MaxStartups 10:30:100` 大幅降低
攻击者可维持的连接速率，将实际利用时间从 6-8 小时延长至数周乃至数月，
在实际场景中几乎不可行。

---

## 实施步骤

1. 移除已废止配置：确认 `LoginGraceTime 0` 不在 sshd_config 中
2. 编辑配置文件添加新配置：`sudo nano /etc/ssh/sshd_config`
3. 验证语法：`sudo sshd -t`
4. 重启服务：`systemctl restart sshd`
5. 验证生效：`sshd -T | grep maxstartups`（应返回 `maxstartups 10:30:100`）

---

## 最终目标

本方案为临时缓解，最终目标仍为正式补丁：
- RHEL 9: `dnf update openssh` → `openssh-8.7p1-38.el9_4.1` ({RHEL9_ERRATA})
- RHEL 8: `dnf update openssh` → `openssh-8.0p1-19.el8_10.1` ({RHEL8_ERRATA})
- 其他系统: 升级至 OpenSSH 9.8p1

---

## 参考

- 安全委员会决议: assets/advisories/security_committee_decision.md (SC-2024-0708-01)
- MaxStartups 指导: assets/advisories/maxstartups_guidance.md
- NVD: https://nvd.nist.gov/vuln/detail/{CVE_ID}
""")

    # ── Q12: exploit_analysis.md ──────────────────────────────────────────
    _w(work / "exploit_analysis.md", f"""# 漏洞利用技术分析：{CVE_ID} (regreSSHion)

## 概述

本分析基于 Qualys 安全研究团队的技术报告，详述 CVE-2024-6387 的利用方法。
权威来源：assets/advisories/qualys_regresshion_report.txt

---

## 关键技术参数

| 指标 | 值 | 来源 |
|------|-----|------|
| 利用所需连接尝试次数 | **~10,000 次** | Qualys TRU 报告 |
| 实验室利用总时间 | **6-8 hours（6-8 小时）** | Qualys TRU 报告 |
| 系统依赖 | **glibc**-based Linux | NVD / Qualys |
| 架构限制 | **32-bit** Linux | OpenSSH 9.8 release notes |
| 地址空间随机化绕过 | ASLR 熵约束（32-bit 下约 13-16 bits） | Qualys 分析 |

**⚠️ 重要说明**：某 Slack 自动摘要工具（BOT_AUTO_SUMMARY）错误声称利用时间为
"30 分钟"，此数据**不可信**。Qualys 权威报告明确指出为 **6-8 小时**。

---

## 利用方法详述

### 1. 漏洞触发机制

sshd 的 `LoginGraceTime` 超时计时器在认证超时时发送 `SIGALRM` 信号。
信号处理器 `grace_alarm_handler()` 调用 `sigdie()` → `sshsigdie()`，后者调用
`syslog()`——而 `syslog()` 并非异步信号安全（async-signal-safe）函数。

当 SIGALRM 在主线程执行 `malloc()` 或 `free()` 期间被投递时，信号处理器内的
`syslog()` 重入调用 `malloc()`，破坏 glibc 堆分配器的内部状态。

### 2. glibc 依赖条件

漏洞利用**仅在使用 glibc 的 Linux 系统上可行**。原因：
- glibc 的堆分配器（ptmalloc2）内部使用特定的 bin/arena 数据结构
- 堆状态损坏可用于操控 `_IO_FILE` 结构的虚函数表指针
- musl libc 系统因不同的堆实现而不受影响

### 3. ASLR 绕过（32-bit 限制）

Qualys 展示的利用基于 **32-bit Linux with ASLR**：
- 32-bit 系统堆地址 ASLR 熵约 13-16 bits（8,192 至 65,536 种可能）
- 通过 ~10,000 次暴力连接尝试，可概率性命中正确堆布局
- 64-bit 系统 ASLR 熵更高（28-56 bits），公开演示中尚未实现可靠利用

### 4. FILE 结构操纵（glibc 利用链）

利用链的核心：
1. 通过堆损坏覆盖 glibc `_IO_FILE` 结构的 `_vtable` 指针
2. 将 `_vtable` 指向攻击者控制的伪造虚函数表
3. 当 glibc 对该 FILE* 结构调用虚函数时（如 `fclose()` 期间），
   执行流跳转到攻击者指定地址

由于 sshd 以 root 权限运行，成功利用直接获得 root shell。

---

## 利用时间线（实验室环境）

| 阶段 | 时间 | 内容 |
|------|------|------|
| 堆布局分析 | 1-2 小时 | 发送认证请求，推断堆状态 |
| 暴力利用 | 4-6 小时 | ~10,000 次连接尝试，等待竞态条件触发 |
| 合计 | **6-8 小时** | 32-bit glibc Linux 实验室条件 |

---

## 参考来源

- Qualys 技术报告: https://blog.qualys.com/vulnerabilities-threat-research/2024/07/01/regresshion-remote-unauthenticated-code-execution-vulnerability-in-openssh-server
- OpenSSH 9.8 发布说明: https://www.openssh.org/txt/release-9.8
""")

    # ── Q13: executive_report.md ──────────────────────────────────────────
    _w(work / "executive_report.md", f"""# 安全执行摘要：CVE-2024-6387 (regreSSHion) 应急响应报告

**报告日期**: 2024-07-08
**报告人**: Lead Security Engineer
**收件人**: CTO (Carol)
**状态**: ACTIVE — 修复进行中

---

## TL;DR

CVE-2024-6387（代号 regreSSHion）是 OpenSSH 服务端的一个高危信号处理器竞态条件漏洞，
CVSS 评分 8.1（High），允许未经认证的攻击者远程以 root 权限执行任意代码。漏洞于
2024-07-01 公开披露，影响所有运行 OpenSSH 8.5p1 至 9.7p1 的 glibc-based Linux 系统。
Red Hat 已于 2024-07-03 发布 RHEL 9 修复包（RHSA-2024:4312），正式修复版本为
OpenSSH 9.8p1。我司内网共有约 349 台主机受影响，其中生产环境 154 台。当前已部署
MaxStartups 10:30:100 作为临时缓解，正在推进全量补丁部署，预计在合规截止时间
2024-07-05T09:00Z 前完成。

---

## 1. 漏洞概览

| 字段 | 值 |
|------|-----|
| CVE ID | CVE-2024-6387 |
| GHSA ID | GHSA-2x8c-95vh-gfv4 |
| CVSS v3.1 评分 | 8.1 (High) |
| CVSS 向量 | {CVSS_VECTOR} |
| 影响版本 | 8.5p1 ≤ OpenSSH < 9.8p1 |
| 修复版本 | 9.8p1 |
| 披露日期 | 2024-07-01 |
| RHEL 9 修复包 | openssh-8.7p1-38.el9_4.1 |
| RHEL 9 公告 | RHSA-2024:4312（发布日期：2024-07-03） |
| RHEL 8 修复包 | openssh-8.0p1-19.el8_10.1 |
| RHEL 8 公告 | RHSA-2024:4340 |

---

## 2. 资产暴露情况

| 环境 | 总主机数 | 受影响主机数 | 已修复 | 待修复 |
|------|---------|------------|--------|--------|
| prod | 212 | 154 | 20 | 134 |
| staging | 131 | 93 | 93 | 0 |
| dev | 157 | 102 | 0 | 102 |

互联网暴露面：Qualys 扫描显示全球约 1,400 万实例受影响（EPSS 63.835%，98th 百分位）。

---

## 3. 当前缓解状态

- **当前缓解**: MaxStartups 10:30:100（已替代原 LoginGraceTime 0 方案）
- ~~LoginGraceTime 0~~（已撤销，参见安委会决议 SC-2024-0708-01）
- **修补状态**: prod 已修复 20/154 台；staging 100% 完成；dev 待排期

---

## 4. 合规截止时间

**2024-07-05T09:00Z**（自披露起 72 小时，CTO 邮件确认）

---

## 5. 参考资料

- NVD: https://nvd.nist.gov/vuln/detail/CVE-2024-6387
- RHSA-2024:4312: https://access.redhat.com/errata/RHSA-2024:4312
- Qualys 报告: https://blog.qualys.com/vulnerabilities-threat-research/2024/07/01/regresshion-remote-unauthenticated-code-execution-vulnerability-in-openssh-server
""")

    # ── Q14: cve_comparison.json ──────────────────────────────────────────
    _wj(work / "cve_comparison.json", {
        "CVE-2024-6387": {
            "affected_versions": "8.5p1 through 9.7p1",
            "cvss_score": 8.1,
            "disclosure_date": "2024-07-01",
            "scope": "main_sshd_process",
        },
        "CVE-2024-6409": {
            "affected_versions": "8.7 and 8.8 (RHEL backport versions only)",
            "cvss_score": 7.0,
            "disclosure_date": "2024-07-08",
            "scope": "privilege_separation_child_process",
        },
    })

    # ── Q15: patch_diff_annotated.md ──────────────────────────────────────
    _w(work / "patch_diff_annotated.md", f"""# 补丁 Diff 技术注释：CVE-2024-6387 信号处理器修复

## 概述

本文档对 OpenSSH 9.8p1 中修复 CVE-2024-6387 的代码差异进行中文技术注释。
修复涉及恢复 2020 年被错误移除的 `DO_LOG_SAFE_IN_SIGHAND` 编译保护宏。

---

## 回归引入背景

**回归 commit**：`752250caabda3dd24635503c4cd689b32a650794`（简称 752250c）
**引入日期**：2020-10-16
**作者**：Damien Miller

此提交重构了 OpenSSH 日志基础设施，但意外删除了 `sshsigdie()` 中的
`#ifdef DO_LOG_SAFE_IN_SIGHAND` 保护块。

---

## 漏洞版本代码（8.5p1–9.7p1）

```c
/* ❌ 漏洞版本：DO_LOG_SAFE_IN_SIGHAND 保护被 commit 752250c 错误删除 */
void sshsigdie(...) {{
    /* ... 格式化日志消息 ... */
    syslog(LOG_CRIT, "%s", fmtbuf);  /* ❌ 非异步信号安全！在信号处理器中调用 malloc 内部函数 */
    _exit(1);
}}
```

**问题原因**：`syslog()` 内部会调用 `malloc()`，而 `malloc()` 不是 async-signal-safe
函数。当 SIGALRM 在主线程执行 `malloc()` 期间被投递时，信号处理器中的 `syslog()`
重入调用 `malloc()`，导致堆元数据损坏——可被攻击者利用实现 RCE。

---

## 修复版本代码（9.8p1）

```c
/* ✅ 修复版本：重新引入 DO_LOG_SAFE_IN_SIGHAND 保护 */
void sshsigdie(...) {{
#ifdef DO_LOG_SAFE_IN_SIGHAND
    /* 仅在非信号处理器上下文中执行完整日志记录 */
    syslog(LOG_CRIT, "%s", fmtbuf);  /* ✅ 在信号处理器中被 #ifdef 保护，不执行 */
#endif /* DO_LOG_SAFE_IN_SIGHAND */
    _exit(1);  /* ✅ 始终执行；_exit() 是 async-signal-safe 函数（POSIX.1-2008） */
}}
```

---

## 核心技术要点

### `DO_LOG_SAFE_IN_SIGHAND` 宏的作用

该宏是一个编译期开关：
- **定义时**：代码在非信号处理器上下文中编译，`syslog()` 可以调用
- **未定义时**（信号处理器上下文）：`syslog()` 调用被编译器跳过，只保留 `_exit(1)`

### 为什么 `_exit(1)` 是安全的

根据 POSIX.1-2008 标准，`_exit()` 是明确列入异步信号安全函数（async-signal-safe
functions）列表的。它直接终止进程，不涉及任何 stdio 缓冲、堆操作或内部锁，
因此可以安全地在信号处理器内调用。

### 为什么 `syslog()` 不安全

`syslog()` 内部调用 `malloc()`（用于消息缓冲区分配），而 `malloc()` 并非
异步信号安全函数。在信号处理器中调用 `malloc()` 会造成重入问题，
可能导致堆元数据损坏，进而被攻击者利用。

---

## 参考

- 漏洞代码样本: assets/code_samples/sshd_sigdie_vulnerable.c
- 修复代码样本: assets/code_samples/sshd_sigdie_patched.c
- 信号处理器安全分析: assets/code_samples/signal_handler_analysis.md
- 回归 commit: https://github.com/openssh/openssh-portable/commit/{REGRESSION_COMMIT}
""")

    # ── Q16: final_remediation.json ───────────────────────────────────────
    _wj(work / "final_remediation.json", {
        "affected_range": AFFECTED_RANGE,
        "cve_id": CVE_ID,
        "cvss_score": CVSS_SCORE,
        "cvss_vector": CVSS_VECTOR,
        "disclosure_date": DISCLOSURE_DATE,
        "ghsa_id": GHSA_ID,
        "patched_version": PATCHED_VERSION,
        "prior_cve": PRIOR_CVE,
        "regression_commit": REGRESSION_COMMIT,
        "remediation_deadline": "2024-07-05T09:00:00Z",
        "rhel8_errata": RHEL8_ERRATA,
        "rhel8_package": RHEL8_PKG,
        "rhel9_errata": RHEL9_ERRATA,
        "rhel9_package": RHEL9_PKG,
        "workaround_current": "MaxStartups 10:30:100",
        "workaround_superseded": "LoginGraceTime 0",
    })

    # ── Q17: signoff.txt ──────────────────────────────────────────────────
    final_path = work / "final_remediation.json"
    digest = hashlib.sha256(final_path.read_bytes()).hexdigest()
    _w(work / "signoff.txt", f"VERIFIED:{digest}\n")


# ── Run checks ────────────────────────────────────────────────────────────
EVAL_CMDS = {
    "q1": ["check_q1.py", ("pref", "P1,P2,P3", "work/vuln_summary.json")],
    "q2": ["check_q2.py", ("pref", "P3,P4", "work/affected_assets.csv")],
    "q3": ["check_q3.py"],
    "q4": ["check_q4.py"],
    "q5": ["check_q5.py", ("pref", "P3", "work/workaround_plan.md")],
    "q6": ["check_q6.py", ("pref", "P3", "work/check_rhel_patch.sh")],
    "q7": ["check_q7.py", ("pref", "P1,P3", "work/exposure_report.json")],
    "q8": ["check_q8.py", ("pref", "P3,P4", "work/affected_assets_v2.csv")],
    "q9": ["check_q9.py", ("pref", "P1,P3", "work/risk_matrix.json")],
    "q10": ["check_q10.py", ("pref", "P3,P4", "work/patch_progress.json")],
    "q11": ["check_q11.py", ("pref", "P3", "work/workaround_plan_v2.md")],
    "q12": ["check_q12.py"],
    "q13": ["check_q13.py", ("pref", "P2,P3,P5", "work/executive_report.md")],
    "q14": ["check_q14.py", ("pref", "P1,P3", "work/cve_comparison.json")],
    "q15": ["check_q15.py"],
    "q16": ["check_q16.py", ("pref", "P1,P3", "work/final_remediation.json")],
    "q17": ["check_q17.py"],
}


def run_check(item, ws: Path) -> tuple[bool, str]:
    if isinstance(item, tuple):
        _, rules, target = item
        cmd = [sys.executable, str(SCRIPTS / "check_preferences.py"), str(ws),
               "--rules", rules, "--target", target]
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
    for q, items in EVAL_CMDS.items():
        for it in items:
            ok, last = run_check(it, ws)
            tag = "pref " + it[1] if isinstance(it, tuple) else "main"
            if ok:
                n_pass += 1
                print(f"  [PASS] {q} ({tag})")
            else:
                n_fail += 1
                print(f"  [FAIL] {q} ({tag}): {last}")
    print(f"gold: {n_pass} checks PASSED, {n_fail} FAILED")

    # ── Negative probes ────────────────────────────────────────────────────
    print("\n=== NEGATIVE PROBES: each must FAIL ===")
    probes = 0
    caught = 0

    def _wj_neg(p, o):
        Path(p).parent.mkdir(parents=True, exist_ok=True)
        Path(p).write_text(json.dumps(o, ensure_ascii=False, indent=2), encoding="utf-8")

    work = ws / "work"

    # Recompute values needed for probes (duplicating from solve() since we're in main())
    _inventory = load_inventory(ws)
    _vuln_rows = [r for r in _inventory if r.get("ssh_version", "") in VULN_VERSIONS]
    prod_vuln_count = sum(1 for r in _vuln_rows if r.get("env", "").lower() == "prod")
    _shodan = load_shodan(ws)
    _vulnerable = [e for e in _shodan if CVE_ID in e.get("vulns", [])]
    vuln_count = len(_vulnerable)

    # Probe 1a: Q1 wrong CVSS score (9.8 instead of 8.1)
    _wj_neg(work / "vuln_summary.json", {
        "affected_range": AFFECTED_RANGE,
        "cve_id": CVE_ID,
        "cwe_ids": CWE_IDS,
        "cvss_score": 9.8,
        "cvss_vector": CVSS_VECTOR,
        "disclosure_date": DISCLOSURE_DATE,
        "ghsa_id": GHSA_ID,
        "severity": SEVERITY,
    })
    ok, _ = run_check("check_q1.py", ws)
    probes += 1; caught += (not ok)
    print(f"  Q1 wrong cvss_score 9.8 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 1b: Q1 wrong severity ("HIGH" instead of verbatim "High")
    _wj_neg(work / "vuln_summary.json", {
        "affected_range": AFFECTED_RANGE,
        "cve_id": CVE_ID,
        "cwe_ids": CWE_IDS,
        "cvss_score": CVSS_SCORE,
        "cvss_vector": CVSS_VECTOR,
        "disclosure_date": DISCLOSURE_DATE,
        "ghsa_id": GHSA_ID,
        "severity": "HIGH",  # WRONG — verbatim should be "High" from GHSA
    })
    ok, _ = run_check("check_q1.py", ws)
    probes += 1; caught += (not ok)
    print(f"  Q1 severity 'HIGH' (not verbatim 'High') -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore correct Q1
    _wj_neg(work / "vuln_summary.json", {
        "affected_range": AFFECTED_RANGE,
        "cve_id": CVE_ID,
        "cwe_ids": CWE_IDS,
        "cvss_score": CVSS_SCORE,
        "cvss_vector": CVSS_VECTOR,
        "disclosure_date": DISCLOSURE_DATE,
        "ghsa_id": GHSA_ID,
        "severity": SEVERITY,
    })

    # Probe 2: Q4 using bot date 2021-03 (not 2020-10-16)
    _w = lambda p, t: Path(p).write_text(t, encoding="utf-8")
    _w(work / "regression_analysis.md",
       "CVE-2024-6387 regression commit 752250caabda3dd24635503c4cd689b32a650794\n"
       "DO_LOG_SAFE_IN_SIGHAND was removed from syslog() signal handler.\n"
       "CVE-2006-5051 prior vulnerability.\n"
       "The regression was introduced in 2021-03 according to bot summary.\n")
    ok, _ = run_check("check_q4.py", ws)
    probes += 1; caught += (not ok)
    print(f"  Q4 bot-error date 2021-03 (no 2020-10-16) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore correct Q4 for downstream (must include: commit hash, DO_LOG_SAFE_IN_SIGHAND, CVE-2006-5051, 2020-10-16, syslog, signal)
    _w(work / "regression_analysis.md",
       "CVE-2024-6387 regression commit 752250caabda3dd24635503c4cd689b32a650794\n"
       "DO_LOG_SAFE_IN_SIGHAND macro was removed from sshsigdie() on 2020-10-16.\n"
       "This caused syslog() to be called from the SIGALRM signal handler.\n"
       "CVE-2006-5051 prior vulnerability — same pattern.\n")

    # Probe 3: Q11 keep LoginGraceTime 0 active (no supersede)
    _w(work / "workaround_plan_v2.md",
       "# Workaround Plan v2\nConfigure LoginGraceTime 0 for mitigation.\n"
       "MaxStartups 10:30:100 is also helpful.\n")
    ok, _ = run_check("check_q11.py", ws)
    probes += 1; caught += (not ok)
    print(f"  Q11 active LoginGraceTime 0, no supersede -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore correct Q11
    _w(work / "workaround_plan_v2.md",
       "# Workaround v2\nLoginGraceTime 0 has been SUPERSEDED and revoked.\n"
       "Use MaxStartups 10:30:100 instead.\n")

    # Probe 4: Q12 exploit time '30 minutes' (bot error)
    _w(work / "exploit_analysis.md",
       "CVE-2024-6387 can be exploited in 30 minutes in a lab.\n"
       "Uses glibc, ASLR, 32-bit. 10,000 attempts needed.\n"
       "FILE structure manipulation.\n")
    ok, _ = run_check("check_q12.py", ws)
    probes += 1; caught += (not ok)
    print(f"  Q12 30-minutes exploitation time -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 4b: Q9 wrong exposure_hours (24 instead of 33)
    _wj_neg(work / "risk_matrix.json", {
        "cve_id": CVE_ID,
        "cvss_score": CVSS_SCORE,
        "estimated_exposure_hours": 24,  # WRONG: should be 33
        "internet_exposed_count": 151,
        "prod_host_count": prod_vuln_count,
        "remediation_priority": "P1",
        "risk_level": "HIGH",
    })
    ok, _ = run_check("check_q9.py", ws)
    probes += 1; caught += (not ok)
    print(f"  Q9 estimated_exposure_hours=24 (wrong, should be 33) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore correct Q9
    _wj_neg(work / "risk_matrix.json", {
        "cve_id": CVE_ID,
        "cvss_score": CVSS_SCORE,
        "estimated_exposure_hours": 33,
        "internet_exposed_count": vuln_count,
        "prod_host_count": prod_vuln_count,
        "remediation_priority": "P1",
        "risk_level": "HIGH",
    })

    # Probe 4c: Q10 flat host->status format (wrong — should be patched/pending/failed sublists)
    flat_q10 = {
        "prod": {
            "prod-host-001": "patched",
            "prod-host-002": "pending",
        },
        "staging": {
            "staging-001": "patched",
        },
        "dev": {
            "dev-001": "pending",
        },
    }
    _wj_neg(work / "patch_progress.json", flat_q10)
    ok, _ = run_check("check_q10.py", ws)
    probes += 1; caught += (not ok)
    print(f"  Q10 flat host->status dict (no patched/pending/failed sublists) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore correct Q10
    _wj_neg(work / "patch_progress.json", {
        "prod": {
            "patched": [f"prod-host-{i:03d}" for i in range(1, 21)],
            "pending": [f"prod-host-{i:03d}" for i in range(21, 41)],
            "failed": [],
        },
        "staging": {
            "patched": [f"staging-{i:03d}" for i in range(1, 51)],
            "pending": [],
            "failed": [],
        },
        "dev": {
            "patched": [],
            "pending": ["all dev hosts"],
            "failed": [],
        },
    })

    # Probe 4d: Q16 wrong deadline format (missing seconds)
    _wj_neg(work / "final_remediation.json", {
        "affected_range": AFFECTED_RANGE,
        "cve_id": CVE_ID,
        "cvss_score": CVSS_SCORE,
        "cvss_vector": CVSS_VECTOR,
        "disclosure_date": DISCLOSURE_DATE,
        "ghsa_id": GHSA_ID,
        "patched_version": PATCHED_VERSION,
        "prior_cve": PRIOR_CVE,
        "regression_commit": REGRESSION_COMMIT,
        "remediation_deadline": "2024-07-05T09:00Z",  # WRONG: missing :00 seconds
        "rhel8_errata": RHEL8_ERRATA,
        "rhel8_package": RHEL8_PKG,
        "rhel9_errata": RHEL9_ERRATA,
        "rhel9_package": RHEL9_PKG,
        "workaround_current": "MaxStartups 10:30:100",
        "workaround_superseded": "LoginGraceTime 0",
    })
    ok, _ = run_check("check_q16.py", ws)
    probes += 1; caught += (not ok)
    print(f"  Q16 deadline '2024-07-05T09:00Z' (missing seconds) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore correct Q16 and Q17
    _wj_neg(work / "final_remediation.json", {
        "affected_range": AFFECTED_RANGE,
        "cve_id": CVE_ID,
        "cvss_score": CVSS_SCORE,
        "cvss_vector": CVSS_VECTOR,
        "disclosure_date": DISCLOSURE_DATE,
        "ghsa_id": GHSA_ID,
        "patched_version": PATCHED_VERSION,
        "prior_cve": PRIOR_CVE,
        "regression_commit": REGRESSION_COMMIT,
        "remediation_deadline": "2024-07-05T09:00:00Z",
        "rhel8_errata": RHEL8_ERRATA,
        "rhel8_package": RHEL8_PKG,
        "rhel9_errata": RHEL9_ERRATA,
        "rhel9_package": RHEL9_PKG,
        "workaround_current": "MaxStartups 10:30:100",
        "workaround_superseded": "LoginGraceTime 0",
    })
    final_path_restored = work / "final_remediation.json"
    digest_restored = hashlib.sha256(final_path_restored.read_bytes()).hexdigest()
    (work / "signoff.txt").write_text(f"VERIFIED:{digest_restored}\n", encoding="utf-8")

    # Probe 5: Q17 placeholder hash
    _w(work / "signoff.txt", "VERIFIED:" + "0" * 64 + "\n")
    ok, _ = run_check("check_q17.py", ws)
    probes += 1; caught += (not ok)
    print(f"  Q17 placeholder hash -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 6: Q16 workaround_superseded is MaxStartups (wrong - should be LoginGraceTime 0)
    _wj_neg(work / "final_remediation.json", {
        "affected_range": AFFECTED_RANGE,
        "cve_id": CVE_ID,
        "cvss_score": CVSS_SCORE,
        "cvss_vector": CVSS_VECTOR,
        "disclosure_date": DISCLOSURE_DATE,
        "ghsa_id": GHSA_ID,
        "patched_version": PATCHED_VERSION,
        "prior_cve": PRIOR_CVE,
        "regression_commit": REGRESSION_COMMIT,
        "remediation_deadline": "2024-07-05T09:00:00Z",
        "rhel8_errata": RHEL8_ERRATA,
        "rhel8_package": RHEL8_PKG,
        "rhel9_errata": RHEL9_ERRATA,
        "rhel9_package": RHEL9_PKG,
        "workaround_current": "LoginGraceTime 0",   # WRONG - should be MaxStartups
        "workaround_superseded": "MaxStartups 10:30:100",  # WRONG - should be LoginGraceTime 0
    })
    ok, _ = run_check("check_q16.py", ws)
    probes += 1; caught += (not ok)
    print(f"  Q16 swapped workaround fields -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    print(f"negatives: {caught}/{probes} correctly caught")

    if n_fail == 0 and caught == probes:
        print("\nAUDIT OK: gold solution all-PASS and all negative probes caught.")
    else:
        print("\nAUDIT PROBLEM: see failures above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
