#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SRM (Sample Ratio Mismatch) checker using chi-squared test.

Reference: https://docs.statsig.com/stats-engine/methodologies/srm-checks
Threshold: p < 0.01 (Statsig) or p < 0.0005 (Microsoft ExP conservative)
"""

import math
import sys


def chi_squared_srm(observed: dict, expected_ratios: dict) -> dict:
    """Perform chi-squared test for Sample Ratio Mismatch.

    Args:
        observed: Dict of variant -> observed count.
        expected_ratios: Dict of variant -> expected proportion.

    Returns:
        Dict with chi2_stat, p_value, srm_detected (bool), and details.
    """
    total = sum(observed.values())
    expected = {k: v * total for k, v in expected_ratios.items()}
    chi2 = sum((observed[k] - expected[k]) ** 2 / expected[k]
               for k in observed if k in expected)
    df = len(observed) - 1
    # Approximate p-value using chi-squared CDF approximation
    p_value = _chi2_sf(chi2, df)
    srm_detected = p_value < 0.01  # Statsig threshold
    return {
        "chi2_stat": round(chi2, 4),
        "p_value": round(p_value, 6),
        "degrees_of_freedom": df,
        "srm_detected": srm_detected,
        "threshold_used": 0.01,
        "source": "Statsig SRM Checks (https://docs.statsig.com/stats-engine/methodologies/srm-checks)"
    }


def _chi2_sf(x, df):
    """Survival function (1 - CDF) for chi-squared distribution."""
    # Simple gamma incomplete function approximation for df=1,2
    if df == 1:
        from math import erfc, sqrt
        return erfc(sqrt(x / 2))
    elif df == 2:
        return math.exp(-x / 2)
    else:
        # General approximation
        k = df / 2.0
        return _regularized_upper_incomplete_gamma(k, x / 2.0)


def _regularized_upper_incomplete_gamma(a, x):
    """Regularized upper incomplete gamma function approximation."""
    if x <= 0:
        return 1.0
    # Series expansion for small x, continued fraction for large x
    import math
    if x < a + 1:
        # Series expansion
        ap = a
        s = 1.0 / a
        delta = s
        for _ in range(200):
            ap += 1
            delta *= x / ap
            s += delta
            if abs(delta) < abs(s) * 3e-7:
                break
        return 1.0 - s * math.exp(-x + a * math.log(x) - math.lgamma(a))
    else:
        # Continued fraction
        b = x + 1 - a
        c = 1e300
        d = 1.0 / b
        h = d
        for i in range(1, 201):
            an = -i * (i - a)
            b += 2
            d = an * d + b
            if abs(d) < 1e-300:
                d = 1e-300
            c = b + an / c
            if abs(c) < 1e-300:
                c = 1e-300
            d = 1.0 / d
            delta = d * c
            h *= delta
            if abs(delta - 1.0) < 3e-7:
                break
        return math.exp(-x + a * math.log(x) - math.lgamma(a)) * h


if __name__ == "__main__":
    # Test on exp002 data
    result = chi_squared_srm(
        observed={"control": 5234, "treatment": 4891},
        expected_ratios={"control": 0.5, "treatment": 0.5}
    )
    print("exp002 SRM check:", result)
