#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# exp005 power analysis — template awaiting correct parameters

import math

def calculate_sample_size(p1, p2, z_alpha_half=1.96, z_beta=0.84):
    """Calculate sample size for two-proportion z-test.

    Args:
        p1: Baseline proportion.
        p2: Expected proportion under treatment.
        z_alpha_half: Z-value for alpha/2 (default 1.96 for 95% CI).
        z_beta: Z-value for beta (default 0.84 for 80% power).

    Returns:
        Sample size per group (int).
    """
    numerator = (z_alpha_half + z_beta) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2))
    denominator = (p1 - p2) ** 2
    return math.ceil(numerator / denominator)

if __name__ == "__main__":
    # Placeholder values — replace with exp005 actual parameters
    n = calculate_sample_size(p1=0.15, p2=0.17)
    print(f"Sample size: {n} per group")
