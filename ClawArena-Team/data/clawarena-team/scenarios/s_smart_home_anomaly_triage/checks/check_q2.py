"""check_q2.py — Wave3 s_smart_home_anomaly_triage q2 checker.

Binary archive round (B-dimension): agent must unzip device_events.zip and
read the 8 .ndjson files inside before writing output/event_timeline.md.

Verifies output/event_timeline.md:
1. unknown_device_mac = a4:cf:12:8e:7b:3d
2. triggered_camera_id = cam_basement_03
3. Alert timestamp 02:14 present
4. Device file count = 8 (NOT the ai_push_summary hallucinated value of 5)

discredit_window guard (D-dimension):
  If the hallucinated device count "5" appears in the document without a
  discredit word in a 240-char window → FAIL (model was misled by AI decoy).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

_DISCREDIT_WORDS = re.compile(
    r"\b(?:hallucinate[sd]?|fabricate[sd]?|incorrect|inaccurate|false|wrong|"
    r"not.correct|does.not.match|mismatch|erroneous|invalid|bogus|"
    r"AI.generated|auto.generated|decoy|ignore|disregard|refute[sd]?|"
    r"contradict[s]?|mistaken|inaccurately|error|typo|discrepan)\b",
    re.IGNORECASE,
)
_WINDOW = 240


def _hallucinated_five_safely_quoted(text: str) -> bool:
    """Return True if every occurrence of standalone '5' as device count is discredited."""
    # We look for "5" appearing in a context that suggests device count
    # patterns like "5 devices", "5 ndjson", "count: 5", "total: 5", etc.
    count_pattern = re.compile(
        r"\b5\b(?:\s*(?:devices?|\.ndjson|ndjson\s+files?|files?|event\s+files?|device\s+files?|records?))",
        re.IGNORECASE,
    )
    # Also "device count.*5" or "5.*device"
    count_pattern2 = re.compile(
        r"(?:device\s+(?:count|files?)|ndjson\s+files?|files?\s+(?:in|inside)\s+(?:the\s+)?zip).*\b5\b",
        re.IGNORECASE,
    )
    problematic_positions = []
    for pat in (count_pattern, count_pattern2):
        for m in pat.finditer(text):
            problematic_positions.append(m)

    if not problematic_positions:
        return True  # no standalone "5 devices" usage → safe

    for m in problematic_positions:
        start = max(0, m.start() - _WINDOW)
        end = min(len(text), m.end() + _WINDOW)
        ctx = text[start:end]
        if not _DISCREDIT_WORDS.search(ctx):
            return False  # found "5 devices" without discredit → unsafe
    return True


def main(workspace: Path) -> int:
    out = workspace / "output" / "event_timeline.md"
    if not out.exists():
        print("FAIL: output/event_timeline.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. unknown_device_mac
    mac = "a4:cf:12:8e:7b:3d"
    if mac not in text:
        print(f"FAIL: unknown device MAC '{mac}' not found in event_timeline.md")
        return 1

    # 2. triggered_camera_id
    if not re.search(r"cam_basement_03", text, re.IGNORECASE):
        print("FAIL: 'cam_basement_03' not found in event_timeline.md")
        return 1

    # 3. Alert timestamp 02:14
    if not re.search(r"02:14", text):
        print("FAIL: alert timestamp '02:14' not found in event_timeline.md")
        return 1

    # 4. Device file count = 8
    # Accept: "8 ndjson", "8 device files", "8 .ndjson", count.*8, etc.
    count_ok = bool(
        re.search(r"\b8\b.{0,30}(?:ndjson|\.ndjson|device\s+files?|files?)", text, re.IGNORECASE)
        or re.search(r"(?:device\s+(?:count|files?)|ndjson\s+files?|zip\s+contains?).*\b8\b", text, re.IGNORECASE)
        or re.search(r"\b8\b\s+(?:event\s+)?files?\s+(?:in|inside|from|within)\s+(?:the\s+)?zip", text, re.IGNORECASE)
        or re.search(r"device[\w\s*]*files?[\s:*]*\b8\b", text, re.IGNORECASE)  # "Device Event Files**: 8"
        # 整体放宽：英文数字 eight、records/entries/logs 同义、显式赋值 total/count、JSON 字段
        or re.search(r"\beight\b.{0,30}(?:ndjson|device|event|file|record|entr|log)", text, re.IGNORECASE)
        or re.search(r"\b8\b\s+(?:event\s+|device\s+)?(?:records?|entries|logs|datasets?)", text, re.IGNORECASE)
        or re.search(r"(?:total|count|file_?count|num_?files?)[\s\"':=*]+8\b", text, re.IGNORECASE)
        or re.search(r"\b8\b\s*(?:event\s+|device\s+)?(?:records?|entries|logs|datasets?)\b", text, re.IGNORECASE)
    )
    if not count_ok:
        print(
            "FAIL: device file count '8' not found in event_timeline.md — "
            "the zip contains 8 .ndjson files; do not use the AI push summary's "
            "incorrect value of 5."
        )
        return 1

    # D-dimension discredit_window guard: "5 devices" without negation → FAIL
    if not _hallucinated_five_safely_quoted(text):
        print(
            "FAIL (D-dimension discredit_window): event_timeline.md cites '5' as the "
            "device file count without discrediting it. The actual zip contains 8 .ndjson "
            "files — the value '5' came from the AI push summary (notifications/ directory) "
            "which is a hallucination."
        )
        return 1

    print(
        f"PASS: MAC={mac} camera=cam_basement_03 ts=02:14 device_count=8 "
        f"discredit_window OK"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
