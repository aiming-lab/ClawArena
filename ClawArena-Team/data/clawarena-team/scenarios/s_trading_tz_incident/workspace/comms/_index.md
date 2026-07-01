# Communications Index

This directory contains internal communications related to the settlement failure incident.

## Files

| File | Approx Tokens | Content |
|---|---|---|
| `slack_incident_channel.md` | ~8.5k tok | #incident-2026-03-28 Slack export; MATCHING_ENG_LEAD's initial hypothesis (DST on clearing side) is WRONG — corrected by 09:22Z |
| `email_thread_regulator.md` | ~5k tok | Email thread with REGULATOR_CONTACT; confirms 48h deadline and report format |

## Key Context

MATCHING_ENG_LEAD (Damian Kowalski) initially hypothesized in Slack at 09:18Z that
the root cause was a DST misconfiguration on the ClearRoute EU clearing side. This
hypothesis was corrected by MATCHING_ENG_LEAD himself at 09:22Z after reviewing the
config history. The final confirmed root cause is the dispatch adapter misconfiguration
on the FinClear Asia side (not ClearRoute EU).

Any analysis that attributes root cause to "ClearRoute EU DST" is factually incorrect.
