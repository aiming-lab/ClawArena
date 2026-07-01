#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_sar_draft.py — Generate SAR (Suspicious Activity Report) draft.

Uses FinCEN Form 111 five-W narrative structure.

Source: https://www.fincen.gov/resources/frequently-asked-questions-regarding-fincen-suspicious-activity-report-sar
        https://www.fluxforce.ai/regulations/us-fincen-suspicious-activity-report-sar

Filing deadline: 30 calendar days from first detection (standard case)
                 60 calendar days if no suspect identified
Bank filing threshold: $5,000
Form: FinCEN Form 111
"""
import json
import sys
from datetime import date, timedelta
from pathlib import Path


def generate_sar(case: dict) -> dict:
    """Generate SAR draft for a given case."""
    detection_date = date.fromisoformat(case["created_at"][:10])
    deadline = detection_date + timedelta(days=30)
    return {
        "schema_version": "1.0",
        "form_number": "FinCEN Form 111",
        "case_id": case["case_id"],
        "filing_deadline": deadline.isoformat(),
        "filing_deadline_days": 30,
        "amount_reported": case["amount_usd"],
        "narrative": {
            "who": "Describe the subject conducting suspicious activity",
            "what": "Describe the suspicious transaction type and pattern",
            "when": f"Activity detected on {detection_date.isoformat()}",
            "where": "Specify accounts and locations involved",
            "why": "Explain indicators of suspicious activity"
        },
        "source_url": "https://www.fincen.gov/resources/frequently-asked-questions-regarding-fincen-suspicious-activity-report-sar"
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: generate_sar_draft.py <case.json>")
        sys.exit(1)
    case = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    print(json.dumps(generate_sar(case), indent=2))
