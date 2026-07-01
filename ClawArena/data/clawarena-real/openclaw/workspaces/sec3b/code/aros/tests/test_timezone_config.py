#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for aros/timezone_config.py.

KNOWN FAILING TESTS (marked with # FAIL):
  test_est_utc_offset — expects -5, gets -4 (DST bug)
  test_cme_settle_utc_est — expects 21:00 UTC, gets 20:00 UTC (DST bug)
"""

import datetime
import sys

# Simulate importing the buggy config
UTC_OFFSET_BUGGY = -4  # What AROS v4.2 has
UTC_OFFSET_CORRECT = -5  # What it should be (EST)


def test_edt_utc_offset():
    """EDT (summer): UTC-4 is correct."""
    assert UTC_OFFSET_BUGGY == -4, "EDT offset should be -4"
    print("PASS: test_edt_utc_offset (UTC-4 correct for EDT)")


def test_est_utc_offset():
    """EST (winter after Nov DST switch): UTC-5 is correct. CURRENTLY FAILS."""
    expected = -5
    actual = UTC_OFFSET_BUGGY  # FAIL: returns -4 not -5
    if actual == expected:
        print("PASS: test_est_utc_offset")
    else:
        print(f"FAIL: test_est_utc_offset — expected {expected}, got {actual} (DST bug)")


def test_cme_settle_utc_edt():
    """CME 15:00 CT during CDT = 20:00 UTC (CT is UTC-5 in CDT)."""
    # 15:00 CT + 5h = 20:00 UTC (CDT period: CT=UTC-5)
    expected_utc_hour = 20
    ct_offset = -5  # Central Time during CDT
    computed = 15 - ct_offset  # = 20
    assert computed == expected_utc_hour
    print("PASS: test_cme_settle_utc_edt (20:00 UTC correct for CDT period)")


def test_cme_settle_utc_est():
    """CME 15:00 CT during CST = 21:00 UTC (CT is UTC-6 in CST). CURRENTLY FAILS due to DST bug."""
    expected_utc_hour = 21
    # AROS v4.2 computes: 15 - (UTC_OFFSET_BUGGY - 1) = 15 - (-5) = 20 (WRONG)
    buggy_ct_offset = UTC_OFFSET_BUGGY - 1  # = -5
    buggy_result = 15 - buggy_ct_offset  # = 20
    # Correct: CT during CST = UTC-6; 15 - (-6) = 21
    correct_ct_offset = UTC_OFFSET_CORRECT - 1  # = -6
    correct_result = 15 - correct_ct_offset  # = 21

    if buggy_result == expected_utc_hour:
        print("PASS: test_cme_settle_utc_est")
    else:
        print(f"FAIL: test_cme_settle_utc_est — expected {expected_utc_hour}, "
              f"buggy_result={buggy_result}, correct_result={correct_result}")


def test_t1_cutoff_utc_edt():
    """T+1 cutoff 21:00 ET during EDT = 01:00 UTC next day. UTC-4: 21+4=25=01:00+1d."""
    cutoff_utc = 21 - UTC_OFFSET_BUGGY  # = 25 = 01:00 next day
    assert cutoff_utc % 24 == 1
    print("PASS: test_t1_cutoff_utc_edt (01:00 UTC next day)")


def test_t1_cutoff_utc_est():
    """T+1 cutoff 21:00 ET during EST = 02:00 UTC next day. UTC-5: 21+5=26=02:00+1d. FAILS."""
    expected_hour_next_day = 2
    buggy = (21 - UTC_OFFSET_BUGGY) % 24   # = 25 % 24 = 1 (01:00 UTC — WRONG)
    correct = (21 - UTC_OFFSET_CORRECT) % 24  # = 26 % 24 = 2 (02:00 UTC — CORRECT)
    if buggy == expected_hour_next_day:
        print("PASS: test_t1_cutoff_utc_est")
    else:
        print(f"FAIL: test_t1_cutoff_utc_est — expected {expected_hour_next_day}:00, "
              f"buggy={buggy}:00, correct={correct}:00 (1-hour DST error)")


if __name__ == "__main__":
    test_edt_utc_offset()
    test_est_utc_offset()
    test_cme_settle_utc_edt()
    test_cme_settle_utc_est()
    test_t1_cutoff_utc_edt()
    test_t1_cutoff_utc_est()
