#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calcchain_parser.py — Extract and compare calcChain order vs visible row order
from an Excel (.xlsx) workbook.

Usage: python calcchain_parser.py <path_to_xlsx> [--sheet Sheet1]
"""
import sys
import zipfile
import xml.etree.ElementTree as ET
import csv
import argparse


def parse_calcchain(xlsx_path: str) -> list[int]:
    """Return list of row numbers in calcChain order."""
    with zipfile.ZipFile(xlsx_path) as zf:
        if "xl/calcChain.xml" not in zf.namelist():
            return []
        tree = ET.parse(zf.open("xl/calcChain.xml"))
    ns = {"c": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    rows = []
    for cell in tree.getroot().findall(".//c:c", ns):
        ref = cell.get("r", "")
        row_str = "".join(ch for ch in ref if ch.isdigit())
        if row_str:
            rows.append(int(row_str))
    return rows


def compare_orders(calcchain_rows: list[int], visible_rows: int) -> list[int]:
    """Return list of row indices (1-based) that are out of order."""
    expected = list(range(2, visible_rows + 2))  # data starts at row 2 (header row 1)
    suspicious = []
    for i, (calc, vis) in enumerate(zip(calcchain_rows, expected)):
        if calc != vis:
            suspicious.append(vis)
    return suspicious


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xlsx_path")
    ap.add_argument("--sheet", default="Sheet1")
    args = ap.parse_args()
    calc_rows = parse_calcchain(args.xlsx_path)
    print(f"calcChain rows parsed: {len(calc_rows)}")
    suspicious = compare_orders(calc_rows, len(calc_rows))
    print(f"Suspicious rows (calcChain mismatch): {len(suspicious)}")
    print(f"Suspicious row numbers: {suspicious}")


if __name__ == "__main__":
    main()
