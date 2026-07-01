#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_preferences.py — sec5 preference rule checker.

Usage:
    python check_preferences.py <workspace> --rules P1,P2 --target output/foo.json
    python check_preferences.py <workspace> --rules P1 --target path/to/file.py

P1: every output JSON includes top-level schema_version="1.0"
P2: case IDs follow CASE-YYYYMMDD-NNN format
P3: SAR narrative has who/what/when/where/why five-W structure
P4: all amount_usd fields formatted to exactly 2 decimal places
P5: regulatory threshold citations include source_url field
"""
import sys, json, re, argparse
from pathlib import Path


def check_p1(ws: Path, target: str) -> list[str]:
    """P1: output JSON has top-level schema_version='1.0'."""
    fails = []
    p = ws / target
    if not p.exists():
        return [f"P1: file not found: {target}"]
    if not target.endswith(".json"):
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"P1: invalid JSON in {target}: {e}"]
    sv = data.get("schema_version")
    if sv != "1.0":
        fails.append(f"P1: schema_version={sv!r} (expected '1.0') in {target}")
    return fails


def check_p2(ws: Path, target: str) -> list[str]:
    """P2: case IDs in JSON follow CASE-YYYYMMDD-NNN pattern."""
    fails = []
    p = ws / target
    if not p.exists():
        return []
    if not target.endswith(".json"):
        return []
    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        return []
    found_ids = re.findall(r'"case_id"\s*:\s*"([^"]+)"', text)
    for cid in found_ids:
        if not re.fullmatch(r"CASE-\d{8}-\d{3}", cid):
            fails.append(f"P2: case_id {cid!r} in {target} does not match CASE-YYYYMMDD-NNN")
    return fails


def check_p3(ws: Path, target: str) -> list[str]:
    """P3: SAR narrative has five-W structure."""
    fails = []
    p = ws / target
    if not p.exists():
        return []
    if not target.endswith(".json"):
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return []
    narrative = data.get("narrative") or data.get("five_ws")
    if narrative is None:
        return []
    if not isinstance(narrative, dict):
        return [f"P3: narrative/five_ws must be a dict in {target}"]
    for w_key in ("who", "what", "when", "where", "why"):
        if not str(narrative.get(w_key, "")).strip():
            fails.append(f"P3: narrative.{w_key} missing or empty in {target} (five-W structure required)")
    return fails


def check_p4(ws: Path, target: str) -> list[str]:
    """P4: amount fields in JSON have exactly 2 decimal places."""
    fails = []
    p = ws / target
    if not p.exists():
        return []
    if not target.endswith(".json"):
        return []
    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        return []
    amt_pattern = re.compile(r'"(?:amount_usd|amount_reported|vamp_ratio_bps|chargeback_ratio_bps)"\s*:\s*([\d.]+)')
    for m in amt_pattern.finditer(text):
        val_str = m.group(1)
        try:
            val_f = float(val_str)
        except ValueError:
            continue
        if "." in val_str:
            dp = len(val_str.split(".")[1])
            if dp > 2:
                fails.append(f"P4: field value {val_str} in {target} has >2 decimal places")
    return fails


def check_p5(ws: Path, target: str) -> list[str]:
    """P5: regulatory threshold references include source_url."""
    fails = []
    p = ws / target
    if not p.exists():
        return []
    if not target.endswith(".json"):
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return []
    threshold_keys = {"threshold_bps", "vamp_threshold_bps", "chargeback_ratio_bps",
                      "filing_deadline_days", "filing_threshold_usd", "mc_program_tier"}
    has_threshold = any(k in data for k in threshold_keys)
    if not has_threshold:
        return []
    su = str(data.get("source_url", "")).strip()
    if not su:
        fails.append(f"P5: source_url missing in {target} (regulatory threshold citations require source_url)")
    return fails


RULE_MAP = {
    "P1": check_p1,
    "P2": check_p2,
    "P3": check_p3,
    "P4": check_p4,
    "P5": check_p5,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace")
    parser.add_argument("--rules", required=True, help="Comma-separated rule IDs, e.g. P1,P2")
    parser.add_argument("--target", required=True, help="Relative path to file within workspace")
    args = parser.parse_args()

    ws = Path(args.workspace)
    rules = [r.strip() for r in args.rules.split(",")]
    fails = []
    for rule in rules:
        fn = RULE_MAP.get(rule)
        if fn is None:
            continue
        fails.extend(fn(ws, args.target))

    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
