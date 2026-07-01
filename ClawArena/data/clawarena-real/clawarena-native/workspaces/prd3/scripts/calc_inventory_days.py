#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
库存周转天数计算（JD 官方口径：×360，5 季度平均库存）。
用法：python scripts/calc_inventory_days.py <inventory_calc_csv>
输出：inventory_days, formula_used, multiplier
"""
import csv
import sys
import json
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("usage: calc_inventory_days.py <calc_csv>"); sys.exit(1)
    path = Path(sys.argv[1])
    data = {}
    with open(path, encoding="utf-8") as fh:
        for row in csv.reader(fh):
            if len(row) >= 2:
                data[row[0]] = row[1]

    avg_inv = float(data.get("avg_5q", 0))
    ttm_cogs = float(data.get("ttm_cogs", 1))
    inv_days = round(avg_inv / ttm_cogs * 360, 1)

    result = {
        "inventory_days": inv_days,
        "formula_used": "(avg_inventory_5q / ttm_cogs) * 360",
        "multiplier": 360,
        "quarters_used": "5 quarters",
        "avg_inventory_5q": avg_inv,
        "ttm_cogs": ttm_cogs,
        "source": "JD.com Full Year 2024 Results formula",
        "source_url": "https://www.globenewswire.com/news-release/2025/03/06/3037984/0/en/JD-com-Announces-Fourth-Quarter-and-Full-Year-2024-Results-and-Annual-Dividend.html"
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
