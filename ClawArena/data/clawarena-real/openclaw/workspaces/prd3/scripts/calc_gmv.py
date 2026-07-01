#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GMV 闭合校验脚本。
用法：python scripts/calc_gmv.py <gmv_csv_path>
验证：GMV = orders × AOV（每行闭合，容差 0.5%）。
v1 数据含 Method 1 口径污染，预期输出 status=FAIL。
"""
import csv
import sys
import json
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("usage: calc_gmv.py <gmv_csv_path>"); sys.exit(1)
    path = Path(sys.argv[1])
    if not path.exists():
        print(json.dumps({"status": "ERROR", "message": "file not found: " + str(path)}))
        sys.exit(1)

    failures = []
    method1_rows = []
    with open(path, encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                orders = int(row["orders"])
                aov = float(row["aov"])
                gmv = float(row["gmv_rmb_million"]) * 1_000_000
                computed = orders * aov
                delta_pct = abs(computed - gmv) / max(gmv, 1) * 100
                if delta_pct > 0.5:
                    failures.append({
                        "date": row.get("date"), "category": row.get("category"),
                        "channel": row.get("channel"), "delta_pct": round(delta_pct, 4)
                    })
                if row.get("gmv_method") == "method1":
                    method1_rows.append(row.get("date"))
            except (ValueError, KeyError):
                pass

    method1_dates = sorted(set(method1_rows))
    status = "FAIL" if method1_rows else "PASS"
    result = {
        "status": status,
        "method1_row_count": len(method1_rows),
        "method1_dates": method1_dates[:10],  # first 10
        "delta_pct": round(sum(f["delta_pct"] for f in failures) / max(len(failures), 1), 4),
        "affected_date_range": {
            "start": method1_dates[0] if method1_dates else None,
            "end": method1_dates[-1] if method1_dates else None
        } if method1_dates else None,
        "total_rows_checked": sum(1 for _ in csv.DictReader(open(path, encoding="utf-8")))
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
