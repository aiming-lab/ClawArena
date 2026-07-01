#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_report.py — Generate escalation report from breach tickets.

Usage: python generate_report.py <breach_tickets_v3.json> <output_report.json>
"""
import sys
import json
from pathlib import Path
from datetime import datetime, timezone


def main():
    if len(sys.argv) < 3:
        print("Usage: generate_report.py <breach_file> <output_file>")
        sys.exit(1)

    breach_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    data = json.loads(breach_path.read_text(encoding="utf-8"))
    tickets = data if isinstance(data, list) else data.get("tickets", [])

    by_sev = {}
    for t in tickets:
        sev = t.get("severity", "UNKNOWN")
        by_sev.setdefault(sev, []).append(t)

    top = sorted(tickets, key=lambda x: x.get("breach_delta_min", 0), reverse=True)[:5]

    report = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "agent_id": "supportops-ai",
            "schema_version": "1.0"
        },
        "report_period": "2024-11",
        "sla_policy_version": "v1",
        "breach_summary": {
            "total_breaches": len(tickets),
            "by_severity": {k: len(v) for k, v in by_sev.items()}
        },
        "top_breached_tickets": top[:5],
        "credit_recommendations": [],
        "reviewer_signature": ""
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Report written to {output_path}")


if __name__ == "__main__":
    main()
