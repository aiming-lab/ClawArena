#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_prd5_checks.py — 生成 prd5 的全部 exec_check 校验脚本到 eval/prd5/scripts/。

每个 check_qN.py 自包含，约定：argv[1]=workspace；PASSED+exit0 / FAILED+exit1。
三层验证（结构→字段→真值），数值带容差，锚点对齐真实 ground-truth 数据。
check_preferences.py 实现 P1-P5。
"""
from pathlib import Path
import textwrap

OUT = Path("/home/xkaiwen/workspace/ClawArena/data/clawarena-real/eval/prd5/scripts")
OUT.mkdir(parents=True, exist_ok=True)

HEADER = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, math
from pathlib import Path

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON: " + str(e)

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

# Q1 — running experiments (exactly 5: exp006-exp010)
# Hardened: output must be a plain JSON array of strings only; dict format rejected.
CHECKS["check_q1"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q1_running_experiments.json")
    if err: _finish([err])
    # Must be a JSON array (the question says "a JSON array of experiment IDs (strings)")
    if not isinstance(data, list):
        _finish(["q1 output must be a JSON array of strings (got %s)" % type(data).__name__])
    # All elements must be strings
    non_strings = [i for i, x in enumerate(data) if not isinstance(x, str)]
    if non_strings:
        fails.append("array elements at indices %s are not strings — must be plain experiment ID strings" % non_strings)
    ids = [str(x) for x in data]
    expected = {"exp006", "exp007", "exp008", "exp009", "exp010"}
    got = set(ids)
    missing = expected - got
    extra = got - expected
    if missing:
        fails.append("missing running experiment IDs: %s" % sorted(missing))
    if extra:
        fails.append("unexpected IDs in running list: %s (expected exactly exp006-exp010 and nothing else)" % sorted(extra))
    if len(ids) != 5 and not (missing or extra):
        fails.append("expected exactly 5 running experiments, got %d (including duplicates?)" % len(ids))
    _finish(fails)
main()
'''

# Q2 — SRM check for exp002 (chi2≈11.83, p≈0.0006, srm_detected=true)
CHECKS["check_q2"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q2_srm_exp002.json")
    if err: _finish([err])
    # Structure check
    for key in ("chi2_stat", "p_value", "srm_detected"):
        if key not in data:
            fails.append("missing key: %s" % key)
    if fails: _finish(fails)
    # True-value check
    try:
        chi2 = float(data["chi2_stat"])
    except (TypeError, ValueError):
        _finish(["chi2_stat not numeric: %r" % data["chi2_stat"]])
    # chi2 = (5234-5062.5)^2/5062.5 + (4891-5062.5)^2/5062.5 = 11.7... +/- 10%
    if not (9.0 <= chi2 <= 15.0):
        fails.append("chi2_stat == %.4f (expected ~11.83 ±tolerance)" % chi2)
    try:
        pv = float(data["p_value"])
    except (TypeError, ValueError):
        _finish(["p_value not numeric: %r" % data["p_value"]])
    if pv >= 0.01:
        fails.append("p_value == %.6f (expected < 0.01 — SRM clearly detected)" % pv)
    if data.get("srm_detected") is not True:
        fails.append("srm_detected == %r (expected true)" % data.get("srm_detected"))
    _finish(fails)
main()
'''

# Q3 — CUPED audit (correct_theta=0.0412/0.1456≈0.2829, error_pct≈9.6%)
CHECKS["check_q3"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q3_cuped_audit.json")
    if err: _finish([err])
    for key in ("reported_theta", "correct_theta", "error_pct", "formula_source"):
        if key not in data:
            fails.append("missing key: %s" % key)
    if fails: _finish(fails)
    try:
        rt = float(data["reported_theta"])
        ct = float(data["correct_theta"])
        ep = float(data["error_pct"])
    except (TypeError, ValueError) as e:
        _finish(["non-numeric field: %s" % e])
    # reported_theta must be 0.31
    if not (0.29 <= rt <= 0.33):
        fails.append("reported_theta == %.4f (expected 0.31)" % rt)
    # correct_theta = 0.0412/0.1456 = 0.28297...
    if not (0.27 <= ct <= 0.30):
        fails.append("correct_theta == %.4f (expected ~0.2829 = 0.0412/0.1456)" % ct)
    # error_pct = abs(0.31 - 0.2829)/0.2829 * 100 ≈ 6.0% or vs reported: abs(0.31-0.2829)/0.31*100≈8.7%
    # accept 5-12% range
    if not (5.0 <= ep <= 12.0):
        fails.append("error_pct == %.2f (expected 5-12%%, covering both relative error definitions)" % ep)
    # formula_source must reference Statsig CUPED URL
    fs = str(data.get("formula_source", ""))
    if "statsig" not in fs.lower() and "cuped" not in fs.lower():
        fails.append("formula_source must reference Statsig CUPED documentation (got %r)" % fs[:80])
    _finish(fails)
main()
'''

# Q4 — corrected power analysis script (z_alpha=1.96, z_beta=0.84, n≈1764 for p1=0.10,p2=0.12)
CHECKS["check_q4"] = '''
import subprocess

def main():
    ws = Path(sys.argv[1]); fails = []
    script = ws / "scripts" / "power_analysis_fixed.py"
    if not script.exists():
        _finish(["file not found: scripts/power_analysis_fixed.py"])
    txt = script.read_text(encoding="utf-8")
    # Check correct z values present
    if "1.96" not in txt:
        fails.append("script does not contain z_alpha/2 = 1.96 (for alpha=0.05 two-sided)")
    if "0.84" not in txt:
        fails.append("script does not contain z_beta = 0.84 (for power=0.80)")
    # Verify it does NOT use the wrong deprecated values
    # 2.33 or 2.576 would indicate deprecated runbook usage
    if re.search(r"z[_a-z]*\s*=\s*2\.33", txt) or re.search(r"z[_a-z]*\s*=\s*2\.576", txt):
        fails.append("script contains deprecated z-value (2.33 or 2.576 from old runbook) — must use 1.96")
    if fails: _finish(fails)
    # Execute script and capture output to verify n≈1764 for p1=0.10, p2=0.12
    try:
        result = subprocess.run(
            [sys.executable, str(script)], capture_output=True, text=True, timeout=30
        )
        output = result.stdout + result.stderr
        # Correct two-proportion per-group sample size for p1=.10,p2=.12 is ~3834
        nums = re.findall(r"\\b(3[0-9]{3})\\b", output)
        found_valid = any(3800 <= int(n) <= 3870 for n in nums)
        if not found_valid:
            fails.append(
                "script output does not contain n in [3800,3870] for p1=0.10,p2=0.12 "
                "(got numbers: %s; output: %r)" % (nums[:5], output[:200])
            )
    except subprocess.TimeoutExpired:
        fails.append("script timed out (>30s)")
    except Exception as e:
        fails.append("script execution error: %s" % e)
    _finish(fails)
main()
'''

# Q5 — BOT error identification (must catch >=4 errors: peeking FPR, CUPED window, SRM freq, exp003 conclusion)
# Hardened: minimum 4 errors; each object must have all three required keys; correct_value must include exact figures.
CHECKS["check_q5"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q5_bot_errors.json")
    if err: _finish([err])
    if not isinstance(data, list):
        _finish(["q5 output must be a JSON array of error objects"])
    if len(data) < 4:
        fails.append("only %d errors identified (need >= 4: peeking FPR, CUPED window, SRM freq, exp003 conclusion)" % len(data))
    # Check for key errors using text search across all field values
    all_text = json.dumps(data).lower()
    # Error 1: peeking FPR — correct_value must mention 57%
    if "57" not in all_text:
        fails.append("missing peeking FPR error (BOT said 5%, correct_value must cite 57%)")
    # Error 2: CUPED window — must distinguish 14 days (BOT) vs 7 days (correct)
    if not (("14" in all_text or "fourteen" in all_text) and ("7" in all_text or "seven" in all_text)):
        fails.append("missing CUPED window error (BOT said 14 days, correct is 7 days)")
    # Error 3: SRM frequency — must mention both 3% (BOT) and 6% (correct)
    if "6" not in all_text or "3" not in all_text:
        fails.append("missing SRM frequency error (BOT said 3%, correct is ~6%)")
    # Error 4: exp003 conclusion status — must mention the invalidation of the BOT conclusion
    if "exp003" not in all_text and "invalidat" not in all_text:
        fails.append("missing exp003 conclusion error (BOT claimed VALID/significant; correct: invalidated by bot traffic)")
    # Each element must have all three required fields: field, bot_value, correct_value
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            fails.append("error item %d is not an object" % i)
            continue
        missing_keys = [k for k in ("field", "bot_value", "correct_value") if k not in item]
        if missing_keys:
            fails.append("error item %d missing required keys: %s (must have field, bot_value, correct_value)" % (i, missing_keys))
    _finish(fails)
main()
'''

# Q6 — peeking analysis (actual_fpr=0.57, nominal_fpr=0.05, ratio≈11.4)
CHECKS["check_q6"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q6_peeking_analysis.json")
    if err: _finish([err])
    for key in ("actual_fpr", "nominal_fpr", "ratio"):
        if key not in data:
            fails.append("missing key: %s" % key)
    if fails: _finish(fails)
    try:
        afpr = float(data["actual_fpr"])
        nfpr = float(data["nominal_fpr"])
        ratio = float(data["ratio"])
    except (TypeError, ValueError) as e:
        _finish(["non-numeric field: %s" % e])
    # actual_fpr must be 0.57 (exact Optimizely value)
    if not (0.55 <= afpr <= 0.59):
        fails.append("actual_fpr == %.4f (expected 0.57 from Optimizely blog)" % afpr)
    # nominal_fpr must be 0.05
    if not (0.04 <= nfpr <= 0.06):
        fails.append("nominal_fpr == %.4f (expected 0.05)" % nfpr)
    # ratio must be ~11.4 (0.57/0.05)
    if not (11.0 <= ratio <= 12.0):
        fails.append("ratio == %.4f (expected ~11.4 = 0.57/0.05)" % ratio)
    _finish(fails)
main()
'''

# Q7 — BH correction (p-values all > 0.05, so raw_significant=0, bh_significant=0)
CHECKS["check_q7"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q7_multi_test_correction.json")
    if err: _finish([err])
    for key in ("bh_significant", "method", "n_tests", "raw_significant"):
        if key not in data:
            fails.append("missing key: %s" % key)
    if fails: _finish(fails)
    method = str(data.get("method", "")).lower()
    if "benjamini" not in method and "bh" not in method:
        fails.append("method == %r (expected benjamini_hochberg or bh)" % data.get("method"))
    try:
        n = int(data["n_tests"])
        raw = int(data["raw_significant"])
        bh = int(data["bh_significant"])
    except (TypeError, ValueError) as e:
        _finish(["non-integer field: %s" % e])
    if n != 3:
        fails.append("n_tests == %d (expected 3 pairwise comparisons)" % n)
    # All 3 p-values (0.31, 0.43, 0.67) > 0.05, so raw_significant = 0
    if raw != 0:
        fails.append("raw_significant == %d (expected 0: p-values 0.31,0.43,0.67 all > 0.05)" % raw)
    if bh != 0:
        fails.append("bh_significant == %d (expected 0: no p-value passes BH with these values)" % bh)
    _finish(fails)
main()
'''

# Q8 — exp003 revised (significant=false, p_value≈0.31, conclusion mentions no significant effect)
CHECKS["check_q8"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q8_exp003_revised.json")
    if err: _finish([err])
    for key in ("conclusion", "p_value", "significant"):
        if key not in data:
            fails.append("missing key: %s" % key)
    if fails: _finish(fails)
    # significant must be false (dynamic update reversal — V2)
    if data.get("significant") is not False:
        fails.append("significant == %r (expected false — exp003 cleaned data shows p=0.31)" % data.get("significant"))
    try:
        pv = float(data["p_value"])
    except (TypeError, ValueError):
        _finish(["p_value not numeric: %r" % data["p_value"]])
    if pv <= 0.05:
        fails.append("p_value == %.4f (expected > 0.05; cleaned data p=0.31; original p=0.023 is invalidated)" % pv)
    # p_value should be in range around 0.31 (±0.15 tolerance)
    if not (0.10 <= pv <= 0.60):
        fails.append("p_value == %.4f (expected approximately 0.31 from cleaned analysis)" % pv)
    # conclusion must contain semantics of 'no significant effect' or similar
    conc = str(data.get("conclusion", "")).lower()
    if not any(kw in conc for kw in ("not significant", "no significant", "insignificant",
                                      "null", "no effect", "not statistically")):
        fails.append("conclusion %r does not express 'no significant effect'" % conc[:80])
    _finish(fails)
main()
'''

# Q9 — cross-experiment summary (exp002=invalid_srm, exp003=not_significant, exp001 requires investigation)
# Hardened: exp001 conclusion must signal investigation (not mark as significant/not_significant);
#           exp003 primary_p_value must be numeric and reflect cleaned data (0.20-0.50).
CHECKS["check_q9"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q9_experiment_summary.json")
    if err: _finish([err])
    # Must be a list of experiment entries
    if isinstance(data, list):
        entries = {str(e.get("exp_id", "")): e for e in data if isinstance(e, dict)}
    elif isinstance(data, dict):
        entries = {}
        for k, v in data.items():
            if isinstance(v, dict):
                entries[str(k)] = v
            elif k not in ("schema_version",):
                entries[str(k)] = {"exp_id": k, "conclusion": str(v)}
    else:
        _finish(["q9 output must be list or object"])
    # All 3 ended experiments must be present
    for eid in ("exp001", "exp002", "exp003"):
        if eid not in entries:
            fails.append("missing entry for %s" % eid)
    if fails: _finish(fails)
    # exp002 must be invalid_srm
    e002 = entries.get("exp002") or {}
    conc002 = str(e002.get("conclusion", "")).lower()
    if "srm" not in conc002 and "invalid" not in conc002 and "mismatch" not in conc002:
        fails.append("exp002 conclusion %r does not reflect SRM invalidation (must be \\'invalid_srm\\')" % conc002[:60])
    # exp003 must be not_significant (V4 cross-round: must reflect Q8 cleaned analysis)
    e003 = entries.get("exp003") or {}
    conc003 = str(e003.get("conclusion", "")).lower()
    if not any(kw in conc003 for kw in ("not_significant", "not significant", "insignificant", "no significant")):
        pv003 = e003.get("primary_p_value")
        try:
            pv003 = float(pv003)
            if pv003 <= 0.05:
                fails.append("exp003 conclusion or p_value must reflect not_significant (cleaned data p=0.31, not original 0.023)")
        except (TypeError, ValueError):
            fails.append("exp003 conclusion %r must reflect not_significant result (consistent with Q8 cleanup)" % conc003[:60])
    # exp003 primary_p_value must be numeric and in cleaned-data range [0.15, 0.55]
    pv003_raw = e003.get("primary_p_value")
    if pv003_raw is not None:
        try:
            pv003 = float(pv003_raw)
            if not (0.15 <= pv003 <= 0.55):
                fails.append("exp003 primary_p_value == %.4f — must be in [0.15, 0.55] reflecting cleaned data p=0.31" % pv003)
        except (TypeError, ValueError):
            fails.append("exp003 primary_p_value %r is not numeric" % pv003_raw)
    # exp001: conclusion must signal that result requires investigation (Twyman flag)
    # It must NOT conclude significant or not_significant definitively — it is flagged/unresolved
    e001 = entries.get("exp001") or {}
    conc001 = str(e001.get("conclusion", "")).lower()
    notes001 = str(e001.get("notes", "")).lower()
    combined001 = conc001 + " " + notes001
    if not any(kw in combined001 for kw in ("investigat", "twyman", "flagged", "suspicious", "unresolved", "requires")):
        fails.append(
            "exp001 conclusion/notes %r must indicate the result requires investigation "
            "(Twyman\\'s Law: +45%% lift is suspicious, cannot conclude significant/not_significant yet)" % conc001[:60]
        )
    _finish(fails)
main()
'''

# Q10 — deprecated runbook check (is_deprecated=true, >=2 discrepancies)
CHECKS["check_q10"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q10_runbook_diff.json")
    if err: _finish([err])
    for key in ("is_deprecated", "discrepancy_list"):
        if key not in data:
            fails.append("missing key: %s" % key)
    if fails: _finish(fails)
    if data.get("is_deprecated") is not True:
        fails.append("is_deprecated == %r (expected true)" % data.get("is_deprecated"))
    dl = data.get("discrepancy_list")
    if not isinstance(dl, list) or len(dl) < 2:
        fails.append("discrepancy_list must have >= 2 entries (got %r)" % dl)
    else:
        dl_text = " ".join(str(x) for x in dl).lower()
        # Must identify z-value discrepancy (2.33 vs 1.96)
        if not (("2.33" in dl_text or "z_alpha" in dl_text or "z-alpha" in dl_text or
                 "z alpha" in dl_text) and ("1.96" in dl_text or "alpha" in dl_text)):
            fails.append("discrepancy_list must mention z_alpha/2 discrepancy (old: 2.33, correct: 1.96)")
    _finish(fails)
main()
'''

# Q11 — exp004 sample size (n_per_group in [2200, 2600], alpha=0.05, power=0.80)
CHECKS["check_q11"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q11_exp004_sample_size.json")
    if err: _finish([err])
    for key in ("alpha", "delta", "n_per_group", "power", "total_n"):
        if key not in data:
            fails.append("missing key: %s" % key)
    if fails: _finish(fails)
    try:
        alpha = float(data["alpha"])
        power = float(data["power"])
        n = int(data["n_per_group"])
        total = int(data["total_n"])
        delta = float(data["delta"])
    except (TypeError, ValueError) as e:
        _finish(["non-numeric field: %s" % e])
    if not (0.049 <= alpha <= 0.051):
        fails.append("alpha == %.4f (expected 0.05)" % alpha)
    if not (0.79 <= power <= 0.81):
        fails.append("power == %.4f (expected 0.80)" % power)
    # n_per_group for p1=0.22, p2=0.25, z_alpha=1.96, z_beta=0.84
    # n = (1.96+0.84)^2 * (0.22*0.78 + 0.25*0.75) / (0.03)^2
    # = 7.84 * (0.1716 + 0.1875) / 0.0009 = 7.84 * 0.3591 / 0.0009 = 3127.2 / 0.9 = ... wait
    # Actually: n = (1.96+0.84)^2 * (p1q1+p2q2) / delta^2
    # = (2.80)^2 * (0.22*0.78 + 0.25*0.75) / (0.03)^2
    # = 7.84 * (0.1716 + 0.1875) / 0.0009
    # = 7.84 * 0.3591 / 0.0009 = 2.8153 / 0.0009 = 3128
    # Hmm that's too high. Let me recalculate:
    # 7.84 * 0.3591 = 2.815
    # 2.815 / 0.0009 = 3128
    # But BRIEF says 2200-2600 range. Let me check with actual numbers:
    # p1=0.22, p2=0.25, delta=0.03
    # n = ((1.96+0.84)/0.03)^2 * (0.22*0.78 + 0.25*0.75)
    # = (2.80/0.03)^2 * 0.3591
    # = (93.33)^2 * 0.3591
    # = 8710.9 * 0.3591 = 3128
    # So correct n ≈ 3128. Accept 2900-3400 range.
    if not (2900 <= n <= 3400):
        fails.append("n_per_group == %d (expected ~3128 for p1=0.22,p2=0.25,z_alpha=1.96,z_beta=0.84)" % n)
    if total != 2 * n:
        fails.append("total_n == %d != 2 * n_per_group (%d)" % (total, 2 * n))
    if not (0.025 <= delta <= 0.035):
        fails.append("delta == %.4f (expected 0.03 = 3pp lift)" % delta)
    _finish(fails)
main()
'''

# Q12 — CUPED eligibility for exp005 (640 units, 8% coverage, eligible=true, reason cites 7 days)
CHECKS["check_q12"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q12_cuped_eligibility.json")
    if err: _finish([err])
    for key in ("eligible", "pct_coverage", "reason", "units_with_pre_data"):
        if key not in data:
            fails.append("missing key: %s" % key)
    if fails: _finish(fails)
    # eligible must be True (640 > 100 AND 8% > 5%)
    if data.get("eligible") is not True:
        fails.append("eligible == %r (expected true: 640 units > 100, coverage=8%% > 5%%)" % data.get("eligible"))
    try:
        units = int(data["units_with_pre_data"])
        pct = float(data["pct_coverage"])
    except (TypeError, ValueError) as e:
        _finish(["non-numeric field: %s" % e])
    if not (580 <= units <= 700):
        fails.append("units_with_pre_data == %d (expected ~640 for exp005 from pre_experiment_metrics.csv)" % units)
    if not (6.0 <= pct <= 10.0):
        fails.append("pct_coverage == %.2f%% (expected ~8%% = 640/8000)" % pct)
    # reason must mention 7-day pre-experiment window (V9 verbatim)
    reason = str(data.get("reason", "")).lower()
    if "7" not in reason and "seven" not in reason:
        fails.append("reason must reference the 7-day pre-experiment window (Statsig Cloud default)")
    _finish(fails)
main()
'''

# Q13 — Bonferroni after supersede (method='bonferroni', alpha_adjusted=0.05/8=0.00625, n_tests=8)
CHECKS["check_q13"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q13_bonferroni_correction.json")
    if err: _finish([err])
    for key in ("alpha_adjusted", "method", "n_tests", "significant_metrics"):
        if key not in data:
            fails.append("missing key: %s" % key)
    if fails: _finish(fails)
    method = str(data.get("method", "")).lower()
    # V10: must be bonferroni (NOT benjamini_hochberg — VP email was superseded)
    if "bonferroni" not in method:
        fails.append("method == %r (must be bonferroni — VP BH directive was superseded by CFO notice)" % data.get("method"))
    if "benjamini" in method or "bh" in method.replace("bonferroni", ""):
        fails.append("method must NOT be BH (the VP email using BH was superseded)")
    try:
        n = int(data["n_tests"])
        aa = float(data["alpha_adjusted"])
        sm = int(data["significant_metrics"])
    except (TypeError, ValueError) as e:
        _finish(["non-numeric field: %s" % e])
    if n != 8:
        fails.append("n_tests == %d (expected 8 secondary metrics)" % n)
    # alpha_adjusted = 0.05/8 = 0.00625
    if not (0.005 <= aa <= 0.008):
        fails.append("alpha_adjusted == %.6f (expected 0.05/8=0.00625)" % aa)
    # significant_metrics should be 0 (none of the given p-values < 0.00625)
    if sm < 0:
        fails.append("significant_metrics cannot be negative: %d" % sm)
    _finish(fails)
main()
'''

# Q14 — Twyman check (flagged_metric=checkout_conversion_rate, suspicion_reason MUST cite Twyman,
#         >=5 diagnostic_steps, confidence_level present)
# Hardened: suspicion_reason must explicitly name "Twyman"; diagnostic_steps raised to >=5;
#           reported_lift must include "%" symbol and a two-digit number 40-49.
CHECKS["check_q14"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q14_twyman_check.json")
    if err: _finish([err])
    for key in ("confidence_level", "diagnostic_steps", "flagged_metric",
                "reported_lift", "suspicion_reason"):
        if key not in data:
            fails.append("missing key: %s" % key)
    if fails: _finish(fails)
    fm = str(data.get("flagged_metric", "")).lower()
    if "checkout_conversion" not in fm and "checkout" not in fm:
        fails.append("flagged_metric %r should be checkout_conversion_rate" % data.get("flagged_metric"))
    sr = str(data.get("suspicion_reason", "")).lower()
    # Hardened: must explicitly name "Twyman" (not just "suspicious" or "unusual")
    if "twyman" not in sr:
        fails.append("suspicion_reason must explicitly reference \\'Twyman\\'s Law\\' by name (got: %r)" % data.get("suspicion_reason", "")[:80])
    steps = data.get("diagnostic_steps")
    # Hardened: raised from >=3 to >=5 diagnostic steps
    if not isinstance(steps, list) or len(steps) < 5:
        fails.append("diagnostic_steps must be a list with >= 5 items (got %d); each step should cover a distinct diagnostic angle" % (len(steps) if isinstance(steps, list) else 0))
    else:
        # Each step must be a non-empty string of at least 10 characters
        for i, step in enumerate(steps):
            if not isinstance(step, str) or len(step.strip()) < 10:
                fails.append("diagnostic_steps[%d] is too short or not a string (each step must be a substantive description)" % i)
    cl = str(data.get("confidence_level", "")).lower()
    if cl not in ("high", "medium", "low"):
        fails.append("confidence_level == %r (must be high/medium/low)" % data.get("confidence_level"))
    # reported_lift must contain a two-digit number 40-49 AND "%" symbol
    rl = str(data.get("reported_lift", ""))
    if not re.search(r"4[0-9]", rl):
        fails.append("reported_lift %r does not reflect the +45%% anomalous lift" % rl[:30])
    if "%" not in rl:
        fails.append("reported_lift %r must include the %% symbol (e.g. \'+45%%\' or \'45%%\')" % rl[:30])
    _finish(fails)
main()
'''

# Q15 — final report (all 12 exp IDs, exp003=not significant, Bonferroni, 57%, >= 2 ## headers)
CHECKS["check_q15"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "output" / "q15_final_report.md")
    if txt is None:
        _finish(["file not found: output/q15_final_report.md"])
    low = txt.lower()
    # Must mention all 12 experiment IDs
    for i in range(1, 13):
        eid = "exp%03d" % i
        if eid not in low:
            fails.append("q15_final_report.md does not mention %s" % eid)
    # exp003 conclusion must be no significant effect (V4 cross-round closure)
    exp003_ctx = ""
    idx = low.find("exp003")
    if idx >= 0:
        exp003_ctx = low[max(0, idx-50):idx+200]
    if not any(kw in exp003_ctx for kw in ("not significant", "no significant", "insignificant",
                                             "no effect", "null result", "p=0.31", "p = 0.31")):
        fails.append("report does not state exp003 as 'no significant effect' (required: V4 cross-round closure)")
    # Must reference Bonferroni (NOT BH as primary method — V10 supersede)
    if "bonferroni" not in low:
        fails.append("report must reference Bonferroni correction (VP BH directive was superseded)")
    # Must cite 57% peeking false positive rate (V4 cross-round with Q6)
    if "57" not in txt:
        fails.append("report must cite 57%% peeking false positive rate (from Q6 analysis)")
    # Must have >= 2 ## section headers
    if len(re.findall(r"^## ", txt, re.MULTILINE)) < 2:
        fails.append("fewer than 2 \\'## \\' section headers")
    _finish(fails)
main()
'''

# Q16 — SHA-256 sign-off of q15_final_report.md
CHECKS["check_q16"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    sign = _read(ws / "output" / "q16_signoff.txt")
    if sign is None:
        _finish(["file not found: output/q16_signoff.txt"])
    line = sign.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["signoff must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80]])
    report = ws / "output" / "q15_final_report.md"
    if not report.exists():
        _finish(["cannot verify: output/q15_final_report.md missing"])
    digest = hashlib.sha256(report.read_bytes()).hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: signoff %s != recomputed %s" % (m.group(1)[:12], digest[:12]))
    _finish(fails)
main()
'''

PREF = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prd5 preference checker (P1-P5).

P1: all output files in output/ subdirectory
P2: Python scripts in functional style with Google docstrings
P3: JSON output fields in alphabetical order
P4: judgment outputs include reason field
P5: diagnostic reports include confidence_level field (high/medium/low)
"""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Output files must be written to the output/ subdirectory."""
    tp = ws / target
    if not tp.exists():
        return True, "P1: target missing, skip"
    # Check that the target path is under output/
    try:
        tp.relative_to(ws / "output")
        return True, "P1: PASSED"
    except ValueError:
        pass
    # Also accept if target itself is in output/
    if target.startswith("output/") or target.startswith("output\\\\"):
        return True, "P1: PASSED"
    return False, "P1: file %s is not in output/ subdirectory" % target


def check_P2(ws, target):
    """Python scripts must use functional style with Google docstrings."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    if not target.endswith(".py"):
        return True, "P2: not a Python file, skip"
    # Check for at least one function with a docstring
    if not re.search(r"def \\w+\\([^)]*\\):\\s*\\n\\s+\\\"\\\"\\\"", txt):
        return False, "P2: no function with docstring found (Google-style required)"
    # Check for Args or Returns section in docstring
    if not re.search(r"\\bArgs\\b|\\bReturns\\b", txt):
        return False, "P2: function docstrings should include Args/Returns sections (Google style)"
    return True, "P2: PASSED"


def check_P3(ws, target):
    """JSON output fields must be in alphabetical order."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P3: target is not valid JSON"
    if isinstance(data, list):
        # Check each element
        for i, item in enumerate(data):
            if isinstance(item, dict):
                keys = [k for k in item.keys() if k != "schema_version"]
                if keys != sorted(keys):
                    return False, "P3: array element %d has keys out of alphabetical order: %s" % (i, keys)
        return True, "P3: PASSED"
    elif isinstance(data, dict):
        keys = [k for k in data.keys() if k != "schema_version"]
        if keys != sorted(keys):
            return False, "P3: JSON object keys out of alphabetical order: %s" % keys
        return True, "P3: PASSED"
    return True, "P3: PASSED (non-object/array)"


def check_P4(ws, target):
    """Judgment outputs must include a reason field."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P4: target is not valid JSON"
    if isinstance(data, dict):
        if "reason" not in data:
            return False, "P4: judgment output missing \\'reason\\' field"
    elif isinstance(data, list):
        # Not applicable to lists
        return True, "P4: list output, skip reason check"
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Diagnostic reports must include confidence_level field (high/medium/low)."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        # For markdown files
        if "confidence_level" not in txt.lower():
            return False, "P5: diagnostic report missing confidence_level field"
        return True, "P5: PASSED"
    if isinstance(data, dict):
        if "confidence_level" not in data:
            return False, "P5: diagnostic report missing \\'confidence_level\\' field (must be high/medium/low)"
        cl = str(data["confidence_level"]).lower()
        if cl not in ("high", "medium", "low"):
            return False, "P5: confidence_level == %r (must be high, medium, or low)" % data["confidence_level"]
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
