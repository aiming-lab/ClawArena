# A/B Testing Runbook — Current Version (v2)

Version: 2.0
Last Updated: 2023-10-15

## Quick Reference

| Parameter | Value | Source |
|-----------|-------|--------|
| Alpha (two-sided) | 0.05 | Industry standard |
| Power | 0.80 | Evan Miller calculator |
| z_alpha/2 | 1.96 | Standard normal 97.5th percentile |
| z_beta | 0.84 | Standard normal 80th percentile |
| SRM threshold | p < 0.01 | Statsig |
| CUPED activation | >100 units with pre-data, >5% coverage | Statsig |
| CUPED window | 7 days pre-exposure | Statsig Cloud default |
| Multiple testing | Bonferroni | Company default |

## Pre-Launch Checklist

- [ ] Experiment hypothesis documented
- [ ] Sample size calculated using n = (z_α/2 + z_β)² × [p1(1-p1)+p2(1-p2)] / (p1-p2)²
- [ ] Primary metric pre-registered
- [ ] SRM monitoring configured (threshold: p < 0.01)
- [ ] Traffic split verified
- [ ] CUPED eligibility checked (if applicable)
- [ ] Multiple testing correction method specified (Bonferroni)

## During Experiment

- Do NOT check results more frequently than pre-planned
- Peeking inflates false positive rate: every-visitor checking → 57% actual FPR
- Run SRM check daily; pause if SRM detected (p < 0.01)

## Analysis

1. Verify no SRM (chi-squared test, p < 0.01)
2. Apply CUPED if eligible (θ = Cov(Y,X)/Var(X))
3. Apply Bonferroni correction for secondary metrics
4. Apply Twyman's Law to any result >20% lift
5. Document conclusion and store in exp_registry.json

## Sample Size Calculator (correct version)

```python
import math

def sample_size(p1, p2, alpha=0.05, power=0.80):
    z_alpha = 1.96   # two-sided alpha=0.05
    z_beta  = 0.84   # power=0.80
    return math.ceil(
        (z_alpha + z_beta)**2 * (p1*(1-p1) + p2*(1-p2)) / (p1-p2)**2
    )
```

## Appendix: Common Mistakes

1. **Peeking**: Stopping early when p < 0.05 observed → inflates FPR to 57%
2. **SRM ignored**: Running analysis on imbalanced samples → biased estimates
3. **CUPED theta hardcoded**: θ must be computed as Cov(Y,X)/Var(X)
4. **Missing multiple correction**: 24 tests without correction → high FPR
5. **Bot traffic**: Contaminated control group biases results
