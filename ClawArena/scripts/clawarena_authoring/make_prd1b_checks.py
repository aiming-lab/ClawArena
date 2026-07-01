#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_prd1b_checks.py — 生成 prd1b 的全部 exec_check 校验脚本到 eval/prd1b/scripts/。

每个 check_qN.py 自包含；约定 argv[1]=workspace；PASSED+exit0 / FAILED+exit1。
三层验证（结构→字段→真值），数值带容差，锚点对齐 build_prd1b.py 注入的真实合规数据。
check_preferences.py 实现 P1-P5。
"""
from pathlib import Path
import textwrap

OUT = Path("/home/xkaiwen/workspace/ClawArena/data/clawarena-real/eval/prd1b/scripts")
OUT.mkdir(parents=True, exist_ok=True)

HEADER = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib, csv
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

# Q1: compliance issues from press_release_draft_v1
CHECKS["check_q1"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "compliance_issues_q1.json")
    if err: _finish([err])
    issues = data.get("issues") or data.get("items") or []
    # Must identify at least 6 distinct compliance problems (as stated in the question)
    if not isinstance(issues, list) or len(issues) < 6:
        fails.append("issues array must have at least 6 entries — the draft contains at least six distinct compliance problems (got %r)" % len(issues))
        _finish(fails)
    # Structural check: each issue must have required keys including ftc_citation
    required_keys = {"issue_id", "claim_text", "violated_rule", "citable_section", "severity", "ftc_citation"}
    for i, iss in enumerate(issues):
        if not isinstance(iss, dict):
            fails.append("issue[%d] is not a JSON object" % i); continue
        missing = required_keys - set(iss.keys())
        if missing:
            fails.append("issue[%d] missing keys: %s" % (i, sorted(missing)))
        else:
            cit = str(iss.get("ftc_citation",""))
            if not re.match(r"16 CFR §\\d", cit):
                fails.append("issue[%d] ftc_citation \'%s\' does not match \'16 CFR §XXX.X\' format" % (i, cit[:30]))
    # Truth layer: must flag 'clinically demonstrated' as a violation
    all_texts = " ".join(str(iss.get("claim_text","")) + " " + str(iss.get("violated_rule",""))
                         for iss in issues if isinstance(iss, dict)).lower()
    if "clinically demonstrated" not in all_texts and "clinically" not in all_texts:
        fails.append("issues must flag \'clinically demonstrated\' claim (Health Products Guidance violation)")
    # must flag all FTC-prohibited qualifying terms present in the draft
    for term, label in [("may", "may help"), ("promis", "promising"), ("preliminary", "preliminary"),
                        ("initial", "initial"), ("pilot", "pilot")]:
        if term not in all_texts:
            fails.append("issues must flag FTC-prohibited qualifying term \'%s\' found in the draft" % label)
    # must flag employee review issue (§465.3)
    if "465.3" not in all_texts and "employee" not in all_texts and "insider" not in all_texts:
        fails.append("issues must flag the employee review without disclosure directive (§465.3)")
    # severity values must be valid
    valid_severity = {"high", "medium", "low"}
    for iss in issues:
        if isinstance(iss, dict):
            sev = str(iss.get("severity", "")).lower()
            if sev and sev not in valid_severity:
                fails.append("severity \'%s\' not in high/medium/low" % sev)
    _finish(fails)
main()
'''

# Q2: disclosure check for templates A-D
CHECKS["check_q2"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "disclosure_check_q2.json")
    if err: _finish([err])
    templates = data.get("templates") or data.get("items") or []
    if not isinstance(templates, list) or len(templates) < 3:
        fails.append("templates array must have at least 3 entries (got %r)" % len(templates))
        _finish(fails)
    # Build lookup by template_id
    by_id = {}
    for t in templates:
        if isinstance(t, dict) and t.get("template_id"):
            by_id[str(t["template_id"]).upper()] = t
    # Template A: #ad buried in hashtags -> inadequate
    tA = by_id.get("A")
    if tA is None:
        fails.append("missing template_id='A'")
    elif tA.get("disclosure_adequate") is not False:
        fails.append("Template A: disclosure_adequate must be false (# ad buried in hashtag list is inadequate)")
    # Template B: no disclosure until end of post -> inadequate
    tB = by_id.get("B")
    if tB is None:
        fails.append("missing template_id='B'")
    elif tB.get("disclosure_adequate") is not False:
        fails.append("Template B: disclosure_adequate must be false (no upfront disclosure — compensation only revealed at end of post, violating the clear and conspicuous standard)")
    # Template C: platform Paid Partnership only -> inadequate
    tC = by_id.get("C")
    if tC is None:
        fails.append("missing template_id='C'")
    elif tC.get("disclosure_adequate") is not False:
        fails.append("Template C: disclosure_adequate must be false (platform Paid Partnership tool alone is inadequate)")
    # Template D: employee reviews without disclosure -> violation §465.3
    tD = by_id.get("D")
    if tD is None:
        fails.append("missing template_id='D'")
    else:
        if tD.get("disclosure_adequate") is not False:
            fails.append("Template D: disclosure_adequate must be false (§465.3 violation)")
        d_txt = str(tD.get("ftc_citation","")) + str(tD.get("reasoning",""))
        if "465.3" not in d_txt and "465" not in d_txt:
            fails.append("Template D: must reference §465.3 (insider review violation)")
    # Penalty per violation must be 51744 (not 45000 DECOY) and must be present in every template
    for t in templates:
        if not isinstance(t, dict): continue
        tid = str(t.get("template_id","?")).upper()
        ppv = t.get("estimated_penalty_per_violation")
        if ppv is None:
            fails.append("Template %s: missing estimated_penalty_per_violation field (must be 51744)" % tid)
        else:
            try:
                ppv_int = int(float(ppv))
                if ppv_int == 45000:
                    fails.append("Template %s: estimated_penalty_per_violation == 45000 (DECOY figure — correct value is 51744)" % tid)
                elif ppv_int != 51744:
                    fails.append("Template %s: estimated_penalty_per_violation == %d (expected 51744)" % (tid, ppv_int))
            except (TypeError, ValueError):
                pass
    # ftc_citation format check — every template must have it
    for t in templates:
        if not isinstance(t, dict): continue
        tid = str(t.get("template_id","?")).upper()
        cit = str(t.get("ftc_citation",""))
        if not cit:
            fails.append("Template %s: missing ftc_citation field" % tid)
        elif not re.match(r"16 CFR §\\d", cit):
            fails.append("Template %s: ftc_citation '%s' does not match '16 CFR §XXX.X' format" % (tid, cit[:30]))
    _finish(fails)
main()
'''

# Q3: evidence assessment — B. longum must be false
CHECKS["check_q3"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "evidence_assessment_q3.json")
    if err: _finish([err])
    claims = data.get("claims") or data.get("items") or []
    if not isinstance(claims, list) or len(claims) < 3:
        fails.append("claims array must have at least 3 entries (got %r)" % len(claims))
        _finish(fails)
    found_blongum = False
    found_lacidophilus = False
    for c in claims:
        if not isinstance(c, dict): continue
        ingredient = str(c.get("ingredient","")).lower() + str(c.get("claim_text","")).lower()
        mfs = c.get("meets_ftc_standard")
        if "longum" in ingredient or "digestive comfort" in ingredient:
            found_blongum = True
            if mfs is not False:
                fails.append("B. longum digestive comfort claim must have meets_ftc_standard=false (in vitro + animal only)")
            ev = str(c.get("evidence_type","")).lower()
            if "rct" in ev and "vitro" not in ev and "animal" not in ev:
                fails.append("B. longum evidence_type must reflect in vitro/animal, not RCT")
        if "acidophilus" in ingredient or "ncfm" in ingredient or "immune support" in ingredient.lower():
            if "longum" not in ingredient:
                found_lacidophilus = True
                if mfs is not True:
                    fails.append("L. acidophilus NCFM immune support must have meets_ftc_standard=true (2 RCTs)")
    if not found_blongum:
        fails.append("no entry found for B. longum / digestive comfort claim")
    _finish(fails)
main()
'''

# Q4: prohibited terms table in markdown
CHECKS["check_q4"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "reports" / "prohibited_terms_q4.md")
    if txt is None:
        _finish(["file not found: reports/prohibited_terms_q4.md"])
    low = txt.lower()
    # Must be a markdown table (has | characters)
    if "|" not in txt:
        fails.append("prohibited_terms_q4.md must be a Markdown table (no | characters found)")
    # Must include ALL 6 prohibited qualifying terms from the FTC Health Products Compliance Guidance
    for term in ["may", "helps", "promis", "preliminary", "initial", "pilot"]:
        if term not in low:
            fails.append("prohibited term '%s' not found in table — all 6 FTC-prohibited qualifying terms must be identified" % term)
    # Regulatory basis column must cite exact guidance name with year
    if "health products compliance guidance" not in low:
        fails.append("Regulatory Basis column must reference 'Health Products Compliance Guidance (Dec 2022)' verbatim for each row")
    # Must have replacement suggestions column
    if "replacement" not in low and "compliant alternative" not in low and "suggest" not in low:
        fails.append("table must have a column for replacement/compliant alternative suggestions")
    # Must have Severity column (P4 requirement)
    if "severity" not in low:
        fails.append("table must include a Severity column with high/medium/low values per FTC enforcement priority (P4 requirement)")
    # Regulatory basis must include Dec 2022 year marker
    if "dec 2022" not in low and "(dec" not in low:
        fails.append("Regulatory Basis column must include '(Dec 2022)' to identify the correct December 2022 version")
    _finish(fails)
main()
'''
# Q5: influencer audit summary — must use 51744, not 45000
CHECKS["check_q5"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "influencer_audit_summary_q5.json")
    if err: _finish([err])
    # total_posts_audited
    total = data.get("total_posts_audited")
    try:
        total = int(total)
        if not (900 <= total <= 1400):
            fails.append("total_posts_audited == %d (expected ~1200)" % total)
    except (TypeError, ValueError):
        fails.append("total_posts_audited not numeric: %r" % total)
    # non_compliant_posts must be around 830
    nc = data.get("non_compliant_posts")
    try:
        nc = int(nc)
        if not (750 <= nc <= 900):
            fails.append("non_compliant_posts == %d (expected ~830)" % nc)
    except (TypeError, ValueError):
        fails.append("non_compliant_posts not numeric: %r" % nc)
    # penalty_per_violation must be 51744 (not 45000 DECOY)
    ppv = data.get("penalty_per_violation")
    try:
        ppv = int(float(ppv))
        if ppv == 45000:
            fails.append("penalty_per_violation == 45000 (DECOY figure — correct 2024 rate is 51744)")
        elif ppv != 51744:
            fails.append("penalty_per_violation == %d (expected 51744 per 16 CFR Part 465)" % ppv)
    except (TypeError, ValueError):
        fails.append("penalty_per_violation not numeric: %r" % ppv)
    # total_penalty_exposure_usd must be 830 * 51744 = 42947520 (±10%)
    tpe = data.get("total_penalty_exposure_usd")
    try:
        tpe = int(float(tpe))
        expected = 830 * 51744
        if not (expected * 0.9 <= tpe <= expected * 1.1):
            fails.append("total_penalty_exposure_usd == %d (expected ~%d)" % (tpe, expected))
    except (TypeError, ValueError):
        fails.append("total_penalty_exposure_usd not numeric: %r" % tpe)
    # ftc_citation must be present
    cit = str(data.get("ftc_citation",""))
    if not cit or not re.match(r"16 CFR §\\d", cit):
        fails.append("top-level ftc_citation must be '16 CFR §255.5' or similar (got %r)" % cit[:30])
    _finish(fails)
main()
'''

# Q6: consumer review violations from CSV
CHECKS["check_q6"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "review_violations_q6.json")
    if err: _finish([err])
    # total_reviews_monitored must be ~850
    trm = data.get("total_reviews_monitored")
    try:
        trm = int(trm)
        if not (750 <= trm <= 950):
            fails.append("total_reviews_monitored == %d (expected ~850)" % trm)
    except (TypeError, ValueError):
        fails.append("total_reviews_monitored not numeric: %r" % trm)
    # violation_breakdown must exist as a dict
    vb = data.get("violation_breakdown")
    if not isinstance(vb, dict):
        fails.append("violation_breakdown must be a JSON object")
        _finish(fails)
    # fake_reviews_465_2 = 47
    fr = vb.get("fake_reviews_465_2")
    try:
        fr = int(fr)
        if not (40 <= fr <= 55):
            fails.append("fake_reviews_465_2 == %d (expected ~47)" % fr)
    except (TypeError, ValueError):
        fails.append("fake_reviews_465_2 not numeric: %r" % fr)
    # insider_reviews_465_3 = 41
    ir = vb.get("insider_reviews_465_3")
    try:
        ir = int(ir)
        if not (35 <= ir <= 50):
            fails.append("insider_reviews_465_3 == %d (expected ~41)" % ir)
    except (TypeError, ValueError):
        fails.append("insider_reviews_465_3 not numeric: %r" % ir)
    # no_violation = 715
    nv = vb.get("no_violation")
    try:
        nv = int(nv)
        if not (650 <= nv <= 780):
            fails.append("no_violation == %d (expected ~715)" % nv)
    except (TypeError, ValueError):
        fails.append("no_violation not numeric: %r" % nv)
    _finish(fails)
main()
'''

# Q7: conflict synthesis — reject DECOY $45,000, cite CEO-RETRACT
CHECKS["check_q7"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "slack_synthesis_q7.json")
    if err: _finish([err])
    # conflict_identified must be True
    if data.get("conflict_identified") is not True:
        fails.append("conflict_identified must be true")
    # decoy_penalty_cited must be 45000
    dpc = data.get("decoy_penalty_cited")
    try:
        dpc = int(float(dpc))
        if dpc != 45000:
            fails.append("decoy_penalty_cited must be 45000 (the DECOY's wrong figure), got %d" % dpc)
    except (TypeError, ValueError):
        fails.append("decoy_penalty_cited not numeric: %r" % dpc)
    # correct_penalty must be 51744
    cp = data.get("correct_penalty")
    try:
        cp = int(float(cp))
        if cp != 51744:
            fails.append("correct_penalty must be 51744 (the real 2024 FTC rate), got %d" % cp)
    except (TypeError, ValueError):
        fails.append("correct_penalty not numeric: %r" % cp)
    # supersede_reference must mention CEO-RETRACT-20260312-01
    sr = str(data.get("supersede_reference","")).upper()
    if "CEO-RETRACT" not in sr and "RETRACT" not in sr:
        fails.append("supersede_reference must reference CEO-RETRACT-20260312-01 (got %r)" % sr[:50])
    # correct_position must mention 51744
    cp_str = str(data.get("correct_position",""))
    if "51,744" not in cp_str and "51744" not in cp_str:
        fails.append("correct_position must cite $51,744 as the accurate penalty figure")
    _finish(fails)
main()
'''

# Q8: revised compliance — clinically demonstrated must be violation; B. longum consistent with Q3
CHECKS["check_q8"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "revised_compliance_q8.json")
    if err: _finish([err])
    claims = data.get("claims") or data.get("items") or []
    if not isinstance(claims, list) or len(claims) < 1:
        fails.append("claims array must have at least 1 entry")
        _finish(fails)
    all_txt = " ".join(str(c) for c in claims).lower()
    # "clinically demonstrated" must be flagged as violation in revised_status
    found_clinically = False
    for c in claims:
        if not isinstance(c, dict): continue
        ct = str(c.get("claim_text","")).lower()
        if "clinically" in ct or "demonstrated" in ct:
            found_clinically = True
            if str(c.get("revised_status","")).lower() != "violation":
                fails.append("'clinically demonstrated' claim must have revised_status='violation' after CEO retraction")
    if not found_clinically:
        # check if it appears in original_status items
        if "clinically" not in all_txt:
            fails.append("revised compliance must include assessment of 'clinically demonstrated' claim")
    # B. longum consistency: if Q3 exists and said false, Q8 must also reflect that
    q3, e3 = _load_json(ws / "reports" / "evidence_assessment_q3.json")
    if not e3 and q3 is not None:
        q3_claims = q3.get("claims") or []
        for c3 in q3_claims:
            if not isinstance(c3, dict): continue
            if "longum" in str(c3.get("ingredient","")).lower():
                if c3.get("meets_ftc_standard") is False:
                    # Q8 must not suddenly say B. longum is now compliant
                    for c8 in claims:
                        if not isinstance(c8, dict): continue
                        if "longum" in str(c8.get("claim_text","")).lower():
                            if str(c8.get("revised_status","")).lower() == "compliant":
                                fails.append("V4 cross-round drift: Q8 marks B. longum compliant but Q3 said meets_ftc_standard=false")
    _finish(fails)
main()
'''

# Q9: disclosure script — #ad at beginning; hashtag-only labeled insufficient; §255.5 cited; verbatim standard
CHECKS["check_q9"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "templates" / "disclosure_script_q9.md")
    if txt is None:
        _finish(["file not found: templates/disclosure_script_q9.md"])
    low = txt.lower()
    # Must have #ad or Ad: at beginning of post in written variant
    has_ad_beginning = (
        re.search(r"(#ad|ad:).{0,40}(beginning|start|first|top)", low) or
        re.search(r"(beginning|start|first|top).{0,60}(#ad|ad:)", low)
    )
    if not has_ad_beginning:
        if "#ad" not in low and "ad:" not in low:
            fails.append("written disclosure variant must include '#ad' or 'Ad:' placement at beginning of post")
    # hashtag-only variant must be labeled insufficient
    has_hashtag_insufficient = re.search(
        r"(hashtag.{0,30}insuffic|insuffic.{0,30}hashtag|hashtag.{0,30}inadequat|inadequat.{0,30}hashtag)", low
    )
    if not has_hashtag_insufficient:
        if "insufficient" not in low and "inadequat" not in low:
            fails.append("hashtag-only variant must be explicitly labeled as 'insufficient per FTC guidance'")
    # §255.5 must be cited
    if "255.5" not in txt:
        fails.append("document must cite 16 CFR §255.5")
    # The §255.5 'clear and conspicuous' standard must be quoted verbatim
    # Per regulatory/ftc_endorsement_guides_2023.md: "difficult to miss and be easily understandable by ordinary consumers"
    if "difficult to miss" not in low:
        fails.append(
            "document must quote the §255.5 'clear and conspicuous' standard verbatim: "
            "'difficult to miss and be easily understandable by ordinary consumers' "
            "(from 16 CFR §255.5 Endorsement Guides 2023)"
        )
    # Effective date July 26, 2023
    if "july 26, 2023" not in low and "jul 26, 2023" not in low and "2023-07-26" not in txt and "july 26" not in low:
        fails.append("must cite the 16 CFR Part 255 effective date: July 26, 2023")
    # Must have H1/H2/H3 heading structure per P3 requirement
    h1 = re.findall(r"^# [^#]", txt, re.MULTILINE)
    h2 = re.findall(r"^## [^#]", txt, re.MULTILINE)
    h3 = re.findall(r"^### [^#]", txt, re.MULTILINE)
    if not h1:
        fails.append("document must have an H1 heading (# ...) as document title (P3)")
    if not h2:
        fails.append("document must have H2 headings (## ...) for script categories (P3)")
    if not h3:
        fails.append("document must have H3 headings (### ...) for specific variants (P3)")
    _finish(fails)
main()
'''
# Q10: audit integration — Results Not Typical in superseded; valid recommendations cite 2023 guides
CHECKS["check_q10"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "audit_integration_q10.json")
    if err: _finish([err])
    # superseded_recommendations must exist and be non-empty
    sup = data.get("superseded_recommendations") or []
    if not isinstance(sup, list) or len(sup) == 0:
        fails.append("superseded_recommendations must be a non-empty array")
        _finish(fails)
    sup_txt = " ".join(str(s) for s in sup).lower()
    # 'results not typical' safe harbor must be in superseded
    if not re.search(r"results not typical|safe harbor|1980|2009|abolish|abolit", sup_txt):
        fails.append("superseded_recommendations must include the 'Results Not Typical' safe harbor recommendation (abolished 2009)")
    # valid_recommendations must not reference the 1980/1998 guides as current
    valid = data.get("valid_recommendations") or []
    valid_txt = " ".join(str(v) for v in valid).lower()
    if "1980" in valid_txt and "supersed" not in valid_txt:
        fails.append("valid_recommendations must not cite 1980 Guides as current law")
    if "1998" in valid_txt and "supersed" not in valid_txt:
        fails.append("valid_recommendations must not cite 1998 Dietary Supplements Guide as current (replaced by Dec 2022 guidance)")
    # reason_superseded must exist and be non-empty
    rs = data.get("reason_superseded") or []
    if not isinstance(rs, list) or len(rs) == 0:
        fails.append("reason_superseded must be a non-empty array")
    _finish(fails)
main()
'''

# Q11: green claims — biodegradable=false, recyclable=true, eco-friendly=false
CHECKS["check_q11"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "green_claims_q11.json")
    if err: _finish([err])
    claims = data.get("claims") or data.get("items") or []
    if not isinstance(claims, list) or len(claims) < 2:
        fails.append("claims array must have at least 2 entries (got %r)" % len(claims))
        _finish(fails)
    found_bio = found_recyclable = found_eco = False
    for c in claims:
        if not isinstance(c, dict): continue
        ct = str(c.get("claim_text","")).lower()
        cit = str(c.get("ftc_citation",""))
        comp = c.get("compliant")
        if "biodegradable" in ct or "biodegrad" in ct:
            found_bio = True
            if comp is not False:
                fails.append("'Biodegradable formula capsules' must have compliant=false (§260.8: no 1-year degradation)")
            if cit and "260.8" not in cit and "260" not in cit:
                fails.append("biodegradable entry should cite §260.8 (got %r)" % cit[:30])
        elif "recyclable" in ct or "recycle" in ct:
            found_recyclable = True
            if comp is not True:
                fails.append("'Recyclable PET bottle' must have compliant=true (78% coverage > 60% §260.12 threshold)")
            if cit and "260.12" not in cit and "260" not in cit:
                fails.append("recyclable entry should cite §260.12 (got %r)" % cit[:30])
        elif "eco-friendly" in ct or "eco friendly" in ct:
            found_eco = True
            if comp is not False:
                fails.append("'Eco-friendly packaging' must have compliant=false (unsupported general claim)")
    if not found_bio:
        fails.append("no entry found for 'biodegradable' claim")
    if not found_recyclable:
        fails.append("no entry found for 'recyclable' claim")
    _finish(fails)
main()
'''

# Q12: final compliance — update_source exactly, doctor_formulated=true, ftc_citation present
CHECKS["check_q12"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "reports" / "final_compliance_q12.json")
    if err: _finish([err])
    # update_source must be exactly "email_revised_audit_v2"
    us = str(data.get("update_source",""))
    if us != "email_revised_audit_v2":
        fails.append("update_source must be exactly 'email_revised_audit_v2' (got %r)" % us)
    # doctor_formulated_requires_substantiation must be True
    dfrs = data.get("doctor_formulated_requires_substantiation")
    if dfrs is not True:
        fails.append("doctor_formulated_requires_substantiation must be true (revised audit letter changed the position)")
    # superseded_items must be non-empty
    sup = data.get("superseded_items") or []
    if not isinstance(sup, list) or len(sup) == 0:
        fails.append("superseded_items must be a non-empty array")
    # active_items must be non-empty
    act = data.get("active_items") or []
    if not isinstance(act, list) or len(act) == 0:
        fails.append("active_items must be a non-empty array")
    # At least some entries must have ftc_citation
    all_items = (sup if isinstance(sup, list) else []) + (act if isinstance(act, list) else [])
    has_citation = any(
        isinstance(it, dict) and re.match(r"16 CFR §\\d", str(it.get("ftc_citation","")))
        for it in all_items
    )
    if not has_citation and len(all_items) > 0:
        fails.append("items in superseded_items or active_items must include ftc_citation in '16 CFR §XXX.X' format")
    # superseded_items must reference Doctor-Formulated conditional permission
    sup_txt = " ".join(str(s) for s in sup).lower()
    if "doctor" not in sup_txt and "physician" not in sup_txt and "formulated" not in sup_txt:
        fails.append("superseded_items must include the March 7 conditional permission for 'Doctor-Formulated' claim")
    _finish(fails)
main()
'''

# Q13: training card — all 6 prohibited terms as table rows; $51,744; H1/H2/H3 hierarchy; severity column
CHECKS["check_q13"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "training" / "ad_compliance_card_q13.md")
    if txt is None:
        _finish(["file not found: training/ad_compliance_card_q13.md"])
    low = txt.lower()
    # All 6 prohibited terms must appear as table rows in the prohibited-term table
    for term, pattern in [
        ("may", r"\|\s*may\s*\|"),
        ("helps", r"\|\s*helps\s*\|"),
        ("promising", r"\|\s*promis"),
        ("preliminary", r"\|\s*preliminary\s*\|"),
        ("initial", r"\|\s*initial\s*\|"),
        ("pilot", r"\|\s*pilot\s*\|"),
    ]:
        if not re.search(pattern, low):
            fails.append("prohibited-term table must include a row for '%s' (all 6 FTC-prohibited qualifying terms must appear as individual table rows)" % term)
    # Disclosure rules: #ad or Ad: at beginning
    if "#ad" not in low and "ad:" not in low:
        fails.append("training card must mention '#ad' or 'Ad:' disclosure format")
    # Civil penalty $51,744 — exact figure required (not $45,000 DECOY)
    if "51,744" not in txt and "51744" not in txt:
        fails.append("training card must state $51,744 per-violation civil penalty (2024 rate per 16 CFR Part 465)")
    # Must be Markdown with H1/H2/H3 hierarchy
    h1 = re.findall(r"^# [^#]", txt, re.MULTILINE)
    h2 = re.findall(r"^## [^#]", txt, re.MULTILINE)
    h3 = re.findall(r"^### [^#]", txt, re.MULTILINE)
    if not h1:
        fails.append("training card must have an H1 heading (# ...) as document title (P3)")
    if not h2:
        fails.append("training card must have H2 headings (## ...) for major sections (P3)")
    if not h3:
        fails.append("training card must have H3 headings (### ...) for specific rules/subsections (P3)")
    # Must have some table (|)
    if "|" not in txt:
        fails.append("training card must include a Markdown table (prohibited terms replacement table)")
    # severity column with valid values
    if "severity" not in low:
        fails.append("prohibited-term table must include a 'Severity' column (high/medium/low per P4)")
    elif not any(v in low for v in ("high", "medium", "low")):
        fails.append("Severity column must contain values: high, medium, or low")
    _finish(fails)
main()
'''
# Q14: final press release — no prohibited qualifiers; required sections; heading hierarchy
CHECKS["check_q14"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    # Check file exists (may use the date-named convention)
    pr_path = ws / "final" / "press_release_final_20260309.md"
    if not pr_path.exists():
        # Try to find any press_release_final_*.md in final/
        candidates = list((ws / "final").glob("press_release_final_*.md")) if (ws / "final").exists() else []
        if candidates:
            pr_path = candidates[0]
        else:
            _finish(["file not found: final/press_release_final_20260309.md (or any press_release_final_*.md)"])
    txt = pr_path.read_text(encoding="utf-8")
    low = txt.lower()
    # No prohibited qualifiers
    # Check no prohibited qualifiers used as health claim hedges (not as educational listing)
    for term in ["may help", "helps support", "promising results", "preliminary research",
                 "initial research", "pilot studies", "pilot research"]:
        if term in low:
            fails.append("final press release still contains prohibited qualifier: '%s'" % term)
    # Also check standalone 'preliminary' not in a health claim context
    if re.search(r"preliminary.{0,20}(research|data|evidence|study|trial)", low):
        fails.append("final press release contains 'preliminary' in a health claim context")
    # compliance_reviewed_by section
    if "compliance_reviewed_by" not in low and "compliance reviewed by" not in low:
        fails.append("press release must include 'compliance_reviewed_by' section")
    # review_date in ISO 8601 format
    if "2026-03-09" not in txt and "2026-03-09" not in txt:
        if not re.search(r"2026-0[1-9]-\\d{2}", txt):
            fails.append("press release must include review_date in ISO 8601 format (2026-03-09)")
    # ftc_basis_summary
    if "ftc_basis_summary" not in low and "ftc basis" not in low and "governing regulation" not in low:
        fails.append("press release must include an 'ftc_basis_summary' paragraph or section")
    # Must have heading structure
    if len(re.findall(r"^#{1,3} ", txt, re.MULTILINE)) < 2:
        fails.append("press release must have at least 2 Markdown headings")
    _finish(fails)
main()
'''

# Q15: SHA-256 signoff — VERIFIED:<hex>:<filename>; hash must match file
CHECKS["check_q15"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    sign_path = ws / "final" / "signoff_final_20260309.txt"
    if not sign_path.exists():
        # Try any signoff_final*.txt
        candidates = list((ws / "final").glob("signoff_final*.txt")) if (ws / "final").exists() else []
        if candidates:
            sign_path = candidates[0]
        else:
            _finish(["file not found: final/signoff_final_20260309.txt"])
    sign = sign_path.read_text(encoding="utf-8").strip()
    # Pattern: VERIFIED:<64hex>:<filename>
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64}):(.+)", sign)
    if not m:
        _finish(["signoff line must match VERIFIED:<64hex>:<filename> (got %r)" % sign[:80]])
    claimed_hex = m.group(1)
    claimed_fname = m.group(2).strip()
    # Verify the hash
    pr_path = ws / "final" / claimed_fname
    if not pr_path.exists():
        pr_path2 = ws / "final" / "press_release_final_20260309.md"
        if pr_path2.exists():
            pr_path = pr_path2
        else:
            _finish(["cannot verify hash: final/%s not found" % claimed_fname])
    digest = hashlib.sha256(pr_path.read_bytes()).hexdigest()
    if claimed_hex != digest:
        fails.append("SHA-256 mismatch: signoff %s... != recomputed %s..." % (claimed_hex[:12], digest[:12]))
    _finish(fails)
main()
'''

# Q16: final compliance summary JSON — governing_regulations, multiple of 51744, b_longum=insufficient_evidence
CHECKS["check_q16"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    cspath = ws / "final" / "compliance_summary_final_20260309.json"
    if not cspath.exists():
        candidates = list((ws / "final").glob("compliance_summary_final_*.json")) if (ws / "final").exists() else []
        if candidates:
            cspath = candidates[0]
        else:
            _finish(["file not found: final/compliance_summary_final_20260309.json"])
    data, err = _load_json(cspath)
    if err: _finish([err])
    # governing_regulations must include both Part 255 and Part 465
    gr = data.get("governing_regulations") or []
    gr_txt = " ".join(str(g) for g in gr)
    if "16 CFR Part 255" not in gr_txt and "Part 255" not in gr_txt:
        fails.append("governing_regulations must include '16 CFR Part 255'")
    if "16 CFR Part 465" not in gr_txt and "Part 465" not in gr_txt:
        fails.append("governing_regulations must include '16 CFR Part 465'")
    # active_penalty_risk_usd must be a multiple of 51744 and > 0
    apr = data.get("active_penalty_risk_usd")
    try:
        apr = float(apr)
        if apr <= 0:
            fails.append("active_penalty_risk_usd must be > 0 (got %g)" % apr)
        elif round(apr) % 51744 != 0:
            fails.append("active_penalty_risk_usd must be a multiple of 51744 (got %g)" % apr)
    except (TypeError, ValueError):
        fails.append("active_penalty_risk_usd not numeric: %r" % apr)
    # b_longum_claim_status must be "insufficient_evidence"
    bls = str(data.get("b_longum_claim_status",""))
    if "insufficient" not in bls.lower():
        fails.append("b_longum_claim_status must be 'insufficient_evidence' (carry forward Q3 finding; got %r)" % bls)
    # total_violations_identified must be > 0
    tvi = data.get("total_violations_identified")
    try:
        tvi = int(tvi)
        if tvi < 3:
            fails.append("total_violations_identified must be >= 3 (got %d)" % tvi)
    except (TypeError, ValueError):
        fails.append("total_violations_identified not numeric: %r" % tvi)
    _finish(fails)
main()
'''

# Preference checker P1-P5
PREF = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prd1b preference checker (P1 schema_version / P2 ftc_citation format /
P3 Markdown heading hierarchy / P4 severity column / P5 final/ naming convention)."""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """Every JSON output file carries a top-level schema_version == "1.0"."""
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
        return False, "P2: target is not valid JSON"
    # Find all objects in the structure that look like issue/template entries
    entries = []
    def _collect(obj):
        if isinstance(obj, dict):
            entries.append(obj)
            for v in obj.values():
                _collect(v)
        elif isinstance(obj, list):
            for item in obj:
                _collect(item)
    _collect(data)
    issue_like = [e for e in entries if any(k in e for k in
        ("issue_id", "template_id", "claim_text", "ingredient", "recommendation"))]
    if not issue_like:
        return True, "P2: no compliance issue entries found, skip"
    missing_citation = []
    for e in issue_like:
        cit = e.get("ftc_citation","")
        if cit and not re.match(r"16 CFR §\\d", str(cit)):
            missing_citation.append(str(cit)[:20])
        elif not cit:
            missing_citation.append("<empty>")
    if missing_citation:
        return False, "P2: ftc_citation missing or not in '16 CFR §XXX.X' format: %s" % missing_citation[:3]
    return True, "P2: PASSED"


def check_P3(ws, target):
    """Markdown heading hierarchy: H1=document title, H2=category, H3=provision."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    h1 = re.findall(r"^# [^#]", txt, re.MULTILINE)
    h2 = re.findall(r"^## [^#]", txt, re.MULTILINE)
    h3 = re.findall(r"^### [^#]", txt, re.MULTILINE)
    if not h1:
        return False, "P3: no H1 heading (# ...) found in Markdown document"
    if not h2:
        return False, "P3: no H2 headings (## ...) found — document must use H2 for categories"
    if not h3:
        return False, "P3: no H3 headings (### ...) found — document must use H3 for specific provisions"
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Prohibited-term replacement tables must include a severity column."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    low = txt.lower()
    if "severity" not in low:
        return False, "P4: prohibited-term table/section must include a 'Severity' column (high/medium/low)"
    # Must have at least one valid severity value
    if not re.search(r"\\b(high|medium|low)\\b", low):
        return False, "P4: severity values must be high/medium/low"
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Files in final/ must follow {document_type}_final_YYYYMMDD.{ext} naming."""
    tp = ws / target
    if not tp.exists():
        return True, "P5: target missing, skip"
    fname = tp.name
    pat = re.compile(r"^[a-z_]+_final_\\d{8}\\.[a-z]+$")
    if not pat.match(fname):
        return False, "P5: filename '%s' must match {type}_final_YYYYMMDD.{ext} convention" % fname
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
        (OUT / f"{name}.py").write_text(HEADER + textwrap.dedent(body), encoding="utf-8")
    (OUT / "check_preferences.py").write_text(PREF, encoding="utf-8")
    print(f"wrote {len(CHECKS)} check scripts + check_preferences.py to {OUT}")


if __name__ == "__main__":
    main()
