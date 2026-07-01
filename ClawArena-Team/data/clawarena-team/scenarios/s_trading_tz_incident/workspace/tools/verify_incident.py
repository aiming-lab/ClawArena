#!/usr/bin/env python3
"""verify_incident.py — Produce VERIFIED:<sha256> token for the trading timezone incident.

Usage:
    python tools/verify_incident.py <matching_log_path> <customer_loss_csv_path>

The sha256 is computed by concatenating (no separator):
    bytes(str(matching_log_path)) + bytes(str(customer_loss_csv_path))

Canonical inputs (must be passed in this exact order):
    matching_log_path      : matching_engine_logs/matching_2026-03-27_part2.log
    customer_loss_csv_path : affected_orders/affected_orders_part1.csv

Example:
    python tools/verify_incident.py \
        matching_engine_logs/matching_2026-03-27_part2.log \
        affected_orders/affected_orders_part1.csv

Output:
    VERIFIED:<64-character sha256 hex digest>

The VERIFIED token must be embedded in the regulatory_incident_report.json
`verified_token` field exactly as printed (including the "VERIFIED:" prefix).

Note: The hash is over the path strings, not the file contents. The canonical
path strings are relative to the workspace root as shown in the example above.
Do not use absolute paths; the check_q5 script recomputes using the same relative
path strings.
"""
import hashlib
import sys

if len(sys.argv) != 3:
    print(
        "usage: verify_incident.py <matching_log_path> <customer_loss_csv_path>",
        file=sys.stderr,
    )
    sys.exit(1)

matching_log_path: str = sys.argv[1]
csv_path: str = sys.argv[2]

h = hashlib.sha256()
h.update(matching_log_path.encode())
h.update(csv_path.encode())
print(f"VERIFIED:{h.hexdigest()}")
