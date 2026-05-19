# Benchmark Report — openclaw

## Summary

- **Tests**: 12
- **Rounds**: 337
- **CRS** (Composite Reliability Score): 68.22%  _= (TCR + SC · FD) / 2_
- **TCR** (Task Completion Rate): 78.22%
- **Robustness**: 58.49%  _= SC · FD_
- **SC** (Success Cohesion): 61.24%
- **FD** (Failure Dispersion): 95.06%
- **Total Tokens**: 75,936,741

## By Test

| Test | Rounds | **CRS** | TCR | Robustness | SC | FD | Tokens |
|------|--------|---------|-----|-----------|----|----|--------|
| hil_c7 | 28 | **67.82%** | 78.57% | 57.07% | 59.26% | 96.30% | 3,257,155 |
| hil_d3 | 30 | **81.27%** | 86.67% | 75.86% | 75.86% | 100.00% | 5,984,031 |
| hil_e4 | 24 | **74.94%** | 83.33% | 66.54% | 69.57% | 95.65% | 4,160,732 |
| hil_f3 | 30 | **81.62%** | 86.67% | 76.57% | 79.31% | 96.55% | 5,090,870 |
| hil_f7 | 27 | **72.17%** | 81.48% | 62.86% | 65.38% | 96.15% | 5,784,211 |
| hil_g1 | 30 | **64.97%** | 76.67% | 53.27% | 55.17% | 96.55% | 7,119,942 |
| hil_g3 | 30 | **52.66%** | 66.67% | 38.65% | 44.83% | 86.21% | 3,835,684 |
| hil_g4 | 27 | **57.37%** | 70.37% | 44.37% | 46.15% | 96.15% | 9,278,441 |
| hil_h3 | 27 | **74.02%** | 81.48% | 66.56% | 69.23% | 96.15% | 5,693,523 |
| hil_i2 | 30 | **74.96%** | 83.33% | 66.59% | 68.97% | 96.55% | 3,699,071 |
| hil_j1 | 30 | **67.23%** | 76.67% | 57.79% | 62.07% | 93.10% | 5,284,747 |
| hil_s1 | 24 | **51.20%** | 66.67% | 35.73% | 39.13% | 91.30% | 16,748,334 |

## By Type

- **multi_choice**: 95 rounds, TCR 75.79%
- **exec_check**: 242 rounds, TCR 79.34%

## Notes

- **CRS** = (TCR + SC · FD) / 2. Range [0, 1]. TCR (correctness) and Robustness (streak health) carry equal weight.
- **SC** = (S − k) / (N − 1) over success run-lengths; L=[N]→1, L=[1,1,…]→0, empty L→0.
- **FD** = 1 − (S_fail − k_fail) / (N − 1) over failure run-lengths; no failures → 1, full failure cascade → 0.
- **Robustness** = SC · FD. Multiplicative: either axis collapsing tanks the score.
