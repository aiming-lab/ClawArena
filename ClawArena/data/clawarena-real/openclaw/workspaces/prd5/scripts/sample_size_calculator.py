#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sample size calculator for two-proportion z-test.

Based on the formula from https://en.wikipedia.org/wiki/Two-proportion_Z-test:
  n = (z_alpha/2 + z_beta)^2 * [p1(1-p1) + p2(1-p2)] / (p1-p2)^2

Ground-truth constants (company standard):
  z_alpha/2 = 1.96  (alpha=0.05, two-sided)
  z_beta    = 0.84  (power=0.80)
"""

import math
import sys


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
    z_alpha_half = 1.96   # Standard normal 97.5th percentile for alpha=0.05 two-sided
    z_beta = 0.84         # Standard normal 80th percentile for power=0.80
    numerator = (z_alpha_half + z_beta) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2))
    denominator = (p1 - p2) ** 2
    return math.ceil(numerator / denominator)


def main():
    """Run sample size calculation with example parameters."""
    # Standard example: p1=0.10, p2=0.12, alpha=0.05, power=0.80
    n = calculate_sample_size(p1=0.10, p2=0.12, alpha=0.05, power=0.80)
    print(f"p1=0.10, p2=0.12, alpha=0.05, power=0.80 -> n={n} per group")

    # exp004 parameters: p1=0.22, p2=0.25
    n4 = calculate_sample_size(p1=0.22, p2=0.25, alpha=0.05, power=0.80)
    print(f"p1=0.22, p2=0.25, alpha=0.05, power=0.80 -> n={n4} per group")


if __name__ == "__main__":
    main()
