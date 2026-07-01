"""check_q6.py — Union feedback prediction (cross-round coherence).

Ground truth:
  UNION_REP likely supportive of RMEA (she submitted the memo mandating it).
  HOSP_B_CARDIO_HEAD loses direct CMO reporting line — union concern about seniority.
  Concession 1: HOSP_B_CARDIO_HEAD retains joint title or co-leadership during transition.
  Concession 2: Union consultation rights before final org chart is filed with accreditor.

Cross-round consistency (hard fail):
  - If q4 output/equipment_disposition_memo.md contains RMEA, then q6 must reference
    RMEA positively (support/align/comply/satisf/approv within 200 chars).
  - If q5 output/merger_plan.md references HOSP_A_CARDIO_HEAD / Garrett Osei as
    org-chart recommendation, then q6 must address HOSP_B_CARDIO_HEAD's seniority concern.

Pass conditions:
  output/union_feedback_prediction.md
    1. Exists; >= 500 bytes; >= 3 distinct sections.
    2. RMEA cross-round closure (conditional).
    3. HOSP_B_CARDIO_HEAD seniority concern present (conditional on q5).
    4. At least one concession proposal.
    5. No new financial facts.
    6. All four stakeholder names present collectively.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Regex anchors.
RMEA_RE = re.compile(r"RMEA|Regional\s+Medical\s+Equipment\s+Authority", re.IGNORECASE)
RMEA_POSITIVE_RE = re.compile(
    r"support|align|satisf|comply|approv|endorse|favor|favour|welcome",
    re.IGNORECASE,
)
HOSP_B_CONCERN_RE = re.compile(
    r"HOSP_B_CARDIO_HEAD|Soo.?Jin\s+Lim|seniority|reporting.*level|level.*report"
    r"|subordinat|demotion|reduced.*reporting|reporting.*chain",
    re.IGNORECASE,
)
# Distinct concession categories. q6 题面要求 'two concrete concessions'，因此必须命中
# 至少两类不同的具体让步，而非任意单个常见词（transition / interim / offer 等）即过。
# 真实 ground truth 的两类让步：
#   (A) joint/co-leadership/保留头衔（过渡期）；
#   (B) 在最终组织架构上报前给予工会协商/咨询权。
# 这里再额外提供若干常见的具体让步类别，要求 >= 2 类不同命中。
CONCESSION_CATEGORIES: list[tuple[str, re.Pattern[str]]] = [
    (
        "joint_or_co_leadership",
        re.compile(
            r"joint(?:\s+title)?|co.?lead|co.?director|co.?head|co.?chair"
            r"|retain.{0,30}title|retain.{0,30}(?:lead|director|head)"
            r"|dual\s+report|shared\s+leadership",
            re.IGNORECASE,
        ),
    ),
    (
        "union_consultation_rights",
        re.compile(
            r"consult.{0,30}union|union.{0,30}consult|consultation\s+right"
            r"|right\s+to\s+consult|union.{0,30}sign.?off\s+window"
            r"|review\s+(?:the\s+)?org.?chart|consult.{0,30}org.?chart",
            re.IGNORECASE,
        ),
    ),
    (
        "transition_or_interim_arrangement",
        re.compile(
            r"transition\s+(?:period|arrangement|plan|window)"
            r"|interim\s+(?:title|role|arrangement|period|leadership)"
            r"|temporary\s+title|phased\s+(?:transition|integration)"
            r"|grace\s+period",
            re.IGNORECASE,
        ),
    ),
    (
        "compensation_or_seniority_protection",
        re.compile(
            r"seniority\s+protection|protect.{0,30}seniority"
            r"|salary\s+protection|red.?circle|grandfather"
            r"|no\s+(?:loss|reduction)\s+(?:in|of)\s+(?:pay|seniority|rank)",
            re.IGNORECASE,
        ),
    ),
]
NEW_FINANCIALS_RE = re.compile(r"\$[0-9]|cost.*[0-9]{5,}|[0-9]{5,}.*cost", re.IGNORECASE)

# Stakeholder detection.
STAKEHOLDERS = [
    ("MERGER_LEAD / Priya Mehta", re.compile(r"MERGER_LEAD|Priya\s+Mehta", re.IGNORECASE)),
    ("HOSP_A_CARDIO_HEAD / Garrett Osei", re.compile(r"HOSP_A_CARDIO_HEAD|Garrett\s+Osei", re.IGNORECASE)),
    ("HOSP_B_CARDIO_HEAD / Soo-Jin Lim", re.compile(r"HOSP_B_CARDIO_HEAD|Soo.?Jin\s+Lim", re.IGNORECASE)),
    ("UNION_REP / Fatima Nkosi", re.compile(r"UNION_REP|Fatima\s+Nkosi", re.IGNORECASE)),
]


def _count_sections(text: str) -> int:
    headers = len(re.findall(r"^#{1,4}\s+\S", text, re.MULTILINE))
    if headers >= 3:
        return headers
    lettered = len(re.findall(r"^\(?[a-cA-C]\)?[\.\)]\s+\S", text, re.MULTILINE))
    list_blocks = re.findall(r"(?:^[ \t]*[-*]\s+.+\n?)+", text, re.MULTILINE)
    return headers + lettered + len(list_blocks)


def _read_q4_has_rmea(ws: Path) -> bool:
    memo = ws / "output" / "equipment_disposition_memo.md"
    if not memo.exists():
        return False
    return bool(RMEA_RE.search(memo.read_text(encoding="utf-8")))


def _read_q5_has_hosp_a_rec(ws: Path) -> bool:
    plan = ws / "output" / "merger_plan.md"
    if not plan.exists():
        return False
    return bool(re.search(r"HOSP_A_CARDIO_HEAD|Garrett\s+Osei", plan.read_text(encoding="utf-8"), re.IGNORECASE))


def _rmea_positive_within(text: str, window: int = 200) -> bool:
    """Return True if a positive framing word appears within `window` chars of any RMEA match."""
    for m in RMEA_RE.finditer(text):
        start = max(0, m.start() - window)
        end = min(len(text), m.end() + window)
        if RMEA_POSITIVE_RE.search(text[start:end]):
            return True
    return False


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: check_q6.py <workspace>", file=sys.stderr)
        return 1
    ws = Path(sys.argv[1])
    errors: list[str] = []
    warnings: list[str] = []

    target = ws / "output" / "union_feedback_prediction.md"
    if not target.exists():
        print(f"FAIL: {target} does not exist")
        return 1

    text = target.read_text(encoding="utf-8")

    # 1. Size and section structure.
    if len(text.encode("utf-8")) < 500:
        errors.append(
            f"union_feedback_prediction.md too short ({len(text.encode())} bytes); "
            "must be >= 500 bytes"
        )
    section_count = _count_sections(text)
    if section_count < 3:
        errors.append(
            f"union_feedback_prediction.md has fewer than 3 distinct sections "
            f"(found {section_count}); expected sections for (a) RMEA response, "
            "(b) org-chart objection, (c) concession proposals"
        )

    # 2. Cross-round RMEA closure.
    q4_has_rmea = _read_q4_has_rmea(ws)
    if q4_has_rmea:
        if not RMEA_RE.search(text):
            errors.append(
                "union_feedback_prediction.md does not reference RMEA — "
                "q4 equipment disposition used RMEA as the disposal authority; "
                "q6 must address UNION_REP's response to the RMEA requirement"
            )
        elif not _rmea_positive_within(text, window=200):
            errors.append(
                "union_feedback_prediction.md references RMEA but does not frame "
                "UNION_REP's response positively (expected 'support', 'align', 'comply', "
                "'approve', or equivalent within 200 chars of RMEA) — "
                "UNION_REP submitted the memo that mandated RMEA; she should be supportive"
            )
    else:
        warnings.append(
            "WARNING: q4 equipment_disposition_memo.md did not use RMEA — "
            "q4 used the wrong arbitration outcome; q6 RMEA cross-check skipped"
        )

    # 3. HOSP_B_CARDIO_HEAD seniority concern (conditional on q5 recommendation).
    q5_has_hosp_a_rec = _read_q5_has_hosp_a_rec(ws)
    if q5_has_hosp_a_rec:
        if not HOSP_B_CONCERN_RE.search(text):
            errors.append(
                "union_feedback_prediction.md does not address "
                "HOSP_B_CARDIO_HEAD / Dr. Soo-Jin Lim's seniority concern — "
                "the org-chart recommendation (Hospital A Director as unified Director) "
                "reduces HOSP_B_CARDIO_HEAD's reporting level; the prediction must "
                "acknowledge this as a likely union objection"
            )

    # 4. Concession proposals — q6 题面要求 'two concrete concessions'。
    matched_concessions = [
        label for label, pat in CONCESSION_CATEGORIES if pat.search(text)
    ]
    if len(matched_concessions) < 2:
        errors.append(
            "union_feedback_prediction.md must propose TWO concrete concessions "
            "(found "
            f"{len(matched_concessions)}: {matched_concessions}). The question asks "
            "for two distinct, concrete concessions MERGER_LEAD could offer "
            "(e.g., joint/co-leadership title retention during transition, AND "
            "union consultation rights before the org chart is filed)."
        )

    # 5. No new financial facts.
    if NEW_FINANCIALS_RE.search(text):
        errors.append(
            "union_feedback_prediction.md introduces new financial figures "
            "not established in prior rounds — q6 must be grounded only in "
            "decisions from rounds 4 and 5"
        )

    # 6. All four stakeholders.
    for label, pattern in STAKEHOLDERS:
        if not pattern.search(text):
            errors.append(
                f"union_feedback_prediction.md does not name stakeholder: {label}"
            )

    # Emit warnings (non-blocking).
    for w in warnings:
        print(w)

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 1

    print(
        "PASS: union_feedback_prediction.md addresses RMEA alignment (positive framing), "
        "HOSP_B_CARDIO_HEAD seniority concern, proposes concessions, "
        "introduces no new financial facts, and names all four stakeholders"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
