#!/usr/bin/env python3
"""check_q5.py (wave3) — verify legal_audit_report.yaml.

锚点：
- termination_cap_final ≥ 12（compliance demand floor）
- sla_final == 99.9（verbal amendment from wav）
- notice_days == 45
- missing_signatories 含 Mercator + GoldenLeaf（v4 全未签）
- compliance_pass == true
- stale guard: 98.5 出现即 fail（stale bot summary）

产出文件：output/legal_audit_report.yaml
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ws = Path(sys.argv[1])
target = ws / "output" / "legal_audit_report.yaml"

if not target.exists():
    print(f"FAIL: {target} does not exist")
    sys.exit(1)

raw = target.read_text(encoding="utf-8")

# ---- YAML 解析（不要求 pyyaml，用正则 schema_by_shape 方式）----
try:
    import yaml
    data = yaml.safe_load(raw)
    if not isinstance(data, dict):
        raise ValueError("top-level must be a mapping")
except Exception as e:
    print(f"FAIL: legal_audit_report.yaml failed to parse as YAML: {e}")
    sys.exit(1)


def _find_numeric(d: dict, *aliases: str):
    """Find first matching key (case-insensitive aliases) and return numeric value."""
    for k, v in d.items():
        kn = str(k).lower().replace("-", "_").replace(" ", "_")
        if any(a in kn for a in aliases):
            try:
                return float(v)
            except (TypeError, ValueError):
                # Try string parse
                if isinstance(v, str):
                    m = re.search(r"[\d.]+", v)
                    if m:
                        return float(m.group())
    return None


def _find_bool(d: dict, *aliases: str):
    for k, v in d.items():
        kn = str(k).lower().replace("-", "_").replace(" ", "_")
        if any(a in kn for a in aliases):
            if isinstance(v, bool):
                return v
            if isinstance(v, str):
                return v.lower() in ("true", "yes", "1")
    return None


def _find_list(d: dict, *aliases: str):
    for k, v in d.items():
        kn = str(k).lower().replace("-", "_").replace(" ", "_")
        if any(a in kn for a in aliases):
            if isinstance(v, list):
                return [str(x) for x in v]
            if isinstance(v, str):
                return [v]
    return None


# ---- 1. termination_cap_final ≥ 12 ----
cap = _find_numeric(data, "termination_cap", "cap_final", "cap_months", "termination")
if cap is None:
    print("FAIL: legal_audit_report.yaml missing termination_cap_final field")
    sys.exit(1)
if cap < 12:
    print(
        f"FAIL: termination_cap_final must be ≥ 12 (compliance demand floor), got {cap}. "
        "The v4 cap of 9 months is insufficient — the compliance demand requires ≥ 12 months."
    )
    sys.exit(1)

# ---- 2. sla_final == 99.9 ----
sla = _find_numeric(data, "sla_final", "sla", "uptime", "sla_percent")
if sla is None:
    print("FAIL: legal_audit_report.yaml missing sla_final field")
    sys.exit(1)
if abs(sla - 99.9) > 0.05:
    print(
        f"FAIL: sla_final must be 99.9 (verbal amendment from voice memo), got {sla}. "
        "Note: 99.7% is the v4 draft value; 99.5% is the v3/transcript decoy; "
        "98.5% is the stale 2025 bot summary — all are wrong."
    )
    sys.exit(1)

# ---- 3. notice_days == 45 ----
notice = _find_numeric(data, "notice_days", "notice", "notice_period")
if notice is None:
    print("FAIL: legal_audit_report.yaml missing notice_days field")
    sys.exit(1)
if int(notice) != 45:
    print(f"FAIL: notice_days must be 45 (v4 unchanged), got {int(notice)}")
    sys.exit(1)

# ---- 4. missing_signatories 含 Mercator + GoldenLeaf ----
signatories = _find_list(data, "missing_signatories", "missing_signer", "signatories")
if signatories is None:
    print("FAIL: legal_audit_report.yaml missing missing_signatories field")
    sys.exit(1)
sig_text = " ".join(signatories).lower()
if "mercator" not in sig_text:
    print(
        f"FAIL: missing_signatories must include 'Mercator' (Mercator has not signed v3 or v4); "
        f"got: {signatories}"
    )
    sys.exit(1)
if "goldenleaf" not in sig_text and "golden leaf" not in sig_text and "golden_leaf" not in sig_text:
    print(
        f"FAIL: missing_signatories must include 'GoldenLeaf' (GoldenLeaf has not signed v4); "
        f"got: {signatories}"
    )
    sys.exit(1)

# ---- 5. compliance_pass == true ----
comp_pass = _find_bool(data, "compliance_pass", "compliance")
if comp_pass is None:
    print("FAIL: legal_audit_report.yaml missing compliance_pass field")
    sys.exit(1)
if comp_pass is not True:
    print(
        f"FAIL: compliance_pass must be true (termination_cap_final={cap} ≥ 12 and "
        f"sla_final={sla} == 99.9 both satisfied), got {comp_pass!r}"
    )
    sys.exit(1)

# ---- 6. stale guard: 98.5 出现即 fail ----
if re.search(r"\b98\.5(?:0+)?\b", raw):
    print(
        "FAIL: stale guard triggered — 98.5 appears in legal_audit_report.yaml. "
        "98.5% is from the stale 2025 bot summary in archive/ and is NOT the correct SLA. "
        "The correct SLA is 99.9% (verbal amendment from the voice memo)."
    )
    sys.exit(1)

print("PASS")
sys.exit(0)
