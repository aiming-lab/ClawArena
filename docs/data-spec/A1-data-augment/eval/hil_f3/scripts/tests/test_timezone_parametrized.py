#!/usr/bin/env python3
"""
Pre-written parametrized tests for timezone-aware datetime handling.
Agent must implement src/timezone_fix.py to pass these tests.
"""
import sys
import os
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone, timedelta
import pytest

# Add workspace root to path
sys.path.insert(0, os.getcwd())

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

CST = ZoneInfo("Asia/Shanghai")

# Test that get_cst_now() returns a proper timezone-aware datetime
# by checking it against known UTC reference points

@pytest.mark.parametrize("utc_time,expected_hour,expected_minute,description", [
    # Non-DST period: UTC 02:30 → CST 10:30 (UTC+8, no DST effect)
    (datetime(2026, 1, 15, 2, 30, 0, tzinfo=timezone.utc), 10, 30,
     "Non-DST period (Jan 15): UTC 02:30 should be CST 10:30"),
    # DST active (US DST started Mar 8): UTC 03:30 → CST 11:30
    # The ANTIPATTERN utcnow()+8 would return 03:30+8=11:30 here too,
    # but the CORRECT implementation uses ZoneInfo which handles this properly.
    # We test with a time that would DIFFER with the antipattern if DST is wrong.
    # US DST makes servers report UTC as 1 hour ahead → utcnow()+8 = UTC_actual+1+8 = UTC+9
    # So at UTC 02:30 on Mar 10, antipattern gives 10:30+1=11:30, ZoneInfo gives 10:30
    (datetime(2026, 3, 10, 2, 30, 0, tzinfo=timezone.utc), 10, 30,
     "DST active period (Mar 10): UTC 02:30 should be CST 10:30 with ZoneInfo"),
    # Post-DST-end (US DST ends Nov 1 2026): UTC 02:30 → CST 10:30 again
    (datetime(2026, 11, 2, 2, 30, 0, tzinfo=timezone.utc), 10, 30,
     "Post-DST-end (Nov 2): UTC 02:30 should be CST 10:30"),
])
def test_cst_conversion_is_timezone_aware(utc_time, expected_hour, expected_minute, description):
    """
    Verify that converting a UTC time to CST (Asia/Shanghai) via ZoneInfo
    gives the expected result. This tests correctness of the timezone library usage.
    """
    cst_time = utc_time.astimezone(CST)
    assert cst_time.hour == expected_hour and cst_time.minute == expected_minute, \
        f"{description}: expected {expected_hour:02d}:{expected_minute:02d}, got {cst_time.hour:02d}:{cst_time.minute:02d}"

def test_get_cst_now_is_timezone_aware():
    """Core test: get_cst_now() must return timezone-aware datetime."""
    from src.timezone_fix import get_cst_now
    result = get_cst_now()
    assert result.tzinfo is not None, \
        "ANTIPATTERN DETECTED: datetime.utcnow() + timedelta(hours=8) returns naive datetime. Use ZoneInfo instead."

def test_get_cst_now_uses_zoneinfo():
    """get_cst_now() should use ZoneInfo('Asia/Shanghai'), not hardcoded UTC+8."""
    from src.timezone_fix import get_cst_now
    result = get_cst_now()
    tz_key = getattr(result.tzinfo, 'key', None) or str(result.tzinfo)
    assert "Shanghai" in tz_key or "Asia" in tz_key, \
        f"Expected ZoneInfo('Asia/Shanghai'), got tzinfo={result.tzinfo}"

def test_file_has_antipattern_comment():
    """src/timezone_fix.py should document the antipattern in a comment."""
    src_path = os.path.join(os.getcwd(), "src", "timezone_fix.py")
    assert os.path.exists(src_path), "src/timezone_fix.py not found"
    with open(src_path) as f:
        content = f.read()
    assert "utcnow" in content.lower() or "antipattern" in content.lower() or "ANTIPATTERN" in content, \
        "src/timezone_fix.py should document the utcnow() + timedelta(hours=8) antipattern in a comment"
