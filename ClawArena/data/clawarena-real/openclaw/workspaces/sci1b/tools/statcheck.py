#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
statcheck.py — Reproduce between-condition statistical comparisons.

Reads pnas_study1_dataset.csv and computes:
- Group means for expense_claimed_usd (bottom vs top)
- Overreport rates for puzzles (bottom vs top)
- Two-sample t-tests for both outcomes

Usage: python statcheck.py <path_to_dataset_csv>
"""
import sys
import csv
import math


def welch_t(a: list[float], b: list[float]):
    """Two-sample Welch t-test (unequal variances)."""
    n1, n2 = len(a), len(b)
    m1, m2 = sum(a) / n1, sum(b) / n2
    v1 = sum((x - m1)**2 for x in a) / (n1 - 1)
    v2 = sum((x - m2)**2 for x in b) / (n2 - 1)
    se = math.sqrt(v1 / n1 + v2 / n2)
    t = (m1 - m2) / se if se > 0 else 0.0
    # Approximate df (Welch–Satterthwaite)
    df = (v1/n1 + v2/n2)**2 / ((v1/n1)**2/(n1-1) + (v2/n2)**2/(n2-1))
    return t, df, m1, m2


def main():
    if len(sys.argv) < 2:
        print("Usage: python statcheck.py <dataset.csv>"); sys.exit(1)
    bottom_exp, top_exp = [], []
    bottom_over, top_over = [], []
    with open(sys.argv[1], newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            cond = row["condition"]
            exp = float(row["expense_claimed_usd"])
            over = int(row["overreported"])
            if cond == "bottom":
                bottom_exp.append(exp)
                bottom_over.append(over)
            elif cond == "top":
                top_exp.append(exp)
                top_over.append(over)
    t_exp, df_exp, m_bot, m_top = welch_t(bottom_exp, top_exp)
    over_bot_pct = round(100 * sum(bottom_over) / len(bottom_over))
    over_top_pct = round(100 * sum(top_over) / len(top_over))
    print(f"Bottom N={len(bottom_exp)}, Top N={len(top_exp)}")
    print(f"Mean expense  — bottom: {m_bot:.2f}, top: {m_top:.2f}")
    print(f"t({df_exp:.1f}) = {t_exp:.3f}")
    print(f"Overreport %  — bottom: {over_bot_pct}%, top: {over_top_pct}%")
    print(f"Reference anchors: expense_bottom≈9.62, expense_top≈5.27")
    print(f"Reference overreport: bottom=79%, top=37%, p=0.0013")


if __name__ == "__main__":
    main()
