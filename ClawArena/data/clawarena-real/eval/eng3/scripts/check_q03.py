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

def _get_val(obj, key):
    """支持 {key: float} 或 {key: {value: float, unit: ...}} 两种形式。"""
    v = obj.get(key)
    if isinstance(v, dict):
        return v.get("value")
    return v

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "output" / "q03_peak_metrics.json")
    if err: _finish([err])
    for k in ("peak_cdn_error_pct", "peak_5xx_pct", "ttfb_p99_multiplier"):
        if k not in data:
            fails.append("missing key: " + k)
    if fails: _finish(fails)
    # peak_cdn_error_pct ∈ [2.0, 2.2]（V5：0.21% 是诱饵，必须 FAIL）
    cdn = _get_val(data, "peak_cdn_error_pct")
    try:
        cdn = float(cdn)
        if not (2.0 <= cdn <= 2.2):
            fails.append("peak_cdn_error_pct == %.4f (expected [2.0, 2.2]; 0.21 is the bot decoy — use real metrics)" % cdn)
    except (TypeError, ValueError):
        fails.append("peak_cdn_error_pct not numeric: %r" % cdn)
    # peak_5xx_pct ∈ [3.4, 3.5]
    p5xx = _get_val(data, "peak_5xx_pct")
    try:
        p5xx = float(p5xx)
        if not (3.4 <= p5xx <= 3.5):
            fails.append("peak_5xx_pct == %.4f (expected [3.4, 3.5])" % p5xx)
    except (TypeError, ValueError):
        fails.append("peak_5xx_pct not numeric: %r" % p5xx)
    # ttfb_p99_multiplier == 3
    mult = _get_val(data, "ttfb_p99_multiplier")
    try:
        if int(float(mult)) != 3:
            fails.append("ttfb_p99_multiplier == %r (expected 3)" % mult)
    except (TypeError, ValueError):
        fails.append("ttfb_p99_multiplier not numeric: %r" % mult)
    _finish(fails)
main()
