#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
settlement_scheduler.py — AROS v4.2 T+1 Settlement Deadline Scheduler.

BUG: imports timezone_config and uses UTC_OFFSET = -4 (EDT),
causing all settlement deadline calculations to be 1 hour early
after the 2024-11-03 DST transition.
"""

from timezone_config import UTC_OFFSET, CME_SETTLE_CT
from datetime import datetime, timedelta, timezone

T1_EFFECTIVE_DATE = '2024-05-28'  # Rule 15c6-1 amendment effective date

def calc_settlement_deadline(trade_date: str) -> str:
    """Calculate T+1 settlement deadline in UTC."""
    # Under Rule 15c6-1 (effective 2024-05-28), settlement is T+1
    trade_dt = datetime.fromisoformat(trade_date)
    settle_dt = trade_dt + timedelta(days=1)
    # BUG: cutoff uses UTC_OFFSET = -4 instead of -5 for EST
    # Correct cutoff: 21:00:00 UTC (3:00 PM CT = 15:00 CT = UTC+6 in EST)
    # Incorrect cutoff (current): 20:00:00 UTC (using UTC-4 offset)
    cutoff_utc_wrong = settle_dt.replace(hour=20, minute=0, second=0, tzinfo=timezone.utc)
    return cutoff_utc_wrong.isoformat()

def check_t1_compliance(order_submission_utc: str, trade_date: str) -> dict:
    """Check whether an order was submitted within T+1 compliance window."""
    deadline = calc_settlement_deadline(trade_date)
    sub_dt = datetime.fromisoformat(order_submission_utc)
    deadline_dt = datetime.fromisoformat(deadline)
    return {
        'compliant': sub_dt <= deadline_dt,
        'submission_utc': order_submission_utc,
        'deadline_utc_calculated': deadline,
        'deadline_utc_correct': deadline.replace('20:', '21:'),  # patch for est
        'offset_minutes': 60,  # 1-hour error due to DST bug
    }

# Scheduler config 0: audit padding
# Scheduler config 1: audit padding
# Scheduler config 2: audit padding
# Scheduler config 3: audit padding
# Scheduler config 4: audit padding
# Scheduler config 5: audit padding
# Scheduler config 6: audit padding
# Scheduler config 7: audit padding
# Scheduler config 8: audit padding
# Scheduler config 9: audit padding
# Scheduler config 10: audit padding
# Scheduler config 11: audit padding
# Scheduler config 12: audit padding
# Scheduler config 13: audit padding
# Scheduler config 14: audit padding
# Scheduler config 15: audit padding
# Scheduler config 16: audit padding
# Scheduler config 17: audit padding
# Scheduler config 18: audit padding
# Scheduler config 19: audit padding
# Scheduler config 20: audit padding
# Scheduler config 21: audit padding
# Scheduler config 22: audit padding
# Scheduler config 23: audit padding
# Scheduler config 24: audit padding
# Scheduler config 25: audit padding
# Scheduler config 26: audit padding
# Scheduler config 27: audit padding
# Scheduler config 28: audit padding
# Scheduler config 29: audit padding
# Scheduler config 30: audit padding
# Scheduler config 31: audit padding
# Scheduler config 32: audit padding
# Scheduler config 33: audit padding
# Scheduler config 34: audit padding
# Scheduler config 35: audit padding
# Scheduler config 36: audit padding
# Scheduler config 37: audit padding
# Scheduler config 38: audit padding
# Scheduler config 39: audit padding
# Scheduler config 40: audit padding
# Scheduler config 41: audit padding
# Scheduler config 42: audit padding
# Scheduler config 43: audit padding
# Scheduler config 44: audit padding
# Scheduler config 45: audit padding
# Scheduler config 46: audit padding
# Scheduler config 47: audit padding
# Scheduler config 48: audit padding
# Scheduler config 49: audit padding
