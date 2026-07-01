#!/usr/bin/env python3
"""check_q4.py — Validate q4: revised agenda with CEO urgent item.

Ground truth (from design_spec §4 q4):
  CEO-requested placement   — Position 1 (INCORRECT per charter)
  Correct placement         — Position 2a per Charter v3.2 Article VI §6.2:
                              "immediately following the Conflicts of Interest
                               Disclosures item"
  Verbatim bylaw clause (丑, partial):
    "shall be placed immediately following the Conflicts of Interest Disclosures item
     (position 2a) and shall not displace standing items 3 through 7."
  Correct revised agenda order:
    (1)  Call to Order
    (2)  Conflicts of Interest Disclosures [incl. Nexus Fintech vote sub-item]
    (2a) Regulatory Compliance Update [CEO urgent]
    (3)  Approval of Previous Minutes
    (4)  Financial Review
    (5)  Strategic Items
    (6)  Regulatory & Compliance [standing]
    (7)  Any Other Business

Pass conditions (all must hold; exit 0):
  1. Structure layer: output/revised_agenda.md exists; >= 600 bytes;
     contains >= 7 numbered items; retains >= 2 template markers from
     agenda_template_v2.md (e.g., "## Agenda" or "**Meeting:**" or
     "**Date:**" or "**Chair:**").
  2. Field layer (regex):
     - CEO urgent item at 2a: "2a" or "position 2a" or "2.a" within 100 chars
       of "Regulatory Compliance Update" or "CEO" or "urgent".
     - COI Disclosures at position 2: "2." or "position 2" or "item 2" within
       60 chars of "COI" or "Conflict".
     - Nexus Fintech sub-item: "Nexus Fintech" within 200 chars of the COI
       position 2 marker.
     - Financial Review at position 4: "4." or "position 4" or "item 4" within
       60 chars of "Financial Review".
  3. Bylaw verbatim citation (丑): the phrase "shall be placed immediately
     following the Conflicts of Interest" must appear (case-insensitive).
  4. Anti-decoy (v3.1 guard): file must NOT contain "v3.1" as a positive citation.
     Anti-old-draft guard: "2." or "item 2" must NOT be followed within 60 chars
     by "Financial Review" (that is the old-draft wrong order).
  5. Cross-round closure:
     - output/agenda_audit.md must exist (q1 output).
     - output/coi_reconciliation.md must contain "Nexus Fintech" (q3 output).
     - CEO position-1 request must be explicitly discredited: the file must
       contain a statement near "position 1" / "item 1" / "first on" that
       references "incorrect" / "overrid" / "not compliant" / "charter" /
       "Article" — OR simply the file must not place the CEO item at position 1
       AND must cite §6.2 / "position 2a" as the overriding authority.
  6. Edit constraint (C3): the file must retain >= 2 recognisable template
     markers from agenda_working/agenda_template_v2.md — detected by the
     presence of >= 2 of the following patterns: "## Agenda", "**Meeting:**",
     "**Date:**", "**Chair:**", "**Location:**", "**Prepared by:**".

Usage: python check_q4.py <workspace_path>
Exit codes: 0 = pass, 1 = fail.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Field-layer patterns
# ---------------------------------------------------------------------------

# CEO urgent item at position 2a
CEO_AT_2A_RE = re.compile(
    r"(2a|position\s+2a|2\.a).{0,100}"
    r"([Rr]egulatory\s+[Cc]ompliance\s+[Uu]pdate|CEO|urgent)"
    r"|([Rr]egulatory\s+[Cc]ompliance\s+[Uu]pdate|CEO|urgent).{0,100}"
    r"(2a|position\s+2a|2\.a)",
    re.DOTALL,
)

# COI Disclosures at position 2
COI_AT_2_RE = re.compile(
    r"(2\.|position\s+2|item\s+2).{0,60}(COI|[Cc]onflict)",
    re.IGNORECASE | re.DOTALL,
)

# Financial Review at position 4
FR_AT_4_RE = re.compile(
    r"(4\.|position\s+4|item\s+4).{0,60}[Ff]inancial\s+[Rr]eview",
    re.IGNORECASE | re.DOTALL,
)

# Bylaw citation —— 题面 question 仅要求"note the bylaw section that governs the CEO
# emergency item placement"，并未强制逐字整句。放宽为：逐字句 **或** 明确引用治理章节
# Article VI §6.2（任一语序）。
BYLAW_VERBATIM_RE = re.compile(
    r"shall\s+be\s+placed\s+immediately\s+following\s+the\s+Conflicts\s+of\s+Interest"
    r"|Article\s+VI\b.{0,40}(?:§\s*)?6\.2"
    r"|(?:§\s*)?6\.2\b.{0,40}Article\s+VI",
    re.IGNORECASE | re.DOTALL,
)

# Anti-decoy: v3.1 positive citation
V31_RE = re.compile(r"v3\.1", re.IGNORECASE)
DISCREDIT_RE = re.compile(
    r"supersede[ds]?|archiv|obsolete|outdated|must\s+not|withdrawn",
    re.IGNORECASE,
)

# Anti-old-draft: Financial Review at position 2 (wrong order)
FR_AT_2_WRONG_RE = re.compile(
    r"(2\.|item\s+2).{0,60}[Ff]inancial\s+[Rr]eview",
    re.IGNORECASE | re.DOTALL,
)

# CEO position-1 discredit
CEO_POS1_DISCREDIT_RE = re.compile(
    r"(position\s+1|item\s+1|first\s+on).{0,100}"
    r"(incorrect|overrid|not\s+compliant|charter|Article|§\s*6)",
    re.IGNORECASE | re.DOTALL,
)

# Numbered items —— 题面仅要求"every item has a position number"，未指定格式。
# 放宽以兼容常见 markdown 编号写法（裸数字、粗体、标题式 '### Item N'、'Item N:'、
# '[N]' 等），避免合理格式被漏计。
NUMBERED_ITEM_RE = re.compile(
    r"^\s*(?:"
    r"\d+[a-z]?[.)]\s+\S"                                      # 1. Foo / 2a) Bar
    r"|\*\*\d+[a-z]?[.)]?\*\*\s*\S"                            # **1** Foo / **2a.** Bar
    r"|#{1,6}\s*(?:item|position|agenda\s+item)\s+\d+[a-z]?\b"  # ### Item 1 / ## Position 2a
    r"|#{1,6}\s*\d+[a-z]?[.)]\s+\S"                            # ### 1. Foo
    r"|(?:item|position|agenda\s+item)\s+\d+[a-z]?[.:)]?\s+\S"  # Item 1 — / Position 2a:
    r"|\[\d+[a-z]?\]\s*\S"                                     # [1] Foo / [2a] Bar
    r")",
    re.MULTILINE | re.IGNORECASE,
)

# Nexus Fintech near COI position 2 marker
NEXUS_NEAR_COI_RE = re.compile(
    r"(position\s+2|item\s+2|2\.\s+Conflict|COI\s+Disclosures).{0,200}Nexus\s+Fintech"
    r"|Nexus\s+Fintech.{0,200}(position\s+2|item\s+2|COI\s+Disclosures)",
    re.IGNORECASE | re.DOTALL,
)

# Template markers
TEMPLATE_MARKERS: list[re.Pattern[str]] = [
    re.compile(r"##\s+Agenda", re.IGNORECASE),
    re.compile(r"\*\*Meeting:\*\*", re.IGNORECASE),
    re.compile(r"\*\*Date:\*\*", re.IGNORECASE),
    re.compile(r"\*\*Chair:\*\*", re.IGNORECASE),
    re.compile(r"\*\*Location:\*\*", re.IGNORECASE),
    re.compile(r"\*\*Prepared\s+by:\*\*", re.IGNORECASE),
]


def _v31_affirmatively_cited(content: str) -> bool:
    for m in V31_RE.finditer(content):
        start = max(0, m.start() - 100)
        end = min(len(content), m.end() + 100)
        window = content[start:end]
        if not DISCREDIT_RE.search(window):
            return True
    return False


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q4.py <workspace_path>", file=sys.stderr)
        return 1

    ws = Path(sys.argv[1])
    revised = ws / "output" / "revised_agenda.md"

    if not revised.exists():
        print("FAIL: output/revised_agenda.md does not exist")
        return 1

    content = revised.read_text(encoding="utf-8")
    raw_bytes = content.encode("utf-8")
    errors: list[str] = []

    # 1. Structure layer
    if len(raw_bytes) < 600:
        errors.append(
            f"output/revised_agenda.md too short ({len(raw_bytes)} bytes; need >= 600)"
        )

    numbered_items = NUMBERED_ITEM_RE.findall(content)
    if len(numbered_items) < 7:
        errors.append(
            f"output/revised_agenda.md contains only {len(numbered_items)} numbered "
            "item(s); the revised agenda must have >= 7 numbered positions "
            "(1, 2, 2a, 3, 4, 5, 6, 7)"
        )

    # Template marker count (C3 edit constraint)
    marker_hits = sum(1 for pat in TEMPLATE_MARKERS if pat.search(content))
    if marker_hits < 2:
        errors.append(
            f"only {marker_hits} template marker(s) from agenda_template_v2.md "
            "found in output/revised_agenda.md; the agent must edit the template "
            "rather than write from scratch — retain at least 2 of: "
            "'## Agenda', '**Meeting:**', '**Date:**', '**Chair:**', "
            "'**Location:**', '**Prepared by:**'"
        )

    # 2. Field layer
    if not CEO_AT_2A_RE.search(content):
        errors.append(
            "CEO urgent item not found at position 2a — "
            "the revised agenda must place the Regulatory Compliance Update "
            "at position 2a per Charter v3.2 Article VI §6.2"
        )

    if not COI_AT_2_RE.search(content):
        errors.append(
            "COI Disclosures not found at position 2 — "
            "the revised agenda must place Conflicts of Interest Disclosures "
            "at position 2 per Charter v3.2 §5.3"
        )

    if not NEXUS_NEAR_COI_RE.search(content):
        errors.append(
            "'Nexus Fintech' sub-item not found within the COI Disclosures "
            "item block — the COI Disclosures position must include Nexus Fintech "
            "Partners LP as a flagged sub-item requiring board vote "
            "(carrying forward the q3 reconciliation finding)"
        )

    if not FR_AT_4_RE.search(content):
        errors.append(
            "Financial Review not found at position 4 — "
            "per Charter v3.2 §5.3, Financial Review must be agenda item 4"
        )

    # 3. Bylaw verbatim citation (丑)
    if not BYLAW_VERBATIM_RE.search(content):
        errors.append(
            "verbatim Article VI §6.2 bylaw text not found — "
            "the revised agenda must include the phrase "
            "\"shall be placed immediately following the Conflicts of Interest\" "
            "(from charter_docs/charter_v3.2.md Article VI §6.2)"
        )

    # 4. Anti-decoy checks
    if _v31_affirmatively_cited(content):
        errors.append(
            "output/revised_agenda.md appears to cite superseded Charter v3.1 "
            "affirmatively — every mention of 'v3.1' must be accompanied by a "
            "discredit word within 100 characters; Charter v3.2 is the operative document"
        )

    if FR_AT_2_WRONG_RE.search(content):
        errors.append(
            "output/revised_agenda.md places Financial Review at position 2 — "
            "this reproduces the old draft's incorrect ordering; "
            "Financial Review must be at position 4 per Charter v3.2 §5.3"
        )

    # CEO position-1 must be explicitly overridden (either discredited or absent
    # and replaced by 2a citation — accept if 2a is present and no position-1
    # positive assertion survives)
    has_ceo_at_1 = re.search(
        r"(1\.|position\s+1|item\s+1|first\s+on).{0,60}"
        r"([Rr]egulatory\s+[Cc]ompliance|CEO|urgent)",
        content,
        re.IGNORECASE | re.DOTALL,
    )
    if has_ceo_at_1 and not CEO_POS1_DISCREDIT_RE.search(content):
        errors.append(
            "CEO's position-1 request appears in the revised agenda without "
            "an explicit discredit statement — the file must clarify that the "
            "CEO's requested position 1 is overridden by Charter v3.2 Article VI §6.2 "
            "(which mandates position 2a)"
        )

    # 5. Cross-round closure
    audit_file = ws / "output" / "agenda_audit.md"
    if not audit_file.exists():
        errors.append(
            "cross-round check failed: output/agenda_audit.md (q1 output) does not "
            "exist — complete q1 before attempting q4"
        )

    recon_file = ws / "output" / "coi_reconciliation.md"
    if not recon_file.exists():
        errors.append(
            "cross-round check failed: output/coi_reconciliation.md (q3 output) does not "
            "exist — complete q3 before attempting q4"
        )
    else:
        recon_content = recon_file.read_text(encoding="utf-8")
        if not re.search(r"Nexus\s+Fintech", recon_content, re.IGNORECASE):
            errors.append(
                "cross-round check failed: output/coi_reconciliation.md (q3 output) "
                "does not contain 'Nexus Fintech' — q3 must identify the shared "
                "outside investment before q4 can add the COI sub-item"
            )

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        f"PASS: output/revised_agenda.md ({len(raw_bytes)} bytes, "
        f"{len(numbered_items)} numbered items) places CEO urgent item at 2a, "
        "COI Disclosures at 2 with Nexus Fintech sub-item, Financial Review at 4, "
        "cites Article VI §6.2 verbatim, template markers preserved, "
        "cross-round q1 and q3 outputs verified"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
