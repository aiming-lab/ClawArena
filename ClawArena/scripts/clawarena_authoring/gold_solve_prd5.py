#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gold_solve_prd5.py — prd5 可解性审计（金标自检）。

在 workspace 的临时副本上模拟 update 生效后的状态，写出每一轮的「正确产物」，
然后运行全部 check_qN.py + check_preferences.py，断言正解全部 PASS。
再做一组反例（错误产物）抽样，断言 check 能 FAIL（不过松）。

运行：python scripts/clawarena_authoring/gold_solve_prd5.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DS = REPO / "data" / "clawarena-real"
WS_SRC = DS / "openclaw" / "workspaces" / "prd5"
UPD = DS / "openclaw" / "updates" / "prd5"
SCRIPTS = DS / "eval" / "prd5" / "scripts"
GOLD = Path("/home/xkaiwen/.claude/jobs/579de28f/tmp/prd5_gold_ws")


def prep_workspace() -> Path:
    if GOLD.exists():
        shutil.rmtree(GOLD)
    shutil.copytree(WS_SRC, GOLD)
    # Apply update1 workspace files
    (GOLD / "experiments" / "exp003_pricing_page").mkdir(parents=True, exist_ok=True)
    shutil.copy(
        UPD / "upd1_workspace" / "results_raw_v2.csv",
        GOLD / "experiments" / "exp003_pricing_page" / "results_raw_v2.csv"
    )
    shutil.copy(
        UPD / "upd1_workspace" / "exp003_bot_audit_log.csv",
        GOLD / "experiments" / "exp003_pricing_page" / "exp003_bot_audit_log.csv"
    )
    shutil.copy(
        UPD / "upd1_workspace" / "analysis_report_FINAL_v2.md",
        GOLD / "experiments" / "exp003_pricing_page" / "analysis_report_FINAL_v2.md"
    )
    # Apply update2 workspace files
    (GOLD / "data").mkdir(parents=True, exist_ok=True)
    shutil.copy(
        UPD / "upd2_workspace" / "q4_segment_analysis.csv",
        GOLD / "data" / "q4_segment_analysis.csv"
    )
    (GOLD / "docs").mkdir(parents=True, exist_ok=True)
    shutil.copy(
        UPD / "upd2_workspace" / "correction_notice_20231115.md",
        GOLD / "docs" / "correction_notice_20231115.md"
    )
    return GOLD


def _w(p: Path, t: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8")


def _wj(p: Path, o) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _sorted_json(o: dict) -> dict:
    """Return a new dict with top-level keys sorted alphabetically (P3)."""
    return {k: o[k] for k in sorted(o.keys())}


def count_exp005_units(ws: Path) -> int:
    """Count users with pre-experiment data for exp005 in pre_experiment_metrics.csv."""
    csv_path = ws / "data" / "pre_experiment_metrics.csv"
    count = 0
    with csv_path.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            if row.get("experiment_id") == "exp005":
                count += 1
    return count


def count_total_users(ws: Path) -> int:
    """Count total users in user_segments.csv."""
    csv_path = ws / "data" / "user_segments.csv"
    count = 0
    with csv_path.open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for _ in reader:
            count += 1
    return count


PY_HEADER = "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\n"

DOCSTRING_SAMPLE_SIZE = '''"""Corrected sample size calculator for two-proportion z-test.

Uses correct z-values from docs/stats_methodology.md:
  z_alpha/2 = 1.96 (alpha=0.05, two-sided)
  z_beta    = 0.84 (power=0.80)

Reference: https://en.wikipedia.org/wiki/Two-proportion_Z-test
"""
import math


def calculate_sample_size(p1: float, p2: float, alpha: float = 0.05, power: float = 0.80) -> int:
    """Calculate required sample size per group for two-proportion z-test.

    Args:
        p1: Baseline conversion rate.
        p2: Expected conversion rate under treatment.
        alpha: Significance level (default 0.05, two-sided).
        power: Statistical power (default 0.80).

    Returns:
        Sample size per group (rounded up to nearest integer).
    """
    z_alpha_half = 1.96   # Correct z for alpha=0.05 two-sided (NOT 2.33 from deprecated runbook)
    z_beta = 0.84         # Correct z for power=0.80 (NOT 1.04 from deprecated runbook)
    numerator = (z_alpha_half + z_beta) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2))
    denominator = (p1 - p2) ** 2
    return math.ceil(numerator / denominator)


def main():
    """Run the corrected sample size calculation.

    Returns:
        None: Prints results to stdout.
    """
    # Standard test case: p1=0.10, p2=0.12 -> should give n≈1764
    n_standard = calculate_sample_size(p1=0.10, p2=0.12, alpha=0.05, power=0.80)
    print(f"p1=0.10, p2=0.12, alpha=0.05, power=0.80 -> n={n_standard} per group")

    # exp004: p1=0.22, p2=0.25
    n_exp004 = calculate_sample_size(p1=0.22, p2=0.25, alpha=0.05, power=0.80)
    print(f"p1=0.22, p2=0.25, alpha=0.05, power=0.80 -> n={n_exp004} per group")


if __name__ == "__main__":
    main()
'''


def solve(ws: Path) -> None:
    out = ws / "output"
    out.mkdir(exist_ok=True)
    (ws / "scripts").mkdir(exist_ok=True)

    # ---- Q1: running experiments (exp006-exp010) ----
    _wj(out / "q1_running_experiments.json",
        ["exp006", "exp007", "exp008", "exp009", "exp010"])

    # ---- Q2: SRM check for exp002 ----
    # chi2 = (5234-5062.5)^2/5062.5 + (4891-5062.5)^2/5062.5
    total = 5234 + 4891
    expected = total / 2
    chi2 = (5234 - expected) ** 2 / expected + (4891 - expected) ** 2 / expected
    # p-value approximation for df=1 (chi2≈11.83)
    import math as _m
    from math import erfc, sqrt
    pv = erfc(sqrt(chi2 / 2))
    _wj(out / "q2_srm_exp002.json", _sorted_json({
        "chi2_stat": round(chi2, 4),
        "degrees_of_freedom": 1,
        "p_value": round(pv, 6),
        "source": "Statsig SRM Checks (https://docs.statsig.com/stats-engine/methodologies/srm-checks)",
        "srm_detected": True,
        "threshold_used": 0.01,
    }))

    # ---- Q3: CUPED audit ----
    cov_yx = 0.0412
    var_x = 0.1456
    correct_theta = round(cov_yx / var_x, 4)
    reported_theta = 0.31
    error_pct = round(abs(reported_theta - correct_theta) / correct_theta * 100, 2)
    _wj(out / "q3_cuped_audit.json", _sorted_json({
        "correct_theta": correct_theta,
        "error_pct": error_pct,
        "formula_source": "https://docs.statsig.com/stats-engine/methodologies/cuped",
        "reported_theta": reported_theta,
    }))

    # ---- Q4: corrected power analysis script ----
    _w(ws / "scripts" / "power_analysis_fixed.py", PY_HEADER + DOCSTRING_SAMPLE_SIZE)

    # ---- Q5: BOT errors ----
    bot_errors = [
        _sorted_json({
            "bot_value": "5%",
            "correct_value": "57%",
            "field": "peeking_false_positive_rate_every_visitor",
        }),
        _sorted_json({
            "bot_value": "14 days",
            "correct_value": "7 days",
            "field": "cuped_pre_experiment_window",
        }),
        _sorted_json({
            "bot_value": "3% of experiments",
            "correct_value": "~6% of experiments (Microsoft & Booking.com research)",
            "field": "srm_industry_frequency",
        }),
        _sorted_json({
            "bot_value": "VALID (original conclusion stands)",
            "correct_value": "INVALIDATED by bot traffic contamination; p=0.31 (not significant)",
            "field": "exp003_conclusion_status",
        }),
    ]
    _wj(out / "q5_bot_errors.json", bot_errors)

    # ---- Q6: peeking analysis ----
    _wj(out / "q6_peeking_analysis.json", _sorted_json({
        "actual_fpr": 0.57,
        "nominal_fpr": 0.05,
        "ratio": round(0.57 / 0.05, 2),
        "source": "https://www.optimizely.com/insights/blog/statistics-for-the-internet-age-the-story-behind-optimizelys-new-stats-engine/",
    }))

    # ---- Q7: BH correction on 3 p-values (all > 0.05, so raw_significant=0, bh_significant=0) ----
    p_values = [0.31, 0.43, 0.67]
    raw_sig = sum(1 for p in p_values if p < 0.05)
    # BH: sort, check p[i] <= alpha * (i+1) / k
    k = len(p_values)
    bh_sig = 0
    for i, p in enumerate(sorted(p_values)):
        if p <= 0.05 * (i + 1) / k:
            bh_sig += 1
    _wj(out / "q7_multi_test_correction.json", _sorted_json({
        "bh_significant": bh_sig,
        "method": "benjamini_hochberg",
        "n_tests": k,
        "p_values_tested": p_values,
        "raw_significant": raw_sig,
    }))

    # ---- Q8: exp003 revised (after update1) ----
    _wj(out / "q8_exp003_revised.json", _sorted_json({
        "conclusion": "No significant effect. Original p=0.023 was a false positive caused by 12% bot traffic contamination in the control group. Post-cleanup p=0.31 (not significant at alpha=0.05).",
        "data_version": "v2 (bot traffic removed)",
        "p_value": 0.31,
        "significant": False,
    }))

    # ---- Q9: cross-experiment summary ----
    summary_list = [
        _sorted_json({
            "conclusion": "requires_investigation",
            "exp_id": "exp001",
            "notes": "SRM check passed (no SRM detected). However, +45% lift on checkout_conversion_rate flagged by Twyman's Law as implausible for a button color change. Requires systematic diagnostic investigation (tracking audit, novelty effect, peeking check) before any rollout decision.",
            "primary_p_value": 0.00001,
        }),
        _sorted_json({
            "conclusion": "invalid_srm",
            "exp_id": "exp002",
            "notes": "SRM detected (chi2=11.83, p=0.0006 < 0.01 Statsig threshold). Results are unreliable. CUPED theta also misconfigured.",
            "primary_p_value": None,
        }),
        _sorted_json({
            "conclusion": "not_significant",
            "exp_id": "exp003",
            "notes": "Original FINAL report conclusion (significant_positive, p=0.023) invalidated by 12% bot traffic in control group. Cleaned data: p=0.31 (not significant).",
            "primary_p_value": 0.31,
        }),
    ]
    _wj(out / "q9_experiment_summary.json", summary_list)

    # ---- Q10: deprecated runbook diff ----
    _wj(out / "q10_runbook_diff.json", _sorted_json({
        "discrepancy_list": [
            "z_alpha/2: deprecated runbook uses 2.33 (alpha=0.02, two-sided), current runbook uses 1.96 (alpha=0.05, two-sided)",
            "z_beta: deprecated runbook uses 1.04 (power~84%), current runbook uses 0.84 (power=80%)",
            "SRM threshold: deprecated runbook uses p<0.05, current standard is p<0.01 (Statsig) or p<0.0005 (Microsoft ExP)",
            "CUPED pre-experiment window: deprecated runbook uses 14 days, correct is 7 days (Statsig Cloud default)",
        ],
        "is_deprecated": True,
        "source": "docs/DEPRECATED_old_runbook_v1.md",
    }))

    # ---- Q11: exp004 sample size ----
    p1, p2 = 0.22, 0.25
    z_a = 1.96
    z_b = 0.84
    n_exp004 = math.ceil((z_a + z_b) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / (p2 - p1) ** 2)
    _wj(out / "q11_exp004_sample_size.json", _sorted_json({
        "alpha": 0.05,
        "delta": round(p2 - p1, 4),
        "n_per_group": n_exp004,
        "power": 0.80,
        "total_n": 2 * n_exp004,
    }))

    # ---- Q12: CUPED eligibility for exp005 ----
    units = count_exp005_units(ws)
    total_users = count_total_users(ws)
    pct = round(100.0 * units / max(total_users, 1), 4)
    eligible = units > 100 and pct > 5.0
    _wj(out / "q12_cuped_eligibility.json", _sorted_json({
        "eligible": eligible,
        "pct_coverage": pct,
        "reason": (
            f"Eligible: {units} units have pre-experiment data ({pct:.2f}% coverage of {total_users} total users). "
            f"Both Statsig activation conditions satisfied: units_with_pre_data > 100 ({units} > 100) "
            f"and coverage > 5% ({pct:.2f}% > 5%). "
            f"Pre-experiment window: 7 days prior to first exposure (Statsig Cloud default). "
            f"Source: https://docs.statsig.com/stats-engine/methodologies/cuped"
        ),
        "units_with_pre_data": units,
    }))

    # ---- Q13: Bonferroni after supersede (update2: VP BH directive superseded) ----
    p_secondary = [0.031, 0.042, 0.078, 0.112, 0.198, 0.234, 0.301, 0.445]
    k_secondary = len(p_secondary)
    alpha_adj = round(0.05 / k_secondary, 6)
    sig_metrics = sum(1 for p in p_secondary if p < alpha_adj)
    _wj(out / "q13_bonferroni_correction.json", _sorted_json({
        "alpha_adjusted": alpha_adj,
        "method": "bonferroni",
        "n_tests": k_secondary,
        "reason": (
            "Bonferroni correction applied per correction_notice_20231115.md (CFO Office). "
            "The VP Marketing email of 2023-11-01 requesting BH correction was SUPERSEDED — "
            "it was misaddressed and intended for another project. "
            "Company default (docs/stats_methodology.md Section 7) is Bonferroni. "
            "alpha_adjusted = 0.05 / 8 = 0.00625."
        ),
        "significant_metrics": sig_metrics,
    }))

    # ---- Q14: Twyman check on exp001 ----
    _wj(out / "q14_twyman_check.json", _sorted_json({
        "confidence_level": "high",
        "diagnostic_steps": [
            "1. Verify event tracking implementation for checkout_conversion_rate metric — check for double-counting or misconfigured funnel events",
            "2. Audit experiment assignment logic — confirm users are not double-counted across control and treatment",
            "3. Check for novelty effect: inspect daily time-series to see if lift inflates early then decays",
            "4. Verify SRM (Sample Ratio Mismatch) was not present for exp001",
            "5. Review peeking protocol — experiment was monitored daily; check if early significance was observed and acted upon",
        ],
        "flagged_metric": "checkout_conversion_rate",
        "reason": (
            "Per Twyman's Law ('Any figure that looks interesting or different is usually wrong'), "
            "a +45% lift on checkout_conversion_rate for a button color change is implausible. "
            "Historical experiments show 2-8% lift for UX changes. This magnitude warrants "
            "systematic diagnostic investigation before any rollout decision."
        ),
        "reported_lift": "+45% (control: 8.2%, treatment: 11.9%)",
        "suspicion_reason": (
            "Twyman's Law: The +45% relative lift on checkout_conversion_rate is 5-20x larger "
            "than typical UX experiment results. Such dramatic improvements from a button color "
            "change are almost always attributable to measurement error, tracking bugs, "
            "SRM, or novelty effects rather than genuine causal effects."
        ),
    }))

    # ---- Q15: comprehensive final report ----
    report = _build_final_report()
    _w(out / "q15_final_report.md", report)

    # ---- Q16: SHA-256 sign-off of q15_final_report.md ----
    digest = hashlib.sha256((out / "q15_final_report.md").read_bytes()).hexdigest()
    _w(out / "q16_signoff.txt", f"VERIFIED:{digest}\n")

    print("  [solve] all outputs written to", out)


def _build_final_report() -> str:
    return """# GrowthCo Q3 A/B Experiment Quality Review — Final Report

**Date**: 2023-11-16
**Prepared by**: GrowthAnalytics AI
**Reviewed by**: Data Science Team

## Executive Summary

This report presents the comprehensive quality review of GrowthCo's Q3 A/B experiment program,
covering 12 experiments (exp001 through exp012): 3 ended, 5 running, and 4 pending.
Multiple statistical methodology issues were identified and corrected.

Key findings:
- **Peeking problem**: Continuous monitoring inflates false positive rate to **57%** vs nominal 5%
  (Optimizely Stats Engine research)
- **SRM detected**: exp002 exhibits Sample Ratio Mismatch (chi2=11.83, p=0.0006 < 0.01 threshold)
- **exp003 conclusion reversed**: Original significant positive result (p=0.023) invalidated by
  12% bot traffic in control group; cleaned analysis shows **no significant effect (p=0.31)**
- **Multiple comparison**: All analyses use **Bonferroni** correction per company standard

## Experiment Status

### Ended Experiments

**exp001 — Checkout CTA Button Color**
- Primary metric: checkout_conversion_rate
- Reported result: +45% lift (control: 8.2%, treatment: 11.9%)
- Status: FLAGGED — Twyman's Law triggered. A +45% lift from a button color change is implausible
  and requires diagnostic investigation before any rollout decision.

**exp002 — Onboarding Flow Redesign**
- Primary metric: activation_rate
- Status: INVALID — SRM detected (control: 5234, treatment: 4891, p=0.0006 < 0.01)
- Additional issue: CUPED theta was manually set (0.31) vs. correctly computed (θ = Cov(Y,X)/Var(X) = 0.2829)
- Action required: Investigate SRM root cause before re-running

**exp003 — Pricing Page Layout**
- Primary metric: paid_conversion_rate
- Original conclusion: SIGNIFICANT POSITIVE (p=0.023) — NOW INVALIDATED
- Corrected conclusion: **NO SIGNIFICANT EFFECT (p=0.31)** after removing 12% bot traffic from control group
- Bot traffic audit: 1,828 users flagged and removed from control group
- Multiple comparison: Bonferroni correction applied (alpha/24 = 0.00208); no secondary metric significant

### Running Experiments

| Experiment | ID | Start Date | Primary Metric |
|---|---|---|---|
| Homepage Hero Banner A/B | exp006 | 2023-10-15 | homepage_ctr |
| Search Autocomplete Enhancement | exp007 | 2023-10-20 | search_to_purchase_rate |
| Notification Timing Optimization | exp008 | 2023-10-22 | notification_open_rate |
| Mobile Checkout Flow Simplification | exp009 | 2023-10-25 | mobile_checkout_completion |
| Referral Program UI Update | exp010 | 2023-10-28 | referral_invite_sent_rate |

### Pending Experiments

| Experiment | ID | Status |
|---|---|---|
| Email Subject Line Optimization | exp004 | Awaiting launch (sample size: 3,129/group) |
| Dashboard Widget Personalization | exp005 | CUPED eligible (640 units, 8% coverage) |
| Plan Upgrade Prompt Positioning | exp011 | Design phase |
| Trial Expiry Email Sequence | exp012 | Design phase |

## Statistical Methodology Corrections

### Peeking (Multiple Testing Over Time)
Per Optimizely Stats Engine (https://www.optimizely.com/insights/blog/statistics-for-the-internet-age-the-story-behind-optimizelys-new-stats-engine/):
- Checking after every visitor: **57% actual false positive rate** (vs nominal 5%)
- Checking every 500 visitors: **26% actual false positive rate**
- exp001 was monitored daily without pre-specified stopping rules — results require validation

### Sample Size Calculator Correction
The deprecated runbook (docs/DEPRECATED_old_runbook_v1.md) uses incorrect z-values:
- Old (WRONG): z_alpha/2=2.33, z_beta=1.04
- Correct: **z_alpha/2=1.96** (alpha=0.05), **z_beta=0.84** (power=0.80)

exp004 sample size: n = (1.96+0.84)^2 × [0.22×0.78 + 0.25×0.75] / 0.03^2 = **3,129 per group**

### Multiple Comparison Correction
All secondary metric analyses use **Bonferroni correction** per company standard (docs/stats_methodology.md).
Note: A VP Marketing email dated 2023-11-01 requesting Benjamini-Hochberg correction was SUPERSEDED
by CFO Office correction notice dated 2023-11-15 (the VP email was misaddressed).

## CUPED Eligibility

exp005 (Dashboard Widget Personalization):
- Units with pre-experiment data: 640 (Statsig threshold: >100) ✓
- Coverage: 8.0% of 8,000 users (Statsig threshold: >5%) ✓
- Pre-experiment window: 7 days prior to exposure (Statsig Cloud default) ✓
- **Eligible for CUPED**: YES
- theta formula: θ = Cov(Y, X) / Var(X) (Statsig implementation)

## Conclusion

The Q3 experiment program revealed systematic statistical methodology issues that require
process improvements. Key actions:
1. Enforce pre-specified stopping rules to eliminate peeking (57% FPR vs 5% nominal)
2. Use correct sample size formula with z_alpha/2=1.96 and z_beta=0.84
3. Apply Bonferroni correction for multiple secondary metrics
4. Implement automated bot traffic detection before experiment launch
5. Enable SRM monitoring from day 1 of each experiment
"""


# --------------------------------------------------------------------------- #
# Run checks
# --------------------------------------------------------------------------- #
EVAL_CMDS = {
    "q1": ["check_q1.py", ("pref", "P1,P3", "output/q1_running_experiments.json")],
    "q2": ["check_q2.py", ("pref", "P1,P3", "output/q2_srm_exp002.json")],
    "q3": ["check_q3.py", ("pref", "P1,P3", "output/q3_cuped_audit.json")],
    "q4": ["check_q4.py", ("pref", "P2", "scripts/power_analysis_fixed.py")],
    "q5": ["check_q5.py", ("pref", "P1,P3", "output/q5_bot_errors.json")],
    "q6": ["check_q6.py", ("pref", "P1,P3", "output/q6_peeking_analysis.json")],
    "q7": ["check_q7.py", ("pref", "P1,P3", "output/q7_multi_test_correction.json")],
    "q8": ["check_q8.py", ("pref", "P1,P3", "output/q8_exp003_revised.json")],
    "q9": ["check_q9.py", ("pref", "P1,P3", "output/q9_experiment_summary.json")],
    "q10": ["check_q10.py", ("pref", "P1,P3", "output/q10_runbook_diff.json")],
    "q11": ["check_q11.py", ("pref", "P1,P3", "output/q11_exp004_sample_size.json")],
    "q12": ["check_q12.py", ("pref", "P1,P3,P4", "output/q12_cuped_eligibility.json")],
    "q13": ["check_q13.py", ("pref", "P1,P3,P4", "output/q13_bonferroni_correction.json")],
    "q14": ["check_q14.py", ("pref", "P1,P3,P4,P5", "output/q14_twyman_check.json")],
    "q15": ["check_q15.py"],
    "q16": ["check_q16.py"],
}


def run_check(item, ws: Path) -> tuple[bool, str]:
    if isinstance(item, tuple):
        _, rules, target = item
        cmd = [sys.executable, str(SCRIPTS / "check_preferences.py"),
               str(ws), "--rules", rules, "--target", target]
    else:
        cmd = [sys.executable, str(SCRIPTS / item), str(ws)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    out = (r.stdout + r.stderr).strip()
    last = out.splitlines()[-1] if out else ""
    return r.returncode == 0, last


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
    print(f"\ngold: {n_pass} checks PASSED, {n_fail} FAILED")

    # --- Negative probes: must FAIL ---
    print("\n=== NEGATIVE PROBES: each must FAIL ===")
    probes = 0
    caught = 0

    # Probe 1: Q6 peeking with BOT decoy value (5% instead of 57%)
    _wj(ws / "output" / "q6_peeking_analysis.json", {
        "actual_fpr": 0.05,  # Wrong — BOT value
        "nominal_fpr": 0.05,
        "ratio": 1.0,
    })
    ok, _ = run_check("check_q6.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  q6 BOT-decoy actual_fpr=0.05 (should be 0.57) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 2: Q8 wrong conclusion (significant=true, original p=0.023)
    _wj(ws / "output" / "q8_exp003_revised.json", {
        "conclusion": "Significant positive effect confirmed. v2_social_proof wins.",
        "p_value": 0.023,  # Wrong — original contaminated value
        "significant": True,
    })
    ok, _ = run_check("check_q8.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  q8 original p=0.023 significant=true -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 3: Q13 using BH instead of Bonferroni (VP email, not superseded)
    _wj(ws / "output" / "q13_bonferroni_correction.json", {
        "alpha_adjusted": 0.05,
        "method": "benjamini_hochberg",  # Wrong — VP email was superseded
        "n_tests": 8,
        "significant_metrics": 2,
    })
    ok, _ = run_check("check_q13.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  q13 BH method (should be bonferroni) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 4: Q16 placeholder SHA-256 hash
    _w(ws / "output" / "q16_signoff.txt", "VERIFIED:" + "a" * 64 + "\n")
    ok, _ = run_check("check_q16.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  q16 placeholder hash -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 5: Q1 wrong count (only 4 running experiments)
    _wj(ws / "output" / "q1_running_experiments.json",
        ["exp006", "exp007", "exp008", "exp009"])  # Missing exp010
    ok, _ = run_check("check_q1.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  q1 missing exp010 (only 4 running) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 6: Q2 srm_detected=false (wrong — ignoring SRM)
    _wj(ws / "output" / "q2_srm_exp002.json", {
        "chi2_stat": 11.83,
        "p_value": 0.0006,
        "srm_detected": False,  # Wrong — should be True
    })
    ok, _ = run_check("check_q2.py", ws)
    probes += 1
    caught += (not ok)
    print(f"  q2 srm_detected=false (should be true) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    print(f"\nnegatives: {caught}/{probes} correctly caught")

    if n_fail == 0 and caught == probes:
        print("\nAUDIT OK: gold solution all-PASS and all negative probes caught.")
    else:
        print("\nAUDIT PROBLEM: see failures above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
