"""check_q1.py — Wave3 s_smart_home_anomaly_triage q1 checker.

Verifies output/anomaly_plan.md:
- File exists
- ≥ 5 section headings (accept #, **, numbered N., or bullet)
- Mentions Mercator (Robotics) — confirms SVP brief was read
- Mentions 02:14 — alert time verbatim
- Covers ≥ 3 investigation topics:
  device/camera/event/zip/ndjson, network/telemetry/DHCP/MAC,
  photo/image/thermal/visual/vlm, audio/wav/recording/omni/nanny/calendar,
  decision/action/police/dispatch
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def main(workspace: Path) -> int:
    out = workspace / "output" / "anomaly_plan.md"
    if not out.exists():
        print("FAIL: output/anomaly_plan.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. ≥ 5 section headings
    headings = re.findall(
        r"(?m)^(?:#{1,4}\s+.+|(?:\*{1,2}|\d+[\.\)])\s+\S.{3,})",
        text,
    )
    if len(headings) < 5:
        print(f"FAIL: found {len(headings)} section headings, need ≥ 5")
        return 1

    # 2. Mentions Mercator (Robotics)
    if not re.search(r"Mercator", text, re.IGNORECASE):
        print("FAIL: 'Mercator' not mentioned — re-read requests/svp_message.txt")
        return 1

    # 3. Mentions 02:14
    if not re.search(r"02:14", text):
        print("FAIL: alert time '02:14' not mentioned")
        return 1

    # 4. ≥ 3 investigation topics covered
    topic_patterns = [
        (r"device|camera|event|zip|ndjson|event.stream", "device_events"),
        (r"network|telemetry|dhcp|mac.address|gateway|syslog", "network_telemetry"),
        (r"photo|image|thermal|visual|vlm|png|floor.?plan", "visual_evidence"),
        (r"audio|wav|recording|omni|nanny|calendar|ics|householder", "audio_nanny"),
        (r"decision|action|police|dispatch|triage|recommend", "final_decision"),
    ]
    hits = [label for pat, label in topic_patterns if re.search(pat, text, re.IGNORECASE)]
    if len(hits) < 3:
        print(
            f"FAIL: only {len(hits)} investigation topic areas covered (need ≥ 3). "
            f"Cover: device events, network telemetry, visual evidence, "
            f"audio/nanny verification, and final decision."
        )
        return 1

    print(
        f"PASS: anomaly_plan.md has {len(headings)} headings, Mercator, 02:14, "
        f"topics={hits}"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
