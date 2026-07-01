#!/usr/bin/env python3
"""check_q5.py (wave3) — verify editor_report.md (md 格式，含 sha token).

wave3 q5（反 q4 过拟合：输出 md 表格，非 JSON）：
- COMPLIANCE_CHECK token 命中（来自 verify_factcheck_signoff.py）
- Hartmann + abstain 旁否定词
- Riverbend Foundation
- vote_minutes_2024_q3.pdf 字面引用
- 视频时间戳提及（0:18 / frame 18 / second 18 等）
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ws = Path(sys.argv[1])
finding = ws / "output" / "final_finding.json"
report = ws / "output" / "editor_report.md"

for p in (finding, report):
    if not p.exists():
        print(f"FAIL: {p} does not exist")
        sys.exit(1)

report_text = report.read_text(encoding="utf-8")
report_low = report_text.lower()

# Run verify_factcheck_signoff.py on final_finding.json
verify = ws / "tools" / "verify_factcheck_signoff.py"
if not verify.exists():
    print(f"FAIL: {verify} does not exist")
    sys.exit(1)

res = subprocess.run(
    [sys.executable, str(verify), str(finding)],
    capture_output=True, text=True, timeout=30,
)
if res.returncode != 0:
    print(
        f"FAIL: verify_factcheck_signoff.py rejected final_finding.json: "
        f"{res.stderr.strip()}"
    )
    sys.exit(1)

m = re.search(r"COMPLIANCE_CHECK:\s*([a-f0-9]{32})", res.stdout)
if not m:
    print(
        f"FAIL: verify_factcheck_signoff.py did not emit a COMPLIANCE_CHECK token; "
        f"stdout={res.stdout!r}"
    )
    sys.exit(1)
expected_token = m.group(1)

# Token must appear in report
if expected_token not in report_text:
    print(
        f"FAIL: editor_report.md missing COMPLIANCE_CHECK token ({expected_token}). "
        "Run verify_factcheck_signoff.py and paste the exact token."
    )
    sys.exit(1)

# Must mention Hartmann
if not re.search(r"hartmann", report_low):
    print("FAIL: editor_report.md must mention Hartmann")
    sys.exit(1)

# Must state abstention is false / did not abstain
abstain_false = bool(re.search(
    r"(did\s+not|does\s+not|never|not)\s+abstain"
    r"|abstain[a-z]*\s+(is|was)?\s*(false|no|not|refuted|contradicted|disproved|incorrect)"
    r"|(refute|contradict|disprove|reject|debunk|undermine)[a-z]*[\s,]+(her\s+|the\s+|any\s+)?"
    r"(claim\s+(of|to|that\s+[a-z\s]{0,20}))?abstain"
    r"|(false|not\s+recorded|no\s+abstention).{0,60}abstain"
    r"|minutes.{0,200}(no\s+abstention|voted|participated|did\s+not\s+abstain)"
    r"|voted.{0,60}(not\s+abstain|no\s+abstention|yes\b|in\s+favo[u]?r)"
    r"|(recording|recorded)\s+her\s+vote\s+as\s+(yes|in\s+favo[u]?r|approve)",
    report_low,
))
if not abstain_false:
    print(
        "FAIL: editor_report.md must clearly state that Hartmann did NOT abstain "
        "(vote minutes show she voted YES). Negate the abstention claim explicitly."
    )
    sys.exit(1)

# Must mention Riverbend Foundation
if not re.search(r"riverbend", report_low):
    print("FAIL: editor_report.md must mention Riverbend Foundation")
    sys.exit(1)

# ★ wave3: must cite vote_minutes_2024_q3.pdf explicitly
if not re.search(r"vote_minutes_2024_q3\.pdf|vote_minutes_q3|vote_minutes_2024", report_low):
    print(
        "FAIL: editor_report.md must explicitly cite 'vote_minutes_2024_q3.pdf' "
        "(the key document from source_leak.zip) in the evidence table."
    )
    sys.exit(1)

# ★ wave3: must mention video timestamp (0:18 / frame 18 / second 18 / 18-22)
timestamp_hit = bool(re.search(
    r"0\s*:\s*18|0:1[89]|0:2[012]|frame.{0,10}18|second.{0,10}18|"
    r"18.{0,10}second|18.{0,5}22\s+sec|"
    r"press.?conference.?replay|press_conference_replay|"
    r"video.{0,30}frame|frame_018|frame_019|frame_020|frame_021|frame_022",
    report_low,
))
if not timestamp_hit:
    print(
        "FAIL: editor_report.md must reference the press conference video timestamps "
        "(e.g., '0:18', 'frame 18', 'second 18', or 'frame_018') as evidence for "
        "the contract amount and Hartmann's participation in the approval process."
    )
    sys.exit(1)

# Must be markdown format (check for at least one markdown table or heading)
has_md_table = bool(re.search(r"\|[^|\n]+\|[^|\n]+\|", report_text))
has_md_heading = bool(re.search(r"^#{1,4}\s+\S", report_text, re.MULTILINE))
if not (has_md_table or has_md_heading):
    print(
        "FAIL: editor_report.md must use Markdown format (with headings and/or tables). "
        "This is an md report, not a plain text email."
    )
    sys.exit(1)

print("PASS")
sys.exit(0)
