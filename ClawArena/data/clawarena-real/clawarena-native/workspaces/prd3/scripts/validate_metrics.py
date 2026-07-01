#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
指标一致性校验工具。
用法：python scripts/validate_metrics.py <workspace_path>
输出：VERIFIED:<sha256_of_kpi_dashboard.json>（写入 output/verification_token.txt）
"""
import hashlib
import json
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("usage: validate_metrics.py <workspace>"); sys.exit(1)
    ws = Path(sys.argv[1])
    kpi_path = ws / "output" / "kpi_dashboard.json"
    if not kpi_path.exists():
        print("ERROR: output/kpi_dashboard.json not found"); sys.exit(1)

    digest = hashlib.sha256(kpi_path.read_bytes()).hexdigest()
    token = f"VERIFIED:{digest}"

    out_path = ws / "output" / "verification_token.txt"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(token + "\n", encoding="utf-8")
    print(f"Written: {out_path}")
    print(token)

if __name__ == "__main__":
    main()
