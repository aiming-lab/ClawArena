#!/usr/bin/env python3
"""Test suite for agent-written scripts/compliance_timeline_builder.py output."""
import sys
import os
import json
import subprocess
import pytest

sys.path.insert(0, os.getcwd())

@pytest.fixture(scope="module")
def compliance_events():
    script = os.path.join(os.getcwd(), "scripts", "compliance_timeline_builder.py")
    assert os.path.exists(script), "scripts/compliance_timeline_builder.py does not exist"
    result = subprocess.run([sys.executable, script], capture_output=True, text=True, cwd=os.getcwd())
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    output_path = os.path.join(os.getcwd(), "analysis", "compliance_events.json")
    assert os.path.exists(output_path), "analysis/compliance_events.json was not created"
    with open(output_path) as f:
        return json.load(f)

def test_output_is_list(compliance_events):
    assert isinstance(compliance_events, list)

def test_has_at_least_2_entries(compliance_events):
    assert len(compliance_events) >= 2, f"Expected >= 2 notices, got {len(compliance_events)}"

def test_has_formal_status_field(compliance_events):
    for i, e in enumerate(compliance_events):
        assert "formal_status" in e, f"Entry {i} missing 'formal_status' field"

def test_has_informal_entry(compliance_events):
    informal = [e for e in compliance_events if e.get("formal_status") in ("informal", "non-formal", "非正式")]
    assert len(informal) >= 1, "Expected at least 1 informal notice (2025-12-20)"

def test_has_formal_entry(compliance_events):
    formal = [e for e in compliance_events if e.get("formal_status") in ("formal", "正式")]
    assert len(formal) >= 1, "Expected at least 1 formal notice (2026-03-16)"
