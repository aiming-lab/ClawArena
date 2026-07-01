#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib
from pathlib import Path

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON in " + p.name + ": " + str(e)

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)


def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "label_compliance_q6.json")
    if err: _finish([err])
    if not isinstance(data, dict):
        _finish(["label_compliance_q6.json must be a JSON object"])
    # mia_claim_present: true
    if data.get("mia_claim_present") is not True and str(data.get("mia_claim_present", "")).lower() != "true":
        fails.append("mia_claim_present must be true ('Made in USA' appears on label)")
    # mia_standard_met: false (Danish probiotic strains fail all-or-virtually-all)
    if data.get("mia_standard_met") is not False and str(data.get("mia_standard_met", "")).lower() != "false":
        fails.append("mia_standard_met must be false (Danish Chr. Hansen probiotic strains fail 'all or virtually all' standard)")
    # reference_cases must include Kubota — each entry must be a JSON object (not a plain string)
    ref_cases = data.get("reference_cases", [])
    if not isinstance(ref_cases, list) or len(ref_cases) == 0:
        fails.append("reference_cases must be a non-empty array")
        _finish(fails)
    # Kubota entry must exist as a dict with penalty_amount_usd == 2000000 (exact integer, not string)
    kubota_entries = [e for e in ref_cases if isinstance(e, dict) and "kubota" in json.dumps(e).lower()]
    if not kubota_entries:
        fails.append("reference_cases must include a Kubota entry as a JSON object (not a plain string)")
    else:
        kub = kubota_entries[0]
        # penalty_amount_usd must be the integer 2000000
        pen_usd = kub.get("penalty_amount_usd")
        if pen_usd is None:
            fails.append("Kubota reference_case entry must have penalty_amount_usd field (integer 2000000)")
        else:
            try:
                if int(pen_usd) != 2000000:
                    fails.append("Kubota penalty_amount_usd must be 2000000 (got %r)" % pen_usd)
            except (TypeError, ValueError):
                fails.append("Kubota penalty_amount_usd must be integer 2000000 (got %r)" % pen_usd)
    # supporting_facts must have at least 3 entries
    sf = data.get("supporting_facts", [])
    if not isinstance(sf, list) or len(sf) < 3:
        fails.append("supporting_facts must contain at least 3 entries explaining the analysis")
    _finish(fails)
main()
