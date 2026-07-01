#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aros/order_router.py — AROS v4.2 Automated Order Router (Core)

Routes orders through venue selection, risk checks, and settlement scheduling.
References UTC-4 offset from timezone_config (bug source for 2024-11-03 incident).

This file is part of AROS v4.2. For the deprecated v3.1 router, see:
  code/legacy/aros_v3_1_router_DEPRECATED.py
  (DO NOT USE — deprecated 2023-06-01; incompatible with MiFIR Field 28 UTC requirement)
"""

import datetime
import hashlib
import json
import logging
from dataclasses import dataclass, field
from typing import Optional, List, Dict

from .timezone_config import UTC_OFFSET, get_t1_cutoff_utc, DST_AWARE
from .settlement_scheduler import SettlementScheduler

logger = logging.getLogger(__name__)

AROS_ROUTER_VERSION = "4.2.1"
SUPPORTED_INSTRUMENTS = ["ESZ4", "NQZ4", "RTYH5", "YMH5", "MES"]
SUPPORTED_VENUES = ["CME", "ICE", "CBOE", "NYSE"]

# Risk limits
MAX_ORDER_QTY = 200
MAX_NOTIONAL_USD = 10_000_000
DAILY_LOSS_LIMIT_USD = 500_000

# MiFIR reporting requirement
MIFIR_FIELD28_TZ = "UTC"  # Must be UTC per FCA Market Watch 59 / RTS 22 Field 28


@dataclass
class Order:
    order_id: str
    instrument: str
    side: str  # BUY or SELL
    quantity: int
    price: float
    order_type: str  # MARKET_MAKE, DELTA_HEDGE, T1_SETTLEMENT, REBALANCE
    submission_time_utc: datetime.datetime
    venue: str = "CME"
    settlement_date: Optional[datetime.date] = None
    mifir_field28: Optional[str] = None  # Must be UTC string
    flags: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "instrument": self.instrument,
            "side": self.side,
            "quantity": self.quantity,
            "price": self.price,
            "order_type": self.order_type,
            "submission_time_utc": self.submission_time_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "venue": self.venue,
            "settlement_date": self.settlement_date.isoformat() if self.settlement_date else None,
            "mifir_field28": self.mifir_field28,
            "flags": self.flags,
        }


class OrderRouter:
    """
    AROS v4.2 core order router.

    BUG: Uses DST-unaware timezone_config for settlement window calculations.
    On 2024-11-03 after DST switch, T+1 settlement orders are 1 hour off.
    """

    def __init__(self, trade_date: datetime.date):
        self.trade_date = trade_date
        self.scheduler = SettlementScheduler(trade_date)
        self._order_count = 0
        self._rejected = 0
        logger.info(
            "OrderRouter v%s initialized; trade_date=%s; T1_cutoff_utc=%s; UTC_OFFSET=%d",
            AROS_ROUTER_VERSION, trade_date,
            self.scheduler.cutoff_utc.strftime("%Y-%m-%dT%H:%M:%SZ"), UTC_OFFSET
        )

    def _gen_order_id(self, instrument: str) -> str:
        ts = datetime.datetime.utcnow().isoformat()
        h = hashlib.md5(f"{instrument}:{ts}:{self._order_count}".encode()).hexdigest()[:12]
        return f"ORD-{h.upper()}"

    def _check_risk(self, order: Order) -> Optional[str]:
        """Pre-trade risk check. Returns rejection reason or None if OK."""
        if order.quantity > MAX_ORDER_QTY:
            return f"qty {order.quantity} exceeds max {MAX_ORDER_QTY}"
        if order.quantity * order.price > MAX_NOTIONAL_USD:
            return f"notional ${order.quantity * order.price:,.0f} exceeds limit"
        return None

    def route(self, instrument: str, side: str, qty: int, price: float,
              order_type: str = "MARKET_MAKE") -> Order:
        """Route a single order through risk checks and settlement scheduling."""
        self._order_count += 1
        now_utc = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

        order = Order(
            order_id=self._gen_order_id(instrument),
            instrument=instrument,
            side=side,
            quantity=qty,
            price=price,
            order_type=order_type,
            submission_time_utc=now_utc,
            venue="CME" if instrument.startswith("ES") else "ICE",
        )

        # Risk check
        rejection = self._check_risk(order)
        if rejection:
            self._rejected += 1
            order.flags.append(f"REJECTED:{rejection}")
            logger.warning("Order rejected: %s", rejection)
            return order

        # Settlement scheduling (buggy: uses UTC_OFFSET = -4 instead of -5)
        order.settlement_date = self.scheduler.get_settlement_date(now_utc)

        # MiFIR Field 28 — Must be UTC per FCA Market Watch 59
        # BUG: system was submitting LOCAL time (UTC-4) instead of UTC
        # This is the compliance violation identified in FCA inquiry
        order.mifir_field28 = now_utc.strftime("%Y-%m-%dT%H:%M:%S.000Z")  # Correct (UTC)
        # Pre-fix (buggy) version was:
        # order.mifir_field28 = (now_utc + timedelta(hours=UTC_OFFSET)).strftime(...)  # WRONG

        return order

    def get_stats(self) -> dict:
        return {
            "total_orders": self._order_count,
            "rejected": self._rejected,
            "utc_offset_used": UTC_OFFSET,
            "dst_aware": DST_AWARE,
        }


# --------------------------------------------------------------------------
# Standalone helpers (used by risk_monitor.py and backtest scripts)
# --------------------------------------------------------------------------

def compute_t1_cutoff_utc(trade_date: datetime.date, utc_offset: int) -> datetime.datetime:
    """
    Compute T+1 settlement cutoff in UTC given a UTC offset for ET.
    Rule 15c6-1: cutoff = 21:00 ET = (21:00 - utc_offset) UTC.

    Correct usage:
      compute_t1_cutoff_utc(date(2024, 11, 3), -5)  # EST → 02:00 UTC next day
    Bug usage (AROS v4.2):
      compute_t1_cutoff_utc(date(2024, 11, 3), -4)  # EDT → 01:00 UTC next day (wrong)
    """
    cutoff_local = datetime.datetime(
        trade_date.year, trade_date.month, trade_date.day, 21, 0, 0
    )
    return cutoff_local - datetime.timedelta(hours=utc_offset)
