#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_dsar_deadlines.py — DSAR deadline compliance checker.

Reads dsar_queue.csv and flags requests that are overdue based on the
Art. 12(3) 1-calendar-month (30-day) response deadline.

Usage: python scripts/check_dsar_deadlines.py <dsar_queue_csv>
"""
import csv
import sys
from datetime import date, timedelta
from pathlib import Path

DEADLINE_DAYS = 30  # Art. 12(3): 1 calendar month


def check_deadlines(path: str, today: date = None) -> dict:
    today = today or date.today()
    overdue = []
    in_time = []

    with Path(path).open(encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            req_date = date.fromisoformat(row["request_date"])
            deadline = req_date + timedelta(days=DEADLINE_DAYS)
            if row["status"] != "COMPLETED" and deadline < today:
                overdue.append({
                    "case_id": row["case_id"],
                    "request_date": row["request_date"],
                    "deadline": deadline.isoformat(),
                    "days_overdue": (today - deadline).days,
                })
            else:
                in_time.append(row["case_id"])

    return {
        "check_date": today.isoformat(),
        "overdue_count": len(overdue),
        "in_time_count": len(in_time),
        "overdue": overdue,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python check_dsar_deadlines.py <dsar_queue_csv>")
        sys.exit(1)
    r = check_deadlines(sys.argv[1])
    import json
    print(json.dumps(r, indent=2))
