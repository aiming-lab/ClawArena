#!/usr/bin/env python3
"""check_near_miss_log.py — validate q15 outputs:
  analysis/near_miss_event_log.json and analysis/presenteeism_vs_absenteeism.md

JSON checks:
  - Array of exactly 2 events
  - NM-1: shift_duration_h >= 18, clinalert_filed=false
  - NM-2: shift_duration_h >= 14, clinalert_filed=false

MD checks:
  - '4.2' and '4.6' present
  - 'presenteeism' discussed
  - >=3 ## headings
"""
import sys
import json
import re
from pathlib import Path


def _find_entry(data, keywords):
    for e in data:
        eid = str(e.get("event_id", "")).upper()
        etype = str(e.get("type", "")).lower()
        for kw in keywords:
            if kw.upper() in eid or kw.lower() in etype:
                return e
    return None


def main():
    if len(sys.argv) < 2:
        print("FAILED: usage: check_near_miss_log.py <workspace>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    # --- File 1: analysis/near_miss_event_log.json ---
    json_path = workspace / "analysis" / "near_miss_event_log.json"
    if not json_path.exists():
        print(f"FAILED: {json_path} not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: near_miss_event_log.json is not valid JSON: {e}")
        sys.exit(1)

    if not isinstance(data, list):
        print("FAILED: near_miss_event_log.json root must be a JSON array")
        sys.exit(1)

    if len(data) != 2:
        errors.append(f"near_miss_event_log.json: array length expected 2, got {len(data)}")
    else:
        nm1 = _find_entry(data, ["NM-1", "NM1", "dosage", "dose"])
        if nm1 is None:
            errors.append("near_miss_event_log.json: NM-1 (dosage confusion) entry not found")
        else:
            dur = nm1.get("shift_duration_h")
            try:
                if float(dur) < 18:
                    errors.append(f"near_miss_event_log.json: NM-1 shift_duration_h={dur} < 18")
            except (TypeError, ValueError):
                errors.append(f"near_miss_event_log.json: NM-1 shift_duration_h '{dur}' is not a number")
            if nm1.get("clinalert_filed") is not False:
                errors.append(f"near_miss_event_log.json: NM-1 clinalert_filed expected false, got {nm1.get('clinalert_filed')!r}")

        nm2 = _find_entry(data, ["NM-2", "NM2", "wrong", "route"])
        if nm2 is None:
            errors.append("near_miss_event_log.json: NM-2 (wrong-route) entry not found")
        else:
            dur = nm2.get("shift_duration_h")
            try:
                if float(dur) < 14:
                    errors.append(f"near_miss_event_log.json: NM-2 shift_duration_h={dur} < 14")
            except (TypeError, ValueError):
                errors.append(f"near_miss_event_log.json: NM-2 shift_duration_h '{dur}' is not a number")
            if nm2.get("clinalert_filed") is not False:
                errors.append(f"near_miss_event_log.json: NM-2 clinalert_filed expected false, got {nm2.get('clinalert_filed')!r}")

    # --- File 2: analysis/presenteeism_vs_absenteeism.md ---
    md_path = workspace / "analysis" / "presenteeism_vs_absenteeism.md"
    if not md_path.exists():
        print(f"FAILED: {md_path} not found")
        sys.exit(1)

    md = md_path.read_text(encoding="utf-8")

    if not re.search(r'(?<!\d)4\.2(?!\d)', md):
        errors.append("presenteeism_vs_absenteeism.md: '4.2' (unit sick leave rate) not found")
    if not re.search(r'(?<!\d)4\.6(?!\d)', md):
        errors.append("presenteeism_vs_absenteeism.md: '4.6' (hospital sick leave avg) not found")
    if not re.search(r'\bpresenteeism\b', md, re.IGNORECASE):
        errors.append("presenteeism_vs_absenteeism.md: 'presenteeism' not discussed")

    headings = re.findall(r'^##\s+.+', md, re.MULTILINE)
    if len(headings) < 3:
        errors.append(f"presenteeism_vs_absenteeism.md: found {len(headings)} ## headings, need >=3")

    if errors:
        for e in errors:
            print(f"FAILED: {e}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
