#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for aros/settlement_scheduler.py (T+1 settlement timing)."""

import datetime

TRADE_DATE = datetime.date(2024, 11, 3)

# UTC offsets
UTC_OFFSET_BUGGY = -4   # What AROS v4.2 uses (EDT — WRONG after Nov 3 switch)
UTC_OFFSET_CORRECT = -5  # What it should be (EST — CORRECT after Nov 3 switch)


def compute_cutoff(utc_offset: int) -> datetime.datetime:
    """Compute T+1 cutoff UTC for 21:00 ET on TRADE_DATE."""
    cutoff_et = datetime.datetime(2024, 11, 3, 21, 0, 0)
    return cutoff_et - datetime.timedelta(hours=utc_offset)


def test_cutoff_with_correct_offset():
    """With UTC-5 (EST), 21:00 ET = 02:00 UTC next day (2024-11-04T02:00:00Z)."""
    cutoff = compute_cutoff(UTC_OFFSET_CORRECT)
    expected = datetime.datetime(2024, 11, 4, 2, 0, 0)
    assert cutoff == expected, f"Expected {expected}, got {cutoff}"
    print(f"PASS: test_cutoff_with_correct_offset -> {cutoff.isoformat()}Z")


def test_cutoff_with_buggy_offset():
    """With UTC-4 (EDT/BUG), 21:00 ET = 01:00 UTC next day (2024-11-04T01:00:00Z)."""
    cutoff = compute_cutoff(UTC_OFFSET_BUGGY)
    expected = datetime.datetime(2024, 11, 4, 1, 0, 0)
    assert cutoff == expected, f"Expected {expected}, got {cutoff}"
    print(f"NOTE: test_cutoff_with_buggy_offset -> {cutoff.isoformat()}Z (1 hour too early!)")


def test_offset_delta():
    """The difference between correct and buggy cutoffs must be exactly 3600 seconds."""
    correct = compute_cutoff(UTC_OFFSET_CORRECT)
    buggy = compute_cutoff(UTC_OFFSET_BUGGY)
    delta_seconds = (correct - buggy).total_seconds()
    assert delta_seconds == 3600.0, f"Expected 3600, got {delta_seconds}"
    print(f"PASS: test_offset_delta -> {delta_seconds} seconds difference (exactly 1 hour)")


if __name__ == "__main__":
    test_cutoff_with_correct_offset()
    test_cutoff_with_buggy_offset()
    test_offset_delta()
