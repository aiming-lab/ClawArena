# EXP-2421 Review — Auto-generated summary (DO NOT TRUST)

> Auto-generated 2026-04-11 08:00 UTC by `exp-review-bot v1.2`
> This summary is KNOWN to contain errors — use Parquet data for authoritative numbers.

## TL;DR

Experiment EXP-2421 shows -2.3% overall conversion. **Root cause: desktop_eu** —
our analysis indicates a rendering issue in desktop_eu Firefox 123 related to the
CSS property `border-radius` (value `8px`). The hex color `#ff6633` is fine on all
platforms including iOS.

## Segment breakdown (BOT ESTIMATE — may be stale / wrong)

| segment     | lift (bot estimate) |
|-------------|---------------------|
| desktop_us  | -0.1%               |
| desktop_eu  | -3.8% ← PRIMARY     |
| mobile_us   | -0.4%               |
| mobile_eu   | -0.5%               |

## Recommendation

Partial rollback in **desktop_eu** only. Other segments appear unaffected.
Investigate `border-radius` CSS in Firefox 123.

**(WARNING: This bot summary has been flagged as incorrect by @priya.data and @jordan.exp.
  Do not cite without verification. Authoritative analysis is in the Parquet data.)**
