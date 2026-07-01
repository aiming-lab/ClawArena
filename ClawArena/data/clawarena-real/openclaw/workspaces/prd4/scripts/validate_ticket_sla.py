#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_ticket_sla.py — Validate ticket SLA compliance.

Usage: python validate_ticket_sla.py <breach_tickets_file.json>
Output: prints JSON summary with validated_count, error_count, invalid_ticket_ids
"""
import sys
import json
from pathlib import Path


REQUIRED_FIELDS = [
    "ticket_id", "severity", "expected_response_min",
    "actual_response_min", "breach_delta_min"
]

VALID_SEVERITIES = {"L1", "L2", "L3", "L4"}


def validate_ticket(ticket: dict) -> list[str]:
    """Return list of validation errors for a ticket."""
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in ticket:
            errors.append(f"Missing field: {field}")
    if "severity" in ticket and ticket["severity"] not in VALID_SEVERITIES:
        errors.append(f"Invalid severity: {ticket['severity']}")
    if "breach_delta_min" in ticket and "actual_response_min" in ticket and "expected_response_min" in ticket:
        try:
            delta = float(ticket["breach_delta_min"])
            actual = float(ticket["actual_response_min"])
            expected = float(ticket["expected_response_min"])
            if abs(delta - (actual - expected)) > 0.01:
                errors.append(
                    f"Arithmetic error: breach_delta_min={delta} != actual-expected={actual-expected:.2f}"
                )
        except (TypeError, ValueError):
            errors.append("Non-numeric response fields")
    return errors


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: validate_ticket_sla.py <breach_file.json>"}))
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(json.dumps({"error": f"File not found: {path}"}))
        sys.exit(1)

    data = json.loads(path.read_text(encoding="utf-8"))
    tickets = data if isinstance(data, list) else data.get("tickets", [])

    validated_count = 0
    error_count = 0
    invalid_ticket_ids = []

    for ticket in tickets:
        errors = validate_ticket(ticket)
        if errors:
            error_count += 1
            tid = ticket.get("ticket_id", "UNKNOWN")
            invalid_ticket_ids.append(tid)
        else:
            validated_count += 1

    result = {
        "validated_count": validated_count,
        "error_count": error_count,
        "invalid_ticket_ids": invalid_ticket_ids
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
