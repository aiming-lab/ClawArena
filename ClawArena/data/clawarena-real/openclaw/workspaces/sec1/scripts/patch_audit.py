#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
patch_audit.py — 批量审计内网资产清单，统计 CVE-2024-6387 漏洞暴露情况。
输入: assets/scan_results/internal_inventory.csv
输出: 按环境分组的漏洞统计报告
"""
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
