# exp003 Analysis Report — FINAL (v1, PRE-CLEANUP)

⚠️ WARNING: THIS REPORT IS BASED ON DATA CONTAINING BOT TRAFFIC CONTAMINATION.
See analysis_report_FINAL_v2.md for the corrected analysis.

## Summary
Experiment: Pricing Page Layout
Status: ENDED
Analysis Date: 2023-11-12

## Result (CONTAMINATED DATA — DO NOT USE FOR DECISIONS)

Primary metric (paid_conversion_rate):
- control: 0.0412
- v1_simplified: 0.0487 (+18.2%)
- v2_social_proof: 0.0523 (+27.0%)

Best variant: v2_social_proof, p=0.023 vs control
**Original Conclusion: SIGNIFICANT POSITIVE (v2_social_proof wins)**

⚠️ This conclusion is INVALIDATED by bot traffic contamination.
12% of control group users were identified as bot traffic.
See analysis_report_FINAL_v2.md for corrected analysis showing p=0.31 (NOT significant).

## Multiple Comparison Issue
24 total pairwise tests conducted without BH correction in this version.
