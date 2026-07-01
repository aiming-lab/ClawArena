"""check_q1.py — Wave3 s_kubernetes_outage_rca q1 checker.

Verifies output/rca_plan.md:
- File exists
- ≥ 5 section headings (accept #, **, or numbered N.)
- Mentions EU-West-2
- Mentions 03:11
- Covers ≥ 3 of: manifest/helm/log/webhook/grafana/dashboard/postmortem/tar/archive

Note: q1 题面只要求点名 cluster region 与 incident start time + 五条调查 track，
从未要求点名具体服务（payment-svc），故不再硬性要求 'payment-svc'。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def main(workspace: Path) -> int:
    out = workspace / "output" / "rca_plan.md"
    if not out.exists():
        print(f"FAIL: output/rca_plan.md not found")
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

    # 2. Mentions EU-West-2 (or EU West 2)
    if not re.search(r"EU[\s\-]West[\s\-]2", text, re.IGNORECASE):
        print("FAIL: EU-West-2 not mentioned")
        return 1

    # 3. Mentions 03:11
    if not re.search(r"03:11", text):
        print("FAIL: incident start time 03:11 not mentioned")
        return 1

    # 4. ≥ 3 investigation topic words
    topics = ["manifest", "helm", "log", "webhook", "grafana", "dashboard",
              "postmortem", "tar", "archive", "cluster"]
    hits = [t for t in topics if re.search(t, text, re.IGNORECASE)]
    if len(hits) < 3:
        print(f"FAIL: only {len(hits)} investigation topics covered (need ≥ 3): {hits}")
        return 1

    print(f"PASS: rca_plan.md has {len(headings)} headings, EU-West-2, 03:11, "
          f"topics: {hits}")
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
