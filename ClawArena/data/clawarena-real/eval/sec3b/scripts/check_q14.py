#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv
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
    path = ws / "output" / "regulatory_submission_summary.json"
    if not path.exists():
        _finish(["file not found: output/regulatory_submission_summary.json"])
    try:
        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        _finish(["invalid JSON: " + str(exc)])
    # P5: field order must be incident_date → rule_violated → financial_impact → remediation_count → submission_date
    required_order = ["incident_date", "rule_violated", "financial_impact", "remediation_count", "submission_date"]
    keys = list(data.keys())
    top5 = [k for k in keys if k in required_order]
    top5_idx = [required_order.index(k) for k in top5]
    if top5_idx != sorted(top5_idx):
        fails.append("P5: field order violation — expected incident_date→rule_violated→"
                     "financial_impact→remediation_count→submission_date, got: %s" % top5)
    for need in required_order:
        if need not in data:
            fails.append("missing required key '%s'" % need)
    # rule_violated must include sub-clause (P3)
    rule = str(data.get("rule_violated") or "")
    if "15c" not in rule:
        fails.append("rule_violated %r does not reference any Rule 15c..." % rule[:50])
    if not re.search(r"\(b\)|\(B\)", rule):
        fails.append("rule_violated %r must include sub-clause (b) per P3" % rule[:50])
    # remediation_count must exactly match the number of remediation items in the CAP from Round 13
    rc = data.get("remediation_count")
    try:
        rc = int(rc)
    except (TypeError, ValueError):
        _finish(["remediation_count not an int: %r" % rc])
    if rc < 4:
        fails.append("remediation_count == %d (expected >= 4)" % rc)
    # Cross-verify remediation_count against the actual CAP from Round 13
    cap_txt = _read(ws / "output" / "corrective_action_plan.md")
    if cap_txt is not None:
        cap_items = re.findall(r"###\s+\d+\.", cap_txt)
        if cap_items:
            actual_cap_count = len(cap_items)
            if rc != actual_cap_count:
                fails.append(
                    "remediation_count == %d but corrective_action_plan.md has %d '### N.' "
                    "remediation items (V4 closure: must match your Round 13 CAP exactly)" % (rc, actual_cap_count)
                )
    # C★ Cross-round closure: financial_impact must include BOTH total_affected AND audit_log_total_scanned
    q3, e3 = _load_json(ws / "output" / "affected_orders_count.json")
    if not e3 and q3 is not None:
        ta = q3.get("total_affected")
        try:
            ta = int(ta)
            fi = str(data.get("financial_impact") or "")
            if str(ta) not in fi and ta > 0:
                fails.append(
                    "financial_impact %r does not contain total_affected=%d from Round 3 "
                    "(C★ cross-round closure: quote the exact count from output/affected_orders_count.json)" % (fi[:80], ta)
                )
        except (TypeError, ValueError):
            pass
        tsc = q3.get("audit_log_total_scanned")
        try:
            tsc = int(tsc)
            fi = str(data.get("financial_impact") or "")
            if str(tsc) not in fi and tsc > 0:
                fails.append(
                    "financial_impact %r does not contain audit_log_total_scanned=%d from Round 3 "
                    "(C★ cross-round closure: include total lines scanned from output/affected_orders_count.json "
                    "— required in regulatory submission to document the scope of log analysis)" % (fi[:80], tsc)
                )
        except (TypeError, ValueError):
            pass
    # C★ Cross-round closure: kcg_reference_loss_usd must match Round 5 output exactly
    kcg_ref = data.get("kcg_reference_loss_usd")
    if kcg_ref is None:
        fails.append(
            "kcg_reference_loss_usd field missing — must be the exact integer from "
            "output/kcg_anchor_check.json (Round 5 output), used as regulatory precedent reference"
        )
    else:
        try:
            kcg_ref = int(kcg_ref)
        except (TypeError, ValueError):
            _finish(["kcg_reference_loss_usd not an int: %r" % kcg_ref])
        q5, e5 = _load_json(ws / "output" / "kcg_anchor_check.json")
        if not e5 and q5 is not None:
            kcg_actual = q5.get("financial_loss_usd")
            try:
                kcg_actual = int(kcg_actual)
                if kcg_ref != kcg_actual:
                    fails.append(
                        "kcg_reference_loss_usd == %d but Round 5 kcg_anchor_check.json has "
                        "financial_loss_usd == %d (must match exactly — read your Round 5 output)" % (kcg_ref, kcg_actual)
                    )
            except (TypeError, ValueError):
                pass
    # submission_date must be a valid YYYY-MM-DD date
    sd = str(data.get("submission_date") or "")
    if not re.match(r"\d{4}-\d{2}-\d{2}", sd):
        fails.append("submission_date == %r (expected YYYY-MM-DD format)" % sd)
    _finish(fails)
main()
