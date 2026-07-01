#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_cdph_log.py — Generates a CDPH-format staffing log CSV from raw
scheduling data, per Title 22 § 70217(d) record-keeping requirements.

Usage: python generate_cdph_log.py <input.csv> <output.csv>
"""
import csv
import sys

FIELDNAMES = ["date", "shift_start", "shift_end", "unit", "nurse_id",
              "license_type", "patient_count", "ratio"]

def generate_log(input_path: str, output_path: str) -> None:
    rows = []
    with open(input_path, encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            shift_parts = row.get("shift", "").split(" ")
            shift_start = shift_parts[1].split("-")[0] if len(shift_parts) > 1 else "07:00"
            shift_end = shift_parts[1].split("-")[1] if len(shift_parts) > 1 else "19:00"
            try:
                nurses = int(row.get("nurses_on_duty_count", 1))
                patients = int(row.get("patient_count", 0))
                ratio = round(patients / max(nurses, 1), 2)
            except ValueError:
                ratio = 0.0
            for nid in row.get("nurse_ids", "").split(","):
                nid = nid.strip()
                if not nid:
                    continue
                rows.append({
                    "date": row.get("date"),
                    "shift_start": shift_start,
                    "shift_end": shift_end,
                    "unit": row.get("unit"),
                    "nurse_id": nid,
                    "license_type": row.get("license_type", "RN"),
                    "patient_count": patients,
                    "ratio": f"{ratio:.2f}",
                })
    with open(output_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Generated {len(rows)} entries in {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: generate_cdph_log.py <input.csv> <output.csv>")
        sys.exit(1)
    generate_log(sys.argv[1], sys.argv[2])
