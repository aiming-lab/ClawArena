# SEC Formal Investigation Notice — ArtemisQ Capital
## SEC Division of Trading and Markets — Case No. TM-2024-1103-AQ
## Date: 2024-11-10

**From**: SEC Division of Trading and Markets
**To**: Elena Vasquez, Chief Compliance Officer, ArtemisQ Capital
**Re**: FORMAL INVESTIGATION — Rule 15c6-1 T+1 Compliance

---

## FORMAL INVESTIGATION ORDER

Following review of ArtemisQ Capital's response to our preliminary inquiry
notice of 2024-11-05, the SEC Division of Trading and Markets has determined
that a **formal investigation** under SEC Case No. TM-2024-1103-AQ is warranted.

## Additional Requirement: System Backtest Certification

In addition to the order-level data already submitted, ArtemisQ Capital is
required to provide a **system backtest certification** demonstrating that:

1. The corrected UTC-5 (EST) timezone configuration correctly computes
   T+1 settlement cutoffs and CME settlement reference times for the
   2024-11-03 trade date scenario

2. The certification must be in the form of a backtest script output
   showing the correct simulated settlement time matches the expected value

### Backtest Requirements

The backtest must demonstrate:
- Configuration: `config_timezone_offset = -5` (EST, correct)
- Expected CME settlement: **2024-11-03T21:00:00Z** (not the buggy 20:00 UTC)
- Expected T+1 cutoff: **2024-11-04T02:00:00Z** (not the buggy 01:00 UTC)
- `match = true` (simulated settlement matches expected)

A template backtest script is provided at:
`regulatory/sec_backtest_template.py`

### SHA-256 Reference Requirement

The backtest certification must reference the SHA-256 hash from your
previously submitted `output/report_signoff.txt` to confirm data chain
of custody.

### Deadline

Backtest certification due: **2024-11-17T15:00:00Z**

SEC Division of Trading and Markets
Case No. TM-2024-1103-AQ
2024-11-10T15:00:00Z
