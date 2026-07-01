#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aros/settlement_scheduler.py — AROS v4.2 Settlement Scheduler

Manages T+1 settlement deadlines and CME daily settlement triggers.
Contains known DST bug: inherits UTC_OFFSET from timezone_config.py.
After 2024-11-03 DST switch, all settlement time calculations are
offset by +60 minutes from correct UTC.
"""

import datetime
import logging
from pathlib import Path

# Import the buggy timezone config
from .timezone_config import (
    UTC_OFFSET, CME_SETTLE_UTC_HOUR_SYSTEM,
    get_t1_cutoff_utc, get_cme_settle_utc,
    DST_AWARE,
)

logger = logging.getLogger(__name__)

# =============================================================================
# T+1 SETTLEMENT SCHEDULER
# =============================================================================

class SettlementScheduler:
    """
    Schedules T+1 settlement deadline checks per SEC Rule 15c6-1.
    Rule 15c6-1 amendments effective 2024-05-28 require T+1 settlement
    for equities, corporate debt, and unit investment trusts.

    BUG: DST-unaware — cutoff times will be 1 hour incorrect after
    November 3, 2024 DST transition until UTC_OFFSET is corrected.
    """

    def __init__(self, trade_date: datetime.date):
        self.trade_date = trade_date
        self._cutoff_utc = get_t1_cutoff_utc(trade_date)
        if not DST_AWARE:
            logger.warning(
                "SettlementScheduler initialized with DST_AWARE=False; "
                "UTC_OFFSET=%d may be stale after DST transition", UTC_OFFSET
            )

    @property
    def cutoff_utc(self) -> datetime.datetime:
        """T+1 settlement cutoff in UTC. BUG: 1 hour wrong after DST switch."""
        return self._cutoff_utc

    def is_within_window(self, order_time_utc: datetime.datetime) -> bool:
        """
        Check if an order timestamp is within the T+1 settlement window.
        Returns True if order_time_utc <= cutoff_utc.
        BUG: cutoff is 1 hour early after DST switch.
        """
        return order_time_utc <= self._cutoff_utc

    def get_settlement_date(self, order_time_utc: datetime.datetime) -> datetime.date:
        """
        Return settlement date (T+1) for an order.
        BUG: Window boundary calculation uses wrong UTC offset.
        """
        if self.is_within_window(order_time_utc):
            # Order is within T+1 window for trade_date
            return self.trade_date + datetime.timedelta(days=1)
        else:
            # Order misses today's T+1 window, settles T+2
            return self.trade_date + datetime.timedelta(days=2)

    def describe(self) -> dict:
        """Return a summary of scheduler configuration (for audit purposes)."""
        return {
            "trade_date": self.trade_date.isoformat(),
            "t1_rule": "Rule 15c6-1 (effective 2024-05-28)",
            "cutoff_utc_system": self._cutoff_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "utc_offset_used": UTC_OFFSET,
            "dst_aware": DST_AWARE,
            "known_bug": "UTC_OFFSET hardcoded; 1-hour error after 2024-11-03 DST switch",
        }
