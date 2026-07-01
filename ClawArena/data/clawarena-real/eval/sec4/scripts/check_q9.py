#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, csv, hashlib
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
    data, err = _load_json(ws / "dpia" / "dpia_hr_analytics_final.json")
    if err: _finish([err])
    # risk_matrix must be a list
    rm = data.get("risk_matrix")
    if not isinstance(rm, list) or len(rm) < 2:
        fails.append("risk_matrix must be a list with >= 2 items (got %r)" % type(rm).__name__)
    else:
        for item in rm:
            if not isinstance(item, dict): continue
            l = item.get("likelihood")
            s = item.get("severity")
            rs = item.get("risk_score")
            try:
                if not (1 <= int(l) <= 5):
                    fails.append("risk item %s: likelihood %r not in [1,5]" % (item.get("risk_id","?"), l))
                if not (1 <= int(s) <= 5):
                    fails.append("risk item %s: severity %r not in [1,5]" % (item.get("risk_id","?"), s))
                if int(rs) != int(l) * int(s):
                    fails.append("risk item %s: risk_score %r != likelihood*severity (%r*%r=%r)" % (
                        item.get("risk_id","?"), rs, l, s, int(l)*int(s)))
            except (TypeError, ValueError):
                fails.append("risk item %s has non-integer likelihood/severity/risk_score" % item.get("risk_id","?"))
    # high_risk_items must have >= 2 entries and reference scores >= 15
    hri = data.get("high_risk_items")
    if not isinstance(hri, list) or len(hri) < 2:
        fails.append("high_risk_items must be a list with >= 2 entries (expected risk_score >= 15 items from special category data)")
    else:
        rm2 = data.get("risk_matrix") or []
        rm_map = {item.get("risk_id"): item for item in rm2 if isinstance(item, dict)}
        for rid in hri:
            item = rm_map.get(rid)
            if item is None:
                fails.append("high_risk_items entry %r not found in risk_matrix" % rid)
            else:
                try:
                    if int(item.get("risk_score", 0)) < 15:
                        fails.append("high_risk_items entry %r has risk_score=%r < 15" % (rid, item.get("risk_score")))
                except (TypeError, ValueError):
                    pass
    # residual_risk_score must equal max of risk_matrix scores
    rrs = data.get("residual_risk_score")
    try:
        rrs_int = int(rrs)
        if rrs_int <= 0:
            fails.append("residual_risk_score == %r (expected positive int)" % rrs)
        rm3 = data.get("risk_matrix") or []
        if isinstance(rm3, list) and len(rm3) >= 1:
            try:
                actual_max = max(int(item.get("risk_score", 0)) for item in rm3 if isinstance(item, dict))
                if rrs_int != actual_max:
                    fails.append(
                        "residual_risk_score %d != max(risk_matrix.risk_score) %d "
                        "(must equal maximum)" % (rrs_int, actual_max)
                    )
            except (TypeError, ValueError):
                pass
    except (TypeError, ValueError):
        fails.append("residual_risk_score not numeric: %r" % rrs)
    # At least one risk item must reference health_risk_score or burnout_probability (Art.9 special data)
    rm4 = data.get("risk_matrix") or []
    special_cat_covered = any(
        re.search(r"health_risk_score|burnout_probability|art\.?\s*9|special.categ", str(item.get("description", "")).lower())
        for item in rm4 if isinstance(item, dict)
    )
    if not special_cat_covered:
        fails.append(
            "risk_matrix must include at least one item referencing 'health_risk_score' or "
            "'burnout_probability' (or Art. 9) — confirmed by Update-1"
        )
    # dpo_consultation_required and sa_prior_consultation_required must be true
    if data.get("dpo_consultation_required") is not True:
        fails.append("dpo_consultation_required must be true (special category + high residual risk)")
    if data.get("sa_prior_consultation_required") is not True:
        fails.append("sa_prior_consultation_required must be true (Art.36 prior consultation required)")
    _finish(fails)
main()
