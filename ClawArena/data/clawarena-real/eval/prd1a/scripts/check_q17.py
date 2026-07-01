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
    data, err = _load_json(ws / "reports" / "decision_timeline_q17.json")
    if err: _finish([err])
    if not isinstance(data, dict):
        _finish(["decision_timeline_q17.json must be a JSON object"])
    events = data.get("events")
    if not isinstance(events, list):
        _finish(["events must be a JSON array"])
    if len(events) < 8:
        fails.append("events must have at least 8 entries, got %d" % len(events))
    # All events must have timestamp in ISO 8601 format
    for i, ev in enumerate(events):
        if not isinstance(ev, dict): continue
        ts = str(ev.get("timestamp", ""))
        if not re.search(r"\d{4}-\d{2}-\d{2}", ts):
            fails.append("event[%d] timestamp not in ISO 8601 format: %r" % (i, ts[:30]))
    # V10: at least one event must have supersedes_event_id referencing another event
    has_supersede = any(
        isinstance(ev, dict) and ev.get("supersedes_event_id") and ev.get("supersedes_event_id") is not None
        and str(ev.get("supersedes_event_id")).lower() not in ("null", "none", "")
        for ev in events
    )
    if not has_supersede:
        fails.append("at least one event must have supersedes_event_id pointing to an earlier event (V10)")
    # V10: email_revised_audit_v2 must appear somewhere
    all_text = json.dumps(events).lower()
    if "email_revised_audit_v2" not in all_text and "revised audit" not in all_text:
        fails.append("events must include reference to email_revised_audit_v2 superseding the initial audit email")
    # CEO supersede must be mentioned
    if not re.search(r"ceo|james.?park|feishu", all_text):
        fails.append("events must include CEO Update 1 supersede event (Feishu withdrawal of 'clinically demonstrated')")
    _finish(fails)
main()
