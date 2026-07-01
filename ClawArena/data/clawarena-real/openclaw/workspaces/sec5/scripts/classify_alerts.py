#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
classify_alerts.py — Classify fraud alerts into priority levels.

Priority rules:
  critical : score >= 0.85
  high     : score >= 0.65
  medium   : score >= 0.45
  low      : score < 0.45

Escalation: amount_usd >= $50000
"""
import json
import sys
from pathlib import Path


def classify(score: float, amount: float) -> dict:
    """Return priority and escalation flag."""
    if score >= 0.85:
        priority = "critical"
    elif score >= 0.65:
        priority = "high"
    elif score >= 0.45:
        priority = "medium"
    else:
        priority = "low"
    return {
        "priority": priority,
        "escalation_required": amount >= 50000,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: classify_alerts.py <alert_batch.json>")
        sys.exit(1)
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    alerts = data.get("alerts", [])
    for alert in alerts:
        result = classify(alert["score"], alert.get("amount_usd", 0))
        alert.update(result)
    print(json.dumps(data, indent=2))
