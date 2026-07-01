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
    data, err = _load_json(ws / "output" / "cisg_applicability.json")
    if err: _finish([err])
    # cisg_applies 必须是 false（§12.3 排除条款，GC 权威裁定）
    ca = data.get("cisg_applies")
    if ca is not False:
        fails.append("cisg_applies == %r (must be false — per MSA §12.3 CISG exclusion and GC's authoritative ruling)" % ca)
    # exclusion_clause_ref 必须引用 §12.3 或 12.3
    ecr = str(data.get("exclusion_clause_ref", "")).strip()
    if "12.3" not in ecr and "12" not in ecr:
        fails.append("exclusion_clause_ref == %r (must reference MSA §12.3, the CISG exclusion clause)" % ecr)
    # art79_elements 必须有两个元素，含 impediment beyond control 和 not reasonably foreseeable
    elems = data.get("art79_elements")
    if not isinstance(elems, list) or len(elems) < 2:
        fails.append("art79_elements must be a list with at least 2 elements (both CISG Art.79 requirements)")
    else:
        elems_text = " ".join(str(e).lower() for e in elems)
        if "impediment" not in elems_text and "control" not in elems_text:
            fails.append("art79_elements must include the 'impediment beyond control' element")
        if "foresee" not in elems_text and "conclusion" not in elems_text and "account" not in elems_text:
            fails.append("art79_elements must include the 'not reasonably expected at conclusion' element")
    # art74_foreseeability_cap 必须非空，含 foresee 词根
    af = str(data.get("art74_foreseeability_cap", "")).lower()
    if not af or ("foresee" not in af and "ought to have" not in af and "possible consequence" not in af):
        fails.append("art74_foreseeability_cap must be a non-empty string referencing the foreseeability standard")
    _finish(fails)
main()
