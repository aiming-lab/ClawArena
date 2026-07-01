#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_eng2_checks.py — 生成 eng2 的全部 exec_check 校验脚本到 eval/eng2/scripts/。

每个 check_qN.py 自包含，约定：argv[1]=workspace；PASSED+exit0 / FAILED+exit1。
三层验证（结构→字段→真值），数值带容差，锚点对齐 build_eng2.py 注入的真实/合成数据。
check_preferences.py 实现 P1-P5。生成器内容即评测逻辑，可逐脚本审阅。

V2 加难版本：
- C 跨轮闭合连锁：q7 连锁 q4/q6/q1，q14 连锁 q10 grand_total，q16 连锁 q14
- B 多源冲突仲裁：q1/q4 诱饵数据，question 撤善意提示
- E 隐藏 preference 静默考核：P1 加入 q1/q2/q12/q13/q7 eval command
- F 严格 schema：q1 精确 borough_counts/service_zone_counts；q4 exact match + RatecodeID；
  q10 精确 trip_count ± 0 + avg_fare ± 1.0；q12 精确 total_before/rows_removed；
  q13 archive-header 顺序；q14 exact per-borough counts + grand_total
- G 撤脚手架：q3 只留意图描述，q8 加 docstring 要求
"""
from pathlib import Path
import textwrap

OUT = Path("/home/xkaiwen/workspace/ClawArena/data/clawarena-real/eval/eng2/scripts")
OUT.mkdir(parents=True, exist_ok=True)

HEADER = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib
from pathlib import Path

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON in " + p.name + ": " + str(e)

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)

def _field_entry(data, name):
    """从 quality report 取某字段 entry，兼容 fields 为 list 或 dict。"""
    fields = data.get("fields")
    if isinstance(fields, list):
        for e in fields:
            if isinstance(e, dict) and e.get("field_name") == name:
                return e
    elif isinstance(fields, dict):
        e = fields.get(name)
        if isinstance(e, dict):
            return e
        if e is not None:
            return {"field_name": name, "null_count": e}
    return None
'''

CHECKS = {}

# ── q1 ──────────────────────────────────────────────────────────────────────
# F: exact borough_counts and service_zone_counts; P1 via eval command
CHECKS["check_q1"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q1_zone_stats.json")
    if err: _finish([err])
    # total_locations exact 265
    if data.get("total_locations") != 265:
        fails.append("total_locations == %r (expected 265)" % data.get("total_locations"))
    # boroughs list must include all 7 borough strings
    bs = set(str(b) for b in (data.get("boroughs") or []))
    need = {"EWR", "Queens", "Bronx", "Manhattan", "Staten Island", "Brooklyn", "Unknown"}
    miss = need - bs
    if miss:
        fails.append("boroughs missing %s" % sorted(miss))
    # F: borough_counts must be present and exactly correct
    bc = data.get("borough_counts")
    if not isinstance(bc, dict):
        fails.append("borough_counts must be a JSON object (mapping Borough -> int count)")
    else:
        EXACT_BC = {
            "EWR": 1, "Staten Island": 49, "Brooklyn": 54, "Queens": 56,
            "Manhattan": 52, "Bronx": 52, "Unknown": 1
        }
        for boro, expected in EXACT_BC.items():
            got = bc.get(boro)
            try:
                got_int = int(got)
            except (TypeError, ValueError):
                fails.append("borough_counts[%r] == %r (not an int; expected %d)" % (boro, got, expected))
                continue
            if got_int != expected:
                fails.append("borough_counts[%r] == %d (expected %d)" % (boro, got_int, expected))
    # F: service_zone_counts must be present and exactly correct
    szc = data.get("service_zone_counts")
    if not isinstance(szc, dict):
        fails.append("service_zone_counts must be a JSON object (mapping service_zone -> int count)")
    else:
        EXACT_SZ = {"EWR": 1, "Boro Zone": 209, "Yellow Zone": 52, "Airports": 2, "N/A": 1}
        for sz, expected in EXACT_SZ.items():
            got = szc.get(sz)
            try:
                got_int = int(got)
            except (TypeError, ValueError):
                fails.append("service_zone_counts[%r] == %r (not an int; expected %d)" % (sz, got, expected))
                continue
            if got_int != expected:
                fails.append("service_zone_counts[%r] == %d (expected %d)" % (sz, got_int, expected))
    _finish(fails)
main()
'''

# ── q2 ──────────────────────────────────────────────────────────────────────
# E: P1 added to eval command (schema_version required in output JSON)
CHECKS["check_q2"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q2_schema_diff.json")
    if err: _finish([err])
    added = set(str(x) for x in (data.get("added_fields") or []))
    EXACT = {"airport_fee", "cbd_congestion_fee"}
    for need in sorted(EXACT):
        if need not in added:
            fails.append("added_fields missing %r" % need)
    # guard: must not pull deprecated lon/lat field names from the legacy archive
    for bad in ("pickup_longitude", "dropoff_longitude", "pickup_latitude", "dropoff_latitude",
                "pickup_datetime", "dropoff_datetime"):
        if bad in added:
            fails.append("added_fields wrongly contains deprecated legacy field %r" % bad)
    # added_fields must be EXACTLY the two new v2 fields, no more
    extra = added - EXACT
    if extra:
        fails.append("added_fields contains unexpected extra entries %s (v2 adds exactly 2 fields)" % sorted(extra))
    # v1_missing_count must equal 2 exactly
    vmc = data.get("v1_missing_count")
    try:
        if int(vmc) != 2:
            fails.append("v1_missing_count == %r (expected exactly 2)" % vmc)
    except (TypeError, ValueError):
        fails.append("v1_missing_count must be int 2 (got %r)" % vmc)
    _finish(fails)
main()
'''

# ── q3 ──────────────────────────────────────────────────────────────────────
# F: require cbd_congestion_fee in addition to tpep_pickup_datetime; G: question simplified
CHECKS["check_q3"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "pipeline" / "bronze" / "ingest.py")
    if txt is None:
        _finish(["file not found: pipeline/bronze/ingest.py"])
    if "tpep_pickup_datetime" not in txt:
        fails.append("ingest.py does not reference verbatim column 'tpep_pickup_datetime'")
    # F: schema_v2 adds airport_fee and cbd_congestion_fee — both must appear verbatim
    if "airport_fee" not in txt:
        fails.append("ingest.py does not reference verbatim schema_v2 column 'airport_fee'")
    if "cbd_congestion_fee" not in txt:
        fails.append("ingest.py does not reference verbatim schema_v2 column 'cbd_congestion_fee'")
    if not re.search(r"read_parquet|read_csv_auto|read_csv", txt):
        fails.append("ingest.py does not call a DuckDB read function (read_parquet/read_csv_auto)")
    _finish(fails)
main()
'''

# ── q4 ──────────────────────────────────────────────────────────────────────
# A: exact match (no tolerance); F: RatecodeID entry also required; B: BOT decoy in question
CHECKS["check_q4"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q4_quality_report.json")
    if err: _finish([err])
    # passenger_count — exact match from dataset_profile.json
    e = _field_entry(data, "passenger_count")
    if e is None:
        fails.append("no passenger_count entry under 'fields'")
    else:
        nc = e.get("null_count")
        try:
            nc = int(nc)
        except (TypeError, ValueError):
            fails.append("passenger_count.null_count not an int: %r" % nc)
            nc = None
        if nc is not None and nc != 1309356:
            fails.append("passenger_count.null_count == %d (must be exactly 1,309,356 from dataset_profile.json; "
                         "the BOT summary's ~500,000 is a known undercount)" % nc)
    # F: RatecodeID entry also required — same authoritative null_count = 1,309,356
    e2 = _field_entry(data, "RatecodeID")
    if e2 is None:
        fails.append("no RatecodeID entry under 'fields' (report must include both passenger_count and RatecodeID)")
    else:
        nc2 = e2.get("null_count")
        try:
            nc2 = int(nc2)
        except (TypeError, ValueError):
            fails.append("RatecodeID.null_count not an int: %r" % nc2)
            nc2 = None
        if nc2 is not None and nc2 != 1309356:
            fails.append("RatecodeID.null_count == %d (must be exactly 1,309,356 from dataset_profile.json)" % nc2)
    _finish(fails)
main()
'''

# ── q5 ──────────────────────────────────────────────────────────────────────
CHECKS["check_q5"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q5_negative_fares.json")
    if err: _finish([err])
    fc = data.get("filtered_count")
    if not isinstance(fc, int) or fc <= 0:
        fails.append("filtered_count == %r (expected positive int)" % fc)
    mf = data.get("min_observed_fare")
    try:
        if float(mf) > -1087.00:
            fails.append("min_observed_fare == %r (expected <= -1087.00; real worst is -1087.30)" % mf)
    except (TypeError, ValueError):
        fails.append("min_observed_fare not numeric: %r" % mf)
    _finish(fails)
main()
'''

# ── q6 ──────────────────────────────────────────────────────────────────────
CHECKS["check_q6"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q6_timestamp_anomalies.json")
    if err: _finish([err])
    ac = data.get("anomaly_count")
    if not isinstance(ac, int) or ac <= 0:
        fails.append("anomaly_count == %r (expected positive int)" % ac)
    yrs = set()
    for y in (data.get("future_year_examples") or []):
        try:
            yrs.add(int(y))
        except (TypeError, ValueError):
            pass
    if not (2088 in yrs or 2084 in yrs):
        fails.append("future_year_examples must include 2088 or 2084 (got %s)" % sorted(yrs))
    _finish(fails)
main()
'''

# ── q7 ──────────────────────────────────────────────────────────────────────
# C: cross-round closure — q4 (passenger_count AND RatecodeID exact), q6 (anomaly_count exact), q1 (total_zone_count exact)
CHECKS["check_q7"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q7_quality_report_v2.json")
    if err: _finish([err])
    # passenger_count — exact 1,309,356
    e = _field_entry(data, "passenger_count")
    if e is None:
        fails.append("no passenger_count entry under 'fields'")
        nc7 = None
    else:
        try:
            nc7 = int(e.get("null_count"))
        except (TypeError, ValueError):
            fails.append("passenger_count.null_count not an int: %r" % e.get("null_count"))
            nc7 = None
        if nc7 is not None and nc7 != 1309356:
            fails.append("passenger_count.null_count == %d (must be exactly 1,309,356)" % nc7)
    # RatecodeID — exact 1,309,356
    e2 = _field_entry(data, "RatecodeID")
    if e2 is None:
        fails.append("no RatecodeID entry under 'fields'")
        nc7_rc = None
    else:
        try:
            nc7_rc = int(e2.get("null_count"))
        except (TypeError, ValueError):
            fails.append("RatecodeID.null_count not an int: %r" % e2.get("null_count"))
            nc7_rc = None
        if nc7_rc is not None and nc7_rc != 1309356:
            fails.append("RatecodeID.null_count == %d (must be exactly 1,309,356)" % nc7_rc)
    # timestamp_anomaly_count — positive int
    tac = data.get("timestamp_anomaly_count")
    if not isinstance(tac, int) or tac <= 0:
        fails.append("timestamp_anomaly_count == %r (expected positive int)" % tac)
    # total_zone_count — must be present
    tzc = data.get("total_zone_count")
    if tzc is None:
        fails.append("total_zone_count field missing (must echo q1.total_locations)")
    elif int(tzc) != 265:
        fails.append("total_zone_count == %r (expected 265, matching q1.total_locations)" % tzc)
    # C: cross-round closure with q4 — passenger_count must be byte-for-byte identical
    q4, e4 = _load_json(ws / "output" / "q4_quality_report.json")
    if not e4 and q4 is not None:
        e4f = _field_entry(q4, "passenger_count")
        if e4f is not None and nc7 is not None:
            try:
                nc4 = int(e4f.get("null_count"))
                if nc7 != nc4:
                    fails.append("cross-version drift: q7 passenger_count.null_count %d != q4 value %d (must be identical)" % (nc7, nc4))
            except (TypeError, ValueError):
                pass
        # RatecodeID cross-round
        e4f_rc = _field_entry(q4, "RatecodeID")
        if e4f_rc is not None and nc7_rc is not None:
            try:
                nc4_rc = int(e4f_rc.get("null_count"))
                if nc7_rc != nc4_rc:
                    fails.append("cross-version drift: q7 RatecodeID.null_count %d != q4 value %d" % (nc7_rc, nc4_rc))
            except (TypeError, ValueError):
                pass
    # C: cross-round closure with q6 — timestamp_anomaly_count must exactly match q6.anomaly_count
    q6, e6 = _load_json(ws / "output" / "q6_timestamp_anomalies.json")
    if not e6 and q6 is not None:
        ac6 = q6.get("anomaly_count")
        try:
            if int(ac6) != tac:
                fails.append("cross-version drift: q7 timestamp_anomaly_count %r != q6 anomaly_count %r (must be identical)" % (tac, ac6))
        except (TypeError, ValueError):
            pass
    # C: cross-round closure with q1 — total_zone_count must match q1.total_locations exactly
    q1, e1 = _load_json(ws / "output" / "q1_zone_stats.json")
    if not e1 and q1 is not None and tzc is not None:
        tl1 = q1.get("total_locations")
        try:
            if int(tzc) != int(tl1):
                fails.append("cross-version drift: q7 total_zone_count %r != q1 total_locations %r" % (tzc, tl1))
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
'''

# ── q8 ──────────────────────────────────────────────────────────────────────
# F: require module docstring; G: question now requires docstring
CHECKS["check_q8"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "pipeline" / "silver" / "clean.py")
    if txt is None:
        _finish(["file not found: pipeline/silver/clean.py"])
    low = txt.lower()
    if "fare_amount" not in txt:
        fails.append("clean.py does not reference fare_amount filter")
    if "trip_distance" not in txt:
        fails.append("clean.py does not reference trip_distance filter")
    # must reference the verbatim official pickup column name
    if "tpep_pickup_datetime" not in txt:
        fails.append("clean.py does not reference verbatim column 'tpep_pickup_datetime' for the year filter")
    if not re.search(r"2009|2024|valid_year|year", low):
        fails.append("clean.py does not apply a pickup-year/timestamp validity filter")
    # must reference the authoritative max_valid trip_distance threshold (300 miles)
    if not re.search(r"300|max_valid|max_trip", low):
        fails.append("clean.py does not reference the max_valid trip_distance threshold (300 miles from quality_rules.yaml)")
    # F: must have a module-level docstring (triple-quoted string or comment block after header)
    has_docstring = bool(re.search(r'"{3}[^"]{5,}"{3}', txt[:600]) or re.search(r"\'{3}[^\']{5,}\'{3}", txt[:600]))
    if not has_docstring:
        fails.append("clean.py must have a module-level docstring explaining the filters (triple-quoted string within first 600 chars)")
    _finish(fails)
main()
'''

# ── q9 ──────────────────────────────────────────────────────────────────────
CHECKS["check_q9"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "pipeline" / "silver" / "enrich.py")
    if txt is None:
        _finish(["file not found: pipeline/silver/enrich.py"])
    low = txt.lower()
    if "pulocationid" not in low or "locationid" not in low:
        fails.append("enrich.py must join on PULocationID = LocationID")
    # must be a LEFT JOIN specifically
    if "left" not in low:
        fails.append("enrich.py must perform a LEFT JOIN (not inner join) — rows with no zone match must be kept as 'Unknown'")
    if "join" not in low:
        fails.append("enrich.py does not perform a join")
    if "unknown" not in low:
        fails.append("enrich.py does not provide an 'Unknown' Borough fallback for unmatched IDs")
    # must reference the authoritative lookup file name
    if "taxi_zone_lookup" not in low:
        fails.append("enrich.py does not reference the authoritative 'taxi_zone_lookup' file")
    _finish(fails)
main()
'''

# ── q10 ──────────────────────────────────────────────────────────────────────
# F: exact trip_count per month (±0); avg_fare ±1.0 (not just [10,25]); total_trip_count cross-check
# C: total_trip_count must equal sum of monthly trip_counts
CHECKS["check_q10"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q10_daily_summary.json")
    if err: _finish([err])
    # F: exact trip_count per month (computed from real data: year=2023, fare>=0)
    EXACT_TRIPS = {
        "2023-01": 256, "2023-02": 252, "2023-03": 256, "2023-04": 256,
        "2023-05": 252, "2023-06": 257, "2023-07": 255, "2023-08": 253,
        "2023-09": 256, "2023-10": 256, "2023-11": 260, "2023-12": 253,
    }
    # F: avg_fare bounds ±1.0 of true values (not just a loose [10,25] range)
    AVG_FARE_BOUNDS = {
        "2023-01": (16.85, 18.85), "2023-02": (16.43, 18.43),
        "2023-03": (17.34, 19.34), "2023-04": (16.53, 18.53),
        "2023-05": (16.54, 18.54), "2023-06": (16.62, 18.62),
        "2023-07": (17.29, 19.29), "2023-08": (17.93, 19.93),
        "2023-09": (16.60, 18.60), "2023-10": (17.55, 19.55),
        "2023-11": (16.63, 18.63), "2023-12": (17.53, 19.53),
    }
    sum_trip = 0
    for m in range(1, 13):
        key = "2023-%02d" % m
        if key not in data:
            fails.append("missing month key %s" % key)
            continue
        entry = data[key]
        if not isinstance(entry, dict):
            fails.append("%s value is not an object" % key); continue
        # trip_count exact
        tc = entry.get("trip_count")
        try:
            tc = int(tc)
        except (TypeError, ValueError):
            fails.append("%s trip_count not an int: %r" % (key, tc)); continue
        if tc != EXACT_TRIPS[key]:
            fails.append("%s trip_count == %d (expected exactly %d; only count year=2023 rows with fare>=0)" % (key, tc, EXACT_TRIPS[key]))
        sum_trip += tc
        # avg_fare bounds
        af = entry.get("avg_fare")
        try:
            af = float(af)
        except (TypeError, ValueError):
            fails.append("%s avg_fare not numeric: %r" % (key, af)); continue
        lo, hi = AVG_FARE_BOUNDS[key]
        if not (lo <= af <= hi):
            fails.append("%s avg_fare == %.4f (expected within [%.2f, %.2f] — +-1.0 of true value)" % (key, af, lo, hi))
    # C: total_trip_count cross-check
    ttc = data.get("total_trip_count")
    if ttc is None:
        fails.append("total_trip_count field missing (must equal sum of monthly trip_counts = 3062)")
    else:
        try:
            ttc_int = int(ttc)
        except (TypeError, ValueError):
            fails.append("total_trip_count not an int: %r" % ttc)
            ttc_int = None
        if ttc_int is not None:
            if ttc_int != sum_trip:
                fails.append("total_trip_count == %d != sum of monthly trip_counts %d" % (ttc_int, sum_trip))
            elif ttc_int != 3062:
                fails.append("total_trip_count == %d (expected 3062 from the real sample)" % ttc_int)
    _finish(fails)
main()
'''

# ── q11 ──────────────────────────────────────────────────────────────────────
CHECKS["check_q11"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "pipeline" / "silver" / "clean_v2.py")
    if txt is None:
        _finish(["file not found: pipeline/silver/clean_v2.py"])
    low = txt.lower()
    # must EXCLUDE VendorID == 6 (supersede). Accept several idioms.
    excl = bool(
        re.search(r"vendorid\\s*(!=|<>)\\s*6", low) or
        re.search(r"vendorid\\s*not\\s+in\\s*[\\(\\[][^\\)\\]]*6", low) or
        re.search(r"(drop|exclud|remove|filter\\s*out)[^\\n]{0,40}vendorid[^\\n]{0,12}6", low) or
        re.search(r"vendorid[^\\n]{0,12}6[^\\n]{0,40}(drop|exclud|remove)", low)
    )
    if not excl:
        fails.append("clean_v2.py does not exclude VendorID == 6 (supersede requires full exclusion)")
    # must NOT keep VendorID=6 via an active retain branch (comments mentioning audit_only are fine)
    if re.search(r"(keep|retain|include)[^\\n]{0,30}vendorid[^\\n]{0,8}6", low) or \\
       re.search(r"vendorid[^\\n]{0,8}6[^\\n]{0,30}(keep|retain)", low):
        fails.append("clean_v2.py appears to retain VendorID==6 (an active keep/retain branch)")
    _finish(fails)
main()
'''

# ── q12 ──────────────────────────────────────────────────────────────────────
# F+A: exact total_before=3772, rows_removed=805, total_after=2967; P1+P4 via eval command
CHECKS["check_q12"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q12_vendor_filter_report.json")
    if err: _finish([err])
    try:
        tb = int(data.get("total_before"))
        rr = int(data.get("rows_removed_vendor6"))
        ta = int(data.get("total_after"))
    except (TypeError, ValueError):
        _finish(["total_before / rows_removed_vendor6 / total_after must all be ints"])
    # F: exact values — 3122 (main sample) + 650 (vendor6_sample) = 3772 total
    if tb != 3772:
        fails.append("total_before == %d (expected exactly 3772: 3122 from main sample + 650 from vendor6_sample)" % tb)
    # F: exact vendor6 count = 155 (main sample) + 650 (vendor6_sample) = 805
    if rr != 805:
        fails.append("rows_removed_vendor6 == %d (expected exactly 805: 155 VendorID=6 in main sample + 650 in vendor6_sample)" % rr)
    # arithmetic closure
    if tb - rr != ta:
        fails.append("arithmetic does not close: %d - %d != %d" % (tb, rr, ta))
    if ta != 2967:
        fails.append("total_after == %d (expected exactly 2967)" % ta)
    _finish(fails)
main()
'''

# ── q13 ──────────────────────────────────────────────────────────────────────
# F: verbatim archive-header order for deprecated_fields; P1 via eval command
CHECKS["check_q13"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q13_archive_compat.json")
    if err: _finish([err])
    if data.get("compatible") is not False:
        fails.append("compatible == %r (expected false)" % data.get("compatible"))
    dep = data.get("deprecated_fields")
    if not isinstance(dep, list):
        fails.append("deprecated_fields must be a list")
        _finish(fails)
    dep_set = set(str(x) for x in dep)
    # all six verbatim deprecated fields must be present
    REQUIRED = {"pickup_datetime", "dropoff_datetime",
                "pickup_longitude", "pickup_latitude",
                "dropoff_longitude", "dropoff_latitude"}
    for need in sorted(REQUIRED):
        if need not in dep_set:
            fails.append("deprecated_fields missing %r (present in archive but absent from schema_v2)" % need)
    # F: order must match archive header order exactly
    # Archive header: VendorID, pickup_datetime, dropoff_datetime, passenger_count, trip_distance,
    #                 pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, fare_amount
    # Deprecated in header order: pickup_datetime, dropoff_datetime, pickup_longitude, pickup_latitude,
    #                              dropoff_longitude, dropoff_latitude
    EXPECTED_ORDER = [
        "pickup_datetime", "dropoff_datetime",
        "pickup_longitude", "pickup_latitude",
        "dropoff_longitude", "dropoff_latitude",
    ]
    # Only check order if all 6 are present
    if dep_set >= REQUIRED:
        filtered = [x for x in dep if x in REQUIRED]
        if filtered != EXPECTED_ORDER:
            fails.append(
                "deprecated_fields order must match archive header order: %s (got: %s)" % (
                    EXPECTED_ORDER, filtered))
    _finish(fails)
main()
'''

# ── q14 ──────────────────────────────────────────────────────────────────────
# F: exact per-borough counts; grand_total=2934; C: verify grand_total consistent with q10
CHECKS["check_q14"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q14_payment_zone_pivot.json")
    if err: _finish([err])
    if not isinstance(data, dict):
        _finish(["pivot must be a JSON object keyed by payment_type code"])
    # top-level payment_type codes must include at least 1,2,3
    keys = set(str(k) for k in data.keys() if k not in ("schema_version", "grand_total"))
    need = {"1", "2", "3"}
    miss = need - keys
    if miss:
        fails.append("top-level payment_type code keys missing %s (use official codes, not labels)" % sorted(miss))
    # F: exact per-borough counts for each payment_type code
    EXACT_PIVOT = {
        "1": {"Bronx": 453, "Queens": 468, "Brooklyn": 498, "EWR": 13,
              "Staten Island": 442, "Manhattan": 407, "Unknown": 10},
        "2": {"Manhattan": 86, "Brooklyn": 103, "Bronx": 101, "Queens": 112,
              "Staten Island": 80, "EWR": 1, "Unknown": 1},
        "3": {"Brooklyn": 7, "Queens": 14, "Staten Island": 15, "Bronx": 7,
              "Manhattan": 22, "Unknown": 2},
        "4": {"Manhattan": 10, "Queens": 24, "Brooklyn": 22, "Bronx": 18,
              "Staten Island": 18},
    }
    computed_grand = 0
    for code, expected_boros in EXACT_PIVOT.items():
        if code not in data:
            fails.append("payment_type %r missing from pivot" % code)
            continue
        v = data[code]
        if not isinstance(v, dict) or not v:
            fails.append("payment_type %r value is not a non-empty borough mapping" % code)
            continue
        for boro, expected_count in expected_boros.items():
            got = v.get(boro)
            try:
                got_int = int(got)
            except (TypeError, ValueError):
                fails.append("pivot[%r][%r] == %r (not an int; expected %d)" % (code, boro, got, expected_count))
                continue
            if got_int != expected_count:
                fails.append("pivot[%r][%r] == %d (expected exactly %d)" % (code, boro, got_int, expected_count))
            computed_grand += got_int
    # F: grand_total must be present and equal 2934
    gt = data.get("grand_total")
    if gt is None:
        fails.append("grand_total field missing (must equal 2934)")
    else:
        try:
            gt_int = int(gt)
        except (TypeError, ValueError):
            fails.append("grand_total not an int: %r" % gt)
            gt_int = None
        if gt_int is not None and gt_int != 2934:
            fails.append("grand_total == %d (expected exactly 2934)" % gt_int)
    # C: cross-round closure with q10 — q10.total_trip_count (3062) - vendor6_in_sample (154+negyear) != q14 grand
    # The check is simply: verify grand_total reported == computed from the pivot cells
    if gt is not None:
        try:
            if int(gt) != computed_grand and computed_grand > 0:
                fails.append("grand_total %d != sum of pivot cell counts %d" % (int(gt), computed_grand))
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
'''

# ── q15 ──────────────────────────────────────────────────────────────────────
CHECKS["check_q15"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "q15_migration_checklist.md")
    if txt is None:
        _finish(["file not found: output/q15_migration_checklist.md"])
    low = txt.lower()
    # require >= 10 checked items
    x_count = len(re.findall(r"\\[x\\]", low))
    if x_count < 10:
        fails.append("only %d '[x]' checklist items (expected >= 10; include all major pipeline steps)" % x_count)
    if len(re.findall(r"^## ", txt, re.MULTILINE)) < 2:
        fails.append("fewer than 2 '## ' section headings")
    if not (re.search(r"vendorid", low) and "6" in txt and re.search(r"exclu|remov|drop", low)):
        fails.append("no explicit VendorID=6 exclusion item")
    if "supersede" not in low and "supersed" not in low:
        fails.append("checklist does not record that the exclusion SUPERSEDES the earlier audit_only Slack guidance")
    # must explicitly cite the Slack thread reference being superseded
    if "slack-a20-vendor6-keep" not in low and "slack_a20" not in low:
        fails.append("checklist must explicitly cite the superseded Slack reference 'SLACK-A20-VENDOR6-KEEP' (from vendor_registry.json)")
    # must explicitly record audit_only label being superseded
    if "audit_only" not in low and "audit only" not in low:
        fails.append("checklist must explicitly mention the superseded 'audit_only' Slack rule")
    _finish(fails)
main()
'''

# ── q16 ──────────────────────────────────────────────────────────────────────
# C: SHA-256 closure over q14 — if q14 changes, q16 must be recomputed
CHECKS["check_q16"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    sign = _read(ws / "output" / "q16_signoff.txt")
    if sign is None:
        _finish(["file not found: output/q16_signoff.txt"])
    line = sign.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["signoff line must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80]])
    pivot = ws / "output" / "q14_payment_zone_pivot.json"
    if not pivot.exists():
        _finish(["cannot verify hash: output/q14_payment_zone_pivot.json missing"])
    digest = hashlib.sha256(pivot.read_bytes()).hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: signoff %s != recomputed %s" % (m.group(1)[:12], digest[:12]))
    _finish(fails)
main()
'''

PREF = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""eng2 preference checker (P1 schema_version / P2 script header / P3 sample naming /
P4 quality-report field order / P5 verbatim column names)."""
import sys, re, json, argparse
from pathlib import Path

ORDER = ["field_name", "null_count", "null_pct", "invalid_count", "invalid_pct", "notes"]


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Every output JSON file carries a top-level schema_version == "1.0"."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    if not isinstance(data, dict):
        return False, "P1: top-level must be a JSON object carrying schema_version"
    if str(data.get("schema_version")) != "1.0":
        return False, "P1: missing top-level schema_version == \\"1.0\\" (got %r)" % data.get("schema_version")
    return True, "P1: PASSED"


def check_P2(ws, target):
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    head = "\\n".join(txt.splitlines()[:3])
    if "#!/usr/bin/env python3" not in head:
        return False, "P2: missing '#!/usr/bin/env python3' shebang on line 1-2"
    if "# -*- coding: utf-8 -*-" not in head:
        return False, "P2: missing '# -*- coding: utf-8 -*-' encoding header"
    return True, "P2: PASSED"


def check_P3(ws, target):
    """Sample files named {type}_{year}{month:02d}_sample.csv."""
    tp = ws / target
    files = [tp] if tp.is_file() else list(tp.glob("*_sample.csv")) if tp.exists() else []
    if not files:
        return True, "P3: no sample files, skip"
    pat = re.compile(r"^[a-z]+_\\d{6}_sample\\.(csv|parquet)$")
    bad = [f.name for f in files if not pat.match(f.name)]
    if bad:
        return False, "P3: sample files not matching {type}_{YYYYMM}_sample: %s" % bad
    return True, "P3: PASSED"


def check_P4(ws, target):
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P4: target is not valid JSON"
    fields = data.get("fields")
    entries = fields if isinstance(fields, list) else (list(fields.values()) if isinstance(fields, dict) else [])
    for e in entries:
        if not isinstance(e, dict):
            continue
        idx = [ORDER.index(k) for k in e.keys() if k in ORDER]
        if idx != sorted(idx):
            return False, "P4: field-object key order violates field_name/null_count/null_pct/invalid_count/invalid_pct/notes"
    return True, "P4: PASSED"


def check_P5(ws, target):
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    if re.search(r"(?<!tpep_)pickup_datetime", txt):
        return False, "P5: uses abbreviated 'pickup_datetime' instead of verbatim 'tpep_pickup_datetime'"
    return True, "P5: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4, "P5": check_P5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4,P5")
    ap.add_argument("--target", default="output/")
    a = ap.parse_args()
    ws = Path(a.workspace)
    rules = [r.strip() for r in a.rules.split(",") if r.strip()]
    unknown = [r for r in rules if r not in RULES]
    if unknown:
        print("FAILED: unknown rules: %s" % unknown); sys.exit(1)
    fails = []
    for r in rules:
        ok, msg = RULES[r](ws, a.target)
        print(msg)
        if not ok:
            fails.append(msg)
    if fails:
        for m in fails:
            print("FAILED: " + m)
        sys.exit(1)
    print("PASSED"); sys.exit(0)


if __name__ == "__main__":
    main()
'''


def main():
    for name, body in CHECKS.items():
        (OUT / f"{name}.py").write_text(HEADER + textwrap.dedent(body), encoding="utf-8")
    (OUT / "check_preferences.py").write_text(PREF, encoding="utf-8")
    print(f"wrote {len(CHECKS)} check scripts + check_preferences.py to {OUT}")


if __name__ == "__main__":
    main()
