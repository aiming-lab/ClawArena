# Archive Policy — Historical Incident Records

Historical incidents are retained for 3 years per the security incident
management policy. Archived incidents must not be used as authoritative
sources for current incident response without verification.

## Key Principles

1. Stale IOC clearances do not carry forward to new incidents.
   An IP cleared in 2025 may be malicious in 2026 if re-compromised.
2. Archived verdicts (false positive, cleared) apply only to the specific
   incident context and date range for which they were assessed.
3. Always check the archive for prior activity, but treat prior verdicts
   as advisory context, not as current ground truth.

## Retention Policy

All P1/P2 incidents are retained for 5 years.
P3 and below incidents are retained for 3 years.
Automated false positive closures are retained for 1 year.
