#!/usr/bin/env python3
"""Test suite for agent-written src/timezone_fix.py."""
import sys
import os
import pytest

# Add workspace root to path (workspace is cwd when running tests)
sys.path.insert(0, os.getcwd())

def test_get_cst_now_exists():
    """get_cst_now function must exist."""
    from src.timezone_fix import get_cst_now
    assert callable(get_cst_now)

def test_get_cst_now_returns_datetime():
    """get_cst_now must return a datetime object."""
    from datetime import datetime
    from src.timezone_fix import get_cst_now
    result = get_cst_now()
    assert isinstance(result, datetime)

def test_get_cst_now_is_timezone_aware():
    """Return value must be timezone-aware (tzinfo is not None)."""
    from src.timezone_fix import get_cst_now
    result = get_cst_now()
    assert result.tzinfo is not None, "get_cst_now() must return timezone-aware datetime, not naive"

def test_get_cst_now_uses_asia_shanghai():
    """Return value must use Asia/Shanghai timezone, not hardcoded UTC+8."""
    from src.timezone_fix import get_cst_now
    result = get_cst_now()
    tz_str = str(result.tzinfo)
    # Accept both ZoneInfo and pytz representations of Asia/Shanghai
    assert "Shanghai" in tz_str or "CST" in tz_str or "+08:00" in tz_str, \
        f"Expected Asia/Shanghai timezone, got: {tz_str}"

def test_src_does_not_use_utcnow_plus_8():
    """src/timezone_fix.py must not contain the antipattern utcnow() + timedelta."""
    src_path = os.path.join(os.getcwd(), "src", "timezone_fix.py")
    assert os.path.exists(src_path), "src/timezone_fix.py does not exist"
    with open(src_path) as f:
        content = f.read()
    # Should not have the antipattern as actual code (comments allowed)
    lines = [l for l in content.split('\n') if not l.strip().startswith('#')]
    code_only = '\n'.join(lines)
    assert not ("utcnow()" in code_only and "timedelta(hours=8)" in code_only), \
        "src/timezone_fix.py must not use datetime.utcnow() + timedelta(hours=8) antipattern"
