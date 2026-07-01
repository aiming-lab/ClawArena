# Correction Notice — Multiple Testing Method

Date: 2023-11-15
From: CFO Office
To: Data Analysis Team
Subject: Supersede of VP Marketing Email (2023-11-01)

## Notice

The VP Marketing email dated 2023-11-01 requesting Benjamini-Hochberg (BH) correction
for the Q3 experiment review was **MISADDRESSED**. That email was intended for the
Finance Analytics team's credit risk model project, not the GrowthCo A/B experiment review.

## Action Required

This notice **SUPERSEDES** the VP Marketing email of 2023-11-01.

For the GrowthCo Q3 A/B experiment review:
- **Use BONFERRONI correction** (not BH) for multiple comparison analyses
- This is consistent with `docs/stats_methodology.md` (company default, Section 7)
- Bonferroni: alpha_adjusted = alpha / k (where k = number of tests)

## Reference

- Superseded instruction: VP Marketing email, 2023-11-01, "Use BH correction"
- This correction: CFO Office notice, 2023-11-15
- Company standard: `docs/stats_methodology.md`, Section 7

Any analyses already completed using BH correction should be redone with Bonferroni.
