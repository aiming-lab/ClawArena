#!/usr/bin/env python3
"""check_q1.py (wave3) — verify factcheck_plan.md.

wave3 新增：至少 1 处提及解压 zip 或 mp4 帧。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ws = Path(sys.argv[1])
target = ws / "output" / "factcheck_plan.md"

if not target.exists():
    print(f"FAIL: {target} does not exist")
    sys.exit(1)

content = target.read_text(encoding="utf-8")
text = content.lower()

# Structure: ≥5 section markers
section_markers = []
for ln in content.splitlines():
    stripped = ln.strip()
    if re.match(r"^#{1,4}\s+\S", stripped):
        section_markers.append(stripped[:80])
    elif re.match(r"^\d+\.\s+\S", stripped):
        section_markers.append(stripped[:80])
    elif re.match(r"^[-*•]\s+\*\*[^*]+\*\*", stripped):
        section_markers.append(stripped[:80])
    elif re.match(r"^\*\*[^*]+\*\*\s*$", stripped):
        section_markers.append(stripped[:80])
if len(section_markers) < 5:
    print(f"FAIL: need >=5 section markers; found {len(section_markers)}: {section_markers}")
    sys.exit(1)

# Minimum length
if len(content.strip()) < 400:
    print(f"FAIL: work plan too short ({len(content)} chars)")
    sys.exit(1)

# 5 topic areas
topics = [
    [r"procurement", r"contract", r"xlsx", r"database"],
    [r"corporate\s+registry", r"company\s+registry", r"annual\s+report", r"coi",
     r"conflict.of.interest", r"shareholder"],
    [r"wav\b", r"audio", r"phone.interview", r"interview\s+recording", r"voice"],
    [r"leak", r"minutes", r"anonymous", r"vote\s+minutes", r"source\s+document",
     r"zip\b", r"unzip"],
    [r"publish", r"editor", r"finding", r"clearance", r"sign.?off", r"report"],
]
missing_topics = []
for i, kws in enumerate(topics, start=1):
    if not any(re.search(p, text) for p in kws):
        missing_topics.append((i, kws))
if missing_topics:
    print(f"FAIL: work plan missing topic markers for areas: {missing_topics}")
    sys.exit(1)

# Must mention Riverbend and Helios
if not re.search(r"riverbend", text):
    print("FAIL: work plan must mention Riverbend")
    sys.exit(1)
if not re.search(r"helios", text):
    print("FAIL: work plan must mention Helios (the winning bidder)")
    sys.exit(1)

# wave3 new: at least 1 mention of unzip/zip or mp4/video frames
has_zip_or_frame = bool(re.search(
    r"unzip|source_leak\.zip|\.zip\b|mp4|video.frame|press_conference_replay_frames|"
    r"frame_0\d\d|extract.zip|zip.extract|decompress",
    text,
))
if not has_zip_or_frame:
    print(
        "FAIL: work plan must mention unzipping the source_leak.zip package "
        "or reading the mp4/video frames for the press conference replay"
    )
    sys.exit(1)

print("PASS")
sys.exit(0)
