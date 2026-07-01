#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# WARNING: This script contains INCORRECT parameters.
# z_alpha uses 99% CI (2.576) instead of 95% CI (1.96)
# z_beta uses 90% power (1.28) instead of 80% power (0.84)
# This script needs to be corrected before use.

import math

def calculate_sample_size_INCORRECT(p1, p2, alpha=0.01, power=0.90):
    # BUG: z_alpha should be 1.96 for alpha=0.05, not 2.576 for alpha=0.01
    z_alpha = 2.576  # WRONG: should be 1.96 for 95% CI
    # BUG: z_beta should be 0.84 for 80% power, not 1.28 for 90% power
    z_beta = 1.28    # WRONG: should be 0.84 for 80% power
    numerator = (z_alpha + z_beta) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2))
    denominator = (p1 - p2) ** 2
    return math.ceil(numerator / denominator)

if __name__ == "__main__":
    n = calculate_sample_size_INCORRECT(p1=0.22, p2=0.25)
    print(f"INCORRECT sample size: {n} per group")
    # This gives n=4871, which is too large due to wrong z values
