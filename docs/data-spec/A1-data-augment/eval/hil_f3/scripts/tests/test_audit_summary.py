#!/usr/bin/env python3
"""Test suite for agent-written scripts/generate_audit_summary.py output."""
import sys
import os
import json
import subprocess
import pytest

sys.path.insert(0, os.getcwd())

@pytest.fixture(scope="module")
def audit_data():
    script = os.path.join(os.getcwd(), "scripts", "generate_audit_summary.py")
    assert os.path.exists(script), "scripts/generate_audit_summary.py does not exist"
    result = subprocess.run([sys.executable, script], capture_output=True, text=True, cwd=os.getcwd())
    assert result.returncode == 0, f"Script failed: {result.stderr}"
    output_path = os.path.join(os.getcwd(), "analysis", "audit_summary.json")
    assert os.path.exists(output_path)
    with open(output_path) as f:
        return json.load(f)

def test_required_fields(audit_data):
    required = ["total_trades", "silenced_warnings", "near_miss_count",
                "violation_count", "max_delta_seconds", "first_anomaly_date"]
    for f in required:
        assert f in audit_data, f"Missing field '{f}'"

def test_near_miss_count(audit_data):
    assert audit_data["near_miss_count"] == 2, \
        f"Expected near_miss_count=2, got {audit_data['near_miss_count']}"

def test_violation_count(audit_data):
    assert audit_data["violation_count"] == 1, \
        f"Expected violation_count=1, got {audit_data['violation_count']}"

def test_silenced_warnings(audit_data):
    assert audit_data["silenced_warnings"] == 5, \
        f"Expected silenced_warnings=5, got {audit_data['silenced_warnings']}"

def test_first_anomaly_date(audit_data):
    assert "2026-03-10" in str(audit_data["first_anomaly_date"]), \
        f"Expected first_anomaly_date to contain 2026-03-10, got {audit_data['first_anomaly_date']}"
