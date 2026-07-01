#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Multiple comparison correction: Bonferroni and Benjamini-Hochberg (BH).

Reference: https://docs.growthbook.io/using/experimentation-problems
Note: With 20 independent tests at alpha=0.05, probability of >= 1 false positive ~ 64%.

Company default: Bonferroni correction.
"""

from typing import List, Tuple


def bonferroni_correction(p_values: List[float], alpha: float = 0.05) -> dict:
    """Apply Bonferroni correction to a list of p-values.

    Args:
        p_values: List of raw p-values.
        alpha: Family-wise error rate (default 0.05).

    Returns:
        Dict with method, alpha_adjusted, significant_indices, significant_count.
    """
    k = len(p_values)
    alpha_adjusted = alpha / k
    significant = [i for i, p in enumerate(p_values) if p < alpha_adjusted]
    return {
        "method": "bonferroni",
        "alpha_original": alpha,
        "alpha_adjusted": round(alpha_adjusted, 6),
        "n_tests": k,
        "significant_count": len(significant),
        "significant_indices": significant
    }


def bh_correction(p_values: List[float], alpha: float = 0.05) -> dict:
    """Apply Benjamini-Hochberg (BH) correction.

    Args:
        p_values: List of raw p-values.
        alpha: False Discovery Rate threshold (default 0.05).

    Returns:
        Dict with method, significant_indices, significant_count, bh_threshold.
    """
    k = len(p_values)
    indexed = sorted(enumerate(p_values), key=lambda x: x[1])
    significant = []
    bh_thresh = 0.0
    for rank, (i, p) in enumerate(indexed, start=1):
        threshold = alpha * rank / k
        if p <= threshold:
            significant.append(i)
            bh_thresh = threshold
    return {
        "method": "benjamini_hochberg",
        "alpha_original": alpha,
        "n_tests": k,
        "significant_count": len(significant),
        "significant_indices": sorted(significant),
        "bh_critical_threshold": round(bh_thresh, 6)
    }


if __name__ == "__main__":
    # Example: exp003 with 24 p-values
    import random
    rng = random.Random(42)
    pvals = [rng.uniform(0, 0.2) for _ in range(24)]
    print("Bonferroni:", bonferroni_correction(pvals))
    print("BH:", bh_correction(pvals))
