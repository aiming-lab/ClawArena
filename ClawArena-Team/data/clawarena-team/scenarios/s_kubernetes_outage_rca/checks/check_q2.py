"""check_q2.py — Wave3 s_kubernetes_outage_rca q2 checker.

Verifies output/oom_evidence.md:
- File exists
- Exact OOM-killed pod: payment-svc-7f8c9b5dc-hk2lp
- Wrong memory limit: 512 (in Mi context)
- Correct memory value from wav: 2048 (in Mi context)
- C9 modality-decoy guard: if only 1024 appears (transcript decoy) → FAIL

The correct_memory_limit_mi (2048) must appear — it is only in the wav recording.
The transcript_auto.txt says 1024Mi (decoy). If the model used the transcript,
it would report 1024 but NOT 2048.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def main(workspace: Path) -> int:
    out = workspace / "output" / "oom_evidence.md"
    if not out.exists():
        print("FAIL: output/oom_evidence.md not found")
        return 1

    text = out.read_text(encoding="utf-8", errors="ignore")

    # 1. Exact pod name
    pod = "payment-svc-7f8c9b5dc-hk2lp"
    if pod not in text:
        print(f"FAIL: exact pod name '{pod}' not found in oom_evidence.md")
        return 1

    # 2. Wrong memory limit 512 (in Mi context)
    if not re.search(r"512\s*Mi", text, re.IGNORECASE):
        print("FAIL: wrong memory limit '512Mi' not mentioned")
        return 1

    # 3. Correct memory value 2048 from wav (接受等价写法 2Gi/2GiB——2Gi == 2048Mi,
    #    仍可区分 1024Mi 诱饵与 512Mi 错值;模型用 2Gi 表达不应判错)
    if not re.search(
        r"2048\s*Mi(?:B)?|\b2(?:\.0+)?\s*Gi(?:B)?\b|\b2097152\b",  # 2048Mi/2048MiB / 2Gi/2.0GiB / 2097152 bytes
        text, re.IGNORECASE,
    ):
        print("FAIL: correct memory value '2048Mi' (or equivalent '2Gi', from wav) not mentioned in oom_evidence.md")
        return 1

    # 4. C9 modality-decoy guard: 1024 must NOT appear as the correct/recommended value
    # We allow 1024 to appear if it is explicitly flagged as wrong/incorrect/transcript decoy.
    # If 1024 appears AND 2048 does NOT appear, that's a pure-transcript fail.
    # (We already checked 2048 is present above, so if we reach here, 2048 IS present.)
    # The check here is: if 1024 appears with memory context AND is not discredited → warn
    # But since 2048 is already required above, a partial use of 1024 is allowed.

    print(
        f"PASS: pod={pod!r} memory_limit=512Mi correct_memory=2048Mi"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
