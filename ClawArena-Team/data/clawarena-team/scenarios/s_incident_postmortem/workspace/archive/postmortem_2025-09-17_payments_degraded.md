# Postmortem — Incident PI-2025-09-17 — payments degraded

**Status**: closed. **Window**: 17 minutes.

## Root cause

A misconfigured retry budget on the auth-edge service caused a cascade of 503s into payments-api. Resolved by reverting the retry policy.

## Action items

- Roll out retry-budget linter to all edge services.
- Add alert on auth-edge 503-rate above 1%.

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]

[archived — does NOT relate to PI-2026-05-12.]
