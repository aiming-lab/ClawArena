# Compliance token guide — gbm-v2-2026q2 audit

The final `audit/model_decision.json` must include a `compliance_token` field.

## How to generate the token

1. Complete `audit/model_decision.json` with all required fields:
   decision, mc_estimate, bs_reference, model_name, var_95, reviewer, decision_date.

2. Run:
       python tools/compute_token.py audit/model_decision.json

3. Copy the hex string after `COMPLIANCE_TOKEN:` into the `compliance_token` field.

## Token algorithm

The token is SHA-256 over a canonical pipe-delimited string:
    decision=<val>|mc_estimate=<val>|bs_reference=<val>|model_name=<val>|var_95=<val>|reviewer=<val>|decision_date=<val>

Changing any of these values invalidates the token.

## Required field values for this audit

| field | expected value |
|---|---|
| decision | approve_model |
| mc_estimate | 2.1552 |
| bs_reference | 2.1477 |
| model_name | gbm-v2-2026q2 |
| var_95 | 0.34 |
| reviewer | (your identifier) |
| decision_date | (YYYY-MM-DD of sign-off) |
