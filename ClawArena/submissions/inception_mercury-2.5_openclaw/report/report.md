# Benchmark Report — openclaw

## Summary

- **Tests**: 12
- **Rounds**: 337
- **CRS** (Composite Reliability Score): 51.99%  _= (TCR + SC · FD) / 2_
- **TCR** (Task Completion Rate): 65.70%
- **Robustness**: 40.92%  _= SC · FD_
- **SC** (Success Cohesion): 44.28%
- **FD** (Failure Dispersion): 86.45%
- **Total Tokens**: 2,591,759

## By Test

| Test | Rounds | **CRS** | TCR | Robustness | SC | FD | Tokens |
|------|--------|---------|-----|-----------|----|----|--------|
| hil_c7 | 28 | **63.84%** | 75.00% | 52.68% | 59.26% | 88.89% | 0 |
| hil_d3 | 30 | **64.20%** | 76.67% | 51.72% | 51.72% | 100.00% | 0 |
| hil_e4 | 24 | **74.94%** | 83.33% | 66.54% | 69.57% | 95.65% | 0 |
| hil_f3 | 30 | **17.68%** | 33.33% | 2.02% | 3.45% | 58.62% | 0 |
| hil_f7 | 27 | **77.73%** | 85.19% | 70.27% | 73.08% | 96.15% | 0 |
| hil_g1 | 30 | **76.15%** | 83.33% | 68.97% | 68.97% | 100.00% | 0 |
| hil_g3 | 30 | **28.57%** | 46.67% | 10.46% | 13.79% | 75.86% | 0 |
| hil_g4 | 27 | **51.09%** | 66.67% | 35.50% | 38.46% | 92.31% | 0 |
| hil_h3 | 27 | **61.89%** | 74.07% | 49.71% | 53.85% | 92.31% | 0 |
| hil_i2 | 30 | **56.64%** | 70.00% | 43.28% | 44.83% | 96.55% | 0 |
| hil_j1 | 30 | **44.03%** | 56.67% | 31.39% | 41.38% | 75.86% | 0 |
| hil_s1 | 24 | **23.00%** | 37.50% | 8.50% | 13.04% | 65.22% | 2,591,759 |

## By Type

- **multi_choice**: 95 rounds, TCR 63.16%
- **exec_check**: 242 rounds, TCR 66.53%

## Notes

- **CRS** = (TCR + SC · FD) / 2. Range [0, 1]. TCR (correctness) and Robustness (streak health) carry equal weight.
- **SC** = (S − k) / (N − 1) over success run-lengths; L=[N]→1, L=[1,1,…]→0, empty L→0.
- **FD** = 1 − (S_fail − k_fail) / (N − 1) over failure run-lengths; no failures → 1, full failure cascade → 0.
- **Robustness** = SC · FD. Multiplicative: either axis collapsing tanks the score.
