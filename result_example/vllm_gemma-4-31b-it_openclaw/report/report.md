# Benchmark Report — openclaw

## Summary

- **Tests**: 12
- **Rounds**: 337
- **CRS** (Composite Reliability Score): 63.58%  _= (TCR + SC · FD) / 2_
- **TCR** (Task Completion Rate): 74.99%
- **Robustness**: 53.85%  _= SC · FD_
- **SC** (Success Cohesion): 56.76%
- **FD** (Failure Dispersion): 91.90%
- **Total Tokens**: 0

## By Test

| Test | Rounds | **CRS** | TCR | Robustness | SC | FD | Tokens |
|------|--------|---------|-----|-----------|----|----|--------|
| hil_c7 | 28 | **73.17%** | 82.14% | 64.20% | 66.67% | 96.30% | 0 |
| hil_d3 | 30 | **69.31%** | 80.00% | 58.62% | 58.62% | 100.00% | 0 |
| hil_e4 | 24 | **69.36%** | 79.17% | 59.55% | 65.22% | 91.30% | 0 |
| hil_f3 | 30 | **69.96%** | 80.00% | 59.93% | 62.07% | 96.55% | 0 |
| hil_f7 | 27 | **72.17%** | 81.48% | 62.86% | 65.38% | 96.15% | 0 |
| hil_g1 | 30 | **89.77%** | 93.33% | 86.21% | 86.21% | 100.00% | 0 |
| hil_g3 | 30 | **43.38%** | 60.00% | 26.75% | 31.03% | 86.21% | 0 |
| hil_g4 | 27 | **60.11%** | 74.07% | 46.15% | 46.15% | 100.00% | 0 |
| hil_h3 | 27 | **83.28%** | 88.89% | 77.66% | 80.77% | 96.15% | 0 |
| hil_i2 | 30 | **62.35%** | 73.33% | 51.36% | 55.17% | 93.10% | 0 |
| hil_j1 | 30 | **58.78%** | 70.00% | 47.56% | 55.17% | 86.21% | 0 |
| hil_s1 | 24 | **21.40%** | 37.50% | 5.30% | 8.70% | 60.87% | 0 |

## By Type

- **multi_choice**: 95 rounds, TCR 81.05%
- **exec_check**: 242 rounds, TCR 73.14%

## Notes

- **CRS** = (TCR + SC · FD) / 2. Range [0, 1]. TCR (correctness) and Robustness (streak health) carry equal weight.
- **SC** = (S − k) / (N − 1) over success run-lengths; L=[N]→1, L=[1,1,…]→0, empty L→0.
- **FD** = 1 − (S_fail − k_fail) / (N − 1) over failure run-lengths; no failures → 1, full failure cascade → 0.
- **Robustness** = SC · FD. Multiplicative: either axis collapsing tanks the score.
