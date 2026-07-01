#!/usr/bin/env python3
"""Test suite for agent-written scripts/trade_window_checker.py output."""
import sys
import os
import json
import subprocess
import pytest

sys.path.insert(0, os.getcwd())

@pytest.fixture(scope="module")
def violations_json():
    """Run the checker script and load output."""
    script = os.path.join(os.getcwd(), "scripts", "trade_window_checker.py")
    assert os.path.exists(script), "scripts/trade_window_checker.py does not exist"
    result = subprocess.run([sys.executable, script], capture_output=True, text=True, cwd=os.getcwd())
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    output_path = os.path.join(os.getcwd(), "analysis", "trade_window_violations.json")
    assert os.path.exists(output_path), "analysis/trade_window_violations.json was not created"
    with open(output_path) as f:
        return json.load(f)

def test_output_is_list(violations_json):
    assert isinstance(violations_json, list), "Output must be a JSON array"

def test_has_at_least_3_entries(violations_json):
    assert len(violations_json) >= 3, f"Expected >= 3 entries, got {len(violations_json)}"

def test_required_fields(violations_json):
    required = {"order_id", "actual_time", "delta_to_close_secs", "status", "near_miss"}
    for i, entry in enumerate(violations_json):
        for field in required:
            assert field in entry, f"Entry {i} missing field '{field}'"

def test_has_near_miss_entries(violations_json):
    near_miss_entries = [e for e in violations_json if e.get("near_miss") is True]
    assert len(near_miss_entries) >= 2, \
        f"Expected >= 2 near-miss entries (Mar 10 and Mar 11), got {len(near_miss_entries)}"

def test_has_rejected_entry(violations_json):
    rejected = [e for e in violations_json if e.get("status") == "REJECTED"]
    assert len(rejected) >= 1, "Expected at least 1 REJECTED entry (Mar 16)"

def test_delta_values_reasonable(violations_json):
    """Verify delta values are in plausible range (not all zeros)."""
    deltas = [e.get("delta_to_close_secs", 0) for e in violations_json]
    assert any(abs(d) > 0 for d in deltas), "All delta_to_close_secs are 0, likely not computed"
