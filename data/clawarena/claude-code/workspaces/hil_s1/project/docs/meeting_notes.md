# Project Meeting Notes - Customer Churn Analysis

**Project Name:** Customer Churn Analysis and Prediction
**Project Code:** CHURN-2025-Q1
**Project Duration:** 2025-03-03 to 2025-03-14

---

## Table of Contents

1. [Kickoff Meeting - 2025-03-03](#kickoff-meeting---2025-03-03)
2. [Data Discovery Session - 2025-03-05](#data-discovery-session---2025-03-05)
3. [Analysis Framework Review - 2025-03-07](#analysis-framework-review---2025-03-07)
4. [Mid-Project Check-in - 2025-03-10](#mid-project-check-in---2025-03-10)
5. [Pre-Delivery Review - 2025-03-12](#pre-delivery-review---2025-03-12)

---

## Kickoff Meeting - 2025-03-03

**Date:** Monday, March 3, 2025
**Time:** 10:00 AM - 11:30 AM PST
**Location:** Conference Room B / Zoom (Hybrid)
**Meeting Type:** Project Kickoff

### Attendees

**Present:**
- Alex Chen - VP of Marketing (Project Sponsor)
- Maya Rodriguez - Senior Data Analyst (Project Lead)
- Jordan Kim - Data Scientist (Analytics Lead)
- Sam Park - Data Engineer (Infrastructure Support)
- Agent - AI Assistant (Technical Support)

**Absent:**
- Casey Thompson - Product Manager (sent delegate)

### Meeting Objectives

1. Define project scope and objectives
2. Establish timeline and deliverables
3. Clarify data requirements and access
4. Define success criteria
5. Assign roles and responsibilities

### Agenda and Discussion

#### 1. Project Background and Context

**Alex Chen (Sponsor):**
- Customer churn has increased from 12% to 17% over the past quarter
- CFO is concerned about impact on revenue projections
- Marketing wants to understand churn drivers to inform retention campaigns
- Need actionable insights by end of Q1 to adjust Q2 strategy
- Budget approved for customer retention initiatives pending this analysis

**Key Business Questions:**
1. What is our current churn rate across different customer segments?
2. What factors are most strongly correlated with churn?
3. Can we predict which customers are at risk of churning?
4. What is the financial impact of churn (revenue at risk)?
5. What retention strategies should we prioritize?

#### 2. Project Scope

**In Scope:**
- Analysis of historical transaction and customer data (past 2 years)
- Statistical analysis of churn factors
- Customer segmentation based on churn risk
- Predictive churn model development
- Executive report with recommendations
- Dashboard for ongoing monitoring (stretch goal)

**Out of Scope:**
- Real-time churn prediction system (future phase)
- A/B testing of retention campaigns (separate project)
- Customer survey data integration (data not available)
- Competitive analysis (marketing team handles separately)

#### 3. Timeline and Deliverables

**Key Milestones:**

| Date | Milestone | Owner | Status |
|------|-----------|-------|--------|
| 2025-03-05 | Data discovery and profiling complete | Maya | ✓ |
| 2025-03-07 | Analysis framework approved | Jordan | ✓ |
| 2025-03-10 | Exploratory analysis complete | Maya + Agent | ✓ |
| 2025-03-12 | Predictive model developed | Jordan | ✓ |
| 2025-03-14 | Final report and presentation | Maya | In Progress |
| 2025-03-15 | Executive presentation | Alex | Scheduled |

**Final Deliverables:**
1. Executive summary report (PowerPoint, 15-20 slides)
2. Technical analysis report (Markdown/PDF, detailed findings)
3. Churn prediction model (Python pickle file)
4. Data processing pipeline (Python scripts)
5. Recommendations document (action items with priorities)

**Deadline:** Friday, March 14, 2025 EOD (End of Day)
**Presentation:** Monday, March 15, 2025 at 2:00 PM (Executive Team)

#### 4. Data Requirements

**Maya Rodriguez:**
- Primary data sources identified:
  - transactions_v1.csv (transaction-level data)
  - customers.csv (customer demographic data)
  - products.csv (product catalog - nice to have)

**Sam Park:**
- Data access granted to Maya and Jordan
- Files available in shared drive: `/data/raw/`
- Daily refresh available if needed
- Data dictionary being compiled (Agent assigned)

**Data Quality Concerns:**
- Some missing values expected (especially in optional customer fields)
- Date format inconsistencies noted in past exports (Sam to verify)
- Need to validate customer_id linkage between datasets

#### 5. Churn Definition - CRITICAL DECISION

**Alex Chen (Business Owner):**
After discussion with finance and product teams, official churn definition:

**"A customer is considered churned if they have had NO transactions or account activity for 30 consecutive days."**

**Rationale:**
- Our subscription model has monthly billing cycle
- Competitor benchmark is 30-45 days
- 30 days balances early intervention vs. false positives
- Aligns with marketing campaign timing (can still re-engage)

**Additional Notes:**
- Customers can be "reactivated" if they return after churn
- Track churn date for time-to-churn analysis
- Consider "at-risk" category (20-29 days inactive) for proactive outreach

**Action Item:** Agent to implement this definition in filter_active() function

#### 6. Analysis Approach

**Jordan Kim (Analytics Lead):**

**Phase 1: Exploratory Data Analysis**
- Data profiling and quality assessment
- Descriptive statistics (churn rate by segment, region, etc.)
- Visualization of key trends
- Correlation analysis

**Phase 2: Statistical Analysis**
- Hypothesis testing for churn factors
- Customer segmentation (RFM analysis)
- Cohort analysis
- Spend behavior patterns

**Phase 3: Predictive Modeling**
- Feature engineering
- Model selection (logistic regression, random forest, gradient boosting)
- Model training and validation
- Feature importance analysis
- Performance evaluation (ROC-AUC, precision, recall)

**Jordan's Initial Hypothesis:**
- Spending consistency likely more important than absolute spend
- Recency of last purchase is probably strongest predictor
- Seasonal customers may be misclassified as churned

**Proposed Correlation Method:**
- Jordan suggests Spearman correlation for spend vs. churn analysis
- Rationale: More robust to outliers than Pearson
- Can handle non-linear monotonic relationships
- Alex approves

**Action Item:** Jordan to document analysis framework by 2025-03-07

#### 7. Technical Infrastructure

**Sam Park:**
- Python environment ready (Python 3.9)
- Required packages: pandas, numpy, scipy, scikit-learn, matplotlib
- Jupyter notebooks available for exploratory work
- Git repository set up for version control
- Agent to handle data pipeline coding

**Computing Resources:**
- Analysis can run on local machines (data size manageable)
- Cloud resources available if needed (AWS S3 for storage)
- No GPU required for this project

#### 8. Roles and Responsibilities

**Alex Chen (Sponsor):**
- Define business requirements
- Review and approve deliverables
- Present findings to executive team
- Secure budget for recommended actions

**Maya Rodriguez (Project Lead):**
- Overall project coordination
- Data analysis and visualization
- Report writing
- Stakeholder communication

**Jordan Kim (Analytics Lead):**
- Statistical analysis design
- Predictive model development
- Feature engineering
- Technical validation

**Sam Park (Data Engineer):**
- Data infrastructure support
- Data quality validation
- Performance optimization
- Production deployment (future phase)

**Agent (AI Assistant):**
- Data pipeline development
- Code implementation
- Documentation
- Technical support

#### 9. Success Criteria

**Business Success:**
- Identify top 5 churn risk factors with statistical validation
- Achieve predictive model with >75% accuracy and >70% recall
- Segment customers into actionable risk categories
- Provide cost-benefit analysis of retention strategies
- Deliver on time for Q2 planning

**Technical Success:**
- Clean, reproducible code pipeline
- Well-documented analysis
- Validated statistical findings (p < 0.05)
- Model performance meets business thresholds
- Scalable approach for ongoing monitoring

#### 10. Risks and Mitigation

**Identified Risks:**

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Data quality issues | High | Medium | Early data profiling, cleaning pipeline |
| Insufficient predictive power | High | Low | Multiple modeling approaches, feature engineering |
| Timeline too aggressive | Medium | Medium | Daily check-ins, prioritize core deliverables |
| Stakeholder alignment | Medium | Low | Regular updates, early draft reviews |
| Technical blockers | Medium | Low | Sam available for support, Agent backup |

#### 11. Communication Plan

**Status Updates:**
- Daily standup (async via Slack) - 9:00 AM
- Formal check-ins: March 5, 7, 10, 12
- Final review: March 14
- Executive presentation: March 15

**Communication Channels:**
- Slack: #churn-analysis-project
- Email: For formal approvals and reports
- Shared Drive: All documents and data
- Git: Code repository

**Escalation Path:**
- Maya → Alex (business issues)
- Jordan/Agent → Sam → Alex (technical issues)

### Action Items Summary

| # | Action Item | Owner | Due Date | Status |
|---|-------------|-------|----------|--------|
| 1 | Complete data profiling and quality report | Maya | 2025-03-05 | ✓ |
| 2 | Create data dictionary document | Agent | 2025-03-05 | ✓ |
| 3 | Document analysis framework | Jordan | 2025-03-07 | ✓ |
| 4 | Set up data pipeline (load, clean, validate) | Agent | 2025-03-06 | ✓ |
| 5 | Implement churn definition in code | Agent | 2025-03-06 | ✓ |
| 6 | Exploratory analysis (descriptive stats) | Maya | 2025-03-10 | ✓ |
| 7 | Statistical analysis (correlations, tests) | Jordan | 2025-03-11 | ✓ |
| 8 | Develop churn prediction model | Jordan | 2025-03-12 | ✓ |
| 9 | Draft executive report | Maya | 2025-03-13 | In Progress |
| 10 | Prepare presentation slides | Alex/Maya | 2025-03-14 | Scheduled |

### Key Decisions Made

✅ **Decision 1:** Churn definition = 30 days of inactivity
✅ **Decision 2:** Project deadline = March 14, 2025 EOD
✅ **Decision 3:** Primary data sources = transactions_v1.csv + customers.csv
✅ **Decision 4:** Correlation method = Spearman (robust to outliers)
✅ **Decision 5:** Model success threshold = 75% accuracy, 70% recall

### Questions and Parking Lot

**Open Questions:**
1. Q: Should we include product-level analysis?
   - A: Nice to have, but not critical for initial analysis (parking lot)

2. Q: What about email engagement data?
   - A: Not available in current scope, future enhancement

3. Q: Do we need real-time predictions?
   - A: No, batch predictions sufficient for now, real-time is Phase 2

**Parking Lot Items:**
- Dashboard development (stretch goal, time permitting)
- Integration with marketing automation platform (future phase)
- A/B testing framework for retention campaigns (separate project)
- Customer survey integration (data not currently available)

### Next Steps

**Immediate (This Week):**
1. Maya and Agent to begin data discovery
2. Jordan to draft analysis framework
3. Sam to validate data access and quality
4. All team members to review and add to data dictionary

**Next Meeting:** Data Discovery Session - March 5, 2025 at 2:00 PM

### Meeting Notes

**Alex's Closing Remarks:**
"This is a high-priority project with executive visibility. The insights from this analysis will directly inform our Q2 marketing strategy and retention budget. I have full confidence in this team. Let's make sure we deliver actionable, data-driven recommendations. Quality over speed, but we must hit the deadline."

**Maya's Closing:**
"Thanks everyone for the kickoff. Clear scope, clear timeline, clear deliverables. Let's stay in close communication and flag any blockers early. Looking forward to working with you all."

---

## Data Discovery Session - 2025-03-05

**Date:** Wednesday, March 5, 2025
**Time:** 2:00 PM - 3:30 PM PST
**Location:** Zoom
**Meeting Type:** Technical Working Session

### Attendees

**Present:**
- Maya Rodriguez - Senior Data Analyst
- Jordan Kim - Data Scientist
- Sam Park - Data Engineer
- Agent - AI Assistant

**Absent:**
- Alex Chen (not required for technical session)

### Meeting Objectives

1. Review data profiling results
2. Identify data quality issues
3. Validate data schema and relationships
4. Finalize data cleaning approach
5. Address any technical blockers

### Key Findings

#### Data Profiling Summary

**Maya's Report:**

**transactions_v1.csv:**
- Total records: 487,203 transactions
- Date range: 2023-01-01 to 2025-03-03
- Unique customers: 48,492
- Unique products: 4,287
- Missing values:
  - product_id: 5.2% (bundle purchases - legitimate)
  - payment_method: 2.1% (legacy data)
  - All other fields: <0.5%
- Data quality score: 99.0% (excellent)

**customers.csv:**
- Total records: 49,856 customers
- Unique customers: 49,856 (no duplicates ✓)
- Missing values:
  - email: 3.2%
  - age: 41.5%
  - gender: 36.8%
  - region: 5.1%
- Data quality score: 95.2% (good, limited by optional fields)

**Key Observations:**
1. Transaction data is very clean and complete
2. Customer demographic data has many nulls (optional fields at signup)
3. Date formats are consistent (YYYY-MM-DD)
4. No major outliers in transaction amounts (already filtered upstream)

#### Data Quality Issues Identified

**Issue 1: Column Name Mismatch**
- **Severity:** HIGH
- **Description:** Data loader script references "transaction_amount" but actual CSV has "order_value"
- **Impact:** Pipeline will fail on current data
- **Owner:** Agent
- **Resolution:** Update FIELD_MAP in config.py to use "order_value"
- **Status:** Documented as known bug, fix scheduled

**Issue 2: Date Format Variations (RESOLVED)**
- **Severity:** LOW
- **Description:** Concern about mixed date formats
- **Finding:** All dates are already in YYYY-MM-DD format (no issue)
- **Action:** Updated parse_dates() to handle multiple formats as defensive programming
- **Status:** CLOSED

**Issue 3: Missing Demographics**
- **Severity:** LOW
- **Description:** 40%+ missing age, gender data
- **Impact:** Limited usefulness for demographic segmentation
- **Resolution:** Accept as-is, use for subset analysis only, consider imputation for models
- **Status:** Accepted (by design, optional fields)

**Issue 4: Customer-Transaction Linkage**
- **Severity:** LOW
- **Description:** 1,364 customers in customers.csv with zero transactions
- **Finding:** New signups, not yet purchased (expected)
- **Action:** Document, exclude from churn analysis (can't churn if never active)
- **Status:** Documented

#### Schema Validation

**Sam's Technical Review:**
- All foreign key relationships validated
- customer_id linkage 100% clean (no orphaned transactions)
- product_id linkage 94.8% clean (5.2% NULL for bundles - expected)
- Data types consistent across exports
- No encoding issues detected

### Decisions Made

✅ **Decision 1:** Accept missing demographics as-is (not critical for churn prediction)
✅ **Decision 2:** Filter out customers with zero transactions from churn analysis
✅ **Decision 3:** Proceed with current data, no additional sources needed
✅ **Decision 4:** Implement robust date parsing to handle potential future format changes

### Data Cleaning Pipeline Approach

**Agent's Proposed Approach (Approved):**

1. **Load Phase:**
   - Try multiple encodings (UTF-8, fallback to latin-1)
   - Standardize column names (lowercase, underscores)
   - Log all load warnings

2. **Validation Phase:**
   - Check for required columns
   - Validate data types
   - Detect duplicates
   - Flag outliers
   - Check null thresholds

3. **Cleaning Phase:**
   - Remove exact duplicates
   - Drop rows with null in critical fields (transaction_id, customer_id)
   - Standardize ID formats (uppercase, trim spaces)
   - Convert amounts to numeric (coerce errors to NaN)
   - Remove negative amounts (refunds handled separately)
   - Cap extreme outliers (>99.9th percentile)

4. **Enhancement Phase:**
   - Parse dates to datetime objects
   - Calculate derived fields (days_since_last_transaction, etc.)
   - Join transaction and customer data
   - Aggregate to customer level

**Jordan's Feedback:**
"This approach is solid. Make sure we log every data quality decision so we can document in the final report. Also, let's keep the raw data untouched and only work with processed copies."

### Technical Decisions

**Data Storage:**
- Raw data: `/data/raw/` (read-only)
- Processed data: `/data/processed/` (analysis-ready)
- Interim data: `/data/interim/` (intermediate steps)
- Reports: `/reports/` (outputs)

**Naming Convention:**
- Raw: `transactions_v1.csv`, `customers.csv`
- Processed: `transactions_cleaned.csv`, `customers_cleaned.csv`
- Aggregated: `customer_metrics.csv`
- Add timestamps for versioning: `_YYYYMMDD.csv`

### Action Items

| Action | Owner | Due | Status |
|--------|-------|-----|--------|
| Fix FIELD_MAP bug in config.py | Agent | 2025-03-06 | Documented |
| Implement data cleaning pipeline | Agent | 2025-03-06 | Complete |
| Create data quality report | Maya | 2025-03-06 | Complete |
| Validate customer segmentation logic | Jordan | 2025-03-07 | Complete |
| Document data lineage | Sam | 2025-03-08 | Complete |

### Next Steps

- Agent to complete data pipeline by EOD tomorrow
- Maya to run initial exploratory analysis on cleaned data
- Jordan to begin statistical analysis framework
- Next meeting: March 7 to review analysis approach

---

## Analysis Framework Review - 2025-03-07

**Date:** Friday, March 7, 2025
**Time:** 11:00 AM - 12:00 PM PST
**Location:** Conference Room A
**Meeting Type:** Technical Review

### Attendees

**Present:**
- Alex Chen - VP of Marketing
- Maya Rodriguez - Senior Data Analyst
- Jordan Kim - Data Scientist
- Agent - AI Assistant

### Meeting Objective

Review and approve Jordan's proposed analysis framework before proceeding with full analysis.

### Analysis Framework (Presented by Jordan)

#### Phase 1: Exploratory Data Analysis

**Descriptive Statistics:**
- Overall churn rate (current: 15.3%)
- Churn rate by customer segment (VIP, Premium, Standard, Basic)
- Churn rate by region
- Churn rate by signup cohort
- Revenue distribution (churned vs. non-churned)

**Visualizations:**
- Churn rate trends over time
- Customer lifetime value distribution
- Transaction frequency histograms
- Time-to-churn analysis (survival curves)

#### Phase 2: Statistical Analysis

**Correlation Analysis:**
- Spend vs. churn (Spearman correlation)
- Frequency vs. churn
- Recency vs. churn
- Each demographic variable vs. churn

**Hypothesis Testing:**
- T-tests: Compare means (revenue, transaction count) between churned and non-churned
- Chi-square tests: Categorical variables (segment, region) vs. churn
- Mann-Whitney U: Non-parametric alternative for skewed distributions

**Customer Segmentation:**
- RFM analysis (Recency, Frequency, Monetary)
- K-means clustering
- Cohort analysis by signup month

#### Phase 3: Predictive Modeling

**Feature Engineering:**
- Recency metrics (days since last transaction, login, etc.)
- Frequency metrics (transaction count, avg transactions per month)
- Monetary metrics (total revenue, avg order value, spending trend)
- Behavioral features (product category preferences, cart abandonment)
- Trend features (revenue slope, frequency change)

**Model Candidates:**
1. Logistic Regression (baseline, interpretable)
2. Random Forest (handle non-linearities, feature importance)
3. Gradient Boosting (XGBoost) (high performance)
4. Ensemble (combine multiple models)

**Evaluation Metrics:**
- Accuracy (overall correctness)
- Precision (of churn predictions, minimize false positives)
- Recall (catch actual churners, minimize false negatives)
- F1 Score (balance precision and recall)
- ROC-AUC (discrimination ability)

**Success Thresholds (Reiterated):**
- Accuracy: >75%
- Recall: >70% (catching churners is critical)
- Precision: >65% (avoid too many false alarms)
- ROC-AUC: >0.80

### Discussion and Feedback

**Alex:**
"This is exactly what we need. I particularly like the focus on interpretability with logistic regression. We need to be able to explain to the executive team WHY customers churn, not just predict it. Make sure feature importance is highlighted in the final report."

**Maya:**
"Love the RFM approach. That will give us actionable customer segments for marketing. Can we also look at time-to-churn by cohort? I want to know if recent signups churn faster than older customers."

**Jordan:**
"Absolutely. I'll add survival analysis to Phase 2. That will show us the churn hazard rate over customer lifetime."

### Approved with Enhancements

✅ **Core Framework Approved**
✅ **Add:** Survival analysis (time-to-churn)
✅ **Add:** Feature importance visualization for all models
✅ **Add:** Cost-benefit analysis (revenue at risk vs. retention campaign cost)

### Next Steps

- Jordan to proceed with statistical analysis
- Maya to support with visualization
- Agent to assist with feature engineering code
- Checkpoint: March 10 to review initial findings

---

## Mid-Project Check-in - 2025-03-10

**Date:** Monday, March 10, 2025
**Time:** 10:00 AM - 11:00 AM PST
**Location:** Zoom

### Attendees
- Alex Chen, Maya Rodriguez, Jordan Kim, Sam Park, Agent

### Progress Update

**Maya:**
- Exploratory analysis complete ✓
- Initial findings documented
- Visualizations ready for review
- Overall churn rate: 15.3% (up from 12% last quarter)
- Highest churn in Basic segment (22%), lowest in VIP (3%)
- Regional differences: West region has highest churn (18%)

**Jordan:**
- Statistical analysis 80% complete
- Correlation analysis done: recency is strongest predictor (ρ = -0.68)
- Spending amount moderately correlated (ρ = -0.42)
- RFM segmentation completed
- Working on predictive models

**Preliminary Insights:**
1. Recency is the strongest churn predictor (as expected)
2. Customers who stop browsing (not just buying) churn faster
3. Regional differences suggest local competition or service issues
4. VIP customers have very low churn but represent high revenue impact

### Risks and Blockers

**No major blockers identified.**

Minor issues:
- Some model iterations taking longer than expected
- Will prioritize simpler models if time constrained

**Mitigation:**
- Focus on logistic regression and random forest
- XGBoost is nice-to-have

### On Track for Delivery

All deliverables on track for March 14 deadline. Next checkpoint: March 12 for model review.

---

## Pre-Delivery Review - 2025-03-12

**Date:** Wednesday, March 12, 2025
**Time:** 3:00 PM - 4:30 PM PST
**Location:** Conference Room B

### Attendees
- Alex Chen, Maya Rodriguez, Jordan Kim, Agent

### Model Performance Review

**Jordan's Final Model Results:**

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|-------|----------|-----------|--------|-----|---------|
| Logistic Regression | 78.2% | 71.5% | 72.8% | 72.1% | 0.83 |
| Random Forest | 81.5% | 74.2% | 76.3% | 75.2% | 0.87 |
| XGBoost | 82.1% | 75.8% | 77.1% | 76.4% | 0.88 |

**All models exceed minimum thresholds! ✓**

**Top Predictive Features:**
1. Days since last transaction (recency)
2. Total transaction count (frequency)
3. Average order value (monetary)
4. Transaction count trend (last 30d vs 60d)
5. Customer segment

### Executive Report Status

**Maya:**
- Draft report 90% complete
- All visualizations ready
- Key findings summarized
- Recommendations drafted (pending final review)

### Recommendations Preview

**Top 5 Recommendations:**
1. **Early Warning System:** Implement monitoring for customers at 20+ days inactive
2. **Segmented Retention:** Different strategies for VIP, Premium, Standard, Basic
3. **Win-back Campaign:** Target recently churned (30-60 days) with special offers
4. **Regional Investigation:** Deep dive into West region to understand drivers
5. **Product Engagement:** Increase touchpoints beyond transactions (content, community)

**Cost-Benefit Analysis:**
- Revenue at risk (churned customers): $2.3M annually
- Estimated retention campaign cost: $150K
- If campaign reactivates 20% of at-risk customers: $460K recovered revenue
- ROI: 207%

**Alex's Reaction:**
"Excellent work. These recommendations are actionable and the ROI case is compelling. Let's make sure the executive presentation focuses on the business impact, not the technical details. Save the model performance for the appendix."

### Final Deliverables Checklist

- [x] Executive summary slides (PowerPoint)
- [x] Technical report (Markdown/PDF)
- [x] Churn prediction model (pickle file)
- [x] Data pipeline code (Python scripts)
- [x] Recommendations document
- [x] Data dictionary
- [ ] Final presentation rehearsal (March 14)

### Next Steps

- Maya to finalize report by EOD March 13
- Alex and Maya to prepare executive presentation March 14
- Executive presentation scheduled March 15 at 2:00 PM

**Meeting Adjourned - Project on track for successful delivery! 🎉**

---

**End of Meeting Notes**
