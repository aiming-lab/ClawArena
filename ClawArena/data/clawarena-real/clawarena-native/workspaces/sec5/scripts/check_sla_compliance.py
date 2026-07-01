#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_sla_compliance.py — Check SLA compliance for fraud investigation cases.

SLA rules (from Hyperbots Fraud Investigation SLA):
  Alert response    : 2 hours
  Case resolution   : 3 business days
  Escalation        : amount >= $50,000

Source: https://www.hyperbots.com/glossary/fraud-investigation-sla
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ALERT_RESPONSE_HOURS = 2
CASE_RESOLUTION_DAYS = 3
ESCALATION_THRESHOLD_USD = 50000


def check_sla(case: dict, now: datetime = None) -> dict:
    """Check SLA compliance for a case."""
    if now is None:
        now = datetime.now(timezone.utc)
    created = datetime.fromisoformat(case["created_at"].replace("Z", "+00:00"))
    deadline = datetime.fromisoformat(case["sla_deadline"].replace("Z", "+00:00"))
    hours_remaining = (deadline - now).total_seconds() / 3600
    return {
        "case_id": case["case_id"],
        "sla_remaining_hours": round(hours_remaining, 2),
        "sla_breached": hours_remaining < 0,
        "escalation_required": case.get("amount_usd", 0) >= ESCALATION_THRESHOLD_USD,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: check_sla_compliance.py <cases.json>")
        sys.exit(1)
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    cases = data.get("cases", [])
    for case in cases:
        result = check_sla(case)
        print(json.dumps(result))
