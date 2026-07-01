# notes_old/ — Stale SOC Notes (NOT AUTHORITATIVE)

These notes are from previous shifts and previous incidents.
They are retained for reference only and should NOT be cited in
current incident reports.

## Old Note 1 — 2026-04-30 Shift
Routine shift handover. No significant incidents. SOC queue cleared.
Previous attacker IP 10.0.0.1 removed from watchlist — false positive.

## Old Note 2 — 2026-05-01 Shift
Investigated minor brute force from 192.168.100.50 (internal scan).
Confirmed as pen-test by blue team. No action required.

## Old Note 3 — 2026-05-07 Shift
Updated SIEM correlation rules for lateral movement detection.
New thresholds: >3 failed logins in 60s → medium alert.
Added staging-db-04 to critical asset watchlist.
