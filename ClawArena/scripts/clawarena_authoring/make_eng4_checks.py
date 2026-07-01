#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_eng4_checks.py — 生成 eng4 的全部 exec_check 校验脚本到 eval/eng4/scripts/。

每个 check_qN.py 自包含，约定：argv[1]=workspace；PASSED+exit0 / FAILED+exit1。
三层验证（结构→字段→真值），数值带容差，锚点对齐 build_eng4.py 注入的真实/合成数据。
check_preferences.py 实现 P1-P5。生成器内容即评测逻辑，可逐脚本审阅。
"""
from pathlib import Path
import textwrap

OUT = Path("/home/xkaiwen/workspace/ClawArena/data/clawarena-real/eval/eng4/scripts")
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
'''

CHECKS = {}

# Q1: Top-5 slow queries from pgstatstatements_snapshot.csv
# mean_exec_time > 500ms; array length = 5; queryids must exactly match top-5 from CSV
# HARDENED: exact queryid set {1003,1014,1010,1013,1017}; mean_exec_time_ms within 1% of CSV values
CHECKS["check_q1"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "work" / "slow_queries_top5.json")
    if err: _finish([err])
    # Structure: must be a list
    if not isinstance(data, list):
        _finish(["slow_queries_top5.json must be a JSON array"])
    if len(data) != 5:
        fails.append("array length == %d (expected exactly 5)" % len(data))
    required_fields = {"queryid", "query_preview", "mean_exec_time_ms", "calls"}
    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            fails.append("entry[%d] is not an object" % i); continue
        missing = required_fields - set(entry.keys())
        if missing:
            fails.append("entry[%d] missing fields %s" % (i, sorted(missing))); continue
        # True-value layer: mean_exec_time_ms must be > 500
        try:
            met = float(entry["mean_exec_time_ms"])
        except (TypeError, ValueError):
            fails.append("entry[%d].mean_exec_time_ms not numeric: %r" % (i, entry["mean_exec_time_ms"])); continue
        if met <= 500:
            fails.append("entry[%d].mean_exec_time_ms == %.2f (must be > 500ms)" % (i, met))
        # calls must be a positive integer
        try:
            c = int(entry["calls"])
            if c <= 0:
                fails.append("entry[%d].calls must be positive int, got %d" % (i, c))
        except (TypeError, ValueError):
            fails.append("entry[%d].calls not an int: %r" % (i, entry["calls"]))
        # queryid must be a positive integer
        try:
            qid = int(entry["queryid"])
            if qid <= 0:
                fails.append("entry[%d].queryid must be positive int, got %r" % (i, qid))
        except (TypeError, ValueError):
            fails.append("entry[%d].queryid not an int: %r" % (i, entry["queryid"]))
    # Verify sorted descending by mean_exec_time_ms
    if len(data) == 5:
        times = []
        for e in data:
            try:
                times.append(float(e["mean_exec_time_ms"]))
            except Exception:
                pass
        if times != sorted(times, reverse=True):
            fails.append("array is not sorted descending by mean_exec_time_ms")
    # HARDENED: exact queryid set must be {1003, 1014, 1010, 1013, 1017} (true top-5 from CSV)
    EXACT_QUERYIDS = {1003, 1014, 1010, 1013, 1017}
    if len(data) == 5 and not any("queryid" in (f or "") for f in fails):
        try:
            got_ids = set(int(e["queryid"]) for e in data if isinstance(e, dict))
            if got_ids != EXACT_QUERYIDS:
                fails.append(
                    "queryid set %s != expected %s (read the CSV: top-5 by mean_exec_time are queryids 1003, 1014, 1010, 1013, 1017 — NOT starting at 1001)" % (
                        sorted(got_ids), sorted(EXACT_QUERYIDS)
                    )
                )
        except (TypeError, ValueError, KeyError):
            pass
    # HARDENED: each entry's mean_exec_time_ms must match the CSV value within 1%
    TRUE_TIMES = {1003: 12450.67, 1014: 9870.34, 1010: 8920.45, 1013: 7340.88, 1017: 6120.45}
    for i, entry in enumerate(data):
        if not isinstance(entry, dict): continue
        try:
            qid = int(entry.get("queryid") or 0)
            met = float(entry.get("mean_exec_time_ms") or 0)
            if qid in TRUE_TIMES:
                ref = TRUE_TIMES[qid]
                if not (ref * 0.99 <= met <= ref * 1.01):
                    fails.append(
                        "entry[%d] queryid=%d mean_exec_time_ms=%.2f does not match CSV value %.2f (within 1%%)" % (
                            i, qid, met, ref
                        )
                    )
        except (TypeError, ValueError):
            pass
    _finish(fails)
main()
'''

# Q2: Query-001 EXPLAIN JSON analysis
# total_cost must match 2876543.20 (within 1%), node_type=Seq Scan
# HARDENED: plan_rows must be exactly 450, actual_rows exactly 24891,
#   rows_estimate_error_pct within 2% of true value 98.19
CHECKS["check_q2"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "work" / "q001_analysis.json")
    if err: _finish([err])
    # node_type / scan_type must be "Seq Scan"
    nt = data.get("node_type") or data.get("scan_type")
    st = data.get("scan_type") or data.get("node_type")
    if nt != "Seq Scan":
        fails.append("node_type == %r (expected \\"Seq Scan\\")" % nt)
    if st != "Seq Scan":
        fails.append("scan_type == %r (expected \\"Seq Scan\\")" % st)
    # total_cost must be within 1% of 2876543.20
    try:
        tc = float(data.get("total_cost") or 0)
        ref = 2876543.20
        if not (ref * 0.99 <= tc <= ref * 1.01):
            fails.append("total_cost == %.2f (expected ~2876543.20 within 1%%)" % tc)
    except (TypeError, ValueError):
        fails.append("total_cost not numeric: %r" % data.get("total_cost"))
    # HARDENED: plan_rows must be exactly 450 (from query_001_before.json Plan Rows field)
    try:
        pr = int(data.get("plan_rows") or 0)
        if pr != 450:
            fails.append("plan_rows == %d (expected exactly 450 from query_001_before.json Plan Rows field)" % pr)
    except (TypeError, ValueError):
        fails.append("plan_rows not an int: %r" % data.get("plan_rows")); pr = 0
    # HARDENED: actual_rows must be exactly 24891 (from query_001_before.json Actual Rows field)
    try:
        ar = int(data.get("actual_rows") or 0)
        if ar != 24891:
            fails.append("actual_rows == %d (expected exactly 24891 from query_001_before.json Actual Rows field)" % ar)
    except (TypeError, ValueError):
        fails.append("actual_rows not an int: %r" % data.get("actual_rows")); ar = 24891
    # HARDENED: rows_estimate_error_pct must be within 2% of 98.19
    # True value: abs(450 - 24891) / 24891 * 100 = 98.19 (NOT a crude >50% check)
    TRUE_ERROR_PCT = 98.19  # abs(450 - 24891) / 24891 * 100 rounded to 2dp
    try:
        rep = float(data.get("rows_estimate_error_pct") or 0)
        if not (TRUE_ERROR_PCT - 2.0 <= rep <= TRUE_ERROR_PCT + 2.0):
            fails.append(
                "rows_estimate_error_pct == %.2f (expected %.2f ± 2%%; formula: abs(450-24891)/24891*100 = 98.19; a colleague\\'s estimate of 5000%% is wrong — verify the actual EXPLAIN data)" % (
                    rep, TRUE_ERROR_PCT
                )
            )
    except (TypeError, ValueError):
        fails.append("rows_estimate_error_pct not numeric: %r" % data.get("rows_estimate_error_pct"))
    _finish(fails)
main()
'''

# Q3: Index recommendation for Query-001
# index_type must be "btree" (not "hash"); columns must include service_id; rationale must cite a URL
CHECKS["check_q3"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "work" / "q001_index_recommendation.json")
    if err: _finish([err])
    # index_type must be a valid PostgreSQL index type and NOT hash (range query on created_at)
    valid_types = {"btree", "hash", "gin", "gist", "spgist", "brin"}
    idx_type = str(data.get("index_type") or "").lower()
    if idx_type not in valid_types:
        fails.append("index_type %r is not a valid PostgreSQL index type (%s)" % (idx_type, sorted(valid_types)))
    if idx_type == "hash":
        fails.append("index_type == \\"hash\\" is incorrect: Hash indexes support only = equality, not range queries on created_at (see https://www.postgresql.org/docs/current/indexes-types.html)")
    # columns must include service_id
    cols = [str(c).lower() for c in (data.get("columns") or [])]
    if not any("service_id" in c for c in cols):
        fails.append("columns must include service_id (the filter column in Query-001)")
    # rationale must cite a URL
    rationale = str(data.get("rationale") or "")
    if "http" not in rationale and "postgresql.org" not in rationale:
        fails.append("rationale must cite a documentation URL (e.g. https://www.postgresql.org/docs/current/indexes-types.html)")
    # table_name must reference events
    tname = str(data.get("table_name") or "").lower()
    if "event" not in tname:
        fails.append("table_name %r must reference the events table" % data.get("table_name"))
    _finish(fails)
main()
'''

# Q4: CREATE INDEX CONCURRENTLY DDL + optimization_log.jsonl
# HARDENED: log entry count must exactly equal CREATE INDEX count in SQL;
#   each log entry requires rationale field; all CREATE INDEX must use CONCURRENTLY
CHECKS["check_q4"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    # Check index_ddl_batch1.sql
    sql_txt = _read(ws / "work" / "index_ddl_batch1.sql")
    if sql_txt is None:
        _finish(["file not found: work/index_ddl_batch1.sql"])
    low_sql = sql_txt.lower()
    # Must contain CONCURRENTLY
    if "concurrently" not in low_sql:
        fails.append("index_ddl_batch1.sql does not contain CONCURRENTLY keyword")
    # All CREATE INDEX statements must use CONCURRENTLY (no exceptions)
    for line in sql_txt.splitlines():
        ll = line.lower().strip()
        if "create index" in ll and "concurrently" not in ll:
            if not ll.startswith("--") and not ll.startswith("#"):
                fails.append("index_ddl_batch1.sql: CREATE INDEX without CONCURRENTLY: %r" % line[:80])
    # Must have at least 3 CREATE INDEX statements
    ci_count = len(re.findall(r"create\\s+index", low_sql))
    if ci_count < 3:
        fails.append("index_ddl_batch1.sql has only %d CREATE INDEX statements (expected >= 3)" % ci_count)
    # Must target events or notifications tables (per question specification)
    if "events" not in low_sql and "notifications" not in low_sql:
        fails.append("index_ddl_batch1.sql must create indexes on events and/or notifications tables")
    # Check optimization_log.jsonl
    log_txt = _read(ws / "work" / "optimization_log.jsonl")
    if log_txt is None:
        _finish(["file not found: work/optimization_log.jsonl"])
    log_lines = [l.strip() for l in log_txt.splitlines() if l.strip()]
    if not log_lines:
        _finish(["optimization_log.jsonl is empty"])
    entries = []
    for i, line in enumerate(log_lines):
        try:
            entry = json.loads(line)
            entries.append(entry)
        except json.JSONDecodeError as e:
            fails.append("optimization_log.jsonl line %d is not valid JSON: %s" % (i+1, str(e)[:80]))
    # HARDENED: log entry count must exactly match CREATE INDEX count in SQL
    if entries and ci_count > 0 and len(entries) != ci_count:
        fails.append(
            "optimization_log.jsonl has %d entries but index_ddl_batch1.sql has %d CREATE INDEX statements "
            "(each DDL must have exactly one log entry)" % (len(entries), ci_count)
        )
    # Each entry must have action == "create_index"
    for i, e in enumerate(entries):
        if not isinstance(e, dict):
            fails.append("log entry %d is not a JSON object" % i); continue
        if e.get("action") != "create_index":
            fails.append("log entry %d: action == %r (expected \\"create_index\\")" % (i, e.get("action")))
        if not e.get("ddl"):
            fails.append("log entry %d: ddl field is empty" % i)
        if not e.get("timestamp"):
            fails.append("log entry %d: timestamp field missing" % i)
        # HARDENED: rationale field must be present and non-empty
        if not e.get("rationale"):
            fails.append("log entry %d: rationale field missing or empty (required for audit trail)" % i)
    _finish(fails)
main()
'''

# Q5: Archive review — is_outdated=true, outdated_recommendations mentions Hash index limitation
# HARDENED: original_text must quote actual DDL from archive file (containing "HASH");
#   reason_outdated must explicitly mention both "equality" AND "range" to show agent read the source
CHECKS["check_q5"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "work" / "archive_review.json")
    if err: _finish([err])
    # is_outdated must be True
    if data.get("is_outdated") is not True:
        fails.append("is_outdated == %r (expected true)" % data.get("is_outdated"))
    # outdated_recommendations must be a non-empty array with at least 2 entries
    # (archive has 2 Hash index recommendations and the work_mem recommendation)
    orecs = data.get("outdated_recommendations") or []
    if not isinstance(orecs, list) or len(orecs) == 0:
        fails.append("outdated_recommendations must be a non-empty array")
    else:
        # HARDENED: at least one entry\'s original_text must contain "HASH" (case-insensitive)
        # and reference an actual DDL/recommendation from the archive file
        found_hash_original = False
        found_hash_reason_complete = False
        for rec in orecs:
            if not isinstance(rec, dict):
                continue
            reason = str(rec.get("reason_outdated") or "").lower()
            orig = str(rec.get("original_text") or "").lower()
            # HARDENED: original_text must contain "hash" to show it came from the archive
            if "hash" in orig:
                found_hash_original = True
                # HARDENED: reason_outdated must mention BOTH "equality" AND "range"
                # (the archive itself explains this limitation explicitly)
                if ("equality" in reason or "only =" in reason or "= operator" in reason or "only equality" in reason) and (
                    "range" in reason
                ):
                    found_hash_reason_complete = True
        if not found_hash_original:
            fails.append(
                "outdated_recommendations: at least one entry\\'s original_text must quote the Hash index DDL "
                "from the archive (must contain \\'HASH\\' — read archive/old_optimization_plan_v0.md literally)"
            )
        elif not found_hash_reason_complete:
            fails.append(
                "outdated_recommendations: reason_outdated for the Hash index entry must explicitly mention "
                "BOTH \\'equality\\' (what Hash supports) AND \\'range\\' (what it cannot support)"
            )
    # valid_recommendations must be an array (can be empty if nothing is valid)
    vrecs = data.get("valid_recommendations")
    if vrecs is not None and not isinstance(vrecs, list):
        fails.append("valid_recommendations must be an array")
    _finish(fails)
main()
'''

# Q6: Query-004 statistics analysis
# n_distinct must be -0.23 (from seed_stats.sql, NOT -1 from the bot decoy)
# diagnosis must be "stale_statistics"
CHECKS["check_q6"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "work" / "q004_stats_analysis.json")
    if err: _finish([err])
    # n_distinct must be -0.23 (authoritative from seed_stats.sql); tolerance ±0.02
    try:
        nd = float(data.get("n_distinct") or 0)
        if not (-0.25 <= nd <= -0.21):
            fails.append("n_distinct == %.4f (expected ~-0.23 from seed_stats.sql; Sreedhar\\'s bot claim of -1.0 is incorrect)" % nd)
    except (TypeError, ValueError):
        fails.append("n_distinct not numeric: %r" % data.get("n_distinct"))
    # correlation must be present and numeric
    try:
        corr = float(data.get("correlation") or 0)
    except (TypeError, ValueError):
        fails.append("correlation not numeric: %r" % data.get("correlation"))
    # diagnosis must be "stale_statistics"
    diag = str(data.get("diagnosis") or "").lower().strip()
    if diag != "stale_statistics":
        fails.append("diagnosis == %r (expected \\"stale_statistics\\")" % data.get("diagnosis"))
    # table_name and column_name must be present
    if not data.get("table_name"):
        fails.append("table_name field missing or empty")
    if not data.get("column_name"):
        fails.append("column_name field missing or empty")
    # column_name must reference is_read
    cn = str(data.get("column_name") or "").lower()
    if "is_read" not in cn and "read" not in cn:
        fails.append("column_name %r must reference the is_read column" % data.get("column_name"))
    _finish(fails)
main()
'''

# Q7: Before/after comparison for Q1-Q9
# 9 entries; query_001 after_node_type="Index Only Scan"; before_total_cost for query_001 consistent with Q2
# cost_reduction_pct formula verified
CHECKS["check_q7"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "work" / "optimization_comparison.json")
    if err: _finish([err])
    results = data.get("results") or []
    if not isinstance(results, list):
        _finish(["optimization_comparison.json: results must be a JSON array"])
    if len(results) != 9:
        fails.append("results array length == %d (expected exactly 9)" % len(results))
    required = {"query_id","before_node_type","after_node_type","before_total_cost",
                "after_total_cost","cost_reduction_pct","before_actual_time_ms","after_actual_time_ms"}
    q001_entry = None
    for i, entry in enumerate(results):
        if not isinstance(entry, dict):
            fails.append("results[%d] is not an object" % i); continue
        missing = required - set(entry.keys())
        if missing:
            fails.append("results[%d] missing fields %s" % (i, sorted(missing)))
        qid = str(entry.get("query_id") or "")
        if "001" in qid:
            q001_entry = entry
        # Verify cost_reduction_pct arithmetic
        try:
            bef = float(entry.get("before_total_cost") or 0)
            aft = float(entry.get("after_total_cost") or 0)
            crp = float(entry.get("cost_reduction_pct") or 0)
            if bef > 0:
                expected_pct = round((bef - aft) / bef * 100, 2)
                if abs(crp - expected_pct) > 0.1:
                    fails.append("results[%d].cost_reduction_pct == %.2f but expected %.2f "
                                 "(formula: (before-after)/before*100)" % (i, crp, expected_pct))
        except (TypeError, ValueError):
            fails.append("results[%d] cost fields not numeric" % i)
    # query_001 specific checks
    if q001_entry is not None:
        ant = q001_entry.get("after_node_type")
        if ant != "Index Only Scan":
            fails.append("query_001 after_node_type == %r (expected \\"Index Only Scan\\")" % ant)
        # Cross-round closure: before_total_cost must match q001_analysis.json
        q2_data, q2_err = _load_json(ws / "work" / "q001_analysis.json")
        if not q2_err and q2_data is not None:
            try:
                q2_cost = float(q2_data.get("total_cost") or 0)
                q7_bef = float(q001_entry.get("before_total_cost") or 0)
                if abs(q7_bef - q2_cost) > q2_cost * 0.01:
                    fails.append("cross-round drift: query_001 before_total_cost %.2f != Q2 total_cost %.2f" % (q7_bef, q2_cost))
            except (TypeError, ValueError):
                pass
    elif len(results) >= 9:
        fails.append("no results entry found for query_001")
    _finish(fails)
main()
'''

# Q8: Query-010 join analysis (before Update 2 supersede)
# has_disk_spill=true, hash_batches > 1, initial recommendation='increase_work_mem'
CHECKS["check_q8"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "work" / "q010_join_analysis.json")
    if err: _finish([err])
    # has_disk_spill must be True
    hds = data.get("has_disk_spill")
    if hds is not True:
        fails.append("has_disk_spill == %r (expected true; EXPLAIN shows Hash Batches=8 and Sort Method=external merge Disk)" % hds)
    # hash_batches must be > 1
    try:
        hb = int(data.get("hash_batches") or 0)
        if hb <= 1:
            fails.append("hash_batches == %d (expected > 1 — indicates disk spill)" % hb)
    except (TypeError, ValueError):
        fails.append("hash_batches not an int: %r" % data.get("hash_batches"))
    # recommendation must be a valid value
    valid_recs = {"increase_work_mem", "rewrite_query", "add_index", "create_statistics"}
    rec = str(data.get("recommendation") or "")
    if rec not in valid_recs:
        fails.append("recommendation %r not in valid set %s" % (rec, sorted(valid_recs)))
    # At this point (Q8, before Update 2), recommendation should be increase_work_mem
    # but we accept any valid value since agent may read Update 2 early
    # join_type must be present and non-empty
    if not data.get("join_type"):
        fails.append("join_type field missing or empty")
    _finish(fails)
main()
'''

# Q9: Partial index for Query-011
# SQL must contain WHERE clause for billed IS NOT TRUE; CONCURRENTLY required
# rationale file must cite partial index documentation
CHECKS["check_q9"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    # Check q011_partial_index.sql
    sql_txt = _read(ws / "work" / "q011_partial_index.sql")
    if sql_txt is None:
        _finish(["file not found: work/q011_partial_index.sql"])
    low_sql = sql_txt.lower()
    # Must have WHERE clause for billed IS NOT TRUE (or equivalent billed = FALSE / billed IS FALSE)
    has_where_billed = bool(
        re.search(r"where\\s+billed\\s+is\\s+not\\s+true", low_sql) or
        re.search(r"where\\s+billed\\s*=\\s*false", low_sql) or
        re.search(r"where\\s+not\\s+billed", low_sql) or
        re.search(r"where\\s+billed\\s+is\\s+false", low_sql)
    )
    if not has_where_billed:
        fails.append("q011_partial_index.sql must contain a WHERE clause equivalent to 'billed IS NOT TRUE'")
    # Must use CONCURRENTLY (P4, implicit)
    if "concurrently" not in low_sql:
        fails.append("q011_partial_index.sql must use CONCURRENTLY (production DDL requirement P4)")
    # Check rationale file
    rationale_txt = _read(ws / "work" / "q011_partial_index_rationale.md")
    if rationale_txt is None:
        fails.append("file not found: work/q011_partial_index_rationale.md")
    else:
        low_rat = rationale_txt.lower()
        # Must reference partial index documentation
        if "partial" not in low_rat:
            fails.append("q011_partial_index_rationale.md must discuss partial indexes")
        if "postgresql.org" not in low_rat and "http" not in low_rat:
            fails.append("q011_partial_index_rationale.md must cite a documentation URL")
    _finish(fails)
main()
'''

# Q10: Supersede applied — recommendation must be "create_statistics"; SQL must use CREATE STATISTICS with dependencies
CHECKS["check_q10"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    # Check q010_join_analysis.json — recommendation must now be create_statistics
    data, err = _load_json(ws / "work" / "q010_join_analysis.json")
    if err: _finish([err])
    rec = str(data.get("recommendation") or "")
    if rec != "create_statistics":
        fails.append("q010_join_analysis.json: recommendation == %r (expected \\"create_statistics\\" per architect\\'s supersede; NOT \\"increase_work_mem\\")" % rec)
    # Check q010_create_statistics.sql
    sql_txt = _read(ws / "work" / "q010_create_statistics.sql")
    if sql_txt is None:
        _finish(["file not found: work/q010_create_statistics.sql"])
    low_sql = sql_txt.lower()
    # Must use CREATE STATISTICS syntax
    if "create statistics" not in low_sql:
        fails.append("q010_create_statistics.sql must use CREATE STATISTICS syntax")
    # Must include "dependencies" statistics kind (from planner-stats docs / Render case study)
    if "dependencies" not in low_sql:
        fails.append("q010_create_statistics.sql must specify \\'dependencies\\' statistics kind (functional dependencies, per planner-stats docs)")
    # Must reference events table
    if "events" not in low_sql:
        fails.append("q010_create_statistics.sql must reference the events table")
    _finish(fails)
main()
'''

# Q11: Covering index with INCLUDE for Query-012
# Must have INCLUDE keyword; INCLUDE must cover name and updated_at; CONCURRENTLY required
# HARDENED: email must be the key column in the ON clause (not in INCLUDE);
#   INCLUDE clause must specifically contain both name and updated_at
CHECKS["check_q11"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    sql_txt = _read(ws / "work" / "q012_covering_index.sql")
    if sql_txt is None:
        _finish(["file not found: work/q012_covering_index.sql"])
    low_sql = sql_txt.lower()
    # Must use INCLUDE keyword
    if "include" not in low_sql:
        fails.append("q012_covering_index.sql must use the INCLUDE clause (for covering index / Index Only Scan)")
    # Must use CONCURRENTLY (P4 implicit)
    if "concurrently" not in low_sql:
        fails.append("q012_covering_index.sql must use CONCURRENTLY (production DDL requirement)")
    # Must reference users table
    if "users" not in low_sql:
        fails.append("q012_covering_index.sql must reference the users table")
    # HARDENED: email must appear as the index key column (in ON clause, before INCLUDE)
    # Strip SQL comments to avoid matching email from comment text
    sql_no_comments_raw = re.sub(r"--[^\\n]*", "", low_sql)
    # email must be in the ON (...) key, not only in INCLUDE (...)
    # Pattern: ON <table> (email ...) INCLUDE (...)
    m_on_key = re.search(r"\\bon\\s+\\w+\\s*\\(([^)]+)\\)\\s*include", sql_no_comments_raw)
    m_email_any = re.search(r"\\bemail\\b", sql_no_comments_raw)
    if not m_email_any:
        fails.append("q012_covering_index.sql must index on email column (the WHERE predicate in query_012)")
    elif m_on_key:
        key_cols = m_on_key.group(1)
        if "email" not in key_cols:
            fails.append(
                "q012_covering_index.sql: email must be the index key column (in ON users (email) before INCLUDE), "
                "not placed inside INCLUDE — email is the filter column, so it must be the indexed key"
            )
    # HARDENED: INCLUDE clause must contain both name and updated_at
    # Strip SQL comments (-- to end of line) to avoid false positives from comment text
    sql_no_comments = re.sub(r"--[^\\n]*", "", low_sql)
    # Find the INCLUDE keyword in actual DDL (not in comments)
    m_include = re.search(r"\\binclude\\s*\\(([^)]+)\\)", sql_no_comments)
    if m_include:
        include_cols = m_include.group(1)
        if "name" not in include_cols:
            fails.append(
                "q012_covering_index.sql: INCLUDE clause must contain \\'name\\' column "
                "(required to cover SELECT u.name without heap fetch)"
            )
        if "updated_at" not in include_cols:
            fails.append(
                "q012_covering_index.sql: INCLUDE clause must contain \\'updated_at\\' column "
                "(required to cover SELECT u.updated_at without heap fetch)"
            )
    elif "include" in sql_no_comments:
        fails.append("q012_covering_index.sql: INCLUDE clause has no valid parenthesized column list")
    _finish(fails)
main()
'''

# Q12: Scan type summary
# total_queries = 12; scan_type_distribution is a non-empty object; seq_scan_remaining < 4
CHECKS["check_q12"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "work" / "scan_type_summary.json")
    if err: _finish([err])
    # total_queries must be exactly 12
    tq = data.get("total_queries")
    try:
        tq = int(tq)
        if tq != 12:
            fails.append("total_queries == %d (expected exactly 12: 9 original + 3 from Update 2)" % tq)
    except (TypeError, ValueError):
        fails.append("total_queries not an int: %r" % data.get("total_queries"))
    # scan_type_distribution must be a non-empty object with string keys and int values
    std = data.get("scan_type_distribution")
    if not isinstance(std, dict) or not std:
        fails.append("scan_type_distribution must be a non-empty object")
    else:
        for k, v in std.items():
            try:
                int(v)
            except (TypeError, ValueError):
                fails.append("scan_type_distribution[%r] value must be an int, got %r" % (k, v))
    # seq_scan_remaining must be a list with < 4 entries (most queries were optimized)
    ssr = data.get("seq_scan_remaining")
    if not isinstance(ssr, list):
        fails.append("seq_scan_remaining must be an array")
    elif len(ssr) >= 4:
        fails.append("seq_scan_remaining has %d entries (expected < 4 — most queries should be optimized)" % len(ssr))
    _finish(fails)
main()
'''

# Q13: Analyze plan for notifications
# tables_need_analyze includes notifications; reason mentions stale_statistics or bulk delete
# run_analyze.sh contains ANALYZE notifications
CHECKS["check_q13"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    # Check analyze_plan.json (P1: must be in work/)
    data, err = _load_json(ws / "work" / "analyze_plan.json")
    if err: _finish([err])
    tables = data.get("tables_need_analyze") or []
    if not isinstance(tables, list) or len(tables) == 0:
        _finish(["tables_need_analyze must be a non-empty array"])
    # Must include notifications
    notif_entry = None
    for t in tables:
        if not isinstance(t, dict): continue
        tn = str(t.get("table_name") or "").lower()
        if "notification" in tn:
            notif_entry = t
            break
    if notif_entry is None:
        fails.append("tables_need_analyze must include 'notifications' table")
    else:
        reason = str(notif_entry.get("reason") or "").lower()
        # reason must mention stale statistics or bulk delete
        if not (re.search(r"stale|statistic|bulk|delete|autovacuum|dead", reason)):
            fails.append("notifications entry: reason must mention stale statistics or bulk delete, got %r" % reason[:80])
    # Check run_analyze.sh (P1: must be in work/)
    sh_txt = _read(ws / "work" / "run_analyze.sh")
    if sh_txt is None:
        fails.append("file not found: work/run_analyze.sh")
    else:
        low_sh = sh_txt.lower()
        if "analyze" not in low_sh:
            fails.append("run_analyze.sh must contain an ANALYZE command")
        if "notification" not in low_sh:
            fails.append("run_analyze.sh must reference the notifications table")
    _finish(fails)
main()
'''

# Q14: Final report + SHA-256 sign-off
# total_queries_optimized=12; work_mem_modified=false; signoff.txt matches recomputed hash
CHECKS["check_q14"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    report_path = ws / "work" / "final_optimization_report.json"
    sign_path = ws / "work" / "signoff.txt"
    data, err = _load_json(report_path)
    if err: _finish([err])
    # total_queries_optimized must be 12 (consistent with Q12)
    tqo = data.get("total_queries_optimized")
    try:
        tqo = int(tqo)
        if tqo != 12:
            fails.append("total_queries_optimized == %d (expected 12, must match Q12 total_queries)" % tqo)
    except (TypeError, ValueError):
        fails.append("total_queries_optimized not an int: %r" % data.get("total_queries_optimized"))
    # work_mem_modified must be False (architect superseded the work_mem change)
    wmm = data.get("work_mem_modified")
    if wmm is not False:
        fails.append("work_mem_modified == %r (must be false — architect superseded the work_mem=256MB directive)" % wmm)
    # indexes_created must be present and non-empty
    ic = data.get("indexes_created") or []
    if not isinstance(ic, list) or len(ic) == 0:
        fails.append("indexes_created must be a non-empty array")
    # statistics_created must reference CREATE STATISTICS
    sc = data.get("statistics_created") or []
    if not isinstance(sc, list) or len(sc) == 0:
        fails.append("statistics_created must be a non-empty array")
    else:
        found_deps = any("statistic" in str(s).lower() for s in sc)
        if not found_deps:
            fails.append("statistics_created must include the CREATE STATISTICS DDL")
    # Cross-round closure with optimization_log.jsonl: indexes_created length must match log entries
    log_txt = _read(ws / "work" / "optimization_log.jsonl")
    if log_txt:
        log_count = sum(1 for l in log_txt.splitlines() if l.strip())
        if log_count > 0 and len(ic) != log_count:
            fails.append("indexes_created length %d != optimization_log.jsonl entries %d (cross-round closure)" % (len(ic), log_count))
    # Check signoff.txt
    sign = _read(sign_path)
    if sign is None:
        _finish(["file not found: work/signoff.txt"])
    line = sign.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        fails.append("signoff.txt must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80])
    elif report_path.exists():
        digest = hashlib.sha256(report_path.read_bytes()).hexdigest()
        if m.group(1) != digest:
            fails.append("sha256 mismatch: signoff %s != recomputed %s" % (m.group(1)[:12], digest[:12]))
    _finish(fails)
main()
'''

PREF = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""eng4 preference checker (P1 work/ dir / P2 snake_case / P3 rationale URL /
P4 CONCURRENTLY / P5 q{N}_ prefix)."""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """All work products must be in the work/ directory."""
    tp = Path(ws) / target
    if not tp.exists():
        return True, "P1: target missing, skip"
    # Verify the target path is under work/
    try:
        tp.relative_to(Path(ws) / "work")
        return True, "P1: PASSED (target is under work/)"
    except ValueError:
        return False, "P1: deliverable %s must be inside work/ directory" % target


def check_P2(ws, target):
    """JSON field names must use snake_case (no camelCase or PascalCase)."""
    txt = _read(Path(ws) / target)
    if txt is None:
        return True, "P2: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return True, "P2: target not JSON, skip"
    # Check all keys at all levels recursively
    def collect_keys(obj):
        if isinstance(obj, dict):
            for k in obj.keys():
                yield k
                yield from collect_keys(obj[k])
        elif isinstance(obj, list):
            for item in obj:
                yield from collect_keys(item)
    camel_pat = re.compile(r"[a-z][A-Z]")  # camelCase indicator
    pascal_pat = re.compile(r"^[A-Z]")     # PascalCase indicator
    bad_keys = []
    for key in collect_keys(data):
        if isinstance(key, str):
            if camel_pat.search(key) or pascal_pat.match(key):
                bad_keys.append(key)
    if bad_keys:
        return False, "P2: non-snake_case JSON keys found: %s" % bad_keys[:5]
    return True, "P2: PASSED"


def check_P3(ws, target):
    """rationale field in index recommendation JSON must cite a documentation URL."""
    txt = _read(Path(ws) / target)
    if txt is None:
        return True, "P3: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return True, "P3: target not JSON, skip"
    # Look for rationale field at any level
    def find_rationale(obj):
        if isinstance(obj, dict):
            if "rationale" in obj:
                yield obj["rationale"]
            for v in obj.values():
                yield from find_rationale(v)
        elif isinstance(obj, list):
            for item in obj:
                yield from find_rationale(item)
    rationales = list(find_rationale(data))
    if not rationales:
        return True, "P3: no rationale field found, skip"
    for rat in rationales:
        if "http" not in str(rat) and "postgresql.org" not in str(rat):
            return False, "P3: rationale must cite a documentation URL, got %r" % str(rat)[:80]
    return True, "P3: PASSED"


def check_P4(ws, target):
    """All CREATE INDEX statements must use CONCURRENTLY."""
    txt = _read(Path(ws) / target)
    if txt is None:
        return True, "P4: target missing, skip"
    low = txt.lower()
    # Check if file contains any CREATE INDEX
    if "create index" not in low:
        return True, "P4: no CREATE INDEX found, skip"
    # Every CREATE INDEX must have CONCURRENTLY
    lines = txt.splitlines()
    for line in lines:
        ll = line.lower().strip()
        if "create index" in ll and "concurrently" not in ll:
            # Allow lines that are just comments
            if not ll.startswith("--") and not ll.startswith("#"):
                return False, "P4: CREATE INDEX without CONCURRENTLY: %r" % line[:80]
    return True, "P4: PASSED"


def check_P5(ws, target):
    """SQL files must use q{N}_ prefix naming convention."""
    tp = Path(ws) / target
    if not tp.exists():
        return True, "P5: target missing, skip"
    fname = tp.name
    if fname.endswith(".sql"):
        pat = re.compile(r"^q\\d+_")
        if not pat.match(fname):
            return False, "P5: SQL file name %r does not use q{N}_ prefix (e.g. q011_partial_index.sql)" % fname
    return True, "P5: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4, "P5": check_P5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4,P5")
    ap.add_argument("--target", default="work/")
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
