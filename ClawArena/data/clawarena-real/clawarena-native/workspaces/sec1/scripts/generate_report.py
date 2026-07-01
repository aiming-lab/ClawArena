#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_report.py — 从 work/ 目录的产物生成最终 HTML 或 Markdown 报告。
"""
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
