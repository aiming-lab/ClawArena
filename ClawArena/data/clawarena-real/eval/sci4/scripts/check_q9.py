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
    data, err = _load_json(ws / "output" / "consequential_damages_analysis.json")
    if err: _finish([err])
    # case_citation 必须精确含方括号形式 [1854] EWHC J70（来自 legal_research/Hadley_v_Baxendale_brief.md）
    cc = str(data.get("case_citation", "")).strip()
    if not re.search(r"\[1854\]\s*EWHC\s*J70", cc):
        fails.append(
            "case_citation == %r (must contain '[1854] EWHC J70' with square brackets verbatim — "
            "format '[1854] EWHC J70'; '9 Exch 341' or '(1854)' without brackets are NOT acceptable)" % cc
        )
    # hadley_rule_applied 必须引用 Rule 2（后果性损害），且 analysis_text 须提及 Rule 2
    hr = str(data.get("hadley_rule_applied", "")).lower()
    if "rule 2" not in hr and "second rule" not in hr and "rule2" not in hr:
        fails.append(
            "hadley_rule_applied must explicitly state 'Rule 2' (special/consequential damages) — "
            "the word 'special' alone is insufficient; 'Rule 2' must appear"
        )
    # bot_claim_status 必须指出 bot 说法不正确
    bs = str(data.get("bot_claim_status", "")).lower()
    if "incorrect" not in bs and "wrong" not in bs and "false" not in bs and "inaccurate" not in bs:
        fails.append("bot_claim_status must state that the bot's claim (Hadley 'superseded') is INCORRECT")
    # analysis_text 必须非空且 ≥ 60 words，并须引用 MSA 具体条款
    at = str(data.get("analysis_text", ""))
    if not at:
        fails.append("analysis_text must be present and non-empty")
    else:
        word_count = len(at.split())
        if word_count < 60:
            fails.append(
                "analysis_text is too short (%d words); must be at least 60 words providing substantive "
                "legal analysis of how Hadley Rule 2 applies to MSA §10.2" % word_count
            )
        at_low = at.lower()
        if "§10.2" not in at and "10.2" not in at:
            fails.append(
                "analysis_text must reference MSA §10.2 (the consequential damages exclusion clause "
                "being analysed in this question)"
            )
    _finish(fails)
main()
