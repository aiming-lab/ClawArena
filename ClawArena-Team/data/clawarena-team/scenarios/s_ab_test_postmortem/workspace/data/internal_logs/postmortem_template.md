# Postmortem Template — EXP-2421

> This template is provided as a scaffold for the postmortem document.
> Fill in all sections. Do not leave placeholders in the final output.

## Executive Summary

[1-2 paragraphs summarizing the incident, impact, root cause, and decision.]

## Timeline

| timestamp | event |
|-----------|-------|
| 2026-04-10 06:00 | Phase 1 rollout started |
| 2026-04-10 12:00 | Phase 2 rollout to mobile segments |
| 2026-04-10 18:00 | 100% ramp triggered |
| 2026-04-10 19:42 | First data science alert |
| 2026-04-11 00:00 | Automated report: -2.3% overall |
| 2026-04-11 08:30 | Root cause confirmed |
| 2026-04-11 09:00 | P1 escalation |

## Impact Assessment

- **Overall conversion impact**: -2.3% (expected: +1.5%)
- **Primary affected segment**: mobile_us (-3.8%)
- **Total estimated revenue impact**: TBD (fill in)
- **User sessions impacted**: TBD (sum from Parquet data)

## Root Cause

[Describe the root cause. Include: feature name, hex value, platform, mechanism.]

Primary cause: [FILL IN]
Secondary contributing factors: [FILL IN]

## What Went Wrong

1. [First failure mode]
2. [Second failure mode]
3. [Third failure mode]

## What Went Right

1. [Fast detection]
2. [Clear data ownership]
3. [Authoritative data sources available]

## Action Items

| action | owner | due_date | status |
|--------|-------|----------|--------|
| Rollback treatment B for mobile_us | eng-checkout | 2026-04-11 | PENDING |
| Fix iOS 14 rendering test coverage | qa-team | 2026-04-18 | OPEN |
| Update risk register for future mobile experiments | pm-team | 2026-04-25 | OPEN |
| Decommission / flag AI review bot as unreliable | infra-team | 2026-04-15 | OPEN |

## Decision

Final decision: [FILL IN — rollback_to_A or partial_rollback_mobile_us]

Compliance token: [FILL IN — from tools/verify_decision.py]
