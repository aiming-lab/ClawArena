#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gold_solve_eng2.py — eng2 可解性审计（金标自检）。

在 workspace 的临时副本上模拟 update 生效后的状态，写出每一轮的「正确产物」，
然后运行全部 check_qN.py + 对应 preference，断言正解全部 PASS。
再做一组反例（错误产物）抽样，断言 check 能 FAIL（不过松）。

V2 加难版：
- q1: 增 borough_counts / service_zone_counts / schema_version
- q2: 增 schema_version
- q3: 增 airport_fee / cbd_congestion_fee 引用
- q4: exact match + RatecodeID entry
- q7: 增 RatecodeID + total_zone_count + cross-round 连锁
- q8: 增 module docstring
- q10: exact trip_count per month; total_trip_count=3062
- q12: exact total_before=3772 / rows_removed=805 / total_after=2967; P1
- q13: deprecated_fields in archive-header order; P1
- q14: exact per-borough counts + grand_total=2934; grand_total cross-check

运行：python scripts/clawarena_authoring/gold_solve_eng2.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DS = REPO / "data" / "clawarena-real"
WS_SRC = DS / "openclaw" / "workspaces" / "eng2"
UPD = DS / "openclaw" / "updates" / "eng2"
SCRIPTS = DS / "eval" / "eng2" / "scripts"
GOLD = Path("/home/xkaiwen/.claude/jobs/579de28f/tmp/eng2_gold_ws")

FIELDS_ORDER = ["field_name", "null_count", "null_pct", "invalid_count", "invalid_pct", "notes"]


def f4(x: float) -> float:
    return round(float(x), 4)


def prep_workspace() -> Path:
    if GOLD.exists():
        shutil.rmtree(GOLD)
    shutil.copytree(WS_SRC, GOLD)
    # 应用 update workspace 文件（new = 覆盖/新增）
    shutil.copy(UPD / "upd1_workspace" / "quality_rules.yaml", GOLD / "pipeline" / "config" / "quality_rules.yaml")
    shutil.copy(UPD / "upd1_workspace" / "yellow_202301_anomalies_sample.csv", GOLD / "data" / "raw" / "yellow_202301_anomalies_sample.csv")
    shutil.copy(UPD / "upd2_workspace" / "vendor_registry.json", GOLD / "data" / "reference" / "vendor_registry.json")
    shutil.copy(UPD / "upd2_workspace" / "yellow_202306_vendor6_sample.csv", GOLD / "data" / "raw" / "yellow_202306_vendor6_sample.csv")
    return GOLD


def read_csv(p: Path) -> list[dict]:
    with p.open(encoding="utf-8") as fh:
        return [r for r in csv.DictReader(fh) if r.get("VendorID", "").strip().isdigit()]


PY_HEADER = "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n"


def solve(ws: Path) -> None:
    out = ws / "output"; out.mkdir(exist_ok=True)
    profile = json.loads((ws / "data" / "reference" / "dataset_profile.json").read_text())
    zones = read_csv_zones(ws / "data" / "reference" / "taxi_zone_lookup.csv")
    sample = read_csv(ws / "data" / "raw" / "yellow_tripdata_2023_sample.csv")

    # q1 — borough_counts, service_zone_counts, schema_version (F/E)
    boroughs = sorted({r["Borough"] for r in zones.values()})
    from collections import Counter
    borough_counts = dict(Counter(r["Borough"] for r in zones.values()))
    sz_counts = dict(Counter(r["service_zone"] for r in zones.values()))
    _wj(out / "q1_zone_stats.json", {
        "schema_version": "1.0",
        "total_locations": len(zones),
        "boroughs": boroughs,
        "borough_counts": borough_counts,
        "service_zone_counts": sz_counts,
    })

    # q2 — schema_version (E/P1)
    _wj(out / "q2_schema_diff.json", {
        "schema_version": "1.0",
        "added_fields": ["airport_fee", "cbd_congestion_fee"],
        "v1_missing_count": 2,
    })

    # q3 bronze ingest — airport_fee + cbd_congestion_fee verbatim (F)
    _w(ws / "pipeline" / "bronze" / "ingest.py", PY_HEADER + (
        'import duckdb\n'
        '# Bronze ingest conforming to schema_v2 — official verbatim columns\n'
        'COLS = ["VendorID", "tpep_pickup_datetime", "tpep_dropoff_datetime", "passenger_count",\n'
        '        "trip_distance", "RatecodeID", "store_and_fwd_flag", "PULocationID", "DOLocationID",\n'
        '        "payment_type", "fare_amount", "congestion_surcharge", "airport_fee", "cbd_congestion_fee"]\n'
        'def ingest(path):\n'
        '    return duckdb.sql(f"SELECT * FROM read_csv_auto(\'{path}\')")\n'))

    # q4 quality report — exact match; RatecodeID entry required (A/F)
    nc = profile["fields"]["passenger_count"]["null_count"]      # 1309356
    nc_rc = profile["fields"]["RatecodeID"]["null_count"]        # 1309356
    total = profile["total_rows"]                                 # 38310226
    _wj(out / "q4_quality_report.json", {"schema_version": "1.0", "fields": [
        _qentry("passenger_count", nc, total, 0, total, "Authoritative null count from dataset_profile.json"),
        _qentry("RatecodeID", nc_rc, total, 0, total, "Authoritative null count from dataset_profile.json"),
    ]})

    # q5 negative fares
    fares = [float(r["fare_amount"]) for r in sample if r["fare_amount"] not in ("", None)]
    neg = [x for x in fares if x < 0]
    _wj(out / "q5_negative_fares.json", {"filtered_count": len(neg), "min_observed_fare": f4(min(fares))})

    # q6 timestamp anomalies
    yrs = [int(r["tpep_pickup_datetime"][:4]) for r in sample if r["tpep_pickup_datetime"][:4].isdigit()]
    bad_years = sorted({y for y in yrs if y < 2009 or y > 2024})
    anomaly_count = sum(1 for y in yrs if y < 2009 or y > 2024)
    _wj(out / "q6_timestamp_anomalies.json", {
        "anomaly_count": anomaly_count,
        "future_year_examples": bad_years,
    })

    # q7 revised report — cross-round closure: q4 (passenger_count + RatecodeID), q6 (anomaly_count), q1 (total_locations) (C)
    _wj(out / "q7_quality_report_v2.json", {
        "schema_version": "1.0",
        "timestamp_anomaly_count": anomaly_count,           # exact match with q6
        "total_zone_count": len(zones),                     # exact match with q1 (265)
        "fields": [
            _qentry("passenger_count", nc, total, 0, total, "Carried forward from q4"),
            _qentry("RatecodeID", nc_rc, total, 0, total, "Carried forward from q4"),
        ],
    })

    # q8 silver clean — module docstring required (F/G)
    _w(ws / "pipeline" / "silver" / "clean.py", PY_HEADER + (
        '"""Silver cleaning pipeline: apply quality_rules.yaml filters.\n'
        'Filter 1: fare_amount >= 0.0 (min_valid from quality_rules.yaml)\n'
        'Filter 2: trip_distance <= 300 (max_valid from quality_rules.yaml)\n'
        'Filter 3: tpep_pickup_datetime year in 2009-2024 (valid_year_range)\n"""\n'
        'MAX_TRIP_DISTANCE = 300  # max_valid from quality_rules.yaml\n'
        'MIN_FARE = 0.0           # min_valid from quality_rules.yaml\n'
        'def clean(rows):\n'
        '    out = []\n'
        '    for r in rows:\n'
        '        if float(r["fare_amount"]) < MIN_FARE: continue\n'
        '        if float(r["trip_distance"]) > MAX_TRIP_DISTANCE: continue\n'
        '        y = int(r["tpep_pickup_datetime"][:4])\n'
        '        if y < 2009 or y > 2024: continue\n'
        '        out.append(r)\n'
        '    return out\n'))

    # q9 enrich (LEFT JOIN, taxi_zone_lookup, Unknown fallback)
    _w(ws / "pipeline" / "silver" / "enrich.py", PY_HEADER + (
        'import csv\n'
        'ZONE_LOOKUP_FILE = "data/reference/taxi_zone_lookup.csv"\n'
        'def load_zones(path):\n'
        '    # Reads taxi_zone_lookup.csv — authoritative reference for Borough mapping\n'
        '    with open(path) as fh:\n'
        '        return {r["LocationID"]: r["Borough"] for r in csv.DictReader(fh)}\n'
        'def enrich(rows, zone_lookup_path=ZONE_LOOKUP_FILE):\n'
        '    # LEFT JOIN on PULocationID = LocationID; unmatched rows -> Borough = Unknown\n'
        '    zones = load_zones(zone_lookup_path)\n'
        '    for r in rows:\n'
        '        r["pickup_borough"] = zones.get(r["PULocationID"], "Unknown")\n'
        '    return rows\n'))

    # q10 daily summary — exact trip_count per month; total_trip_count (F/C)
    by_month: dict = defaultdict(list)
    for r in sample:
        y = r["tpep_pickup_datetime"][:4]
        if y != "2023":
            continue
        fa = float(r["fare_amount"])
        dist = float(r["trip_distance"])
        if fa < 0:
            continue
        by_month[r["tpep_pickup_datetime"][:7]].append((fa, dist))
    summ: dict = {}
    total_trips = 0
    for m in range(1, 13):
        key = f"2023-{m:02d}"
        rows_m = by_month.get(key, [])
        if not rows_m:
            rows_m = [(15.0, 2.0)]
        tc = len(rows_m)
        total_trips += tc
        summ[key] = {
            "trip_count": tc,
            "avg_fare": f4(sum(a for a, _ in rows_m) / len(rows_m)),
            "avg_distance": f4(sum(d for _, d in rows_m) / len(rows_m)),
        }
    summ["total_trip_count"] = total_trips   # C: cross-round anchor (3062)
    summ["schema_version"] = "1.0"
    _wj(out / "q10_daily_summary.json", summ)

    # q11 clean_v2 (exclude VendorID=6, supersede)
    _w(ws / "pipeline" / "silver" / "clean_v2.py", PY_HEADER + (
        'def clean_v2(rows):\n'
        '    # Ops notice SUPERSEDES the earlier audit_only rule: exclude VendorID=6 entirely.\n'
        '    out = []\n'
        '    for r in rows:\n'
        '        if int(r["VendorID"]) == 6: continue\n'
        '        if float(r["fare_amount"]) < 0: continue\n'
        '        y = int(r["tpep_pickup_datetime"][:4])\n'
        '        if y < 2009 or y > 2024: continue\n'
        '        out.append(r)\n'
        '    return out\n'))

    # q12 vendor filter report — exact counts (F): total_before=3772, removed=805, after=2967; P1
    vendor6_csv = read_csv(ws / "data" / "raw" / "yellow_202306_vendor6_sample.csv")
    combined = sample + vendor6_csv
    rr = sum(1 for r in combined if r["VendorID"] == "6")
    tb = len(combined)
    _wj(out / "q12_vendor_filter_report.json", {
        "schema_version": "1.0",
        "total_before": tb,
        "rows_removed_vendor6": rr,
        "total_after": tb - rr,
    })

    # q13 archive compat — deprecated_fields in archive-header order; schema_version (F/P1)
    _wj(out / "q13_archive_compat.json", {
        "schema_version": "1.0",
        "compatible": False,
        "deprecated_fields": [
            "pickup_datetime", "dropoff_datetime",
            "pickup_longitude", "pickup_latitude",
            "dropoff_longitude", "dropoff_latitude",
        ],
    })

    # q14 payment_type × borough pivot — exact per-borough counts, grand_total=2934; C
    pivot: dict = defaultdict(lambda: defaultdict(int))
    for r in sample:
        if r["VendorID"] == "6" or float(r["fare_amount"]) < 0:
            continue
        zrow = zones.get(r["PULocationID"])
        boro = zrow["Borough"] if zrow else "Unknown"
        pivot[str(r["payment_type"])][boro] += 1
    q14: dict = {k: dict(v) for k, v in pivot.items()}
    grand_total = sum(sum(v.values()) for v in pivot.values())
    q14["grand_total"] = grand_total
    q14["schema_version"] = "1.0"
    _wj(out / "q14_payment_zone_pivot.json", q14)

    # q15 checklist (>= 10 [x], SLACK-A20-VENDOR6-KEEP, audit_only)
    _w(out / "q15_migration_checklist.md", (
        "# Migration Checklist\n\n## Completed\n"
        "- [x] Schema diff (v1 vs v2; airport_fee, cbd_congestion_fee added; v1_missing_count=2)\n"
        "- [x] Bronze ingest scaffold (verbatim columns: tpep_pickup_datetime, airport_fee, cbd_congestion_fee, DuckDB read)\n"
        "- [x] Field-level null/quality reporting (passenger_count null_count = 1,309,356; RatecodeID null_count = 1,309,356 from dataset_profile.json)\n"
        "- [x] Negative fare_amount handling (min_observed_fare = -1087.30; scan confirmed against raw sample)\n"
        "- [x] Timestamp anomaly detection (future_year_examples: 2084, 2088; anomaly_count confirmed)\n"
        "- [x] Revised quality rules applied (timestamp valid_year_range 2009-2024, max_valid trip_distance 300 miles)\n"
        "- [x] Silver clean (fare_amount >= 0.0, trip_distance <= 300, year 2009-2024; includes module docstring)\n"
        "- [x] Enrich / LEFT JOIN Borough on PULocationID = LocationID from taxi_zone_lookup; Unknown fallback\n"
        "- [x] Gold daily summary (12 months 2023-01 to 2023-12; negative fares excluded; year=2023 only; total_trip_count=3062)\n"
        "- [x] Payment-type × Borough pivot (payment_type codes 1-4, VendorID=6 and negative fares excluded, grand_total=2934)\n"
        "- [x] VendorID=6 fully EXCLUDED from Silver (clean_v2.py; status changed to test_account per vendor_registry.json v1.1)\n\n"
        "## Notes\n"
        "- The VendorID=6 exclusion SUPERSEDES the earlier Slack 'keep as audit_only' guidance "
        "(SLACK-A20-VENDOR6-KEEP), per the operations notice on Feishu #ops-bridge.\n"
        "- Old rule (audit_only, exclude_from_silver=false in vendor_registry.json schema_version 1.0) is "
        "no longer in effect; updated vendor_registry.json schema_version 1.1 sets exclude_from_silver=true.\n"))

    # q16 signoff over q14 bytes (C)
    digest = hashlib.sha256((out / "q14_payment_zone_pivot.json").read_bytes()).hexdigest()
    _w(out / "q16_signoff.txt", f"VERIFIED:{digest}\n")


def _qentry(name, null_count, total, invalid_count, denom, notes):
    return {
        "field_name": name,
        "null_count": int(null_count),
        "null_pct": f4(100.0 * null_count / total),
        "invalid_count": int(invalid_count),
        "invalid_pct": f4(100.0 * invalid_count / max(denom, 1)),
        "notes": notes,
    }


def read_csv_zones(p: Path) -> dict:
    with p.open(encoding="utf-8") as fh:
        return {r["LocationID"]: r for r in csv.DictReader(fh)}


def _w(p: Path, t: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8")


def _wj(p: Path, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2), encoding="utf-8")


# --------------------------------------------------------------------------- #
# 运行 check
# --------------------------------------------------------------------------- #
EVAL_CMDS = {
    "q1": ["check_q1.py", ("pref", "P1", "output/q1_zone_stats.json")],
    "q2": ["check_q2.py", ("pref", "P1", "output/q2_schema_diff.json")],
    "q3": ["check_q3.py", ("pref", "P2,P5", "pipeline/bronze/ingest.py")],
    "q4": ["check_q4.py", ("pref", "P1,P4", "output/q4_quality_report.json")],
    "q5": ["check_q5.py"], "q6": ["check_q6.py"],
    "q7": ["check_q7.py", ("pref", "P1,P4", "output/q7_quality_report_v2.json")],
    "q8": ["check_q8.py", ("pref", "P2,P5", "pipeline/silver/clean.py")],
    "q9": ["check_q9.py", ("pref", "P2,P5", "pipeline/silver/enrich.py")],
    "q10": ["check_q10.py", ("pref", "P1", "output/q10_daily_summary.json")],
    "q11": ["check_q11.py", ("pref", "P2,P5", "pipeline/silver/clean_v2.py")],
    "q12": ["check_q12.py", ("pref", "P1,P4", "output/q12_vendor_filter_report.json")],
    "q13": ["check_q13.py", ("pref", "P1", "output/q13_archive_compat.json")],
    "q14": ["check_q14.py", ("pref", "P1", "output/q14_payment_zone_pivot.json")],
    "q15": ["check_q15.py"], "q16": ["check_q16.py"],
}


def run_check(item, ws: Path) -> tuple[bool, str]:
    if isinstance(item, tuple):
        _, rules, target = item
        cmd = [sys.executable, str(SCRIPTS / "check_preferences.py"), str(ws), "--rules", rules, "--target", target]
    else:
        cmd = [sys.executable, str(SCRIPTS / item), str(ws)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    return r.returncode == 0, (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout or r.stderr) else ""


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
                print(f"  [PASS] {q} ({tag}): {last}")
            else:
                n_fail += 1
                print(f"  [FAIL] {q} ({tag}): {last}")
    print(f"gold: {n_pass} checks PASSED, {n_fail} FAILED")

    # 反例抽样：错误产物必须 FAIL
    print("\n=== NEGATIVE PROBES: each must FAIL ===")
    probes = 0; caught = 0

    # q1: borough_counts wrong (EWR=5 instead of 1)
    good_q1 = json.loads((ws / "output" / "q1_zone_stats.json").read_text())
    bad_q1 = dict(good_q1)
    bad_q1["borough_counts"] = dict(good_q1["borough_counts"]); bad_q1["borough_counts"]["EWR"] = 5
    _wj(ws / "output" / "q1_zone_stats.json", bad_q1)
    ok, _ = run_check("check_q1.py", ws); probes += 1; caught += (not ok)
    print(f"  q1 wrong EWR count -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    _wj(ws / "output" / "q1_zone_stats.json", good_q1)  # restore

    # q2 extra field in added_fields (pulls from legacy archive)
    _wj(ws / "output" / "q2_schema_diff.json", {"schema_version": "1.0", "added_fields": ["airport_fee", "cbd_congestion_fee", "pickup_longitude"], "v1_missing_count": 3})
    ok, _ = run_check("check_q2.py", ws); probes += 1; caught += (not ok)
    print(f"  q2 extra legacy field in added_fields -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # restore q2 correct
    _wj(ws / "output" / "q2_schema_diff.json", {"schema_version": "1.0", "added_fields": ["airport_fee", "cbd_congestion_fee"], "v1_missing_count": 2})

    # q4 BOT decoy 500000 for passenger_count
    nc = json.loads((ws / "data" / "reference" / "dataset_profile.json").read_text())["fields"]["passenger_count"]["null_count"]
    total_r = json.loads((ws / "data" / "reference" / "dataset_profile.json").read_text())["total_rows"]
    _wj(ws / "output" / "q4_quality_report.json", {"schema_version": "1.0", "fields": [_qentry("passenger_count", 500000, total_r, 0, total_r, "BOT value")]})
    ok, _ = run_check("check_q4.py", ws); probes += 1; caught += (not ok)
    print(f"  q4 BOT-decoy 500000 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # q4 missing RatecodeID entry
    _wj(ws / "output" / "q4_quality_report.json", {"schema_version": "1.0", "fields": [_qentry("passenger_count", nc, total_r, 0, total_r, "OK")]})
    ok, _ = run_check("check_q4.py", ws); probes += 1; caught += (not ok)
    print(f"  q4 missing RatecodeID entry -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # restore q4 correct
    nc_rc = json.loads((ws / "data" / "reference" / "dataset_profile.json").read_text())["fields"]["RatecodeID"]["null_count"]
    _wj(ws / "output" / "q4_quality_report.json", {"schema_version": "1.0", "fields": [
        _qentry("passenger_count", nc, total_r, 0, total_r, "Authoritative"),
        _qentry("RatecodeID", nc_rc, total_r, 0, total_r, "Authoritative"),
    ]})

    # q5 wrong min -200
    _wj(ws / "output" / "q5_negative_fares.json", {"filtered_count": 5, "min_observed_fare": -200.0})
    ok, _ = run_check("check_q5.py", ws); probes += 1; caught += (not ok)
    print(f"  q5 wrong min -200 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # q7 cross-round drift — timestamp_anomaly_count doesn't match q6
    good_q7 = json.loads((ws / "output" / "q7_quality_report_v2.json").read_text())
    bad_q7 = dict(good_q7); bad_q7["timestamp_anomaly_count"] = 999
    _wj(ws / "output" / "q7_quality_report_v2.json", bad_q7)
    ok, _ = run_check("check_q7.py", ws); probes += 1; caught += (not ok)
    print(f"  q7 timestamp_anomaly_count drift from q6 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # q7 missing total_zone_count
    bad_q7b = dict(good_q7); bad_q7b.pop("total_zone_count", None)
    _wj(ws / "output" / "q7_quality_report_v2.json", bad_q7b)
    ok, _ = run_check("check_q7.py", ws); probes += 1; caught += (not ok)
    print(f"  q7 missing total_zone_count -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    _wj(ws / "output" / "q7_quality_report_v2.json", good_q7)  # restore

    # q10 wrong trip_count (use 300 for Jan instead of 256)
    good_q10 = json.loads((ws / "output" / "q10_daily_summary.json").read_text())
    bad_q10 = dict(good_q10)
    bad_q10["2023-01"] = dict(good_q10["2023-01"]); bad_q10["2023-01"]["trip_count"] = 300
    _wj(ws / "output" / "q10_daily_summary.json", bad_q10)
    ok, _ = run_check("check_q10.py", ws); probes += 1; caught += (not ok)
    print(f"  q10 wrong trip_count Jan=300 (should be 256) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    _wj(ws / "output" / "q10_daily_summary.json", good_q10)  # restore

    # q11 audit_only retain (no supersede)
    _w(ws / "pipeline" / "silver" / "clean_v2.py", PY_HEADER + 'def clean_v2(rows):\n    return [r for r in rows]  # audit_only: keep VendorID=6\n')
    ok, _ = run_check("check_q11.py", ws); probes += 1; caught += (not ok)
    print(f"  q11 audit_only retain -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # q12 wrong total_before (using 3100 instead of 3772)
    _wj(ws / "output" / "q12_vendor_filter_report.json", {"schema_version": "1.0", "total_before": 3100, "rows_removed_vendor6": 155, "total_after": 2945})
    ok, _ = run_check("check_q12.py", ws); probes += 1; caught += (not ok)
    print(f"  q12 wrong total_before=3100 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # restore q12
    import csv as csv_mod
    vendor6_csv_rows = []
    with open(str(ws / "data" / "raw" / "yellow_202306_vendor6_sample.csv")) as fh:
        vendor6_csv_rows = list(csv_mod.DictReader(fh))
    main_rows = read_csv(ws / "data" / "raw" / "yellow_tripdata_2023_sample.csv")
    combined_rows = main_rows + vendor6_csv_rows
    rr_r = sum(1 for r in combined_rows if r.get("VendorID") == "6")
    tb_r = len(combined_rows)
    _wj(ws / "output" / "q12_vendor_filter_report.json", {"schema_version": "1.0", "total_before": tb_r, "rows_removed_vendor6": rr_r, "total_after": tb_r - rr_r})

    # q13 wrong order in deprecated_fields
    _wj(ws / "output" / "q13_archive_compat.json", {"schema_version": "1.0", "compatible": False,
        "deprecated_fields": ["pickup_longitude", "dropoff_longitude", "pickup_latitude", "dropoff_latitude",
                              "pickup_datetime", "dropoff_datetime"]})
    ok, _ = run_check("check_q13.py", ws); probes += 1; caught += (not ok)
    print(f"  q13 wrong deprecated_fields order -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # restore q13
    _wj(ws / "output" / "q13_archive_compat.json", {"schema_version": "1.0", "compatible": False,
        "deprecated_fields": ["pickup_datetime", "dropoff_datetime", "pickup_longitude", "pickup_latitude",
                              "dropoff_longitude", "dropoff_latitude"]})

    # q14 wrong grand_total
    good_q14 = json.loads((ws / "output" / "q14_payment_zone_pivot.json").read_text())
    bad_q14 = dict(good_q14); bad_q14["grand_total"] = 9999
    _wj(ws / "output" / "q14_payment_zone_pivot.json", bad_q14)
    ok, _ = run_check("check_q14.py", ws); probes += 1; caught += (not ok)
    print(f"  q14 wrong grand_total=9999 -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    _wj(ws / "output" / "q14_payment_zone_pivot.json", good_q14)  # restore

    # q15 missing SLACK reference and audit_only
    _w(ws / "output" / "q15_migration_checklist.md", (
        "# Migration Checklist\n\n## Completed\n"
        + "".join(f"- [x] Step {i}\n" for i in range(1, 11))
        + "\n## Notes\n- VendorID=6 exclusion SUPERSEDES the earlier guidance.\n"))
    ok, _ = run_check("check_q15.py", ws); probes += 1; caught += (not ok)
    print(f"  q15 missing SLACK-A20 reference and audit_only -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # q16 placeholder hash
    _w(ws / "output" / "q16_signoff.txt", "VERIFIED:" + "0" * 64 + "\n")
    ok, _ = run_check("check_q16.py", ws); probes += 1; caught += (not ok)
    print(f"  q16 placeholder hash -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    print(f"negatives: {caught}/{probes} correctly caught")

    if n_fail == 0 and caught == probes:
        print("\nAUDIT OK: gold solution all-PASS and all negative probes caught.")
    else:
        print("\nAUDIT PROBLEM: see failures above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
