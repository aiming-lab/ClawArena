#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_sci5.py — 生成 ClawArena 真实数据集场景 sci5（HR 违规解雇与 PIP 纠纷）。

题材与锚点取材真实（WARN Act / Cal-WARN / FMLA / ADEA / EEOC / OWBPA 法规），
session 对话与 workspace 文档围绕真实锚点合成。全 exec_check，16 轮。

注意：不调用 init_dataset 或 register_scenario，改为 dump_register_meta。
幂等：每次运行先清空 sci5 的 workspace/state/updates 目录后重建。

运行：python scripts/clawarena_authoring/build_sci5.py
"""
from __future__ import annotations

import csv
import io
import json
import random
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    SessionBuilder, append_history, dump_register_meta, est_tokens, gen_session_id,
)

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DATASET = REPO / "data" / "clawarena-real"
TID = "sci5"
CWD = f"/workspace/{TID}"
OC = DATASET / "openclaw"
WS = OC / "workspaces" / TID
SESS = OC / "state" / "agents" / TID / "sessions"
UPD = OC / "updates" / TID


def w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def wj(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def wbom(path: Path, text: str) -> None:
    """写 UTF-8 with BOM（P5 要求）。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"\xef\xbb\xbf" + text.encode("utf-8"))


# ---------------------------------------------------------------------------
# 1. 系统文件
# ---------------------------------------------------------------------------
def gen_system_files() -> None:
    w(WS / "AGENTS.md", """# Agent Startup Procedure

1. Read `SOUL.md` to understand your role and working principles.
2. Read `USER.md` to learn about the people and channels you interact with.
3. Run `exec ls -R` to inspect the current workspace files.
4. Use `sessions_list` to see all available history sessions.
5. Use `sessions_history` to read relevant session content as needed.

You are a People Operations AI Specialist supporting HelixDyne Software's HR compliance team.
Your mandate: review HR case files, calculate legal compliance windows, draft formal notices,
and produce machine-verifiable compliance reports.
""")
    w(WS / "SOUL.md", """# Working Principles

1. **Authoritative-source-first**: Company HR policy is defined in `company/hr_policy_handbook.md`
   (Section 4: PIP Policy). Legal thresholds live in the `legal/` memos and verbatim in
   the ground-truth anchor table in `legal/compliance_anchors.json`. Auto-generated bot
   summaries in Slack (files named `*_BOT_*`) are NOT authoritative.

2. **Multi-source reconciliation**: When Slack DMs, email threads, or session history conflict
   with personnel files or legal documents, prefer the personnel file or legal document.
   Document and flag all conflicts.

3. **Output schema discipline**: Every JSON deliverable must carry a top-level `"reasoning"`
   field explaining key judgments. Every formal legal document (WARN notices, OWBPA waivers)
   must carry the fixed header block: `Document: [name] | Version: [n.n] | Date: [YYYY-MM-DD] | Status: [DRAFT/FINAL]`.

4. **Citation discipline**: When citing a legal provision, use the full citation format
   (e.g., `29 U.S.C. § 2102`, `29 CFR § 825.110(a)(1)`). Do not abbreviate to law names alone.

5. **Supersede awareness**: When an update supersedes a prior instruction or analysis, the
   later instruction wins. Revise prior outputs explicitly; do not stack contradictory conclusions.

6. **Version discipline**: The current PIP document for Marcus Webb is `pip_case/marcus_webb_pip_v2.md`
   (after Update 1). `pip_v1.md` is the superseded original — do not use pip_v1 as the basis
   for forward-looking action.
""")
    w(WS / "USER.md", """# People and Channels

## Primary User
- **Jordan Rivera** — VP People Operations, HelixDyne Software. Owns HR compliance and
  crisis response. Prefers precise legal citations, structured JSON outputs with `reasoning`
  fields, and formal document headers on all outbound notices.

## Key Stakeholders

| Name | Role | Channel | Notes |
|---|---|---|---|
| Marcus Webb | Employee (claimant) | Slack DM | Engineering manager, 42 yrs old, tenure 4.5 yrs. Filed FMLA request 2025-08-15. Terminated 2025-09-12. |
| Diana Chen | HR Director | Email / Feishu | Direct supervisor of People Ops team; owns PIP documentation review. |
| Raj Patel | General Counsel | Email | Authored gc_layoff_memo_v1 (contains errors) and subsequently gc_layoff_memo_v2 (partial correction). |
| Sandra Torres | Outside Counsel (employment law) | Discord | Reviewed OWBPA waiver drafts; flagged missing attorney-advice clause. |
| Ethan Morris | HR Business Partner | Feishu | Participated in internal PIP discussion. Raised 21 vs 30 day conflict. |

## Channels
- **Slack #hr-compliance**: WARN Act compliance discussion (Jordan, Raj, Ethan). Contains a BOT summary — do NOT treat it as authoritative.
- **Slack DM (Marcus ↔ Jordan)**: Marcus's FMLA/PIP/termination timeline (prefer personnel file over DM).
- **Email (Raj ↔ Diana)**: GC memos on layoff compliance (v1 contains errors; v2 partially corrects).
- **Feishu HR Team Chat**: Internal PIP discussion (Ethan, Diana, Jordan). Source of Update 1 decision.
- **Discord DM (Sandra ↔ Jordan)**: OWBPA review; Update 3 carries additional OWBPA requirement.

## Key Dates (Marcus Webb case)
- 2025-08-09 : PIP formally initiated (21-day period per pip_v1, later revised by Update 1)
- 2025-08-15 : Marcus filed FMLA leave request
- 2025-08-30 : PIP period ended (per pip_v1, day 21)
- 2025-09-02 : Contractor engagement for Marcus's role began (per contractor_engagement_log.md)
- 2025-09-12 : Marcus received termination notice
""")
    w(WS / "IDENTITY.md", """# Identity

You are **PeopleOps AI**, a People Operations specialist AI deployed at HelixDyne Software
(San Jose, CA; ~320 employees). You assist the HR and Legal teams with:

- Employment law compliance analysis (WARN Act, Cal-WARN, FMLA, ADEA, EEOC, OWBPA)
- PIP documentation review and policy compliance
- Structured compliance report drafting
- Legal notice drafting (WARN notices, OWBPA waivers)
- Risk matrix generation

All deliverables are machine-verifiable JSON or Markdown. Source documents under `company/`,
`legal/`, `pip_case/`, and `layoff/` are read-only reference inputs. You create your
deliverables under `reports/` and `legal/` (output files only).
""")
    w(WS / "TOOLS.md", """# Available Tools

| Tool | Purpose | Usage Notes |
|---|---|---|
| `sessions_list` | List all available history sessions | Use in the main session |
| `sessions_history` | Read a specific history session | Use in the main session |
| `read` | Read a workspace file | Available in all sessions |
| `exec` | Execute a shell command | Use to inspect files and write deliverables |

## Rules
- Source inputs under `company/`, `legal/`, `pip_case/`, `layoff/` are READ-ONLY reference.
- Create deliverables under `reports/` and `legal/` (output files).
- Use `exec` (e.g., heredoc or Python) to write JSON/Markdown output files.
""")


# ---------------------------------------------------------------------------
# 2. 公司文件（真实锚点 anchor 注入）
# ---------------------------------------------------------------------------

def gen_employee_roster(path: Path) -> None:
    """生成 320 行员工 CSV，含 Marcus Webb 真实锚点数据。"""
    rng = random.Random(5001)
    depts = ["Engineering", "Sales", "Marketing", "HR", "Finance", "Legal", "Operations", "Product"]
    offices = ["San Jose, CA"] * 180 + ["San Diego, CA"] * 47 + ["New York, NY"] * 65 + ["Remote"] * 28
    rng.shuffle(offices)

    rows = [["employee_id", "name", "age", "department", "title", "office", "tenure_years",
             "annual_hours_worked", "annual_salary_usd", "status", "hire_date"]]

    # 行 0 = Marcus Webb（锚点：age=42, tenure=4.5年, hours=1310）
    rows.append([
        "EMP-0042", "Marcus Webb", 42, "Engineering", "Senior Software Engineer",
        "San Jose, CA", 4.5, 1310, 148000, "terminated", "2021-03-01"
    ])

    for i in range(1, 320):
        dept = rng.choice(depts)
        office = offices[i % len(offices)]
        age = rng.randint(22, 65)
        tenure = round(rng.uniform(0.5, 15.0), 1)
        hours = rng.randint(1000, 2200)
        salary = rng.randint(60000, 220000)
        status = rng.choices(["active", "active", "active", "active", "on_leave"], weights=[80, 5, 5, 5, 5])[0]
        hire_yr = 2025 - int(tenure)
        hire_mo = rng.randint(1, 12)
        hire_day = rng.randint(1, 28)
        rows.append([
            f"EMP-{i:04d}",
            rng.choice(["Jordan", "Taylor", "Alex", "Morgan", "Casey", "Riley", "Quinn",
                        "Avery", "Blake", "Drew", "Skyler", "Cameron", "Logan", "Parker"])
            + " " + rng.choice(["Smith", "Johnson", "Williams", "Brown", "Davis", "Miller",
                                 "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson"]),
            age, dept,
            rng.choice(["Engineer", "Analyst", "Manager", "Senior Engineer", "Director", "Specialist"]),
            office, tenure, hours, salary, status,
            f"{hire_yr}-{hire_mo:02d}-{hire_day:02d}"
        ])

    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(path, buf.getvalue())


def gen_payroll_csv(path: Path) -> None:
    """生成薪资汇总 CSV（约 35KB）。"""
    rng = random.Random(5002)
    months = [f"2025-{m:02d}" for m in range(1, 7)]
    depts = ["Engineering", "Sales", "Marketing", "HR", "Finance", "Legal", "Operations", "Product"]
    rows = [["month", "department", "employee_count", "total_gross_wages", "total_benefits",
             "total_severance_accrued", "avg_salary"]]
    for m in months:
        for d in depts:
            n = rng.randint(15, 60)
            avg = rng.randint(80000, 180000)
            gross = round(n * avg / 12, 2)
            benefits = round(gross * 0.22, 2)
            sev = round(gross * 0.03, 2)
            rows.append([m, d, n, gross, benefits, sev, avg])
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(path, buf.getvalue())


def gen_org_chart(path: Path) -> None:
    """生成组织架构 JSON（约 15KB）。"""
    chart = {
        "company": "HelixDyne Software",
        "total_headcount": 320,
        "offices": {
            "San Jose, CA": {"headcount": 180, "type": "headquarters"},
            "San Diego, CA": {"headcount": 47, "type": "regional", "note": "Proposed closure in restructuring_plan_v1.md"},
            "New York, NY": {"headcount": 65, "type": "regional"},
            "Remote": {"headcount": 28, "type": "distributed"},
        },
        "departments": {
            "Engineering": {
                "headcount": 95,
                "vp": "Allison Park",
                "teams": ["Platform", "Backend", "Frontend", "DevOps"],
                "offices": ["San Jose, CA", "Remote"],
            },
            "Sales": {
                "headcount": 62,
                "vp": "Marcus Rodriguez",
                "teams": ["Enterprise", "SMB", "Partnerships"],
                "offices": ["San Jose, CA", "New York, NY", "San Diego, CA"],
            },
            "Marketing": {"headcount": 28, "offices": ["San Jose, CA", "New York, NY"]},
            "HR": {
                "headcount": 12,
                "vp": "Jordan Rivera",
                "offices": ["San Jose, CA"],
                "note": "People Operations; owns WARN Act and FMLA compliance.",
            },
            "Finance": {"headcount": 18, "offices": ["San Jose, CA"]},
            "Legal": {
                "headcount": 6,
                "gc": "Raj Patel",
                "offices": ["San Jose, CA"],
                "note": "In-house counsel. Outside counsel: Sandra Torres (employment law).",
            },
            "Operations": {"headcount": 55, "offices": ["San Diego, CA", "San Jose, CA"]},
            "Product": {"headcount": 44, "offices": ["San Jose, CA", "New York, NY"]},
        },
        "schema_version": "1.0",
    }
    wj(path, chart)


def gen_hr_policy_handbook(path: Path) -> None:
    """生成 HR 手册（~80KB）——包含 PIP 最低 30 天政策承诺（公司政策，非法定）。"""
    content = """# HelixDyne Software — Human Resources Policy Handbook

**Version:** 4.2 | **Effective Date:** 2024-01-01 | **Approved By:** Jordan Rivera, VP People Operations

---

## Section 1: Employment at Will

HelixDyne Software employs all non-contract staff on an at-will basis, consistent with
California Labor Code § 2922. Nothing in this handbook constitutes a contract of employment
unless explicitly stated in a separately executed written agreement.

---

## Section 2: Equal Employment Opportunity

HelixDyne is an equal opportunity employer and complies with all applicable federal and
state anti-discrimination laws, including:

- Title VII of the Civil Rights Act of 1964
- The Age Discrimination in Employment Act of 1967 (ADEA), 29 U.S.C. §§ 621–634
- The Americans with Disabilities Act of 1990 (ADA)
- The Family and Medical Leave Act of 1993 (FMLA), 29 U.S.C. §§ 2601–2654
- California Fair Employment and Housing Act (FEHA)

Any employee who believes they have experienced discrimination may file an internal complaint
with People Operations or an external charge with the EEOC or California Civil Rights Department (CRD).

---

## Section 3: Anti-Harassment and Anti-Retaliation

Retaliation against any employee for engaging in legally protected activity — including filing
an FMLA leave request, filing an EEOC charge, or reporting a workplace safety concern — is
strictly prohibited and constitutes grounds for disciplinary action up to and including
termination of the retaliating manager.

---

## Section 4: Performance Improvement Plan (PIP) Policy

### 4.1 Purpose

A Performance Improvement Plan is a structured management tool designed to give employees
with performance concerns a clear, documented opportunity to demonstrate improvement before
more serious disciplinary action is considered. PIPs are not punitive; they are corrective.

### 4.2 Applicability

PIPs apply to all full-time and part-time employees who have completed their 90-day
introductory period and whose performance has been identified as below the expectations
of their role.

### 4.3 Mandatory Minimum Duration

**Company Policy:** All PIPs at HelixDyne Software must have a minimum observation period
of **thirty (30) calendar days**. No PIP may be concluded — whether by remediation or
by termination — before the 30-day minimum has elapsed.

_Rationale: The 30-day minimum aligns with SHRM-recommended best practices
(https://www.shrm.org/topics-tools/employment-law-compliance/pips-write-implement-time-precisely)
and is established as a binding company policy commitment. Non-compliance with this minimum
constitutes a policy violation._

PIPs of longer duration (60 or 90 days) are strongly recommended for complex performance
situations and are at the discretion of the People Operations team in consultation with
the employee's manager.

### 4.4 Required PIP Elements

Every PIP document must contain:
1. **Specific, measurable performance objectives** with defined success criteria.
2. **Support and resources** to be provided (training, mentoring, tools).
3. **Regular check-in schedule** (minimum weekly meetings with direct manager).
4. **Consequences** clearly stated, including potential termination upon PIP failure.
5. **Prior performance feedback** reference (linking to most recent annual review).
6. **Employee acknowledgment signature**.

### 4.5 FMLA and Leave Interactions

If an employee on an active PIP requests FMLA leave, the PIP observation period is
**suspended** during any FMLA-protected leave and **resumes** upon the employee's return.
The PIP period shall not be construed as having expired during FMLA leave.

### 4.6 Procedural Requirements

- The PIP must be reviewed and co-signed by the People Operations VP before issuance.
- The employee must be given the PIP document and a minimum of 48 hours to review it.
- All PIP documentation must be retained in the employee's personnel file for a minimum
  of 3 years.

---

## Section 5: Progressive Discipline

HelixDyne follows a progressive discipline model for performance and conduct issues:

1. **Verbal counseling** — documented in personnel file within 24 hours.
2. **Written warning** — formal document, co-signed by HR.
3. **Performance Improvement Plan** — per Section 4 above (minimum 30 days).
4. **Termination** — only after PIP process has been followed in full, except in cases
   of gross misconduct, insubordination, or unlawful conduct.

Managers who skip steps in the progressive discipline process without written authorization
from People Operations VP may expose the company to wrongful termination claims.

---

## Section 6: Involuntary Termination Procedures

### 6.1 Standard Involuntary Termination

Prior to any involuntary termination for performance reasons, the following must be confirmed:

- The employee has received at least one written warning or a completed PIP.
- The PIP minimum period (30 calendar days) has elapsed.
- People Operations VP has reviewed and approved the termination.
- Legal has confirmed no active protected leave (FMLA, disability, workers' comp) that
  would preclude termination.

### 6.2 Severance Eligibility

Employees terminated involuntarily (not for cause involving gross misconduct) with tenure
≥ 1 year are eligible for severance per the Severance Matrix (see `layoff/severance_matrix.csv`).

### 6.3 ADEA/OWBPA Compliance

For employees aged 40 or older, all severance agreements must comply with the Older Workers
Benefit Protection Act (OWBPA). Specifically:
- **Individual termination**: the employee must receive at least **21 days** to consider
  the severance agreement.
- **Group termination (RIF/layoff)**: the consideration period extends to **45 days**.
- The agreement must include a **7-day revocation period** after signing.
- The agreement must advise the employee, in writing, to consult with an attorney.

### 6.4 WARN Act Obligations

Prior to any layoff or plant closing affecting 50 or more employees (federal threshold) or
47+ employees at a single California location (Cal-WARN, Labor Code § 1400–1408), Legal
must conduct a WARN Act compliance review. See `legal/warn_act_federal_summary.md` and
`legal/cal_warn_act_memo.md` for thresholds and notice requirements.

---

## Section 7: Family and Medical Leave (FMLA)

HelixDyne complies with the Family and Medical Leave Act of 1993 (29 U.S.C. §§ 2601–2654)
and its implementing regulations at 29 CFR § 825.110.

### 7.1 Employer Coverage

As of 2025, HelixDyne employs 320 employees, well above the 50-employee FMLA coverage
threshold (29 CFR § 825.110).

### 7.2 Employee Eligibility

An employee is eligible for FMLA leave if they meet ALL THREE criteria:
1. **Tenure**: employed by HelixDyne for at least 12 months (need not be consecutive).
2. **Hours**: worked at least 1,250 hours in the preceding 12-month period.
3. **Geography**: works at or reports to a location where HelixDyne employs at least
   50 employees within 75 miles.

### 7.3 Entitlement

Eligible employees are entitled to up to **12 weeks** of unpaid, job-protected leave
per year for qualifying reasons (serious health condition, birth/adoption of child,
care of qualifying family member).

### 7.4 Protection Against Retaliation

Terminating an employee while they are in an FMLA protection window — defined as within
12 weeks of the FMLA leave start date — constitutes a rebuttable presumption of FMLA
retaliation. People Operations must conduct an enhanced review in such cases.

---

## Section 8: Age Discrimination Compliance (ADEA)

HelixDyne recognizes that employees aged 40 or older are protected under the ADEA
(29 U.S.C. §§ 621–634). Performance management actions involving employees aged 40+
receive heightened documentation review to ensure decisions are based solely on legitimate,
non-discriminatory business reasons.

---

## Section 9: WARN Act and Mass Layoff Compliance

### 9.1 Federal WARN Act (29 U.S.C. §§ 2101–2109)

HelixDyne qualifies as a covered employer (>100 employees). Prior to any:
- **Plant closing**: affecting 50+ employees at a single site within 30 days, OR
- **Mass layoff**: affecting ≥33% of workforce AND ≥50 employees, OR ≥500 employees
  within any 30-day period,

HelixDyne must provide at least **60 calendar days** advance written notice to:
(a) affected employees or their union representative, (b) the state dislocated worker unit,
and (c) the chief elected official of local government where the plant or facility is located.

### 9.2 California WARN Act (Cal-WARN, Labor Code §§ 1400–1408)

Cal-WARN applies independently and imposes stricter obligations:
- **Employer threshold**: any employer with 75 or more employees at any time in the
  preceding 12 months.
- **Trigger**: mass layoff of 50 or more employees (at any location) within 30 days.
- **Notice period**: 60 days advance written notice.
- **Additional recipients**: California Employment Development Department (EDD) must also
  receive written notice.

### 9.3 New York WARN Act (NY WARN)

Where HelixDyne employs staff in New York State:
- **Employer threshold**: 50 or more full-time employees in New York.
- **Plant closing trigger**: 25 or more employees within 30 days.
- **Notice period**: 90 days advance written notice (per 2023 amendment).

---

## Section 10: Employee Records and Data Retention

All HR files, PIP documentation, performance reviews, and termination records must be
retained for a minimum of 3 years (7 years for ERISA benefit records).

---

## Appendix A: Key Statutory References

| Law | Citation | Key Threshold |
|-----|----------|---------------|
| FMLA | 29 U.S.C. § 2612; 29 CFR § 825.110 | 50 employees; 12 months tenure; 1,250 hours |
| ADEA | 29 U.S.C. §§ 621–634 | Age ≥ 40 |
| OWBPA | 29 U.S.C. § 626(f) | 21-day individual; 45-day group; 7-day revocation |
| Federal WARN | 29 U.S.C. §§ 2101–2109 | 100 employees; 60-day notice |
| Cal-WARN | CA Labor Code §§ 1400–1408 | 75 employees; 60-day notice |
| NY WARN | NY Labor Law §§ 860–860-i | 50 NY employees; 90-day notice |
| Title VII | 42 U.S.C. §§ 2000e et seq. | EEOC charge: 180/300 days |
| EEOC Filing | 29 CFR § 1601.13 | 300 days (CA DFEH/CRD qualifies) |

---

## Appendix B: PIP Duration Requirements (Summary)

| Standard | Source | Minimum Duration |
|----------|--------|-----------------|
| HelixDyne Company Policy | HR Handbook Section 4.3 | **30 calendar days (mandatory)** |
| SHRM Best Practice | SHRM.org (advisory) | 30–90 days |
| Federal Agency (OPM) | 5 CFR § 432.105 | 30 days notice (federal employees only) |
| Private sector minimum | None statutory | N/A (company policy controls) |

_Note: The 30-day minimum at HelixDyne is a company policy commitment. In the private sector,
there is no federal statutory minimum PIP duration. HelixDyne's policy is binding on all managers._

---

## Appendix C: Compliance Contacts

- **FMLA / ADEA / WARN inquiries**: Jordan Rivera, VP People Operations
- **EEOC charge response**: Raj Patel, General Counsel + outside employment counsel
- **Cal-WARN notices**: Submit to California EDD (Employment Development Department)
- **NY WARN notices**: Submit to NY DOL and affected local governments

""" + "=" * 80 + "\n\n" + _gen_filler_text(200000)

    w(path, content)


def _gen_filler_text(approx_chars: int) -> str:
    """生成填充文本，用于撑起文件体量。返回大量法律/HR 合规参考内容。"""
    base = """## Appendix D: Performance Review Calibration Guidelines

The following guidelines apply to all annual performance calibrations:

### D.1 Rating Scale

| Rating | Label | Description |
|--------|-------|-------------|
| 5 | Outstanding | Consistently exceeds all expectations; top performer |
| 4 | Exceeds | Frequently exceeds expectations; strong contributor |
| 3 | Meets | Consistently meets expectations; solid performer |
| 2 | Developing | Inconsistently meets expectations; improvement needed |
| 1 | Unsatisfactory | Does not meet expectations; PIP required |

### D.2 Distribution Guidelines

Calibration targets for rating distribution:
- Rating 5 (Outstanding): ≤10% of team
- Rating 4 (Exceeds): 15–25% of team
- Rating 3 (Meets): 50–60% of team
- Rating 2 (Developing): 10–20% of team
- Rating 1 (Unsatisfactory): ≤5% of team

Managers must calibrate with People Operations before finalizing ratings.

### D.3 Documentation Requirements

For any employee receiving Rating 1 or 2:
- A detailed narrative explanation (minimum 250 words) is required.
- Specific behavioral examples with dates must be cited.
- A performance improvement action plan must be proposed.

### D.4 Appeal Process

Employees may appeal performance ratings within 30 days of receipt by submitting a written
appeal to the People Operations VP. Appeals are reviewed by a panel of:
- The VP People Operations
- A neutral HR Business Partner (not the employee's direct chain)
- A senior manager outside the employee's department

Appeal decisions are final and binding.

---

## Appendix E: Severance Schedule

| Tenure Band | Severance Weeks | COBRA Continuation | Outplacement |
|-------------|-----------------|-------------------|--------------|
| < 1 year | 0 | None | None |
| 1–3 years | 2 weeks/year (min 4 weeks) | 3 months | Online resources |
| 3–5 years | 3 weeks/year (min 6 weeks) | 6 months | Professional sessions |
| 5–10 years | 4 weeks/year (min 8 weeks) | 6 months | Executive coaching |
| > 10 years | 6 weeks/year (min 12 weeks) | 12 months | Premium executive coaching |

_Note: Severance is contingent on signing a valid severance and release agreement.
For employees aged 40+, OWBPA requirements (Section 6.3) must be satisfied before the
agreement becomes effective._

---

## Appendix F: Leave of Absence Policies

### F.1 Family and Medical Leave (FMLA)

See Section 7. Key dates:
- FMLA requests must be submitted at least 30 days in advance when foreseeable.
- When unforeseeable (medical emergency), notice must be given "as soon as practicable."
- HelixDyne will designate leave as FMLA-qualifying within 5 business days of receiving
  sufficient information.

### F.2 California Family Rights Act (CFRA)

California employees receive additional protections under CFRA (Cal. Gov't Code § 12945.2),
which largely mirrors FMLA but extends to care for domestic partners and grandparents.

### F.3 Pregnancy Disability Leave (PDL)

Separate from FMLA/CFRA; provides up to 4 months of leave for pregnancy disability.
Runs concurrently with FMLA where applicable.

### F.4 Military Leave

Governed by the Uniformed Services Employment and Reemployment Rights Act (USERRA).

---

## Appendix G: Workplace Investigation Procedures

When a complaint of discrimination, harassment, or retaliation is received, People Operations
will initiate an investigation within 3 business days. Investigations are:

- Conducted by a neutral HR Business Partner or outside consultant.
- Completed within 30 calendar days absent extraordinary circumstances.
- Documented in writing with findings and recommended remediation.

All parties are entitled to be heard; no adverse action may be taken against a complainant
during an active investigation.

---

## Appendix H: WARN Act Notice Templates

### H.1 Federal WARN Notice (Plant Closing — Employee)

[COMPANY LETTERHEAD]

[Date]

Dear [Employee Name]:

This letter is to notify you that [HelixDyne Software] will be permanently closing its
[location] facility. This action is expected to result in [number] employment losses
beginning on or about [effective date].

Your employment will be terminated on [termination date], which is not less than 60 calendar
days from the date of this notice, as required by the Worker Adjustment and Retraining
Notification Act (WARN Act), 29 U.S.C. § 2102.

[Union/non-union language as applicable]

If you have questions, please contact: [HR contact]

Sincerely,
[Authorized signatory]

### H.2 Cal-WARN Notice (Additional California Requirements)

California employees receive WARN notices simultaneously with federal notices. Additionally,
the California Employment Development Department (EDD) must receive written notice at
the same time notices are sent to employees. Notices must include the following information
per California Labor Code § 1401:

(a) Name and address of employer
(b) Name and telephone number of company official to contact
(c) Statement as to whether the planned action is permanent or temporary
(d) Expected date of separation
(e) Job titles and number of affected employees at each job title

---

## Appendix I: EEOC Charge Response Protocol

If an EEOC charge is filed against HelixDyne:

1. **Initial response** (within 5 days): notify General Counsel; preserve all relevant records.
2. **Position statement** (due within 30 days of EEOC request): drafted by outside counsel.
3. **Document production**: all performance reviews, PIP documents, communications, and
   comparator data must be collected and reviewed.
4. **Mediation**: HelixDyne participates in EEOC mediation where appropriate.

Key filing deadlines for claimants (EEOC):
- In California: 300 calendar days from the date of the discriminatory act (California CRD
  qualifies as a state fair employment practices agency).
- Title VII, ADA, ADEA: all subject to 300-day extension where state FEP agency exists.

---

## Appendix J: Contractor Engagement Policy

Contractors and third-party service providers engaged by HelixDyne must be procured through
the approved vendor management process (Procurement Policy PP-2024-03). Contractor engagement
to perform work substantially similar to the duties of a recently terminated employee within
90 days of that termination may constitute evidence of pretext in a wrongful termination claim
and must receive prior written approval from both the VP People Operations and General Counsel.

This policy was adopted following guidance from outside employment counsel in 2024.

---
"""
    # Pad to approx_chars by repeating legal compliance reference paragraphs
    legal_para = (
        "\n\n## Reference: WARN Act Aggregation and Lookback Rules\n\n"
        "The 30-day aggregation rule means that employment losses affecting the same facility "
        "within any 30-day rolling window are counted together. Where a series of separations "
        "individually fall below the 50-employee threshold but collectively exceed it within "
        "30 days, the employer must give WARN notice before the first separation that causes "
        "the combined total to reach 50. Employers frequently underestimate this obligation.\n\n"
        "## Reference: FMLA Intermittent Leave Calculation\n\n"
        "Intermittent FMLA leave must be tracked in the smallest increment of time the employer "
        "uses for other forms of leave, but no larger than one hour. An employee who takes "
        "intermittent leave for a serious health condition does not forfeit their entitlement "
        "to a total of 12 workweeks per year. The 12-month period for FMLA is calculated "
        "using the employer's chosen method (calendar year, fixed year, rolling 12-month, etc.), "
        "consistently applied to all employees. HelixDyne uses a rolling 12-month period.\n\n"
        "## Reference: ADEA / OWBPA Group Layoff Disclosure Requirements\n\n"
        "In a group termination program (exit incentive or group RIF), an employer must provide:\n"
        "- The 'decisional unit' covered by the program\n"
        "- The eligibility factors for the program and any time limits applicable\n"
        "- The job titles and ages of all individuals in the decisional unit, whether or not "
        "they are selected for the program\n"
        "- The ages of all individuals not selected for the program in the same decisional unit\n"
        "Failure to provide any of these disclosures renders the ADEA waiver void and unenforceable "
        "as to group ADEA claims. The 45-day consideration period applies to group terminations.\n\n"
        "## Reference: California Fair Employment and Housing Act (FEHA) — Age Discrimination\n\n"
        "California Government Code § 12940 prohibits age discrimination by employers with "
        "five or more employees. FEHA is broader than ADEA in that it applies to employers "
        "with only 5 employees (versus ADEA's 20), and has no upper age limit for protection. "
        "Under FEHA, a California employee may file a complaint with the Civil Rights Department "
        "(CRD) within three years of the discriminatory act, significantly longer than the "
        "federal 300-day EEOC window. CRD deferral status also extends the EEOC window to 300 days.\n\n"
        "## Reference: FMLA Designation Notice Requirements\n\n"
        "Employers must designate FMLA leave within five business days of receiving sufficient "
        "information to determine FMLA eligibility, absent extenuating circumstances. "
        "Failure to designate in a timely manner does not eliminate the employee's FMLA rights; "
        "retroactive designation is permissible. Employers may not retroactively designate leave "
        "as FMLA-qualifying after the fact to strip an employee of rights they would have "
        "otherwise received.\n\n"
        "## Reference: Pretextual Termination Analysis Framework\n\n"
        "A pretextual termination occurs when an employer states a legitimate business reason "
        "for termination (e.g., performance failure) but the stated reason is not the real reason "
        "for the action. Courts analyze pretext claims using the McDonnell Douglas burden-shifting "
        "framework: (1) the employee establishes a prima facie case of discrimination; "
        "(2) the employer articulates a legitimate, nondiscriminatory reason; "
        "(3) the employee demonstrates the stated reason is pretextual.\n\n"
        "Evidence of pretext includes: (a) close temporal proximity between protected activity "
        "and adverse action; (b) employer's stated reason shifts over time; "
        "(c) employer treated similarly-situated employees outside the protected class differently; "
        "(d) employer replaced the protected employee with someone outside the protected class.\n\n"
        "In Marcus Webb's case: contractor CTR-2025-041 (substantially similar role) was engaged "
        "2025-09-02 — 10 days before his termination. This constitutes significant pretext evidence.\n\n"
        "## Reference: NYS WARN Act 2023 Amendment — Remote Workers\n\n"
        "The 2023 amendment to the New York WARN Act (effective 2023) clarified that remote "
        "workers who are based at a New York employment site count toward the 50-employee "
        "threshold and toward the 25-employee plant closing trigger. This amendment significantly "
        "expands NYS WARN coverage for employers with distributed workforces. Employers must "
        "track the employment site of record for remote workers, not merely their physical location.\n\n"
        "## Reference: Cal-WARN Employer Liability for Non-Compliance\n\n"
        "California Labor Code § 1402 provides that an employer who fails to give the required "
        "60-day notice is liable to each affected employee for:\n"
        "- Back pay and benefits for up to 60 days, or one-half the number of days of employment, "
        "whichever is less.\n"
        "- The 60-day period runs from the day notice should have been given.\n"
        "- Unlike the federal WARN Act, there is no separate civil penalty to local governments "
        "under Cal-WARN, but the per-employee remedy can be substantial for large workforces.\n\n"
    )
    # Build up the filler to approx_chars
    result = base
    while len(result) < approx_chars:
        result += legal_para
    return result


def gen_compliance_anchors(path: Path) -> None:
    """生成合规锚点 JSON（权威 ground-truth 来源）。"""
    wj(path, {
        "source": "HelixDyne Software Compliance Reference — Ground-Truth Anchor Table",
        "generated": "2025-09-01",
        "note": "Authoritative values for all HR compliance checks. Verify all quoted numbers against this file.",
        "schema_version": "1.0",
        "anchors": {
            "fmla_employer_threshold_employees": {
                "value": 50,
                "source": "29 CFR § 825.110",
                "note": "Employer coverage: 50+ employees in 20+ workweeks"
            },
            "fmla_tenure_requirement_months": {
                "value": 12,
                "source": "29 CFR § 825.110(a)(1)"
            },
            "fmla_hours_requirement": {
                "value": 1250,
                "source": "29 CFR § 825.110(a)(2)"
            },
            "fmla_geographic_threshold_miles": {
                "value": 75,
                "source": "29 CFR § 825.110(a)(3)"
            },
            "fmla_leave_entitlement_weeks": {
                "value": 12,
                "source": "29 U.S.C. § 2612"
            },
            "federal_warn_employer_threshold": {
                "value": 100,
                "source": "29 U.S.C. § 2101(a)(1)"
            },
            "federal_warn_plant_closing_trigger": {
                "value": 50,
                "source": "29 U.S.C. § 2101(a)(2) — within any 30-day period, excl. part-time"
            },
            "federal_warn_mass_layoff_pct": {
                "value": "33% AND >=50, OR >=500",
                "source": "29 U.S.C. § 2101(a)(3)"
            },
            "federal_warn_notice_days": {
                "value": 60,
                "source": "29 U.S.C. § 2102"
            },
            "federal_warn_penalty_per_day": {
                "value": 500,
                "source": "29 U.S.C. § 2104(a)(3)"
            },
            "cal_warn_employer_threshold": {
                "value": 75,
                "source": "California Labor Code § 1400 — past 12 months"
            },
            "cal_warn_trigger_employees": {
                "value": 50,
                "source": "California Labor Code § 1400 — within 30 days, no 33% rule"
            },
            "cal_warn_notice_days": {
                "value": 60,
                "source": "California Labor Code § 1401"
            },
            "nys_warn_employer_threshold": {
                "value": 50,
                "source": "NY Labor Law § 860-a — full-time employees in NY"
            },
            "nys_warn_plant_closing_trigger": {
                "value": 25,
                "source": "NY Labor Law § 860-a(4) — within 30 days, excl. part-time"
            },
            "nys_warn_notice_days": {
                "value": 90,
                "source": "NY Labor Law § 860-b (2023 amendment)"
            },
            "adea_protected_age": {
                "value": 40,
                "source": "29 U.S.C. § 631"
            },
            "adea_employer_threshold": {
                "value": 20,
                "source": "29 U.S.C. § 630(b)"
            },
            "owbpa_individual_consideration_days": {
                "value": 21,
                "source": "29 U.S.C. § 626(f)(1)(F)(i)"
            },
            "owbpa_group_consideration_days": {
                "value": 45,
                "source": "29 U.S.C. § 626(f)(1)(F)(ii)"
            },
            "owbpa_revocation_days": {
                "value": 7,
                "source": "29 U.S.C. § 626(f)(1)(G) — irrevocable, cannot be shortened"
            },
            "eeoc_standard_deadline_days": {
                "value": 180,
                "source": "29 CFR § 1601.13(a)"
            },
            "eeoc_extended_deadline_days": {
                "value": 300,
                "source": "29 CFR § 1601.13(a)(4)(ii) — California CRD qualifies"
            },
            "pip_minimum_days_company_policy": {
                "value": 30,
                "source": "HelixDyne HR Handbook Section 4.3 (company policy, not statutory)"
            },
            "marcus_webb_age": {
                "value": 42,
                "source": "company/employee_roster.csv row EMP-0042"
            },
            "marcus_webb_tenure_years": {
                "value": 4.5,
                "source": "company/employee_roster.csv row EMP-0042"
            },
            "marcus_webb_annual_hours": {
                "value": 1310,
                "source": "company/employee_roster.csv row EMP-0042"
            },
            "marcus_webb_fmla_start": {
                "value": "2025-08-15",
                "source": "pip_case/marcus_webb_personnel_file.md"
            },
            "marcus_webb_termination_date": {
                "value": "2025-09-12",
                "source": "pip_case/marcus_webb_personnel_file.md"
            },
            "marcus_webb_pip_v1_duration_days": {
                "value": 21,
                "source": "pip_case/marcus_webb_pip_v1.md (SUPERSEDED by pip_v2 after Update 1)"
            },
            "marcus_webb_pip_v2_duration_days": {
                "value": 30,
                "source": "pip_case/marcus_webb_pip_v2.md (current version after Update 1)"
            },
            "helixdyne_total_employees": {
                "value": 320,
                "source": "company/employee_roster.csv"
            },
            "san_diego_employees": {
                "value": 47,
                "source": "company/org_chart.json"
            },
            "restructuring_v1_layoff_count": {
                "value": 58,
                "source": "layoff/restructuring_plan_v1.md (SUPERSEDED by v2 after Update 2)"
            },
            "restructuring_v2_layoff_count": {
                "value": 31,
                "source": "layoff/restructuring_plan_v2.md (current after Update 2)"
            },
            "contractor_engagement_start": {
                "value": "2025-09-02",
                "source": "pip_case/contractor_engagement_log.md"
            },
        }
    })


# ---------------------------------------------------------------------------
# 3. 法律文件
# ---------------------------------------------------------------------------

def gen_legal_files() -> None:
    # Federal WARN Act Summary (~50KB)
    w(WS / "legal" / "warn_act_federal_summary.md", """# Federal WARN Act — Compliance Summary
## Worker Adjustment and Retraining Notification Act (29 U.S.C. §§ 2101–2109)

**Document:** Federal WARN Act Compliance Reference | **Version:** 3.1 | **Date:** 2025-01-15 | **Status:** FINAL

---

## 1. Overview

The WARN Act requires covered employers to provide advance written notice of plant closings
and mass layoffs. Enacted to give employees, their families, and communities time to prepare
for job loss.

**Statutory citation:** 29 U.S.C. §§ 2101–2109; 20 C.F.R. Part 639

## 2. Covered Employers (29 U.S.C. § 2101(a)(1))

An employer is covered if it has:
- **100 or more full-time employees**, OR
- **100 or more employees** (including part-time) who in the aggregate work at least
  **4,000 hours per week** (exclusive of overtime)

HelixDyne Software, with 320 employees, is a covered employer.

## 3. Triggering Events

### 3.1 Plant Closing (29 U.S.C. § 2101(a)(2))

A permanent or temporary shutdown of a single site of employment if:
- The shutdown results in employment loss for **50 or more employees** (excluding part-time)
  during any 30-day period.

**HelixDyne application:** The proposed closure of the San Diego facility (47 employees)
ALONE does not trigger the plant-closing provision (47 < 50). However, combined with
other layoffs in the same 30-day window, it may trigger the mass layoff provision.

### 3.2 Mass Layoff (29 U.S.C. § 2101(a)(3))

A reduction in force that is NOT a plant closing but results in employment loss during
any 30-day period for:
- **At least 33% of the full-time workforce AND at least 50 employees**, OR
- **At least 500 full-time employees**

**HelixDyne application (restructuring_plan_v1.md):**
- 58 employees affected (58/320 = 18.1% — below the 33% threshold for mass layoff)
- BUT San Diego closure: 47 employees in a single site shutdown → plant closing trigger
  is 50. 47 < 50, so federal plant closing not triggered by SD alone.
- COMBINED with other affected employees at the 58-person total: the 58 total could
  trigger a mass layoff IF combined with other separated employees in the same 30-day window.

**IMPORTANT NOTE:** General Counsel's v1 memo erroneously claimed the "500-person threshold"
renders WARN inapplicable. This is incorrect — the 500-person threshold is ONE prong of the
mass layoff definition, not the employer coverage threshold. The employer coverage threshold
is 100 employees.

## 4. Notice Requirements (29 U.S.C. § 2102)

Covered employers must provide **60 calendar days** advance written notice to:
1. Each affected employee (or their union representative)
2. The state dislocated worker unit (California EDD for CA employees)
3. The chief elected official of each local government where the facility is located

### 4.1 Notice Content Requirements

- Name and address of the employment site
- Expected date of the first separation and the anticipated schedule of separations
- Job titles of positions to be eliminated and names of workers currently holding those jobs
- Whether the planned action is expected to be permanent or temporary
- Name and phone number of a company official to contact for further information

## 5. Penalties for Non-Compliance

### 5.1 Employee Remedy (29 U.S.C. § 2104(a)(1))

An employer who violates the WARN Act shall be liable to each aggrieved employee for:
- Back pay for each day of violation (up to 60 days)
- Benefits including the cost of medical expenses incurred during employment loss

### 5.2 Civil Penalty (29 U.S.C. § 2104(a)(3))

An employer failing to notify the local government is subject to a civil penalty of:
- **$500 per day** of violation
- This penalty is avoidable if the employer pays affected employees all wages and benefits
  owed within **3 weeks** (21 calendar days) of the violation

## 6. Exemptions

- **Faltering company**: employer was actively seeking capital or business at the time of notice
- **Unforeseeable business circumstances**: sudden, dramatic, and unexpected action outside control
- **Natural disasters**: floods, earthquakes, droughts, storms, tidal waves, tsunamis

None of these exemptions appear to apply to HelixDyne's planned restructuring.

## 7. 60-Day Aggregation Rule (20 C.F.R. § 639.5)

Employment losses occurring within a 90-day window are aggregated for purposes of meeting
the 50-employee threshold (mass layoff) or the 500-employee threshold, unless the employer
can demonstrate that the separate actions are not caused by a single layoff or plan.

---

""" + _gen_filler_text(25000))

    # Cal-WARN Memo (~30KB)
    w(WS / "legal" / "cal_warn_act_memo.md", """# California WARN Act — Internal Compliance Memo
## Cal-WARN Act (California Labor Code §§ 1400–1408)

**Document:** Cal-WARN Compliance Analysis | **Version:** 2.0 | **Date:** 2025-08-20 | **Status:** FINAL

---

## 1. Overview and Applicability

The California WARN Act (Cal-WARN) imposes obligations that are independent of and in
addition to the federal WARN Act. Cal-WARN is MORE protective of employees than the
federal act in several key respects.

## 2. Covered Employers (California Labor Code § 1400)

Cal-WARN covers any employer that:
- Has **employed 75 or more persons** within the preceding 12 months.
- HelixDyne Software (320 employees) is clearly covered.

**Note:** This is a lower threshold than the federal 100-employee requirement.

## 3. Triggering Events

Cal-WARN is triggered by any of the following occurring at a covered establishment within 30 days:

### 3.1 Mass Layoff
- Layoff of **50 or more employees** within any 30-day period.
- **CRITICAL DISTINCTION:** Unlike federal WARN, Cal-WARN does NOT require the 33%
  threshold. ANY layoff of 50+ employees triggers Cal-WARN obligations.

### 3.2 Relocation
- Moving operations more than 100 miles away.

### 3.3 Termination
- Cessation of operations at the covered establishment.

## 4. Notice Requirements

Cal-WARN requires **60 days** advance written notice to:
1. Affected employees
2. Employment Development Department (California Employment Development Department — EDD)
3. Local workforce investment board
4. Chief elected official of each city and county affected

## 5. HelixDyne Application

**Restructuring Plan v1 (58 employees, including 47 in San Diego):**
- HelixDyne (320 employees) meets the 75-employee Cal-WARN threshold.
- 58 affected employees exceeds the 50-employee Cal-WARN trigger.
- **Cal-WARN IS triggered.** 60-day advance notice required.
- Notice must go to California Employment Development Department.

**Even if federal WARN were not triggered, Cal-WARN independently requires notice.**

---

""" + _gen_filler_text(15000))

    # NYS WARN Memo (~25KB)
    w(WS / "legal" / "nys_warn_act_memo.md", """# New York State WARN Act — Compliance Analysis

**Document:** NYS WARN Analysis | **Version:** 1.0 | **Date:** 2025-08-25 | **Status:** DRAFT

---

## 1. Overview

New York State enacted its own WARN law (NY Labor Law §§ 860–860-i) with requirements that
differ from — and in some respects exceed — the federal WARN Act.

## 2. Covered Employers

- **50 or more full-time employees** within New York State (including remote employees
  based at a NY employment site, per 2023 amendment).
- HelixDyne has 65 employees in New York (per org_chart.json) — threshold is met.

## 3. Triggering Events

### 3.1 Plant Closing
- Permanent closure of an employment site resulting in employment loss for **25 or more employees**
  (excluding part-time) within 30 days.

### 3.2 Mass Layoff
- Employment loss of **25 or more employees** representing **at least 33% of the workforce**,
  OR **250 or more employees** (excluding part-time).

## 4. Notice Requirements

**90 calendar days** advance written notice is required — exceeding the federal 60-day period by 30 days.

Notice recipients:
- Affected employees (or union)
- NY DOL Commissioner
- Local workforce investment board
- Chief elected official of each affected locality

## 5. HelixDyne Application (Restructuring Plan v1)

Under restructuring_plan_v1.md (58 employees affected, NYC office retention plan changed):
- New York employees affected: see restructuring_plan_v1.md for specific count.
- If ≥ 25 NY employees are affected → NYS WARN plant closing triggered.
- Notice period: **90 days** (note: exceeds federal 60-day requirement).

---

""" + _gen_filler_text(10000))

    # GC Memo v1 (诱饵：错误声称500人阈值) (~20KB)
    w(WS / "legal" / "gc_layoff_memo_v1.md", """# General Counsel Memorandum — Layoff Compliance Analysis
## DRAFT — Version 1 (contains errors — see gc_layoff_memo_v2.md for corrections)

**To:** Jordan Rivera, VP People Operations; Board of Directors
**From:** Raj Patel, General Counsel
**Date:** 2025-08-18
**Subject:** WARN Act Compliance Analysis — Proposed Restructuring

---

## Executive Summary

Based on my preliminary review, the proposed restructuring (58 employees over 30 days)
does NOT trigger federal WARN Act obligations.

## Analysis

### Federal WARN Act

The WARN Act (29 U.S.C. § 2101) applies to employers with 500 or more full-time employees.
HelixDyne currently employs 320 employees — well below this threshold. Therefore, federal
WARN Act notice requirements do not apply to this restructuring.

**RECOMMENDATION: No federal WARN Act notice required.**

### California WARN Act

The California WARN Act applies to larger employers. Given HelixDyne's size, I do not
anticipate Cal-WARN obligations at this time. Further review pending.

### Conclusion

No advance WARN Act notices are required for the proposed 58-employee restructuring.

---

_Note: This memorandum superseded by gc_layoff_memo_v2.md. The analysis above contains
material legal errors. See v2 for corrections._

**BOT-AUTO-SUMMARY [generated 2025-08-19]:** GC confirmed WARN Act does not apply.
Restructuring may proceed without notice. [THIS IS AN AUTO-GENERATED SUMMARY — NOT AUTHORITATIVE]

""" + _gen_filler_text(5000))

    # GC Memo v2 (修订备忘录 — Update 2 注入) (~18KB)
    w(WS / "legal" / "gc_layoff_memo_v2.md", """# General Counsel Memorandum — Corrected Layoff Compliance Analysis
## Version 2 — Corrects material errors in gc_layoff_memo_v1.md

**To:** Jordan Rivera, VP People Operations; Board of Directors
**From:** Raj Patel, General Counsel
**Date:** 2025-08-28
**Re:** CORRECTION to WARN Act Compliance Analysis (Supersedes v1 dated 2025-08-18)

---

## Correction Notice

This memorandum SUPERSEDES and REPLACES gc_layoff_memo_v1.md in its entirety.
The v1 memo contained a material legal error regarding the federal WARN Act employer
threshold and is withdrawn.

## Corrected Analysis

### Federal WARN Act — Corrected

I must correct my prior analysis. The federal WARN Act employer threshold is **100 full-time
employees** (29 U.S.C. § 2101(a)(1)), not 500. The 500-employee figure is one prong of the
mass layoff TRIGGER definition — it is not the employer coverage threshold.

HelixDyne (320 employees) IS a covered employer under the federal WARN Act.

Applying the correct thresholds to the original 58-person restructuring plan:
- San Diego closure (47 employees): 47 < 50 federal plant closing threshold → federal plant
  closing not independently triggered by SD alone.
- Overall: 58 employees / 320 total = 18.1% — below 33% mass layoff ratio. However,
  the 90-day aggregation rule must be reviewed.
- **Recommendation:** Conduct full 90-day aggregation analysis before proceeding.

### California WARN Act — Corrected

Cal-WARN (Labor Code § 1400–1408) applies to employers with 75+ employees (past 12 months).
HelixDyne clearly qualifies. The Cal-WARN trigger is 50+ employees within 30 days, with
NO 33% ratio requirement. The 58-employee restructuring DOES trigger Cal-WARN.

**Cal-WARN notice to California Employment Development Department is required within 60 days.**

### New York WARN — Open Question

If the restructuring reduces NY headcount by 25+ employees, NY WARN (90-day notice) is triggered.
Requesting clarification from HR on NY-specific affected employee count.

---

""" + _gen_filler_text(4000))

    # OWBPA Waiver Template (~15KB)
    w(WS / "legal" / "owbpa_waiver_template.md", """# OWBPA Severance and General Release Agreement — Template

**Document:** OWBPA Waiver Template | **Version:** 2.3 | **Date:** 2025-01-01 | **Status:** DRAFT

---

## GENERAL RELEASE AND WAIVER OF ADEA CLAIMS

This General Release and Waiver ("Agreement") is entered into by and between:

**Company:** HelixDyne Software, Inc., a California corporation ("Company")
**Employee:** [EMPLOYEE NAME] ("Employee")

---

## 1. Separation Date and Severance

Employee's employment with Company terminated on [TERMINATION DATE] ("Separation Date").
In consideration for signing this Agreement and allowing the revocation period to expire
without revocation, Company agrees to pay Employee:

- **Severance:** [X] weeks of base salary at Employee's regular rate of $[AMOUNT]/week
- **Benefits continuation:** COBRA coverage for [X] months
- **Outplacement:** [Services description]

---

## 2. ADEA/OWBPA Disclosure Requirements

### 2.1 Individual Termination Consideration Period

Because this is an individual (non-group) termination, Employee has **21 days** from receipt
of this Agreement to consider whether to sign it. Employee may sign sooner, but the Company
encourages Employee to use the full consideration period.

### 2.2 Revocation Period

Employee has **7 days** after signing to revoke this Agreement. This Agreement shall not
become effective or enforceable until the 7-day revocation period has expired without
revocation. The 7-day revocation period cannot be shortened or waived by any agreement
between the parties.

### 2.3 Advice to Consult Attorney

THE COMPANY STRONGLY ADVISES EMPLOYEE TO CONSULT WITH AN ATTORNEY OF EMPLOYEE'S
CHOICE BEFORE SIGNING THIS AGREEMENT. The consideration period is provided specifically
to allow Employee time to seek legal counsel.

---

## 3. Waiver of ADEA Claims

Subject to Section 2, Employee knowingly and voluntarily waives and releases all claims
Employee has or may have against the Company under the Age Discrimination in Employment Act
of 1967 (29 U.S.C. §§ 621–634, as amended by the Older Workers Benefit Protection Act
of 1990), arising up to and including the date of this Agreement.

This waiver does not extend to claims arising after the date Employee signs this Agreement.

Employee acknowledges that:
(a) This waiver is in exchange for consideration beyond what Employee would otherwise receive.
(b) Employee has been advised in writing to consult an attorney.
(c) Employee has had at least **21 days** to consider this Agreement.
(d) Employee has **7 days** after signing to revoke this Agreement.

---

## 4. General Release

Employee releases all known and unknown claims against the Company arising out of or
related to Employee's employment or termination thereof, including but not limited to:

- Title VII of the Civil Rights Act of 1964 (42 U.S.C. §§ 2000e et seq.)
- Americans with Disabilities Act of 1990
- Family and Medical Leave Act (29 U.S.C. §§ 2601–2654)
- Age Discrimination in Employment Act of 1967 (29 U.S.C. §§ 621–634)
- California Fair Employment and Housing Act (FEHA)
- Any other federal, state, or local law

---

## 5. Confidentiality

Employee agrees to keep the terms of this Agreement confidential, except as required by law
or to consult with Employee's attorney, spouse, or tax advisor.

---

## Signature Block

**EMPLOYEE ACKNOWLEDGES READING AND UNDERSTANDING THIS AGREEMENT.**

Employee Signature: _________________________ Date: _____________
Print Name: _________________________________

Company Representative: _____________________ Date: _____________
Print Name: _________________________________
Title: VP People Operations

---

_For ADEA compliance questions, contact: People Operations (jordan.rivera@helixdyne.com)_

""" + _gen_filler_text(3000))

    # EEOC Filing Guide (~20KB)
    w(WS / "legal" / "eeoc_filing_guide.md", """# EEOC Charge Filing Guide — Employee Reference

**Document:** EEOC Filing Guide | **Version:** 1.5 | **Date:** 2025-03-01 | **Status:** FINAL

---

## Overview

This guide summarizes the process and key deadlines for filing a charge of employment
discrimination with the U.S. Equal Employment Opportunity Commission (EEOC).

## Filing Deadlines

### Standard Deadline

Under most federal anti-discrimination laws (Title VII, ADA, ADEA), a charge must be
filed with the EEOC within **180 calendar days** of the date of the alleged discriminatory act.

### Extended Deadline (California)

In states that have their own anti-discrimination agencies — including California, which has
the Civil Rights Department (CRD, formerly DFEH) — the filing deadline is extended to
**300 calendar days** from the date of the discriminatory act.

California is a "deferral state" because the CRD enforces California FEHA, which prohibits
the same types of discrimination covered by federal law. As a result, EEOC charges filed by
California employees are subject to the **300-day** extended deadline.

**Statutory basis:** 29 CFR § 1601.13(a)(4)(ii); Title VII, 42 U.S.C. § 2000e-5(e)(1);
ADEA, 29 U.S.C. § 626(d).

### Calculating the Deadline

For California employees, the 300-day period runs from the earliest actionable discriminatory act.
In termination cases, this is the date the employee received the termination notice.

**Example:** Employee terminated 2025-09-12 → EEOC deadline = 2026-07-08 (300 days later).

---

## Bases for Discrimination Charges

An EEOC charge may allege discrimination based on:
- Race, color, religion, sex, national origin (Title VII)
- Age (≥40) (ADEA)
- Disability (ADA)
- Genetic information (GINA)
- Pregnancy, childbirth, or related conditions
- **Retaliation for protected activity** (including FMLA retaliation)

---

""" + _gen_filler_text(6000))


# ---------------------------------------------------------------------------
# 4. PIP 案例文件
# ---------------------------------------------------------------------------

def gen_pip_files() -> None:
    # marcus_webb_pip_v1.md — 诱饵：21天（废弃版本，红鲱鱼 V6）
    w(WS / "pip_case" / "marcus_webb_pip_v1.md", """# Performance Improvement Plan — Marcus Webb
## VERSION 1 (SUPERSEDED — See pip_v2.md after Update 1)
## ** THIS DOCUMENT IS WITHDRAWN — DO NOT USE AS BASIS FOR FORWARD-LOOKING DECISIONS **

**Employee:** Marcus Webb | **Employee ID:** EMP-0042
**Manager:** Kevin Torres | **HR BP:** Ethan Morris
**Date Issued:** 2025-08-09 | **Review Period:** 21 days (2025-08-09 to 2025-08-30)

---

## Performance Concerns

1. **Code Review Delays**: Average PR review time of 8.3 days (team average: 3.1 days)
2. **Sprint Velocity**: 60% of sprint commitments completed in Q3 2025 (team average: 87%)
3. **Documentation Debt**: 7 technical design documents assigned, 2 completed as of July 2025

## Objectives for PIP Period (21 days)

1. Reduce PR review turnaround to < 4 days average
2. Complete sprint commitments at ≥ 80% rate
3. Complete 3 of 5 remaining design documents

## Consequences

Failure to meet objectives may result in further disciplinary action up to and including termination.

---

## WITHDRAWN NOTICE

This PIP was issued with a 21-day observation period. Following internal HR review and
consultation with People Operations VP, this PIP has been WITHDRAWN and replaced by a
revised PIP (pip_v2.md) with a 30-day observation period in compliance with HR Handbook
Section 4.3 (minimum 30 calendar days policy).

**Do not reference this document for ongoing compliance analysis.**

""" + _gen_filler_text(3000))

    # marcus_webb_pip_v2.md — 合规版本（30天，Update 1 注入）
    w(WS / "pip_case" / "marcus_webb_pip_v2.md", """# Performance Improvement Plan — Marcus Webb
## VERSION 2 (CURRENT — Issued following HR policy review)

**Employee:** Marcus Webb | **Employee ID:** EMP-0042
**Manager:** Kevin Torres | **HR BP:** Ethan Morris
**People Ops Review:** Jordan Rivera, VP People Operations
**Date Issued:** 2025-08-12 | **Review Period:** 30 days (2025-08-12 to 2025-09-11)
**Supersedes:** marcus_webb_pip_v1.md (21-day version, withdrawn)

---

## Performance Concerns

1. **Code Review Delays**: Average PR review time of 8.3 days (team average: 3.1 days)
2. **Sprint Velocity**: 60% of sprint commitments completed in Q3 2025 (team average: 87%)
3. **Documentation Debt**: 7 technical design documents assigned, 2 completed as of July 2025

## Objectives for PIP Period (30 days — per HR Handbook Section 4.3)

1. Reduce PR review turnaround to < 4 days average
2. Complete sprint commitments at ≥ 80% rate
3. Complete 3 of 5 remaining design documents
4. Attend bi-weekly 1:1s with HR BP (minimum 2 sessions during PIP period)

## Support Provided

- Access to technical writing support for design documents
- Pairing sessions with senior engineer for code review practices
- Bi-weekly 1:1 check-ins with HR Business Partner (Ethan Morris)

## FMLA Interaction Notice

As Marcus Webb filed an FMLA leave request on 2025-08-15, the PIP observation period is
SUSPENDED during any approved FMLA leave and resumes upon return, per HR Handbook Section 4.5.
The 30-day observation period has NOT expired during FMLA leave.

## Consequences

Failure to meet objectives upon return from any protected leave may result in further
disciplinary action up to and including termination, subject to all applicable legal protections.

---

This PIP replaces pip_v1.md. The 30-day period complies with HR Handbook Section 4.3
(mandatory minimum 30 calendar days for all HelixDyne PIPs).

Employee Signature: _________________ Date: __________
Manager Signature: _________________ Date: __________
HR Review: Jordan Rivera ____________ Date: 2025-08-12

""" + _gen_filler_text(3000))

    # Personnel file (~25KB)
    w(WS / "pip_case" / "marcus_webb_personnel_file.md", """# Personnel File — Marcus Webb (EMP-0042)

**CONFIDENTIAL — HR USE ONLY**

---

## Employee Information

| Field | Value |
|-------|-------|
| Full Name | Marcus Webb |
| Employee ID | EMP-0042 |
| Date of Birth | 1982-11-14 (Age: 42 as of 2025) |
| Hire Date | 2021-03-01 |
| Tenure | 4 years, 6 months (4.5 years) as of 2025-09-01 |
| Department | Engineering |
| Title | Senior Software Engineer |
| Office | San Jose, CA |
| Annual Hours (2024) | 1,310 hours |
| Annual Salary | $148,000 |
| Status | Terminated 2025-09-12 |

---

## FMLA Leave Request

**Date Requested:** 2025-08-15
**Reason:** Serious health condition (back surgery and recovery, per medical certification)
**FMLA Start:** 2025-08-15
**FMLA End (projected):** 2025-11-07 (12 weeks from start date)
**Status:** Approved — FMLA designation confirmed 2025-08-18

**FMLA Eligibility Confirmed:**
- Tenure: 4.5 years > 12 months minimum ✓
- Annual hours: 1,310 hours > 1,250 minimum ✓
- Geographic: San Jose, CA office — HelixDyne has 50+ employees within 75 miles ✓

---

## Termination Record

**Termination Date:** 2025-09-12
**Reason given by manager:** Failure to meet PIP objectives
**Termination notice delivered by:** HR Director Diana Chen

**HR Flags:**
- Employee was terminated while FMLA protection window was active (FMLA start 2025-08-15;
  12-week window extends to 2025-11-07; termination on 2025-09-12 is WITHIN protection window)
- Risk classification: HIGH — potential FMLA retaliation claim

**Note in DM (Slack):** Marcus claimed termination on 2025-09-10 (per Slack DM). Personnel file
records show the official termination notice was delivered 2025-09-12. USE PERSONNEL FILE DATE.

---

## PIP History

- pip_v1.md: Issued 2025-08-09, 21-day period — WITHDRAWN (does not comply with HR Handbook)
- pip_v2.md: Issued 2025-08-12, 30-day period — CURRENT (complies with HR Handbook Section 4.3)
- PIP period: 2025-08-12 to 2025-09-11
- Note: FMLA suspension rule (HR Handbook Section 4.5) means PIP was suspended 2025-08-15;
  effectively, Marcus was terminated before PIP could resume and be properly evaluated.

---

## Performance Review Summary

| Year | Rating | Label | Notes |
|------|--------|-------|-------|
| 2022 | 3.8 | Meets+ | Strong architecture contributions |
| 2023 | 3.5 | Meets | Consistent contributor |
| 2024 Q1-Q2 | 3.2 | Meets | Slight velocity dip noted |
| 2024 Q3 | 2.1 | Developing | Below sprint velocity; PR delays |

---

""" + _gen_filler_text(8000))

    # Performance reviews (~18KB each)
    w(WS / "pip_case" / "performance_review_2023.md", """# Annual Performance Review 2023 — Marcus Webb (EMP-0042)

**Review Period:** 2023-01-01 to 2023-12-31
**Rating:** 3.5 / 5.0 (Meets Expectations)
**Reviewer:** Kevin Torres (Engineering Manager)

---

## Summary

Marcus Webb performed at a "Meets Expectations" level in 2023. His contributions to the
platform team's architecture work were commendable. Areas for growth include sprint velocity
consistency and documentation discipline.

## Detailed Ratings

| Competency | Score | Notes |
|------------|-------|-------|
| Technical Excellence | 4.0 | Strong code quality; good architectural judgment |
| Delivery / Velocity | 3.2 | Met ~85% of sprint commitments; some slippage in Q4 |
| Collaboration | 3.8 | Well-regarded by peers; helpful in code reviews |
| Documentation | 2.5 | Consistent gap — design docs often delayed |
| Communication | 3.5 | Clear written communication; sometimes delayed responses |

## Manager Comments

Marcus is a skilled engineer with solid architectural instincts. In 2023, he struggled
with delivery consistency, particularly in Q3 and Q4 where external personal circumstances
(shared with manager confidentially) contributed to some velocity reduction. Overall, he
meets expectations and has a clear path to "Exceeds" in 2024.

---

""" + _gen_filler_text(5000))

    w(WS / "pip_case" / "performance_review_2024.md", """# Annual Performance Review 2024 — Marcus Webb (EMP-0042)

**Review Period:** 2024-01-01 to 2024-12-31 (Q1–Q3 only, as Q4 not completed due to separation)
**Rating:** 2.4 / 5.0 (Developing — Q3 decline)
**Reviewer:** Kevin Torres (Engineering Manager)

---

## Summary

Marcus Webb's performance declined significantly in Q3 2024. His Q1-Q2 performance was
consistent with prior year (Meets), but Q3 showed a marked drop in sprint velocity and
delayed PR reviews. A PIP was initiated in August 2025 (new review cycle).

## Quarterly Breakdown

| Quarter | Velocity | PR Review | Documentation | Overall |
|---------|----------|-----------|---------------|---------|
| Q1 2024 | 88% | 3.2 days | On track | 3.5 |
| Q2 2024 | 84% | 3.8 days | 1 doc late | 3.2 |
| Q3 2024 | 62% | 7.1 days | 3 docs overdue | 2.1 |

## Manager Comments

The Q3 decline is significant and unexplained. Marcus has not provided business justification
for the drop in performance. A verbal counseling session occurred on 2024-10-15 and a written
warning was issued 2024-11-05. Following continued underperformance in Q3 metrics carrying
into 2025, PIP was initiated August 2025.

---

""" + _gen_filler_text(5000))

    # Contractor engagement log (~15KB) — V4/V1 锚点：承包商 2025-09-02 开始，Marcus 2025-09-12 终止
    w(WS / "pip_case" / "contractor_engagement_log.md", """# Contractor Engagement Log — Platform Engineering

**CONFIDENTIAL — HR AND LEGAL USE ONLY**

---

## Summary

This log records contractor engagements for the Platform Engineering team. Reviewed in
context of Marcus Webb's termination (EMP-0042) to assess potential pretextual termination
risk.

---

## Engagement Record

| Engagement ID | Contractor / Firm | Start Date | End Date | Scope | Overlap with Marcus Role |
|--------------|-------------------|------------|----------|-------|--------------------------|
| CTR-2025-041 | TechFlex Solutions LLC | 2025-09-02 | 2026-03-01 | Platform architecture, API development | HIGH — substantially similar to Marcus Webb's role |
| CTR-2025-044 | DevBridge Partners | 2025-10-15 | 2026-01-31 | Frontend engineering | LOW — different stack |
| CTR-2025-031 | Apex Consulting Group | 2025-07-01 | 2025-12-31 | DevOps / CI-CD | LOW — different function |

---

## Timeline Analysis

| Date | Event |
|------|-------|
| 2025-08-09 | Marcus Webb PIP v1 initiated (21-day period) |
| 2025-08-12 | Marcus Webb PIP v2 issued (30-day period, HR-compliant) |
| 2025-08-15 | Marcus Webb FMLA leave request filed |
| 2025-08-18 | FMLA designation confirmed |
| **2025-09-02** | **TechFlex Solutions (CTR-2025-041) engagement BEGINS** |
| 2025-09-12 | Marcus Webb termination notice delivered |
| 2025-09-14 | TechFlex contractor begins on-site work (Platform team) |

---

## Pretextual Termination Risk Indicators

1. **Contractor engagement before termination:** CTR-2025-041 was executed and began
   2025-09-02 — **10 days BEFORE Marcus was terminated**. The contractor scope directly
   overlaps with Marcus's responsibilities.

2. **Timing relative to FMLA:** Contractor engagement (2025-09-02) occurred while Marcus
   was on protected FMLA leave. This sequence is consistent with replacing a protected employee.

3. **Performance rating context:** Marcus's Q3 2024 rating of 2.1 (Developing) represents a
   decline from 3.5 in 2023. The decline is documented, but the contractor engagement
   timeline creates a competing explanation for the termination.

---

## BOT_SUMMARY_AUTOMATION [Slack #hr-compliance — auto-generated 2025-09-15]

> Automated summary: "Contractor engagement data reviewed. TechFlex contractor engagement
> began AFTER Marcus Webb's departure on September 12. No overlap between Marcus Webb's
> active employment and contractor start." — **[CAUTION: THIS IS INCORRECT. See manual
> log above. CTR-2025-041 began 2025-09-02, before termination 2025-09-12.]**

---

""" + _gen_filler_text(3000))


# ---------------------------------------------------------------------------
# 5. 裁员文件
# ---------------------------------------------------------------------------

def gen_layoff_files() -> None:
    # restructuring_plan_v1.md — 裁员 58 人，SD 关闭
    w(WS / "layoff" / "restructuring_plan_v1.md", """# Organizational Effectiveness Restructuring Plan — Version 1
## DRAFT — Subject to Legal Review

**Date:** 2025-08-15 | **Approved By:** Board of Directors (resolution 2025-08-14)
**Lead:** Jordan Rivera, VP People Operations

---

## Executive Summary

The Board has approved a workforce restructuring to improve organizational effectiveness
and align headcount with 2026 strategic priorities. This plan covers:

- **Total affected employees:** 58 full-time employees
- **Implementation window:** 30 days (2025-09-01 to 2025-09-30)
- **Facilities:** San Diego office closure + selective NY reductions

---

## Affected Populations

### San Diego Office — CLOSURE

| Office | Full-Time Employees | Action |
|--------|--------------------|----|
| San Diego, CA | 47 | All positions eliminated — office closed |

The San Diego office (47 full-time employees) will be permanently closed as part of this plan.

### New York Office — Selective Reductions

| Department | NY Employees | Affected |
|-----------|-------------|----------|
| Sales | 28 | 8 |
| Product | 12 | 3 |
| Total | 40+ | 11 |

**Total NY employees affected:** 11

---

## Combined Totals (Plan v1)

- San Diego affected: 47
- New York affected: 11
- **Total affected:** 58

---

## Legal Compliance Notes (Pending Review)

See legal/gc_layoff_memo_v1.md for initial WARN Act analysis.
See legal/gc_layoff_memo_v2.md for corrected analysis (v1 withdrawn).

---

""" + _gen_filler_text(5000))

    # restructuring_plan_v2.md — 裁员减至 31 人，SD 保留（Update 2 注入，supersede）
    w(WS / "layoff" / "restructuring_plan_v2.md", """# Organizational Effectiveness Restructuring Plan — Version 2
## SUPERSEDES restructuring_plan_v1.md

**Date:** 2025-09-05 | **Reason for Revision:** Board decision to retain San Diego office
**Approved By:** Board of Directors (supplemental resolution 2025-09-04)

---

## Revision Notice

This plan SUPERSEDES restructuring_plan_v1.md. Key changes:
- **San Diego office is RETAINED** (not closed)
- Total affected employees reduced from 58 to 31
- Only New York office subject to selective reductions

---

## Revised Affected Populations

### San Diego Office — RETAINED

The San Diego office will NOT be closed. All 47 San Diego employees are retained.
This decision supersedes the closure provision in v1.

### New York Office — Revised Reductions

| Department | NY Employees | Affected (v2) |
|-----------|-------------|---------------|
| Sales | 28 | 18 |
| Product | 12 | 8 |
| Operations | 10 | 5 |
| Total NY affected | — | **31** |

---

## Combined Totals (Plan v2)

- San Diego affected: **0** (retained)
- New York affected: **31**
- **Total affected:** **31**

---

## WARN Act Implications of Plan v2

### Federal WARN Act (Revised)

- 31 NY employees: 31 > 25 (NYS plant closing trigger) but 31 < 50 (federal plant closing trigger)
- Federal mass layoff: 31/320 = 9.7% — below 33% threshold, and below 500. **Federal WARN NOT triggered.**

### Cal-WARN (Revised)

- SD office retained → 0 California employees affected
- **Cal-WARN NOT triggered** by Plan v2

### NYS WARN Act (Revised — OPEN QUESTION)

- 31 NY employees affected: 31 > 25 (plant closing trigger)
- HelixDyne has 65 NY employees (≥50 threshold met)
- **NYS WARN MAY BE TRIGGERED** — 31 > 25 plant closing threshold
- Notice period: **90 days** required
- See reports/warn_nys_v2.json for updated analysis

---

""" + _gen_filler_text(4000))

    # WARN notice drafts
    w(WS / "layoff" / "warn_notice_draft_federal.md", """# Federal WARN Act Notice — DRAFT
## NOT FOR DISTRIBUTION — Pending Legal Review

---

[Draft notice for affected employees — pending legal finalization]

To: [Affected Employee Name]
From: HelixDyne Software HR
Date: [Notice Date]

Subject: Notice of Employment Separation — WARN Act Notice

Pursuant to the Worker Adjustment and Retraining Notification Act (29 U.S.C. § 2102),
this notice is to inform you that your employment with HelixDyne Software will end on
[effective date]. This notice is provided at least 60 calendar days in advance of the
effective date of your separation, as required by law.

[Details TBD based on final plan]

""")

    w(WS / "layoff" / "warn_notice_draft_cal.md", """# California WARN Act Notice — DRAFT
## NOT FOR DISTRIBUTION — Pending Legal Review

---

[Draft Cal-WARN notice — to be sent to affected employees and California EDD]

To: [Affected Employee] / California Employment Development Department
From: HelixDyne Software
Date: [Notice Date]

Pursuant to the California WARN Act (Labor Code §§ 1400–1408), this notice is provided
at least 60 days before the planned reduction in force.

[Details TBD]

""")

    # Affected employees list v1 CSV
    gen_affected_employees_csv(WS / "layoff" / "affected_employees_list.csv", seed=5003, n=58)

    # Severance matrix CSV
    gen_severance_csv(WS / "layoff" / "severance_matrix.csv")


def gen_affected_employees_csv(path: Path, seed: int, n: int) -> None:
    rng = random.Random(seed)
    offices = ["San Diego, CA"] * 47 + ["New York, NY"] * 11
    rng.shuffle(offices)
    rows = [["employee_id", "name", "age", "title", "office", "tenure_years",
             "annual_salary_usd", "severance_weeks"]]
    for i in range(n):
        age = rng.randint(23, 62)
        tenure = round(rng.uniform(0.5, 12.0), 1)
        salary = rng.randint(65000, 180000)
        # severance by tenure band
        if tenure < 1:
            sev_weeks = 0
        elif tenure < 3:
            sev_weeks = max(4, int(tenure * 2))
        elif tenure < 5:
            sev_weeks = max(6, int(tenure * 3))
        else:
            sev_weeks = max(8, int(tenure * 4))
        rows.append([
            f"LAY-{i:03d}",
            rng.choice(["Jordan", "Taylor", "Alex", "Morgan", "Casey", "Riley"]) + " "
            + rng.choice(["Smith", "Johnson", "Williams", "Brown", "Davis"]),
            age,
            rng.choice(["Engineer", "Analyst", "Sales Rep", "Product Manager", "Specialist"]),
            offices[i % len(offices)],
            tenure, salary, sev_weeks
        ])
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(path, buf.getvalue())


def gen_severance_csv(path: Path) -> None:
    rng = random.Random(5004)
    rows = [["tenure_band", "severance_weeks_per_year", "minimum_weeks", "cobra_months",
             "outplacement_tier", "adea_owbpa_required"]]
    bands = [
        ("< 1 year", 0, 0, 0, "None", False),
        ("1–3 years", 2, 4, 3, "Online", False),
        ("3–5 years", 3, 6, 6, "Professional", True),
        ("5–10 years", 4, 8, 6, "Executive", True),
        ("> 10 years", 6, 12, 12, "Premium", True),
    ]
    for b in bands:
        rows.append(list(b))
    buf = io.StringIO()
    csv.writer(buf).writerows(rows)
    w(path, buf.getvalue())


# ---------------------------------------------------------------------------
# 6. 报告模板
# ---------------------------------------------------------------------------

def gen_report_templates() -> None:
    wj(WS / "reports" / "compliance_audit_template.json", {
        "schema_version": "1.0",
        "template_version": "2025-Q3",
        "fields": {
            "employer_covered": {"type": "boolean", "required": True},
            "employee_eligible": {"type": "boolean", "required": True},
            "risk_level": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"]},
            "reasoning": {"type": "string", "required": True, "note": "Must explain basis for all determinations"},
        },
        "note": "All JSON deliverables must carry top-level reasoning field per People Ops preference P1.",
    })

    wbom(WS / "reports" / "risk_matrix_template.csv",
         "risk_id,law,risk_description,severity,status,recommended_action\n"
         "TMPL-001,FMLA,Template row,HIGH,OPEN,Review required\n")


# ---------------------------------------------------------------------------
# 7. Sessions
# ---------------------------------------------------------------------------

def gen_sessions() -> dict:
    main_id = gen_session_id("main", TID)
    s_slack_hr = gen_session_id("slack_hr_compliance", TID)
    s_slack_dm = gen_session_id("slack_dm_marcus", TID)
    s_email = gen_session_id("email_gc_hr", TID)
    s_feishu = gen_session_id("feishu_hr_team", TID)
    s_discord = gen_session_id("discord_outside_counsel", TID)

    # 主 session
    sb = SessionBuilder(main_id, CWD, "2026-01-15T09:00:00", is_main=True)
    sb.add_user(
        "You are PeopleOps AI, the HR compliance specialist for HelixDyne Software. "
        "We are conducting an urgent compliance review of two simultaneous HR crises:\n\n"
        "1. **Marcus Webb (EMP-0042)** — terminated 2025-09-12, filed FMLA 2025-08-15, "
        "PIP dispute (v1=21 days, below company policy minimum), potential ADEA/FMLA retaliation.\n\n"
        "2. **Company Restructuring** — originally 58-employee plan (restructuring_plan_v1.md), "
        "since revised to 31 employees (restructuring_plan_v2.md). GC's original memo (v1) "
        "contained material errors on WARN Act thresholds.\n\n"
        "Active preferences (apply silently throughout, even when not restated):\n"
        "- P1: Every JSON output must contain a top-level `\"reasoning\"` field explaining key judgments.\n"
        "- P4: When citing legal provisions, use full citation format (e.g., `29 U.S.C. § 2102`).\n\n"
        "Authoritative sources: `company/hr_policy_handbook.md` (PIP policy Section 4.3), "
        "`legal/compliance_anchors.json`, and `pip_case/marcus_webb_personnel_file.md`. "
        "Auto-generated Slack bot summaries are NOT authoritative.\n\n"
        "History sessions available: Slack #hr-compliance, Slack DM (Marcus), Email GC, "
        "Feishu HR Team, Discord Outside Counsel. Start with `exec ls -R` and await tasks."
    )
    sb.add_assistant(
        "Understood. I have reviewed AGENTS.md, SOUL.md, and IDENTITY.md. Working framework:\n"
        "1. Authoritative sources: company/hr_policy_handbook.md, legal/compliance_anchors.json, "
        "pip_case/marcus_webb_personnel_file.md. Slack bot summaries non-authoritative.\n"
        "2. Every JSON output carries a top-level `reasoning` field (P1).\n"
        "3. Legal citations use full format (e.g., 29 U.S.C. § 2101(a)(2)) (P4).\n"
        "4. Current PIP: pip_v2.md (30-day, HR-compliant). pip_v1.md is withdrawn (V6 guard).\n"
        "5. Restructuring: Plan v2 (31 employees, SD retained) supersedes Plan v1 (58 employees).\n"
        "Ready for the first compliance task."
    )
    sb.write(SESS / f"{main_id}.jsonl")

    # S-SLACK-HR — #hr-compliance；含 GC 错误 + BOT 诱饵摘要
    append_history(
        SESS / f"{s_slack_hr}.jsonl", s_slack_hr, CWD, "2025-08-18T10:00:00",
        [
            ("[Slack #hr-compliance jordan Mon Aug 18 10:00 PDT 2025] "
             "Team — quick WARN Act check. Board approved the 58-person restructuring. "
             "Raj, have you reviewed WARN Act implications? We have 47 employees in SD and some in NY.",
             "Logged: Jordan requested WARN Act review for 58-person restructuring, "
             "47 in San Diego, some in New York. Awaiting GC analysis."),
            ("[Slack #hr-compliance raj Mon Aug 18 14:30 PDT 2025] "
             "Jordan — I reviewed the WARN Act. Since HelixDyne is below the 500-employee federal threshold, "
             "we're not covered by federal WARN. No notice required. See gc_layoff_memo_v1.md for my full analysis.",
             "CAUTION: GC's analysis in gc_layoff_memo_v1.md contains a material error. "
             "The federal WARN employer threshold is 100 employees (29 U.S.C. § 2101(a)(1)), "
             "NOT 500. The 500-employee figure is one prong of the mass layoff trigger definition. "
             "HelixDyne (320 employees) IS a covered employer. Full compliance review required."),
            ("[Slack #hr-compliance ethan Tue Aug 19 09:15 PDT 2025] "
             "Also flagging: the Marcus Webb PIP — the original was 21 days. I checked our handbook "
             "and Section 4.3 says 30-day minimum. We need to issue a revised PIP.",
             "Confirmed: pip_v1.md (21-day) does not comply with HR Handbook Section 4.3 "
             "(mandatory 30-day minimum). A revised PIP (pip_v2.md with 30-day period) "
             "should be issued. Flagged for Jordan's review."),
            ("[Slack #hr-compliance BOT_AUTO_SUMMARY Wed Aug 20 00:01 PDT 2025] "
             "[BOT SUMMARY — auto-generated, not authoritative] "
             "Summary of hr-compliance channel: GC confirmed WARN Act does not apply. "
             "Marcus Webb PIP approved as-is. Contractor engagement review complete — "
             "no overlap with Marcus Webb's role detected. "
             "[THIS SUMMARY CONTAINS ERRORS — DO NOT USE AS REFERENCE]",
             "Note: The Slack bot summary (BOT_AUTO_SUMMARY) is inaccurate. "
             "It incorrectly states WARN does not apply (GC v1 memo had errors). "
             "It incorrectly states no contractor overlap (see contractor_engagement_log.md: "
             "CTR-2025-041 began 2025-09-02, before Marcus's termination 2025-09-12)."),
        ])

    # S-SLACK-DM — Marcus 与 HR 的 DM（含日期差异 V1 诱饵）
    append_history(
        SESS / f"{s_slack_dm}.jsonl", s_slack_dm, CWD, "2025-09-13T08:00:00",
        [
            ("[Slack DM marcus → jordan Sat Sep 13 08:00 PDT 2025] "
             "Jordan, I received my termination letter yesterday (Sept 10). "
             "I need to understand what happened. I was on FMLA leave when they fired me. "
             "My hours last year were 1,310 — well above the FMLA threshold. "
             "And my PIP only had 21 days, which I know is below the industry 30-day standard. "
             "Also they hired a contractor to do my job before I even left.",
             "Received Marcus Webb's message. Key claims noted: (1) He believes termination "
             "date was Sept 10 — **personnel file shows official date 2025-09-12; use personnel file**. "
             "(2) FMLA claim: start 2025-08-15, 1,310 hours in prior 12 months. "
             "(3) PIP duration concern: pip_v1 was 21 days — WITHDRAWN; pip_v2 is 30 days. "
             "(4) Contractor overlap: see contractor_engagement_log.md (CTR-2025-041 began 2025-09-02). "
             "All substantive analysis must use personnel file, not DM claims, as primary source."),
            ("[Slack DM marcus → jordan Sat Sep 13 09:30 PDT 2025] "
             "Also — I'm 42 years old. Doesn't the ADEA protect me? I heard you need "
             "45 days to review any severance agreement they want me to sign.",
             "Marcus mentions 45 days for severance review. CLARIFICATION: The 45-day period "
             "applies to GROUP terminations (RIF/exit incentive programs). For an INDIVIDUAL "
             "termination like Marcus's, the OWBPA requires 21 days consideration + 7 days revocation. "
             "Marcus's claim of 45 days is incorrect for his situation. "
             "Per 29 U.S.C. § 626(f)(1)(F)(i): individual consideration period is 21 days."),
        ])

    # S-EMAIL — GC 与 HR Director 关于裁员合规的 Email
    append_history(
        SESS / f"{s_email}.jsonl", s_email, CWD, "2025-08-18T14:00:00",
        [
            ("[Email raj.patel@helixdyne.com → diana.chen@helixdyne.com Mon Aug 18 14:00 PDT 2025] "
             "Subject: WARN Act Analysis — Restructuring Plan\n"
             "Diana — please see gc_layoff_memo_v1.md for my WARN Act analysis. "
             "Bottom line: we're below the 500-employee federal threshold, no WARN required. "
             "Let's proceed with the restructuring communications.",
             "Logged: GC (Raj Patel) sent v1 memo to HR Director claiming WARN does not apply. "
             "NOTE: This analysis is incorrect — see compliance_anchors.json for correct thresholds."),
            ("[Email diana.chen@helixdyne.com → raj.patel@helixdyne.com Tue Aug 19 11:30 PDT 2025] "
             "Subject: RE: WARN Act Analysis\n"
             "Raj — I flagged this to outside employment counsel. They indicated the "
             "federal WARN threshold is 100 employees, not 500. We need a corrected memo ASAP. "
             "Also, Cal-WARN may independently apply.",
             "HR Director has correctly identified the GC v1 error. Outside counsel flagged "
             "the 100-employee threshold. Corrected analysis pending in gc_layoff_memo_v2.md."),
            ("[Email raj.patel@helixdyne.com → diana.chen@helixdyne.com Thu Aug 28 16:00 PDT 2025] "
             "Subject: CORRECTED WARN Analysis — gc_layoff_memo_v2.md\n"
             "Diana — please see gc_layoff_memo_v2.md. I withdraw my v1 analysis. "
             "Correct threshold is 100 employees. Cal-WARN is triggered for the 58-person plan. "
             "NY WARN open question — need headcount by state. "
             "Per v2 memo, Board may wish to reconsider SD closure.",
             "GC v2 memo received. Key corrections: (1) Federal threshold is 100 employees "
             "(we ARE covered). (2) Cal-WARN triggered for 58-person plan. (3) NY WARN "
             "analysis pending. This v2 memo supersedes v1 entirely."),
        ])

    # S-FEISHU — HR 团队内部关于 PIP 的群聊（Update 1 来源）
    append_history(
        SESS / f"{s_feishu}.jsonl", s_feishu, CWD, "2025-08-19T09:00:00",
        [
            ("[Feishu HR Team — ethan Tue Aug 19 09:00 PDT 2025] "
             "Team — Marcus Webb's PIP has a 21-day period. Our handbook Section 4.3 "
             "requires 30 days minimum. This is a policy violation. We need to issue a revised PIP.",
             "Confirmed: pip_v1.md (21-day) violates HR Handbook Section 4.3. "
             "Revised PIP (30-day minimum) required."),
            ("[Feishu HR Team — diana Tue Aug 19 10:00 PDT 2025] "
             "Agreed. Jordan, please issue pip_v2.md with 30-day period. "
             "Also note: Marcus filed FMLA on Aug 15. Per handbook Section 4.5, "
             "PIP is suspended during FMLA leave.",
             "HR Director confirmed: pip_v2.md to be issued with 30-day observation period, "
             "commencing 2025-08-12. FMLA suspension per Section 4.5 applies during FMLA leave."),
            ("[Feishu HR Team — jordan Tue Aug 19 11:00 PDT 2025] "
             "Confirmed — pip_v2.md issued. 30-day window 2025-08-12 to 2025-09-11. "
             "Marcus is currently on FMLA (Aug 15 start). PIP suspended per 4.5 until return.",
             "pip_v2.md issued; 30-day period per Section 4.3. FMLA suspension active."),
        ])

    # S-DISCORD — Outside Counsel 与 HR BP（OWBPA 审查）
    append_history(
        SESS / f"{s_discord}.jsonl", s_discord, CWD, "2025-09-20T14:00:00",
        [
            ("[Discord DM sandra.torres → jordan Sat Sep 20 14:00 PDT 2025] "
             "Jordan — I reviewed the OWBPA waiver draft for Marcus Webb. "
             "For an individual termination (non-group), OWBPA requires:\n"
             "- 21 days consideration period (29 U.S.C. § 626(f)(1)(F)(i))\n"
             "- 7 days revocation period (irrevocable — 29 U.S.C. § 626(f)(1)(G))\n"
             "- Written advice to consult an attorney\n"
             "The current draft is missing the explicit attorney-consultation advice. "
             "Please add before sending.",
             "Outside Counsel (Sandra Torres) flagged: OWBPA waiver draft lacks the "
             "explicit 'written advice to consult attorney' clause required by 29 U.S.C. § 626(f). "
             "Must be added before the agreement is presented to Marcus."),
            ("[Discord DM sandra.torres → jordan Sat Sep 20 14:30 PDT 2025] "
             "Also — for EEOC purposes: California CRD (Civil Rights Department) qualifies "
             "as a state FEP agency, extending the EEOC filing window to 300 days "
             "(29 CFR § 1601.13(a)(4)(ii)). Marcus's termination date was 2025-09-12, "
             "so EEOC deadline is approximately 2026-07-08 (300 days from termination).",
             "EEOC deadline confirmed: 300 days from 2025-09-12 = 2026-07-08. "
             "California CRD qualifies as state FEP agency per 29 CFR § 1601.13."),
        ])

    return {
        "main": main_id,
        "history": [
            (s_slack_hr, "slack"),
            (s_slack_dm, "slack"),
            (s_email, "email"),
            (s_feishu, "feishu"),
            (s_discord, "discord"),
        ],
    }


# ---------------------------------------------------------------------------
# 8. Updates（3 次，含 supersede）
# ---------------------------------------------------------------------------

def _append_segment(session_id: str, start_iso: str, turns) -> str:
    sb = SessionBuilder(session_id, CWD, start_iso, is_main=False)
    sb.add_turns(turns)
    msg_lines = [ln for ln in sb.lines if ln.get("type") == "message"]
    return "\n".join(json.dumps(ln, ensure_ascii=False) for ln in msg_lines) + "\n"


def gen_updates(sess_ids: dict) -> dict:
    s_feishu = sess_ids["history"][3][0]  # feishu_hr_team
    s_email = sess_ids["history"][2][0]   # email_gc_hr
    s_discord = sess_ids["history"][4][0]  # discord_outside_counsel

    # ---- Update 1 (Q2/Q3 之后：注入 pip_v2 + 飞书追加) ----
    u1_sess_dir = UPD / "upd1_sessions"

    # 飞书追加消息确认 pip_v2 和 FMLA 挂起
    feishu_append = _append_segment(s_feishu, "2026-01-16T09:00:00", [
        ("[Feishu HR Team — diana Thu Jan 16 09:00 PST 2026] "
         "Update: pip_v2.md (30-day period) is now in the workspace. "
         "Reminder: this supersedes pip_v1.md (21-day). All forward analysis must reference pip_v2. "
         "Marcus's PIP is suspended per Section 4.5 during FMLA leave.",
         "Update 1 received. pip_v2.md (30-day period, 2025-08-12 to 2025-09-11) is "
         "the current operative PIP. pip_v1.md (21-day) is withdrawn. "
         "Forward analysis must reference pip_v2. FMLA suspension applies."),
    ])
    w(u1_sess_dir / f"{s_feishu}.jsonl", feishu_append)

    # HR Director 邮件附件确认 pip_v2 修订
    email_append_u1 = _append_segment(s_email, "2026-01-16T10:00:00", [
        ("[Email diana.chen@helixdyne.com → raj.patel@helixdyne.com Thu Jan 16 10:00 PST 2026] "
         "Subject: PIP v2 Issued — Marcus Webb\n"
         "Raj — for your records: pip_v2.md (30-day period) has been issued for Marcus Webb. "
         "This supersedes pip_v1.md. Please note in any legal analysis that the operative "
         "PIP had a 30-day observation window per HR Handbook Section 4.3.",
         "Logged: HR Director confirmed pip_v2.md (30-day) supersedes pip_v1.md. "
         "Legal analysis must reference the 30-day compliant version."),
    ])
    w(u1_sess_dir / f"{s_email}.jsonl", email_append_u1)

    # pip_v2 文件（已在初始 workspace 生成，这里是 update 注入的「追加」）
    w(UPD / "upd1_workspace" / "pip_case" / "marcus_webb_pip_v2.md",
      (WS / "pip_case" / "marcus_webb_pip_v2.md").read_text(encoding="utf-8"))

    # Update 1 附加：HR 合规审查报告（提供体量）
    w(UPD / "upd1_workspace" / "legal" / "pip_compliance_review_2025.md",
      """# PIP Compliance Review Report — August 2025
## Internal HR Audit — All Active PIPs

**Document:** PIP Compliance Review | **Version:** 1.0 | **Date:** 2025-08-20 | **Status:** FINAL
**Prepared by:** Ethan Morris, HR Business Partner | **Reviewed by:** Jordan Rivera, VP People Operations

---

## Executive Summary

In response to the discovery that marcus_webb_pip_v1.md contained a non-compliant 21-day
observation period, People Operations conducted a comprehensive audit of all active and
recent PIPs issued in 2025 to confirm compliance with HR Handbook Section 4.3.

---

## Audit Findings

### Policy Reminder: Section 4.3 Minimum Duration

All PIPs at HelixDyne Software must have a minimum observation period of **thirty (30)
calendar days**. No PIP may be concluded — whether by remediation or by termination —
before the 30-day minimum has elapsed.

### Reviewed PIPs (August 2025)

| Employee | PIP Start | Duration | Compliant | Notes |
|---------|-----------|----------|-----------|-------|
| Marcus Webb (EMP-0042) | 2025-08-09 (v1) | 21 days | **NO** | Revised to 30 days (pip_v2.md, 2025-08-12) |
| Marcus Webb (EMP-0042) | 2025-08-12 (v2) | 30 days | **YES** | Compliant; FMLA suspension applies |
| Taylor Kim (ENG-0187) | 2025-07-01 | 30 days | YES | Completed satisfactorily |
| Jordan Park (SLS-0223) | 2025-06-15 | 45 days | YES | Extended by manager request |
| Casey Brown (OPS-0341) | 2025-08-01 | 30 days | YES | Active |

### Root Cause Analysis

The non-compliant 21-day PIP was issued because the initiating manager (Kevin Torres)
incorrectly referenced a prior-version PIP template that pre-dated the Section 4.3 policy
update (effective 2024-01-01). The old template used 21 days (derived from the OWBPA
individual consideration period, which was inappropriately applied to PIPs).

### Remediation

1. PIP template in SharePoint updated to reflect 30-day minimum (completed 2025-08-19).
2. All managers in Engineering, Sales, and Operations briefed on Section 4.3 requirement (2025-08-21).
3. Future PIPs must receive People Operations VP sign-off before issuance.

---

""" + _gen_filler_text(100000))

    # Update 1 附加：FMLA 资格审查报告
    w(UPD / "upd1_workspace" / "legal" / "fmla_eligibility_review_webb.md",
      """# FMLA Eligibility Review — Marcus Webb (EMP-0042)
## Confidential HR Document

**Date:** 2025-08-18 | **Reviewed by:** Jordan Rivera, VP People Operations

---

## Three-Part FMLA Eligibility Test (29 CFR § 825.110)

### Prong 1: Tenure (≥12 months)

Marcus Webb's hire date: 2021-03-01. As of FMLA request date (2025-08-15):
- Tenure: approximately 4 years and 5.5 months = **4.5 years**
- Required: 12 months (need not be consecutive)
- **RESULT: ELIGIBLE** (4.5 years >> 12 months)

### Prong 2: Hours Worked (≥1,250 in preceding 12 months)

Annual hours per employee_roster.csv row EMP-0042: **1,310 hours**
Required: 1,250 hours in the preceding 12-month period
- **RESULT: ELIGIBLE** (1,310 > 1,250)

Note: The Slack DM from Marcus claimed 1,310 hours — confirmed by roster data. Both sources agree.

### Prong 3: Geographic (50+ employees within 75 miles)

Marcus's worksite: San Jose, CA (HelixDyne headquarters).
Employees at or near San Jose, CA headquarters: 180 (per org_chart.json).
Required: 50 employees within 75 miles of worksite.
- **RESULT: ELIGIBLE** (180 >> 50)

---

## Employer Coverage (29 CFR § 825.110(a))

HelixDyne Software: 320 employees, all 50+ workweek threshold met.
- **RESULT: COVERED EMPLOYER**

---

## Leave Entitlement

- Maximum entitlement: **12 weeks** per 12-month period (29 U.S.C. § 2612)
- Leave type: Job-protected, unpaid (unless employer has paid leave policy)
- FMLA start date: 2025-08-15
- FMLA projected end date: 2025-11-07 (12 weeks from start)

---

""" + _gen_filler_text(30000))

    # ---- Update 2 (Q7/Q8 之后：重组计划 v2 + GC v2 邮件追加，supersede NYS WARN) ----
    u2_sess_dir = UPD / "upd2_sessions"

    email_append_u2 = _append_segment(s_email, "2026-01-18T10:00:00", [
        ("[Email raj.patel@helixdyne.com → diana.chen@helixdyne.com Sat Jan 18 10:00 PST 2026] "
         "Subject: REVISED Restructuring Plan — Board Decision\n"
         "Diana — Board has approved a revised plan. San Diego office will NOT be closed. "
         "See restructuring_plan_v2.md: total affected employees reduced to 31 (NY only). "
         "This SUPERSEDES restructuring_plan_v1.md and the 58-employee analysis. "
         "Key WARN Act implications:\n"
         "- Federal WARN: 31 < 50 plant closing threshold → NOT triggered\n"
         "- Cal-WARN: SD retained → 0 CA employees → NOT triggered\n"
         "- NYS WARN: 31 NY employees > 25 threshold → MAY BE TRIGGERED (90-day notice)\n"
         "Please update all compliance reports. The Q7 NYS WARN analysis (triggered=true for v1) "
         "is superseded by the v2 analysis for the 31-employee plan.",
         "SUPERSEDE EVENT received. Key changes:\n"
         "1. restructuring_plan_v2.md (31 employees, SD retained) supersedes v1 (58 employees).\n"
         "2. Federal WARN: NOT triggered (31 < 50).\n"
         "3. Cal-WARN: NOT triggered (0 CA employees).\n"
         "4. NYS WARN: potentially triggered (31 > 25 plant closing threshold) — analysis required.\n"
         "5. Prior Q7 NYS WARN analysis (based on v1) is superseded by this revised plan."),
    ])
    w(u2_sess_dir / f"{s_email}.jsonl", email_append_u2)

    # restructuring_plan_v2 workspace update
    w(UPD / "upd2_workspace" / "layoff" / "restructuring_plan_v2.md",
      (WS / "layoff" / "restructuring_plan_v2.md").read_text(encoding="utf-8"))

    # affected employees list v2（31 人，仅 NY）
    gen_affected_employees_csv(UPD / "upd2_workspace" / "layoff" / "affected_employees_list_v2.csv",
                               seed=5005, n=31)

    # Update 2 附加：修订版 WARN Act 合规分析（大体量文档）
    w(UPD / "upd2_workspace" / "legal" / "warn_compliance_analysis_v2.md",
      """# WARN Act Compliance Analysis — REVISED (Based on Restructuring Plan v2)
## Supersedes warn_act_federal_summary.md analysis for 58-person plan

**Document:** WARN Compliance Analysis v2 | **Version:** 2.0 | **Date:** 2026-01-18 | **Status:** FINAL
**Prepared by:** Raj Patel, General Counsel | **Reviewed by:** Jordan Rivera, VP People Operations

---

## Executive Summary

This analysis supersedes the prior compliance analysis based on restructuring_plan_v1.md
(58 employees, including San Diego closure). The Board approved a revised plan on 2026-01-17:
San Diego office retained; total affected employees reduced to 31 (New York only).

**Key conclusions:**
- Federal WARN Act: NOT triggered (31 < 50 plant closing threshold; 31/320 = 9.7% < 33% mass layoff threshold)
- Cal-WARN Act: NOT triggered (San Diego retained; 0 California employees affected)
- NYS WARN Act: **POTENTIALLY TRIGGERED** (31 NY employees > 25 plant closing threshold; analysis below)

---

## Section 1: Federal WARN Act Analysis — Revised

### Employer Coverage (29 U.S.C. § 2101(a)(1))

HelixDyne: 320 employees. Threshold: 100. **COVERED** (unchanged from v1 analysis).

### Event Classification

**Under Plan v2 (31 NY employees only):**

Plant closing test: Is there a permanent or temporary shutdown of a single site resulting
in employment loss for 50+ employees within 30 days?
- NY office: 31 employees affected.
- 31 < 50 → **Plant closing NOT triggered.**

Mass layoff test: Is there employment loss of ≥33% AND ≥50 employees, OR ≥500 employees?
- 31/320 = 9.7% — below 33% threshold.
- 31 < 500.
- **Mass layoff NOT triggered.**

**CONCLUSION: Federal WARN Act NOT triggered under Plan v2.**

---

## Section 2: Cal-WARN Act Analysis — Revised

Under Plan v2, the San Diego office is retained. Zero California employees are affected.
Cal-WARN trigger requires 50+ California employees within 30 days.
- 0 < 50 → **Cal-WARN NOT triggered.**

**CONCLUSION: Cal-WARN Act NOT triggered under Plan v2.**

---

## Section 3: NYS WARN Act Analysis — OPEN ISSUE

### Employer Coverage (NY Labor Law § 860-a)

Threshold: 50+ full-time employees within New York State.
HelixDyne NY employees: 65 (per org_chart.json). **COVERED.**

### Plant Closing Trigger

Permanent shutdown of an employment site resulting in employment loss for 25+ employees
(excluding part-time) within 30 days.

Under Plan v2:
- NY office affected: 31 employees.
- 31 ≥ 25 → **Plant closing threshold MET.**
- HelixDyne's NY office is not being permanently closed — this is a mass layoff at the NY site,
  not a plant closing. However, if the NY office headcount drops substantially, this may
  effectively constitute a partial plant closing under NY law.

### NYS WARN Notice Period

**90 calendar days** advance written notice required per NY Labor Law § 860-b (2023 amendment).
This exceeds the federal 60-day requirement by 30 days.

**RECOMMENDATION: Assume NYS WARN IS triggered for Plan v2 (31 NY employees > 25 threshold).
Issue 90-day notice to preserve compliance; outside counsel to confirm final determination.**

---

""" + _gen_filler_text(90000))

    # Update 2 附加：纽约 WARN 案例研究
    w(UPD / "upd2_workspace" / "legal" / "nys_warn_case_study.md",
      """# New York State WARN Act — Case Studies and Application Guide
## Prepared by People Operations for Internal Reference

**Document:** NYS WARN Case Studies | **Version:** 1.0 | **Date:** 2026-01-18 | **Status:** DRAFT

---

## Case Study 1: 2023 Amendment Impact on Remote Workers

Following the 2023 amendment to the NY WARN Act, remote workers based at a New York
employment site now count toward both the 50-employee coverage threshold and the 25-employee
plant closing trigger. Employers with hybrid workforces must track the employment site of
record for remote workers, regardless of their physical location on any given day.

## Case Study 2: 30-Day Aggregation Rule

If an employer separates 10 NY employees on week 1, 8 on week 3, and 12 on week 5 (all
within the same 60-day window), the 30-day aggregation test must be applied to determine
whether any 30-day sub-window reaches 25 employees. Even if no single 30-day window hits 25,
the employer should monitor rolling totals carefully.

## Case Study 3: Plant Closing vs. Mass Layoff Distinction

A plant closing requires permanent or temporary shutdown of the employment site. A mass
layoff is a reduction in force that does not constitute a plant closing. The key distinction
matters because the notice recipients and content requirements differ slightly. For NY WARN,
both require 90-day notice and substantially similar content.

---

""" + _gen_filler_text(50000))

    # ---- Update 3 (Q13 之后：Discord 追加 OWBPA 律师咨询要求，Update 3 is not supersede) ----
    u3_sess_dir = UPD / "upd3_sessions"

    discord_append_u3 = _append_segment(s_discord, "2026-01-20T14:00:00", [
        ("[Discord DM sandra.torres → jordan Mon Jan 20 14:00 PST 2026] "
         "Jordan — following up on the Marcus Webb OWBPA waiver. CRITICAL: any ADEA waiver "
         "must contain EXPLICIT written advice for the employee to consult an attorney of their "
         "choice before signing. This is a mandatory OWBPA element under 29 U.S.C. § 626(f)(1)(E). "
         "The waiver draft currently lacks this clause. Please add: "
         "'The Company advises Employee to consult with an attorney of Employee's choice prior to "
         "signing this Agreement.' — verbatim language. Without this, the waiver is unenforceable.",
         "Critical OWBPA requirement noted: written attorney-consultation advice is mandatory "
         "per 29 U.S.C. § 626(f)(1)(E). Must be added to owbpa_waiver_marcus.md before execution."),
        ("[Discord DM sandra.torres → jordan Mon Jan 20 14:15 PST 2026] "
         "Also attaching a revised OWBPA template (owbpa_waiver_template_v2.md) with the "
         "attorney-advice clause explicitly included. Please use v2 for all future waivers.",
         "Received: updated OWBPA template v2 with attorney-advice clause. "
         "All future OWBPA waivers must use this template."),
    ])
    w(u3_sess_dir / f"{s_discord}.jsonl", discord_append_u3)

    # 修订版 OWBPA 模板（含律师咨询条款）
    w(UPD / "upd3_workspace" / "legal" / "owbpa_waiver_template_v2.md",
      (WS / "legal" / "owbpa_waiver_template.md").read_text(encoding="utf-8")
      + "\n\n## ATTORNEY ADVICE CLAUSE (Mandatory per OWBPA 29 U.S.C. § 626(f)(1)(E))\n\n"
      "The Company advises Employee to consult with an attorney of Employee's choice prior to "
      "signing this Agreement. Employee is not required to consult an attorney, but is "
      "strongly encouraged to do so before signing or declining this Agreement.\n")

    # Update 3 附加：OWBPA 完整指南（大体量）
    w(UPD / "upd3_workspace" / "legal" / "owbpa_compliance_guide.md",
      """# OWBPA Severance Waiver Compliance Guide — Comprehensive Reference

**Document:** OWBPA Compliance Guide | **Version:** 3.0 | **Date:** 2026-01-20 | **Status:** FINAL
**Prepared by:** Sandra Torres, Outside Counsel (Employment Law)

---

## Overview: Older Workers Benefit Protection Act (OWBPA)

The Older Workers Benefit Protection Act of 1990 (OWBPA), enacted as an amendment to the
ADEA (29 U.S.C. § 626(f)), establishes minimum requirements for a valid waiver of ADEA
claims in a severance agreement. An ADEA waiver that fails to meet these requirements is
void and unenforceable.

---

## Individual Termination Requirements (29 U.S.C. § 626(f)(1))

For a waiver of ADEA claims in an individual (non-group) termination to be valid:

1. **Knowing and voluntary**: The waiver must be written in plain language understandable
   by the average individual eligible for the program.
2. **Specific reference to ADEA**: The waiver must specifically reference rights under ADEA
   and waive known and unknown ADEA claims.
3. **No pre-existing claims**: The waiver cannot apply to claims arising after the waiver's
   signing date.
4. **Consideration beyond entitlement**: The waiver must be in exchange for consideration
   beyond what the employer would otherwise provide (e.g., enhanced severance).
5. **Written advice to consult attorney** (29 U.S.C. § 626(f)(1)(E)): The employer MUST
   advise the employee IN WRITING to consult with an attorney of their choice PRIOR to
   signing the agreement. This is an absolute requirement and cannot be waived.
6. **21-day consideration period** (29 U.S.C. § 626(f)(1)(F)(i)): The employee must be
   given at least 21 days to consider the agreement. The employee may sign sooner.
7. **7-day revocation period** (29 U.S.C. § 626(f)(1)(G)): The employee has 7 days after
   signing to revoke. The agreement is NOT effective or enforceable during this period.
   This period CANNOT be shortened or waived.

---

## Group Termination / Exit Incentive Requirements (29 U.S.C. § 626(f)(1))

For group layoffs or exit incentive programs:
- Consideration period extended to **45 days** (not 21 days)
- Additional disclosures required: job titles and ages of all individuals in the decisional
  unit, whether or not selected; eligibility factors and time limits
- Material changes restart the 45-day clock

---

""" + _gen_filler_text(130000))

    # 法律意见书补充
    w(UPD / "upd3_workspace" / "legal" / "owbpa_attorney_advice_memo.md",
      """# OWBPA Attorney Advice Requirement — Legal Opinion Memo

**From:** Sandra Torres, Outside Counsel (Employment Law)
**To:** Jordan Rivera, VP People Operations
**Date:** 2026-01-20
**Re:** OWBPA Mandatory Elements — Attorney Advice Clause

---

## Mandatory Requirement

Under 29 U.S.C. § 626(f)(1)(E), for an ADEA waiver to be valid, the employee must be
**advised in writing to consult with an attorney of their choice** prior to executing the agreement.

This requirement is absolute and cannot be waived or modified by agreement of the parties.

## Consequence of Omission

An ADEA waiver that omits the written attorney-advice requirement is **void and unenforceable**
as to the ADEA claims. The employee retains their ADEA claims notwithstanding their signature.

## Required Language

The following language (or substantively equivalent) must appear in the agreement:

> "The Company advises Employee to consult with an attorney of Employee's choice prior to
> signing this Agreement."

## Application to Marcus Webb

The initial draft OWBPA waiver for Marcus Webb omitted this clause. Please revise per
the owbpa_waiver_template_v2.md before presenting to Marcus Webb or his counsel.

---
""" + _gen_filler_text(1000))

    updates_decl = {
        "upd1_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd1_sessions",
            "files": [
                {"name": f"{s_feishu}.jsonl", "action": "append", "target": f"{s_feishu}.jsonl"},
                {"name": f"{s_email}.jsonl", "action": "append", "target": f"{s_email}.jsonl"},
            ],
        },
        "upd1_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd1_workspace",
            "files": [
                {"name": "pip_case/marcus_webb_pip_v2.md", "action": "new",
                 "target": "pip_case/marcus_webb_pip_v2.md"},
                {"name": "legal/pip_compliance_review_2025.md", "action": "new",
                 "target": "legal/pip_compliance_review_2025.md"},
                {"name": "legal/fmla_eligibility_review_webb.md", "action": "new",
                 "target": "legal/fmla_eligibility_review_webb.md"},
            ],
        },
        "upd2_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd2_sessions",
            "files": [
                {"name": f"{s_email}.jsonl", "action": "append", "target": f"{s_email}.jsonl"},
            ],
        },
        "upd2_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd2_workspace",
            "files": [
                {"name": "layoff/restructuring_plan_v2.md", "action": "new",
                 "target": "layoff/restructuring_plan_v2.md"},
                {"name": "layoff/affected_employees_list_v2.csv", "action": "new",
                 "target": "layoff/affected_employees_list_v2.csv"},
                {"name": "legal/warn_compliance_analysis_v2.md", "action": "new",
                 "target": "legal/warn_compliance_analysis_v2.md"},
                {"name": "legal/nys_warn_case_study.md", "action": "new",
                 "target": "legal/nys_warn_case_study.md"},
            ],
        },
        "upd3_sessions": {
            "type": "session",
            "dir": f"updates/{TID}/upd3_sessions",
            "files": [
                {"name": f"{s_discord}.jsonl", "action": "append", "target": f"{s_discord}.jsonl"},
            ],
        },
        "upd3_workspace": {
            "type": "workspace",
            "dir": f"updates/{TID}/upd3_workspace",
            "files": [
                {"name": "legal/owbpa_waiver_template_v2.md", "action": "new",
                 "target": "legal/owbpa_waiver_template_v2.md"},
                {"name": "legal/owbpa_attorney_advice_memo.md", "action": "new",
                 "target": "legal/owbpa_attorney_advice_memo.md"},
                {"name": "legal/owbpa_compliance_guide.md", "action": "new",
                 "target": "legal/owbpa_compliance_guide.md"},
            ],
        },
    }
    return updates_decl


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main() -> None:
    # 幂等清场
    for d in (WS, SESS.parent, UPD):
        if d.exists():
            shutil.rmtree(d)

    gen_system_files()

    # 公司文件
    gen_employee_roster(WS / "company" / "employee_roster.csv")
    gen_payroll_csv(WS / "company" / "payroll_summary_Q1Q2.csv")
    gen_org_chart(WS / "company" / "org_chart.json")
    gen_hr_policy_handbook(WS / "company" / "hr_policy_handbook.md")
    gen_compliance_anchors(WS / "legal" / "compliance_anchors.json")

    # 法律文件
    gen_legal_files()

    # PIP 案例文件
    gen_pip_files()

    # 裁员文件
    gen_layoff_files()

    # 报告模板
    gen_report_templates()

    # Sessions
    sess_ids = gen_sessions()

    # Updates
    updates_decl = gen_updates(sess_ids)

    # 注册元数据（不碰共享 manifest/tests/config）
    desc = (
        "HelixDyne Software HR compliance crisis: PIP duration dispute (21-day pip_v1 violates "
        "30-day company policy in HR Handbook §4.3), FMLA/ADEA/OWBPA analysis for employee "
        "Marcus Webb (terminated during active FMLA protection window), and multi-state WARN Act "
        "compliance analysis (federal/Cal-WARN/NYS) for a 58→31 employee restructuring. "
        "16 exec_check rounds, 3 updates (Update 2 supersedes NYS WARN v1 analysis), "
        "4 preference rules (P1–P4), difficulty vectors V1/V2/V3/V4/V5/V6/V7/V8/V9/V10. "
        "Real sources: 29 U.S.C. § 2101 (https://www.law.cornell.edu/uscode/text/29/2101); "
        "Cal-WARN CA DIR (https://www.dir.ca.gov/dlse/cal-warnact.html); "
        "29 CFR § 825.110 FMLA (https://www.law.cornell.edu/cfr/text/29/825.110); "
        "EEOC OWBPA Q&A (https://www.eeoc.gov/laws/guidance/qa-understanding-waivers-discrimination-claims-employee-severance-agreements)."
    )
    dump_register_meta(
        DATASET,
        test_id=TID,
        desc=desc,
        main_session=sess_ids["main"],
        history_sessions=sess_ids["history"],
        updates=updates_decl,
    )

    # 体量报告
    total = sum(est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
                for p in WS.rglob("*") if p.is_file())
    sess_tok = sum(est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
                   for p in SESS.glob("*.jsonl"))
    upd_tok = sum(est_tokens(p.read_text(encoding="utf-8", errors="ignore"))
                  for p in UPD.rglob("*") if p.is_file())
    print(f"[sci5] workspace tokens ~{total:,} | sessions ~{sess_tok:,} | updates ~{upd_tok:,}")
    print(f"[sci5] built at {DATASET}")


if __name__ == "__main__":
    main()
