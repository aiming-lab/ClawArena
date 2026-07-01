#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CUPED (Controlled-experiment Using Pre-Experiment Data) adjustment.

Reference: https://docs.statsig.com/stats-engine/methodologies/cuped
Formula: theta = Cov(Y, X) / Var(X)
Adjusted metric: Y_adjusted = Y - theta * X + theta * E[X]

Activation conditions (Statsig):
- > 100 units with pre-experiment data
- Coverage > 5%
- Pre-experiment window: 7 days prior to exposure
"""

import math
from typing import List


def compute_theta(Y: List[float], X: List[float]) -> float:
    """Compute CUPED theta = Cov(Y, X) / Var(X).

    Args:
        Y: Post-experiment outcome metric values.
        X: Pre-experiment covariate values (same units as Y).

    Returns:
        theta (float): CUPED adjustment coefficient.
    """
    n = len(Y)
    if n != len(X):
        raise ValueError("Y and X must have the same length")
    mean_y = sum(Y) / n
    mean_x = sum(X) / n
    cov = sum((Y[i] - mean_y) * (X[i] - mean_x) for i in range(n)) / (n - 1)
    var_x = sum((X[i] - mean_x) ** 2 for i in range(n)) / (n - 1)
    if var_x == 0:
        return 0.0
    return cov / var_x


def adjust_metric(Y: List[float], X: List[float], theta: float) -> List[float]:
    """Apply CUPED adjustment.

    Args:
        Y: Post-experiment outcome metric values.
        X: Pre-experiment covariate values.
        theta: CUPED coefficient computed by compute_theta().

    Returns:
        List of CUPED-adjusted outcome values.
    """
    mean_x = sum(X) / len(X)
    return [y - theta * (x - mean_x) for y, x in zip(Y, X)]


def check_eligibility(n_units_with_pre_data: int, total_units: int) -> dict:
    """Check Statsig CUPED activation conditions.

    Args:
        n_units_with_pre_data: Number of units with pre-experiment data.
        total_units: Total number of units in experiment.

    Returns:
        Dict with eligible (bool), units_check (bool), coverage_check (bool),
        pct_coverage (float), and reason (str).
    """
    units_ok = n_units_with_pre_data > 100
    pct = 100.0 * n_units_with_pre_data / max(total_units, 1)
    coverage_ok = pct > 5.0
    eligible = units_ok and coverage_ok
    reason_parts = []
    if not units_ok:
        reason_parts.append(f"units_with_pre_data={n_units_with_pre_data} <= 100")
    if not coverage_ok:
        reason_parts.append(f"coverage={pct:.2f}% <= 5%")
    if eligible:
        reason = (f"Eligible: {n_units_with_pre_data} units with pre-experiment data "
                  f"({pct:.2f}% coverage), both exceed Statsig thresholds "
                  f"(>100 units, >5% coverage, 7-day pre-experiment window)")
    else:
        reason = "Not eligible: " + "; ".join(reason_parts)
    return {
        "eligible": eligible,
        "units_with_pre_data": n_units_with_pre_data,
        "pct_coverage": round(pct, 4),
        "units_check": units_ok,
        "coverage_check": coverage_ok,
        "reason": reason
    }
