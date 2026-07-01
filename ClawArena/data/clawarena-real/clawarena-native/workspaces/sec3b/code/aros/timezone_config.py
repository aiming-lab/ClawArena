#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aros/timezone_config.py — AROS v4.2 Timezone Configuration Module

WARNING: This file contains a known BUG introduced at deployment on 2024-10-15.
The UTC_OFFSET is hardcoded as -4 (America/New_York EDT) and does NOT
automatically update when the US Eastern timezone switches to EST (UTC-5)
on the first Sunday of November.

The BUG is on line 42: UTC_OFFSET = -4
The CORRECT value after 2024-11-03 02:00 local time should be: UTC_OFFSET = -5
"""

import datetime
import logging

logger = logging.getLogger(__name__)

# =============================================================================
# VERSION INFORMATION
# =============================================================================
AROS_VERSION = "4.2.1"
CONFIG_FILE_VERSION = "2024.10.15"
DEPLOYED_BY = "kenji.nakamura@artemisq.com"
DEPLOYMENT_DATE = "2024-10-15"

# =============================================================================
# TIMEZONE CONFIGURATION
# =============================================================================

# BUG: This value was set during EDT (UTC-4) and was NOT updated when
# US Eastern switched to EST (UTC-5) on 2024-11-03.
# See incident report: aros_v4_2_audit_log.jsonl events starting 2024-11-03T14:00:00Z
UTC_OFFSET = -4  # line 42 — BUG: should be -5 (EST) after 2024-11-03 switch

# The CORRECT timezone for post-DST-switch operation:
# UTC_OFFSET_CORRECT = -5  # EST (Eastern Standard Time), UTC-5

# Timezone abbreviation (also incorrect after switch)
TIMEZONE_ABBR = "EDT"  # BUG: should be "EST" after 2024-11-03
TIMEZONE_NAME = "America/New_York"

# DST awareness flag — DISABLED in this version
DST_AWARE = False  # Known deficiency; scheduled for v4.3 upgrade

# =============================================================================
# SETTLEMENT TIMING CONSTANTS
# =============================================================================

# CME E-Mini daily settlement: 15:00:00 CT
# In CDT (UTC-5 Central): 15:00 CDT = 20:00 UTC
# In CST (UTC-6 Central): 15:00 CST = 21:00 UTC
# NOTE: After US EST/EDT switch on 2024-11-03, ET becomes UTC-5,
# making CME Central Time UTC-6, so 15:00 CT = 21:00 UTC (NOT 20:00 UTC)
CME_DAILY_SETTLE_HOUR_CT = 15
CME_DAILY_SETTLE_MINUTE_CT = 0

# System's (incorrect) CME settlement UTC time
# BUG: system computes as 20:00 UTC because it uses UTC-4 offset for ET
# which then propagates to CT offset calculation
CME_SETTLE_UTC_HOUR_SYSTEM = 20  # BUG: should be 21 after DST switch

# T+1 Settlement cutoff (ET) per SEC Rule 15c6-1 (effective 2024-05-28)
T1_CUTOFF_HOUR_ET = 21  # 9:00 PM ET
T1_CUTOFF_MINUTE_ET = 0

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def get_utc_offset() -> int:
    """Return the configured UTC offset. WARNING: Does not handle DST."""
    logger.warning("UTC_OFFSET is static (%d); DST_AWARE=%s", UTC_OFFSET, DST_AWARE)
    return UTC_OFFSET


def local_to_utc(local_dt: datetime.datetime) -> datetime.datetime:
    """Convert local ET time to UTC using hardcoded offset. BUG: ignores DST."""
    utc = local_dt - datetime.timedelta(hours=UTC_OFFSET)
    logger.debug("local_to_utc: %s + (%d) = %s (DST-unaware)", local_dt, -UTC_OFFSET, utc)
    return utc


def utc_to_local(utc_dt: datetime.datetime) -> datetime.datetime:
    """Convert UTC to local ET time using hardcoded offset. BUG: ignores DST."""
    local = utc_dt + datetime.timedelta(hours=UTC_OFFSET)
    return local


def get_cme_settle_utc(trade_date: datetime.date) -> datetime.datetime:
    """
    Return CME daily settlement time in UTC for a given trade date.
    BUG: Returns 20:00 UTC on 2024-11-03 (should be 21:00 UTC after EST switch).
    """
    settle_local = datetime.datetime(
        trade_date.year, trade_date.month, trade_date.day,
        CME_DAILY_SETTLE_HOUR_CT, CME_DAILY_SETTLE_MINUTE_CT
    )
    # Approximate CT-to-UTC offset using ET offset - 1
    ct_utc_offset = UTC_OFFSET - 1
    settle_utc = settle_local - datetime.timedelta(hours=ct_utc_offset)
    return settle_utc


def get_t1_cutoff_utc(trade_date: datetime.date) -> datetime.datetime:
    """
    Return T+1 settlement cutoff in UTC for a given trade date.
    Under Rule 15c6-1 (effective 2024-05-28), cutoff is 21:00 ET.
    BUG: Returns wrong UTC time because UTC_OFFSET is -4 instead of -5.
    """
    cutoff_local = datetime.datetime(
        trade_date.year, trade_date.month, trade_date.day,
        T1_CUTOFF_HOUR_ET, T1_CUTOFF_MINUTE_ET
    )
    # BUG: uses UTC_OFFSET = -4; should use -5 (EST)
    cutoff_utc = cutoff_local - datetime.timedelta(hours=UTC_OFFSET)
    return cutoff_utc


# Legacy compatibility alias (do not use in new code)
OFFSET_HOURS = UTC_OFFSET
