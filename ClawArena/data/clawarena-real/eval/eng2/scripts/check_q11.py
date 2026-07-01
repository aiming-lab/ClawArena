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

def _field_entry(data, name):
    """从 quality report 取某字段 entry，兼容 fields 为 list 或 dict。"""
    fields = data.get("fields")
    if isinstance(fields, list):
        for e in fields:
            if isinstance(e, dict) and e.get("field_name") == name:
                return e
    elif isinstance(fields, dict):
        e = fields.get(name)
        if isinstance(e, dict):
            return e
        if e is not None:
            return {"field_name": name, "null_count": e}
    return None

def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "pipeline" / "silver" / "clean_v2.py")
    if txt is None:
        _finish(["file not found: pipeline/silver/clean_v2.py"])
    low = txt.lower()
    # must EXCLUDE VendorID == 6 (supersede). Accept several idioms.
    excl = bool(
        re.search(r"vendorid\s*(!=|<>)\s*6", low) or
        re.search(r"vendorid\s*not\s+in\s*[\(\[][^\)\]]*6", low) or
        re.search(r"(drop|exclud|remove|filter\s*out)[^\n]{0,40}vendorid[^\n]{0,12}6", low) or
        re.search(r"vendorid[^\n]{0,12}6[^\n]{0,40}(drop|exclud|remove)", low)
    )
    if not excl:
        fails.append("clean_v2.py does not exclude VendorID == 6 (supersede requires full exclusion)")
    # must NOT keep VendorID=6 via an active retain branch (comments mentioning audit_only are fine)
    if re.search(r"(keep|retain|include)[^\n]{0,30}vendorid[^\n]{0,8}6", low) or \
       re.search(r"vendorid[^\n]{0,8}6[^\n]{0,30}(keep|retain)", low):
        fails.append("clean_v2.py appears to retain VendorID==6 (an active keep/retain branch)")
    _finish(fails)
main()
