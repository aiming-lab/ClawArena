#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_prd1a_checks.py — 生成 prd1a 的全部 exec_check 校验脚本到 eval/prd1a/scripts/。

每个 check_qN.py 自包含，约定：argv[1]=workspace；PASSED+exit0 / FAILED+exit1。
三层验证（结构→字段→真值），数值带容差，锚点对齐 build_prd1a.py 注入的真实锚点。
check_preferences.py 实现 P1-P5。生成器内容即评测逻辑，可逐脚本审阅。
"""
from pathlib import Path
import textwrap

OUT = Path("/home/xkaiwen/workspace/ClawArena/data/clawarena-real/eval/prd1a/scripts")
OUT.mkdir(parents=True, exist_ok=True)

HEADER = '''#!/usr/bin/env python3
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
'''

CHECKS = {}

# Q1: compliance_issues_q1.json — JSON array with issues, schema_version, prohibited qualifiers
CHECKS["check_q1"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "compliance_issues_q1.json")
    if err: _finish([err])
    # P1: schema_version at top level
    if not isinstance(data, dict) or str(data.get("schema_version")) != "1.0":
        fails.append("top-level schema_version must be '1.0'")
    # Issues array
    issues = data.get("issues") if isinstance(data, dict) else None
    if issues is None and isinstance(data, list):
        issues = data
    if not isinstance(issues, list) or len(issues) == 0:
        _finish(["issues array is missing or empty"])
    # Must have at least 4 entries (6 prohibited qualifiers + at least some other violations)
    if len(issues) < 4:
        fails.append("expected at least 4 compliance issues, got %d" % len(issues))
    # Each entry must have required fields
    for i, entry in enumerate(issues):
        if not isinstance(entry, dict):
            fails.append("issue[%d] is not a dict" % i); continue
        for req in ("issue_id", "claim_text", "violated_rule", "ftc_citation", "severity"):
            if not entry.get(req):
                fails.append("issue[%d] missing or empty field '%s'" % (i, req))
    # Check that prohibited qualifiers are flagged — look for at least 'promis' or 'preliminar' or 'may' or 'initial'
    all_text = json.dumps(issues).lower()
    found_qualifiers = sum(1 for q in ("may", "promis", "preliminar", "initial", "pilot", "helps")
                          if q in all_text)
    if found_qualifiers < 3:
        fails.append("expected at least 3 of the prohibited qualifiers (may/promising/preliminary/initial/pilot/helps) to be flagged, found markers for %d" % found_qualifiers)
    _finish(fails)
main()
'''

# Q2: disclosure_check_q2.json — per-claim disclosure analysis; penalty = 51744
CHECKS["check_q2"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "disclosure_check_q2.json")
    if err: _finish([err])
    issues = data.get("issues") if isinstance(data, dict) else None
    if issues is None and isinstance(data, list):
        issues = data
    if not isinstance(issues, list) or len(issues) == 0:
        _finish(["disclosure_check_q2.json issues array missing or empty"])
    # Check that at least one entry has disclosure_adequate: false
    has_inadequate = any(
        e.get("disclosure_adequate") is False or str(e.get("disclosure_adequate")).lower() == "false"
        for e in issues if isinstance(e, dict)
    )
    if not has_inadequate:
        fails.append("at least one entry must have disclosure_adequate: false (undisclosed paid endorsement)")
    # Check penalty field — must be 51744, NOT 45000
    for entry in issues:
        if not isinstance(entry, dict): continue
        pen = entry.get("estimated_penalty_per_violation")
        if pen is not None:
            try:
                pen_f = float(pen)
                if abs(pen_f - 45000.0) < 100:
                    fails.append("estimated_penalty_per_violation = 45000 (DECOY value); must be 51744")
                if abs(pen_f - 51744.0) > 100 and pen_f != 0.0:
                    fails.append("estimated_penalty_per_violation = %s (expected 51744 or 0 for compliant)" % pen)
            except (TypeError, ValueError):
                pass
    # Must have at least one entry with penalty = 51744
    has_correct_penalty = any(
        abs(float(e.get("estimated_penalty_per_violation", 0)) - 51744.0) < 100
        for e in issues if isinstance(e, dict) and e.get("estimated_penalty_per_violation") is not None
    )
    if not has_correct_penalty:
        fails.append("at least one entry must have estimated_penalty_per_violation = 51744 (2024 rate per 16 CFR Part 465)")
    # V9: §255.5 must be referenced
    all_text = json.dumps(data).lower()
    if "255.5" not in all_text and "255" not in all_text:
        fails.append("report must reference 16 CFR §255.5 (material connection disclosure)")
    # P2: ftc_citation format check
    for entry in issues:
        if not isinstance(entry, dict): continue
        cit = entry.get("ftc_citation", "")
        if cit and not re.search(r"16 CFR §\d", str(cit)):
            fails.append("ftc_citation '%s' does not match '16 CFR §XXX.X' format" % cit[:40])
    _finish(fails)
main()
'''

# Q3: evidence_assessment_q3.json — meets_ftc_standard: in vitro/animal must be false
CHECKS["check_q3"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "evidence_assessment_q3.json")
    if err: _finish([err])
    items = data.get("claims") if isinstance(data, dict) else None
    if items is None and isinstance(data, list):
        items = data
    if not isinstance(items, list) or len(items) == 0:
        _finish(["evidence_assessment_q3.json claims array missing or empty"])
    for entry in items:
        if not isinstance(entry, dict): continue
        ev = str(entry.get("evidence_type", "")).lower()
        std = entry.get("meets_ftc_standard")
        # In vitro studies, animal studies, pilot studies must NOT meet standard
        if any(x in ev for x in ("in vitro", "animal", "pilot")):
            if std is True or str(std).lower() == "true":
                fails.append("claim with evidence_type '%s' must have meets_ftc_standard: false per FTC guidance" % ev[:50])
        # RCT claims can meet standard
        if "rct" in ev or "randomized" in ev:
            pass  # acceptable either way for this check
    # At least one entry must be false (in vitro Bi-07 evidence)
    has_false = any(
        e.get("meets_ftc_standard") is False or str(e.get("meets_ftc_standard")).lower() == "false"
        for e in items if isinstance(e, dict)
    )
    if not has_false:
        fails.append("at least one claim must have meets_ftc_standard: false (in vitro/animal/pilot evidence is insufficient per FTC)")
    # At least one entry must be true (LGG has 3 RCTs)
    has_true = any(
        e.get("meets_ftc_standard") is True or str(e.get("meets_ftc_standard")).lower() == "true"
        for e in items if isinstance(e, dict)
    )
    if not has_true:
        fails.append("at least one claim must have meets_ftc_standard: true (LGG has adequate RCT evidence)")
    _finish(fails)
main()
'''

# Q4: prohibited_terms_q4.md — Markdown table with all 6 prohibited qualifiers
CHECKS["check_q4"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "reports" / "prohibited_terms_q4.md")
    if txt is None:
        _finish(["file not found: reports/prohibited_terms_q4.md"])
    low = txt.lower()
    # Must be a Markdown file with at least one table
    if "|" not in txt:
        fails.append("prohibited_terms_q4.md must contain a Markdown table (no '|' found)")
    # Check all 6 prohibited qualifiers are present
    for term in ("may", "helps", "promis", "preliminar", "initial", "pilot"):
        if term not in low:
            fails.append("prohibited term '%s...' not found in table" % term)
    # Check ftc_basis column content
    if "health products compliance guidance" not in low:
        fails.append("ftc_basis column must reference 'Health Products Compliance Guidance (Dec 2022)'")
    # Check severity column present
    if "severity" not in low:
        fails.append("table must include 'severity' column (high/medium/low)")
    # Replacement sentences must not contain prohibited terms as standalone qualifiers
    # (loose check — if "may help" appears in replacement text, that's the original, not a replacement)
    _finish(fails)
main()
'''

# Q5: review_management_policy_q5.md — verbatim §465.2(a) and §465.7 text; $51,744
CHECKS["check_q5"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "policies" / "review_management_policy_q5.md")
    if txt is None:
        _finish(["file not found: policies/review_management_policy_q5.md"])
    low = txt.lower()
    # V9: §465.2(a) verbatim language
    if "write, create, or sell" not in low and "write, create" not in low:
        fails.append("must include verbatim §465.2(a) language: 'write, create, or sell a consumer review'")
    # V9: §465.7 verbatim language
    if "unfounded or groundless" not in low and "groundless legal threat" not in low:
        fails.append("must include verbatim §465.7 language: 'unfounded or groundless legal threat'")
    # Penalty amount: 51744, NOT 45000
    if "45,000" in txt or "45000" in txt:
        fails.append("penalty amount must be $51,744 (not $45,000 from DECOY summary)")
    if "51,744" not in txt and "51744" not in txt:
        fails.append("must state $51,744 per violation (2024 rate per 16 CFR Part 465)")
    # §465.5 insider reviews
    if "465.5" not in txt and "insider" not in low:
        fails.append("must address §465.5 insider reviews without disclosure")
    _finish(fails)
main()
'''

# Q6: label_compliance_q6.json — Made in USA; mia_standard_met: false; Kubota $2M
CHECKS["check_q6"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "label_compliance_q6.json")
    if err: _finish([err])
    if not isinstance(data, dict):
        _finish(["label_compliance_q6.json must be a JSON object"])
    # mia_claim_present: true
    if data.get("mia_claim_present") is not True and str(data.get("mia_claim_present", "")).lower() != "true":
        fails.append("mia_claim_present must be true ('Made in USA' appears on label)")
    # mia_standard_met: false (Danish probiotic strains fail all-or-virtually-all)
    if data.get("mia_standard_met") is not False and str(data.get("mia_standard_met", "")).lower() != "false":
        fails.append("mia_standard_met must be false (Danish Chr. Hansen probiotic strains fail 'all or virtually all' standard)")
    # reference_cases must include Kubota — each entry must be a JSON object (not a plain string)
    ref_cases = data.get("reference_cases", [])
    if not isinstance(ref_cases, list) or len(ref_cases) == 0:
        fails.append("reference_cases must be a non-empty array")
        _finish(fails)
    # Kubota entry must exist as a dict with penalty_amount_usd == 2000000 (exact integer, not string)
    kubota_entries = [e for e in ref_cases if isinstance(e, dict) and "kubota" in json.dumps(e).lower()]
    if not kubota_entries:
        fails.append("reference_cases must include a Kubota entry as a JSON object (not a plain string)")
    else:
        kub = kubota_entries[0]
        # penalty_amount_usd must be the integer 2000000
        pen_usd = kub.get("penalty_amount_usd")
        if pen_usd is None:
            fails.append("Kubota reference_case entry must have penalty_amount_usd field (integer 2000000)")
        else:
            try:
                if int(pen_usd) != 2000000:
                    fails.append("Kubota penalty_amount_usd must be 2000000 (got %r)" % pen_usd)
            except (TypeError, ValueError):
                fails.append("Kubota penalty_amount_usd must be integer 2000000 (got %r)" % pen_usd)
    # supporting_facts must have at least 3 entries
    sf = data.get("supporting_facts", [])
    if not isinstance(sf, list) or len(sf) < 3:
        fails.append("supporting_facts must contain at least 3 entries explaining the analysis")
    _finish(fails)
main()
'''

# Q7: slack_synthesis_q7.json — V1+V5: Sarah correct; penalty 51744; safe harbor abolished
CHECKS["check_q7"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "slack_synthesis_q7.json")
    if err: _finish([err])
    if not isinstance(data, dict):
        _finish(["slack_synthesis_q7.json must be a JSON object"])
    # V5: correct penalty must be 51744, NOT 45000
    pen = data.get("correct_penalty_usd")
    try:
        pen_f = float(pen)
        if abs(pen_f - 45000.0) < 100:
            fails.append("correct_penalty_usd = 45000 (DECOY value from bot summary); correct 2024 rate is 51744")
        elif abs(pen_f - 51744.0) > 100:
            fails.append("correct_penalty_usd = %s (expected 51744 per 16 CFR Part 465, 2024 rate)" % pen)
    except (TypeError, ValueError):
        fails.append("correct_penalty_usd must be a number, got: %r" % pen)
    # V1: conflict identified
    if not data.get("conflict_identified"):
        fails.append("conflict_identified must be true")
    # Safe harbor: abolished
    sh = str(data.get("safe_harbor_status", "")).lower()
    if not (re.search(r"abolish|abol|remov|no longer|invalid|void", sh)):
        fails.append("safe_harbor_status must describe 'results not typical' safe harbor as abolished/no longer valid")
    # V5: discarded_position must mention $45,000 is wrong / from bot summary
    discard = str(data.get("discarded_position", "")).lower()
    if not (re.search(r"45[,]?000|bot|decoy|non.authoritativ|not authoritativ", discard)):
        fails.append("discarded_position must explain that Mike's $45,000 came from the non-authoritative bot summary")
    _finish(fails)
main()
'''

# Q8: revised_compliance_q8.json — V2+V10: clinically demonstrated still violation; Q3 consistent
CHECKS["check_q8"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "revised_compliance_q8.json")
    if err: _finish([err])
    items = data.get("claims") if isinstance(data, dict) else None
    if items is None and isinstance(data, list):
        items = data
    if not isinstance(items, list) or len(items) == 0:
        _finish(["revised_compliance_q8.json claims array missing or empty"])
    # V2: "clinically demonstrated" must still be flagged as violation
    all_text = json.dumps(data).lower()
    if "clinically demonstrated" in all_text:
        # find the entry
        for entry in items:
            if not isinstance(entry, dict): continue
            if "clinically demonstrated" in str(entry.get("claim_text", "")).lower() or \
               "clinically demonstrated" in str(entry.get("claim_id", "")).lower():
                revised = str(entry.get("revised_status", "")).lower()
                if re.search(r"compliant|approved|acceptable|valid|permitted", revised):
                    fails.append("'clinically demonstrated' must remain a violation after Update 1 (CEO withdrawal doesn't change FTC standards)")
    # V4: consistency with Q3 — in vitro/animal claims must still be non-compliant
    for entry in items:
        if not isinstance(entry, dict): continue
        ev = str(entry.get("evidence_type", "")).lower()
        rev_status = str(entry.get("revised_status", "")).lower()
        if any(x in ev for x in ("in vitro", "animal", "pilot")):
            if re.search(r"compliant\b|accepted|standard.?met", rev_status):
                fails.append("in vitro/animal/pilot claims must remain non-compliant after Update 1 (consistent with Q3)")
    # P2: ftc_citation format
    for entry in items:
        if not isinstance(entry, dict): continue
        cit = str(entry.get("ftc_citation", ""))
        if cit and not re.search(r"16 CFR §\d", cit):
            fails.append("ftc_citation '%s' does not match '16 CFR §XXX.X' format" % cit[:40])
    _finish(fails)
main()
'''

# Q9: disclosure_script_q9.md — V9: #ad at beginning; hashtag-only labeled insufficient; July 26 2023
CHECKS["check_q9"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "templates" / "disclosure_script_q9.md")
    if txt is None:
        _finish(["file not found: templates/disclosure_script_q9.md"])
    low = txt.lower()
    # Must have #ad or Ad: at beginning of post example
    if not re.search(r"(#ad|ad:).*beginning|beginning.*(#ad|ad:)|start.*#ad|#ad.*start", low):
        # More lenient: just check #ad or Ad: appears AND beginning somewhere
        if not re.search(r"#ad|ad:", low):
            fails.append("social media version must include '#ad' or 'Ad:' disclosure example")
        elif "beginning" not in low and "start" not in low:
            fails.append("must specify that '#ad' or 'Ad:' goes at the BEGINNING of the post")
    # Hashtag-only version must be labeled insufficient
    if not re.search(r"hashtag.{0,60}(insuffici|inadequat|not.?enough|not.?compliant)", low) and \
       not re.search(r"(insuffici|inadequat|not.?enough).{0,60}hashtag", low):
        fails.append("hashtag-only version must be explicitly labeled as insufficient per FTC guidance")
    # July 26 2023 effective date
    if "july 26, 2023" not in low and "july 26 2023" not in low and "2023-07-26" not in txt:
        fails.append("must reference July 26, 2023 (effective date of 16 CFR Part 255)")
    # V9: §255.5 material connection definition
    if "materially affect" not in low and "material connection" not in low:
        fails.append("must quote or reference §255.5 material connection language")
    _finish(fails)
main()
'''

# Q10: audit_integration_q10.json — V6+V10: results not typical in superseded_recommendations
CHECKS["check_q10"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "audit_integration_q10.json")
    if err: _finish([err])
    if not isinstance(data, dict):
        _finish(["audit_integration_q10.json must be a JSON object"])
    sup = data.get("superseded_recommendations")
    if not isinstance(sup, list) or len(sup) == 0:
        fails.append("superseded_recommendations must be a non-empty array")
    else:
        # V6: results not typical must be in superseded
        sup_text = json.dumps(sup).lower()
        if not re.search(r"results\s+not\s+typical|results.not.typical", sup_text):
            fails.append("superseded_recommendations must include the 'results not typical' safe harbor reference (it was abolished in 2009)")
    reason = data.get("reason_superseded")
    if not isinstance(reason, list) or len(reason) == 0:
        fails.append("reason_superseded must be a non-empty array")
    else:
        reason_text = json.dumps(reason).lower()
        if not re.search(r"abolish|2009|no longer|remov|invalid", reason_text):
            fails.append("reason_superseded must explain that the safe harbor was abolished (reference to 2009 or abolition)")
    valid = data.get("valid_recommendations")
    if not isinstance(valid, list) or len(valid) == 0:
        fails.append("valid_recommendations must be a non-empty array")
    _finish(fails)
main()
'''

# Q11: green_claims_q11.json — V4+V8+V9: biodegradable non-compliant per §260.8; recyclable 60% threshold
CHECKS["check_q11"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "green_claims_q11.json")
    if err: _finish([err])
    items = data.get("claims") if isinstance(data, dict) else None
    if items is None and isinstance(data, list):
        items = data
    if not isinstance(items, list) or len(items) == 0:
        _finish(["green_claims_q11.json claims array missing or empty"])
    all_text = json.dumps(data).lower()
    # biodegradable must be non-compliant
    bio_found = False
    for entry in items:
        if not isinstance(entry, dict): continue
        claim = str(entry.get("claim", "")).lower()
        if "biodegrad" in claim:
            bio_found = True
            compliant = entry.get("compliant")
            if compliant is True or str(compliant).lower() == "true":
                fails.append("'Biodegradable Capsule Shells' must be compliant: false (HDPE fails one-year standard per §260.8)")
    if not bio_found:
        fails.append("must include assessment of 'Biodegradable' claim")
    # §260.8 must be cited
    if "260.8" not in all_text:
        fails.append("must cite §260.8 for the biodegradable claim assessment")
    # 60% threshold must be mentioned for recyclable
    if "60" not in all_text and "sixty" not in all_text:
        fails.append("must mention the 60% (substantial majority) threshold for recyclable claims per §260.12")
    # V9: ftc_citation format
    for entry in items:
        if not isinstance(entry, dict): continue
        cit = str(entry.get("ftc_citation", ""))
        if cit and not re.search(r"16 CFR §\d", cit):
            fails.append("ftc_citation '%s' does not match '16 CFR §XXX.X' format" % cit[:40])
    _finish(fails)
main()
'''

# Q12: final_compliance_q12.json — V2+V10: update_source exact; doctor_formulated_requires_substantiation: true
CHECKS["check_q12"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "final_compliance_q12.json")
    if err: _finish([err])
    if not isinstance(data, dict):
        _finish(["final_compliance_q12.json must be a JSON object"])
    # V10: update_source must be exactly "email_revised_audit_v2"
    src = data.get("update_source", "")
    if src != "email_revised_audit_v2":
        fails.append("update_source must be exactly 'email_revised_audit_v2' (got %r)" % src)
    # V2: doctor_formulated_requires_substantiation must be true after supersede
    dr = data.get("doctor_formulated_requires_substantiation")
    if dr is not True and str(dr).lower() != "true":
        fails.append("doctor_formulated_requires_substantiation must be true (revised audit v2 withdrew conditional permission)")
    # superseded_items must be a non-empty array of plain strings (not objects/dicts)
    sup = data.get("superseded_items")
    if not isinstance(sup, list) or len(sup) == 0:
        fails.append("superseded_items must be a non-empty array of plain strings")
    else:
        for i, item in enumerate(sup):
            if not isinstance(item, str):
                fails.append("superseded_items[%d] must be a plain string, not a %s (object entries are not accepted)" % (i, type(item).__name__))
        # At least one string must mention the 'results not typical' retraction
        sup_text = " ".join(str(s) for s in sup if isinstance(s, str)).lower()
        if not re.search(r"results\s+not\s+typical|results.not.typical", sup_text):
            fails.append("superseded_items must include a string entry referencing the 'results not typical' safe harbor retraction")
    # active_items must be non-empty
    act = data.get("active_items")
    if not isinstance(act, list) or len(act) == 0:
        fails.append("active_items must be a non-empty array")
    else:
        if len(act) < 5:
            fails.append("active_items must list at least 5 current compliance requirements, got %d" % len(act))
    _finish(fails)
main()
'''

# Q13: ad_compliance_card_q13.md — P3+P4: all 6 prohibited qualifiers; #ad example; July 26 2023; severity
CHECKS["check_q13"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "training" / "ad_compliance_card_q13.md")
    if txt is None:
        _finish(["file not found: training/ad_compliance_card_q13.md"])
    low = txt.lower()
    # All 6 prohibited qualifiers must be listed
    for term in ("may", "helps", "promis", "preliminar", "initial", "pilot"):
        if term not in low:
            fails.append("prohibited qualifier '%s...' not found in training card" % term)
    # #ad disclosure example
    if "#ad" not in txt and "ad:" not in low:
        fails.append("must include '#ad' or 'Ad:' disclosure example")
    # July 26, 2023 effective date
    if "july 26, 2023" not in low and "july 26 2023" not in low and "2023-07-26" not in txt:
        fails.append("must reference July 26, 2023 (effective date of 16 CFR Part 255)")
    # severity column
    if "severity" not in low:
        fails.append("any prohibited terms table must include 'severity' column (P4)")
    # H1 heading present (P3)
    if not re.search(r"^#\s+", txt, re.MULTILINE):
        fails.append("must have H1 heading (P3 heading structure)")
    _finish(fails)
main()
'''

# Q14: final/press_release_final_20260603.md — P3+P5: exact filename; compliance review summary; ftc_basis_summary
CHECKS["check_q14"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    # P5: exact filename
    p = ws / "final" / "press_release_final_20260603.md"
    if not p.exists():
        _finish(["file not found: final/press_release_final_20260603.md (P5 naming required)"])
    txt = p.read_text(encoding="utf-8")
    low = txt.lower()
    # Compliance Review Summary section
    if "compliance review summary" not in low:
        fails.append("must include '## Compliance Review Summary' section")
    # ftc_basis_summary
    if "ftc_basis_summary" not in low and "ftc basis summary" not in low:
        fails.append("must include ftc_basis_summary paragraph listing governing regulations")
    # compliance_reviewed_by
    if "compliance_reviewed_by" not in low and "compliance reviewed by" not in low:
        fails.append("must include compliance_reviewed_by field")
    # review_date in ISO 8601
    if not re.search(r"review_date|review date", low):
        fails.append("must include review_date field")
    if not re.search(r"\d{4}-\d{2}-\d{2}", txt):
        fails.append("review_date must be in ISO 8601 format (YYYY-MM-DD)")
    # Must NOT contain worst prohibited terms in claims context
    if "clinically demonstrated to support" in low:
        fails.append("'clinically demonstrated to support' still present — this claim was flagged as a violation in Q1")
    if "scientifically proven" in low:
        fails.append("'scientifically proven' still present — this was flagged as a violation")
    _finish(fails)
main()
'''

# Q15: final/signoff_final_20260603.txt — V7: VERIFIED:<sha256>:filename
CHECKS["check_q15"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    # P5: exact filename
    sign_path = ws / "final" / "signoff_final_20260603.txt"
    if not sign_path.exists():
        _finish(["file not found: final/signoff_final_20260603.txt (P5 naming required)"])
    sign = sign_path.read_text(encoding="utf-8")
    line = sign.strip()
    # Format: VERIFIED:<64hex>:filename
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64}):press_release_final_20260603\\.md", line)
    if not m:
        _finish(["signoff line must match VERIFIED:[a-f0-9]{64}:press_release_final_20260603.md (got %r)" % line[:100]])
    # Recompute SHA-256 of the press release
    pr = ws / "final" / "press_release_final_20260603.md"
    if not pr.exists():
        _finish(["cannot verify hash: final/press_release_final_20260603.md missing"])
    digest = hashlib.sha256(pr.read_bytes()).hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: signoff %s...!= recomputed %s..." % (m.group(1)[:12], digest[:12]))
    _finish(fails)
main()
'''

# Q16: final/compliance_summary_q16.json — V8+V4+V9: strict schema; governing_regulations; penalty multiple
CHECKS["check_q16"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "final" / "compliance_summary_q16.json")
    if err: _finish([err])
    if not isinstance(data, dict):
        _finish(["compliance_summary_q16.json must be a JSON object"])
    # schema_version
    if str(data.get("schema_version")) != "1.0":
        fails.append("schema_version must be '1.0'")
    # total_violations_identified: positive integer
    tvi = data.get("total_violations_identified")
    if not isinstance(tvi, int) or tvi <= 0:
        fails.append("total_violations_identified must be a positive integer")
    # violations_resolved: non-negative integer
    vr = data.get("violations_resolved")
    if not isinstance(vr, int) or vr < 0:
        fails.append("violations_resolved must be a non-negative integer")
    # active_penalty_risk_usd: positive multiple of 51744
    apr = data.get("active_penalty_risk_usd")
    try:
        apr_f = float(apr)
        if apr_f <= 0:
            fails.append("active_penalty_risk_usd must be positive")
        # Must be a multiple of 51744 (within ±100)
        remainder = apr_f % 51744.0
        if remainder > 100 and (51744.0 - remainder) > 100:
            fails.append("active_penalty_risk_usd = %s must be a multiple of 51744 (per-violation rate; NOT 45000)" % apr_f)
    except (TypeError, ValueError):
        fails.append("active_penalty_risk_usd must be a number, got: %r" % apr)
    # governing_regulations: must contain "16 CFR Part 255" AND "16 CFR Part 465"
    gov = data.get("governing_regulations")
    if not isinstance(gov, list):
        fails.append("governing_regulations must be an array")
    else:
        gov_strs = [str(x) for x in gov]
        if not any("16 CFR Part 255" in s for s in gov_strs):
            fails.append("governing_regulations must include '16 CFR Part 255'")
        if not any("16 CFR Part 465" in s for s in gov_strs):
            fails.append("governing_regulations must include '16 CFR Part 465'")
    # review_date: ISO 8601
    rd = data.get("review_date", "")
    if not re.search(r"\d{4}-\d{2}-\d{2}", str(rd)):
        fails.append("review_date must be in ISO 8601 format (YYYY-MM-DD)")
    _finish(fails)
main()
'''

# Q17: decision_timeline_q17.json — V4+V10: 8 events; two supersede chains
CHECKS["check_q17"] = '''
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
'''

# check_preferences.py — P1-P5
PREF = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prd1a preference checker (P1-P5).

P1: Every JSON output must carry top-level schema_version == "1.0"
P2: Every compliance issue entry must carry ftc_citation in "16 CFR §XXX.X" format
P3: Markdown reports use H1=document title, H2=claim category, H3=specific provision
P4: Prohibited terms table must include severity column (high/medium/low)
P5: All files under final/ must follow {document_type}_final_YYYYMMDD.{ext} naming
"""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Every JSON output file carries a top-level schema_version == '1.0'."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    if not isinstance(data, dict):
        return False, "P1: top-level must be a JSON object carrying schema_version"
    if str(data.get("schema_version")) != "1.0":
        return False, "P1: missing top-level schema_version == \\"1.0\\" (got %r)" % data.get("schema_version")
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Every compliance issue entry must carry ftc_citation in '16 CFR §XXX.X' format."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return True, "P2: not JSON, skip"
    # Get items — could be at root list or under 'issues'/'claims'/'entries' key
    items = None
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        for k in ("issues", "claims", "entries", "items"):
            if isinstance(data.get(k), list):
                items = data[k]; break
    if not items:
        return True, "P2: no items array found, skip"
    for i, entry in enumerate(items):
        if not isinstance(entry, dict): continue
        cit = str(entry.get("ftc_citation", ""))
        if not cit:
            return False, "P2: item[%d] missing ftc_citation field" % i
        if not re.search(r"16 CFR §\d", cit):
            return False, "P2: item[%d] ftc_citation '%s' does not match '16 CFR §XXX.X' format" % (i, cit[:40])
    return True, "P2: PASSED"


def check_P3(ws, target):
    """Markdown reports: H1=document title, H2=claim category, H3=specific provision."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    if not target.endswith(".md"):
        return True, "P3: not a Markdown file, skip"
    # Must have at least one H1 (#) heading
    if not re.search(r"^#\s+\S", txt, re.MULTILINE):
        return False, "P3: Markdown file missing H1 heading (must be '# Document Title')"
    # Must have at least one H2 (##) heading for claim category
    if not re.search(r"^##\s+\S", txt, re.MULTILINE):
        return False, "P3: Markdown file missing H2 section heading (must be '## Claim Category')"
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Prohibited terms table must include severity column."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    if not target.endswith(".md"):
        return True, "P4: not a Markdown file, skip"
    # Only check if the file has a table
    if "|" not in txt:
        return True, "P4: no Markdown table found, skip"
    if "severity" not in txt.lower():
        return False, "P4: Markdown table missing 'severity' column (must be high/medium/low)"
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Files under final/ must follow {document_type}_final_YYYYMMDD.{ext} naming."""
    p = Path(target)
    if "final" not in str(p.parent):
        return True, "P5: not under final/, skip"
    name = p.name
    pat = re.compile(r"^[a-z_]+_final_\d{8}\.[a-z]+$")
    if not pat.match(name):
        return False, "P5: file name '%s' does not match {document_type}_final_YYYYMMDD.{ext} pattern" % name
    return True, "P5: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4, "P5": check_P5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4,P5")
    ap.add_argument("--target", default="reports/")
    a = ap.parse_args()
    ws = Path(a.workspace)
    rules = [r.strip() for r in a.rules.split(",") if r.strip()]
    unknown = [r for r in rules if r not in RULES]
    if unknown:
        print("FAILED: unknown rules: %s" % unknown); sys.exit(1)
    fails = []
    for r in rules:
        ok, msg = RULES[r](ws, a.target)
        print(msg)
        if not ok:
            fails.append(msg)
    if fails:
        for m in fails:
            print("FAILED: " + m)
        sys.exit(1)
    print("PASSED"); sys.exit(0)


if __name__ == "__main__":
    main()
'''


def main():
    for name, body in CHECKS.items():
        code = HEADER + "\n" + textwrap.dedent(body)
        (OUT / f"{name}.py").write_text(code, encoding="utf-8")
    (OUT / "check_preferences.py").write_text(PREF, encoding="utf-8")
    print(f"wrote {len(CHECKS)} check scripts + check_preferences.py to {OUT}")


if __name__ == "__main__":
    main()
