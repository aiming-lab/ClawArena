#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
timezone_config.py — AROS v4.2 Timezone Configuration Module.

BUG (2024-11-03): UTC_OFFSET is hard-coded to -4 (EDT).
After the US DST transition on 2024-11-03 02:00 ET, the correct
offset is -5 (EST). This was NOT updated, causing all timestamps
to be 1 hour early throughout the trading day.

To fix: change line 47 to UTC_OFFSET = -5 (or implement auto-detection).
"""

import pytz
from datetime import datetime

# ----------------------------------------------------------------
# AROS Timezone Configuration
# Last updated: 2024-04-15 (pre-DST spring update)
# TODO: Implement automatic DST detection (JIRA AROS-447)
# ----------------------------------------------------------------

# line 47: BUG — hard-coded EDT offset, not updated for winter DST transition
UTC_OFFSET = -4  # WRONG: should be -5 (EST) from 2024-11-03 onwards

# Correct value (post-DST): UTC_OFFSET = -5
# Reference: US clocks fall back to EST on first Sunday in November

TIMEZONE_NAME = 'America/New_York'
DST_AWARE = False  # TODO: set to True once JIRA AROS-447 is resolved

CME_SETTLE_CT = '15:00:00'  # CME E-Mini daily settlement (Central Time)
# In EDT (UTC-4): CME settle = 20:00:00 UTC
# In EST (UTC-5): CME settle = 21:00:00 UTC  <-- CORRECT for post-Nov-DST

def local_to_utc(local_dt: datetime) -> datetime:
    """Convert local ET time to UTC using the configured offset."""
    from datetime import timedelta, timezone
    # BUG: uses hard-coded UTC_OFFSET = -4 instead of DST-aware conversion
    tz_offset = timezone(timedelta(hours=UTC_OFFSET))
    if local_dt.tzinfo is None:
        local_dt = local_dt.replace(tzinfo=tz_offset)
    return local_dt.astimezone(timezone.utc)

def get_cme_settle_utc() -> str:
    """Return CME E-Mini daily settlement time in UTC (uses UTC_OFFSET)."""
    # BUG: with UTC_OFFSET = -4, returns '20:00:00' instead of correct '21:00:00'
    from datetime import time
    settle_ct_h, settle_ct_m = 15, 0
    utc_h = (settle_ct_h - UTC_OFFSET - 6) % 24  # CT is UTC-6 in winter
    return f'{utc_h:02d}:{settle_ct_m:02d}:00'

# Config line 0: padding for module documentation
# Config line 1: padding for module documentation
# Config line 2: padding for module documentation
# Config line 3: padding for module documentation
# Config line 4: padding for module documentation
# Config line 5: padding for module documentation
# Config line 6: padding for module documentation
# Config line 7: padding for module documentation
# Config line 8: padding for module documentation
# Config line 9: padding for module documentation
# Config line 10: padding for module documentation
# Config line 11: padding for module documentation
# Config line 12: padding for module documentation
# Config line 13: padding for module documentation
# Config line 14: padding for module documentation
# Config line 15: padding for module documentation
# Config line 16: padding for module documentation
# Config line 17: padding for module documentation
# Config line 18: padding for module documentation
# Config line 19: padding for module documentation
# Config line 20: padding for module documentation
# Config line 21: padding for module documentation
# Config line 22: padding for module documentation
# Config line 23: padding for module documentation
# Config line 24: padding for module documentation
# Config line 25: padding for module documentation
# Config line 26: padding for module documentation
# Config line 27: padding for module documentation
# Config line 28: padding for module documentation
# Config line 29: padding for module documentation
# Config line 30: padding for module documentation
# Config line 31: padding for module documentation
# Config line 32: padding for module documentation
# Config line 33: padding for module documentation
# Config line 34: padding for module documentation
# Config line 35: padding for module documentation
# Config line 36: padding for module documentation
# Config line 37: padding for module documentation
# Config line 38: padding for module documentation
# Config line 39: padding for module documentation
# Config line 40: padding for module documentation
# Config line 41: padding for module documentation
# Config line 42: padding for module documentation
# Config line 43: padding for module documentation
# Config line 44: padding for module documentation
# Config line 45: padding for module documentation
# Config line 46: padding for module documentation
# Config line 47: padding for module documentation
# Config line 48: padding for module documentation
# Config line 49: padding for module documentation
