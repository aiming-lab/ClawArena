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
    data, err = _load_json(ws / "rca_outputs" / "nimbus_fishbone.json")
    if err: _finish([err])
    cats = data.get("categories")
    if not isinstance(cats, dict):
        _finish(["'categories' must be a JSON object (dict)"])
    # Six-M 分类必须存在
    six_m = {"Man","Machine","Material","Method","Environment","Measurement"}
    cat_keys = {str(k).strip().title() for k in cats.keys()}
    missing_m = six_m - cat_keys
    if missing_m:
        fails.append("categories missing Six-M keys: %s" % sorted(missing_m))
    # Machine 必须含精确标识符 battery_failure 和 occlusion_sensor（含下划线）
    machine = None
    for k, v in cats.items():
        if str(k).strip().lower() == "machine":
            machine = v
            break
    if machine is None:
        fails.append("categories missing 'Machine' key")
    else:
        m_txt = json.dumps(machine, ensure_ascii=False).lower()
        if "battery_failure" not in m_txt:
            fails.append(
                "Machine category does not contain identifier 'battery_failure' "
                "(must use this exact key, not just 'battery')"
            )
        if "occlusion_sensor" not in m_txt:
            fails.append(
                "Machine category does not contain identifier 'occlusion_sensor' "
                "(must use this exact key, not just 'occlusion')"
            )
    # Material 必须含精确标识符 sterile_barrier（含下划线）
    material = None
    for k, v in cats.items():
        if str(k).strip().lower() == "material":
            material = v
            break
    if material is not None:
        mat_txt = json.dumps(material, ensure_ascii=False).lower()
        if "sterile_barrier" not in mat_txt:
            fails.append(
                "Material category does not contain identifier 'sterile_barrier' "
                "(must use this exact key, not just 'sterile' or 'barrier')"
            )
    else:
        fails.append("categories missing 'Material' key")
    # 必须含 root_causes 列表，含三个核心根因标识符
    rc = data.get("root_causes")
    if not isinstance(rc, list) or len(rc) == 0:
        fails.append(
            "nimbus_fishbone.json must contain a 'root_causes' list with at least 3 entries "
            "referencing battery_failure, occlusion_sensor, and sterile_barrier"
        )
    else:
        rc_txt = json.dumps(rc, ensure_ascii=False).lower()
        if "battery_failure" not in rc_txt:
            fails.append("root_causes must reference 'battery_failure'")
        if "occlusion_sensor" not in rc_txt and "occlusion" not in rc_txt:
            fails.append("root_causes must reference 'occlusion_sensor' or occlusion detection")
        if "sterile_barrier" not in rc_txt:
            fails.append("root_causes must reference 'sterile_barrier'")
    _finish(fails)
main()
