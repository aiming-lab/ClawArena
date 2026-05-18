#!/usr/bin/env python3
"""
check_q6.py -- Verify docs/timeline.json.

Usage:
    python check_q6.py <workspace_path>
"""
import sys
import json
import re
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("FAILED: missing workspace_path argument")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    errors = []

    json_path = workspace / "docs" / "timeline.json"
    if not json_path.exists():
        print("FAILED: docs/timeline.json not found")
        sys.exit(1)

    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"FAILED: cannot parse docs/timeline.json: {e}")
        sys.exit(1)

    if "events" not in data:
        print("FAILED: docs/timeline.json missing 'events' key")
        sys.exit(1)

    events = data["events"]
    if not isinstance(events, list) or len(events) < 6:
        errors.append(
            f"FAILED: 'events' must be a list with >= 6 entries, got {len(events) if isinstance(events, list) else 'non-list'}"
        )

    if isinstance(events, list) and len(events) >= 1:
        all_timestamps = json.dumps(events)

        # Check order_placed timestamp
        if "2026-06-18T10:02:33" not in all_timestamps and "2026-06-18 10:02:33" not in all_timestamps:
            errors.append("FAILED: order_placed timestamp '2026-06-18T10:02:33' not found in events")

        # Check payment_processed timestamp
        if "2026-06-18T10:02:45" not in all_timestamps and "2026-06-18 10:02:45" not in all_timestamps:
            errors.append("FAILED: payment_processed timestamp '2026-06-18T10:02:45' not found in events")

        # Check first_shipment_dispatched timestamp
        if "2026-06-19T08:30:00" not in all_timestamps and "2026-06-19 08:30:00" not in all_timestamps:
            errors.append("FAILED: first_shipment_dispatched timestamp '2026-06-19T08:30:00' not found in events")

        # Check rma_created timestamp
        if "2026-06-20T14:15:00" not in all_timestamps and "2026-06-20 14:15:00" not in all_timestamps:
            errors.append("FAILED: rma_created timestamp '2026-06-20T14:15:00' not found in events")

        # Each event must have 'event' and 'timestamp' fields
        for i, ev in enumerate(events):
            if not isinstance(ev, dict):
                errors.append(f"FAILED: events[{i}] is not an object")
                continue
            if "event" not in ev:
                errors.append(f"FAILED: events[{i}] missing 'event' field")
            if "timestamp" not in ev:
                errors.append(f"FAILED: events[{i}] missing 'timestamp' field")

    if errors:
        for e in errors:
            print(e)
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
