# Data Colada [112] — Data Falsificada (Part 4): Why Connect

**Source URL**: https://datacolada.org/112
**Published**: 2023 (Uri Simonsohn, Leif Nelson, Joe Simmons)

---

## Summary

This report analyses the JPSP 2020 paper:

> Gino, F., Kouchaki, M., & Casciaro, T. (2020).
> Why connect? Moral consequences of relationship avoidance.
> *Journal of Personality and Social Psychology*, **120**(5), 1281–1300.
> DOI: 10.1037/pspa0000226

---

## Study 3a: Condition Main Effect

Study 3a examined how social connection conditions (Promotion, Prevention, Control)
affected ethical perceptions. Participants (**N ≈ 601**; df₂ = 596 confirms ~599 usable)
were randomly assigned to one of three conditions.

### Reported Statistics

The paper reports a significant main effect of condition:

> F(2, 596) = **17.69**, p < .0001

Note: `df₁ = 2` (two contrasts for three conditions) and
`df₂ = 596` (residual, consistent with ~599 participants).

### Data Integrity Problems Identified

1. **Word–Rating Mismatch (Prevention condition)**:
   Eighteen participants in the Prevention condition received a rating of **3.0** on the
   ethical-perception scale but were paired with *positive* words in their response files.
   Under a genuine Prevention paradigm, high-ethics ratings (3.0 = max on the scale used)
   should correlate with negative words, not positive ones.

2. **Reverse correlation in Prevention vs. Control**:
   - Prevention group: word–rating correlation r = **−0.20**
   - Control group: word–rating correlation r = **−0.56**
   These differ significantly (Fisher z: p = .026), indicating data anomalies.

3. **Promotion word means reversed**:
   - Promotion group mean: **4.74** (should be below Prevention if Prevention promotes ethics)
   - Prevention group mean: **5.14** (inconsistency with paradigm direction)

### Forensic Method

The word-rating mismatch is detectable because the raw response file retains both the
numeric rating and the associated word list. Comparing these two columns reveals the
18 impossible {3.0-rating + positive-word} pairs unique to Prevention.

---

## Conclusion

The statistical pattern in Study 3a and the forensic word–rating mismatch together
indicate data manipulation. The F(2,596) = 17.69 result should be treated
as a product of manipulated data.
