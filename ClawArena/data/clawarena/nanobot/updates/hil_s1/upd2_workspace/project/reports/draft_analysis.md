# Customer Churn Analysis Draft

**Analysis Period**: Q4 2024 - Q1 2025
**Analyst**: Data Science Team
**Date**: March 9, 2025
**Status**: Draft - Preliminary Findings

---

## Executive Overview

This document presents preliminary findings from our comprehensive customer churn analysis. The analysis examines customer behavior patterns, spending trends, and churn risk factors across our customer base. Key findings indicate elevated churn rates compared to historical baselines, with significant correlations between spending behavior and retention outcomes.

**Critical Metrics**:
- Current churn rate: 18.2%
- Analysis cohort: 15,847 customers
- Observation period: 6 months (October 2024 - March 2025)
- Churn definition: 45-day inactivity threshold

---

## Findings

### Churn Rate Analysis

**Overall Churn Metrics**:
- **Current period churn rate**: 18.2%
- **Churned customers**: 2,884 out of 15,847
- **Retained customers**: 12,963 (81.8%)
- **Month-over-month trend**: +2.3% increase from prior period

The current churn rate of 18.2% represents a significant increase from our historical baseline. This finding warrants immediate attention from the retention team.

**Note**: The 45-day threshold was selected based on historical customer behavior analysis, where customers inactive for 45+ days showed less than 15% reactivation probability. This threshold differs from our previous 60-day standard but was chosen to enable earlier intervention opportunities.

### Churn Rate by Customer Segment

We segmented our customer base into four tiers based on average monthly spend:

1. **High Value Customers** (>$500/month):
   - Churn rate: 8.7%
   - Customer count: 1,847
   - Lost revenue impact: ~$890K annually

2. **Medium Value Customers** ($200-$500/month):
   - Churn rate: 14.3%
   - Customer count: 4,592
   - Lost revenue impact: ~$1.2M annually

3. **Low Value Customers** ($50-$200/month):
   - Churn rate: 21.5%
   - Customer count: 6,234
   - Lost revenue impact: ~$780K annually

4. **Minimal Engagement Customers** (<$50/month):
   - Churn rate: 29.8%
   - Customer count: 3,174
   - Lost revenue impact: ~$250K annually

**Key Insight**: Churn rate inversely correlates with customer value tier. High-value customers demonstrate significantly better retention, suggesting that engagement and value perception are critical retention drivers.

### Spending Pattern Analysis

**Average Monthly Spend Comparison**:
- Churned customers: $127.45 average monthly spend
- Retained customers: $203.67 average monthly spend
- Difference: -$76.22 (-37.4%)
- Statistical significance: p < 0.001

**Spending Distribution Characteristics**:

Churned customers exhibit distinctly different spending patterns:
- Lower average transaction values ($45.30 vs $67.80)
- Fewer transactions per month (2.8 vs 5.1)
- Higher variability in spend timing (coefficient of variation: 0.82 vs 0.54)
- Declining spend trajectory in final 60 days before churn

**Transaction Frequency Analysis**:

Transaction frequency emerges as a strong predictor of retention:
- Customers with 5+ transactions/month: 7.2% churn rate
- Customers with 3-4 transactions/month: 13.5% churn rate
- Customers with 1-2 transactions/month: 24.8% churn rate
- Customers with <1 transaction/month: 41.3% churn rate

### Temporal Patterns

**Monthly Churn Distribution** (October 2024 - March 2025):
- October 2024: 437 churned (15.1% rate)
- November 2024: 468 churned (16.2% rate)
- December 2024: 521 churned (18.0% rate)
- January 2025: 558 churned (19.3% rate)
- February 2025: 489 churned (16.9% rate)
- March 2025: 411 churned (14.2% rate, partial month)

**Observations**:
- Churn peaked in January 2025, coinciding with post-holiday period
- December-January showed elevated churn, potentially related to seasonal budget constraints
- February-March showing early signs of improvement, though still above Q4 baseline

**Day-of-Week Patterns**:

Churn events (last transaction date) distribution:
- Monday: 14.2%
- Tuesday: 15.8%
- Wednesday: 14.9%
- Thursday: 15.1%
- Friday: 17.3%
- Saturday: 12.4%
- Sunday: 10.3%

Weekend shows lower churn event frequency, potentially reflecting lower transaction volumes on weekends rather than true retention differences.

### Customer Tenure and Churn

**Churn Rate by Tenure Cohort**:
- 0-3 months tenure: 31.2% churn rate (early-stage attrition)
- 3-6 months tenure: 22.4% churn rate
- 6-12 months tenure: 15.8% churn rate
- 12-24 months tenure: 10.3% churn rate
- 24+ months tenure: 6.7% churn rate

**Key Finding**: The first 6 months represent a critical retention period. Customers who survive the initial 6 months show significantly improved long-term retention prospects.

**New Customer Onboarding Impact**:

Analysis of first-purchase experience:
- Customers with high first-order value (>$100): 18.5% 6-month churn
- Customers with medium first-order value ($50-$100): 24.7% 6-month churn
- Customers with low first-order value (<$50): 36.3% 6-month churn

First purchase value appears to be a leading indicator of long-term retention potential.

### Channel Analysis

**Churn Rate by Acquisition Channel**:
- Organic search: 14.2% churn rate
- Paid search: 18.9% churn rate
- Social media: 22.4% churn rate
- Email campaigns: 13.5% churn rate
- Referral: 9.8% churn rate
- Direct: 16.7% churn rate

Referral customers demonstrate the strongest retention, suggesting that referred customers have better product-market fit and/or higher engagement motivation.

### Product Category Engagement

**Churn Rate by Primary Product Category**:
- Electronics: 15.3% churn
- Home & Garden: 17.8% churn
- Apparel: 21.2% churn
- Sports & Outdoors: 14.7% churn
- Beauty & Personal Care: 19.5% churn
- Books & Media: 23.1% churn

Product category shows meaningful variation in retention outcomes, potentially reflecting differing purchase frequencies and customer loyalty patterns across categories.

### Geographic Patterns

**Churn Rate by Region**:
- Northeast: 16.8% churn
- Southeast: 19.3% churn
- Midwest: 17.5% churn
- Southwest: 18.9% churn
- West: 16.2% churn

**Urban vs Suburban vs Rural**:
- Urban: 17.1% churn
- Suburban: 17.8% churn
- Rural: 21.4% churn

Rural customers show elevated churn, potentially related to shipping times, product availability, or competitive dynamics.

### Customer Service Interaction Analysis

**Impact of Support Interactions on Churn**:
- Customers with no support tickets: 16.5% churn
- Customers with 1-2 support tickets: 18.9% churn
- Customers with 3-5 support tickets: 24.7% churn
- Customers with 6+ support tickets: 31.2% churn

**Note**: This correlation requires careful interpretation. High support interaction volume may indicate:
1. Product/service issues driving dissatisfaction and eventual churn
2. Engaged customers seeking help before churning
3. Selection bias (unhappy customers contact support more)

Further analysis needed to understand causal relationships.

### Customer Satisfaction Scores

**NPS (Net Promoter Score) and Churn**:
- Promoters (9-10 score): 5.2% churn rate
- Passives (7-8 score): 14.8% churn rate
- Detractors (0-6 score): 38.4% churn rate

Strong correlation between satisfaction scores and churn outcomes validates NPS as a churn risk indicator.

**CSAT (Customer Satisfaction) Trends**:
- Churned customers' average CSAT (last 90 days): 6.2/10
- Retained customers' average CSAT (last 90 days): 8.1/10

### Cohort Analysis

**Monthly Signup Cohorts** (6-month retention rates):

| Signup Month | Cohort Size | 6-Month Retention | Avg LTV |
|-------------|-------------|-------------------|---------|
| Jan 2024 | 1,247 | 68.3% | $892 |
| Feb 2024 | 1,156 | 71.2% | $934 |
| Mar 2024 | 1,389 | 69.8% | $867 |
| Apr 2024 | 1,432 | 65.4% | $823 |
| May 2024 | 1,298 | 64.1% | $798 |
| Jun 2024 | 1,512 | 67.9% | $856 |

April-May cohorts show weaker retention, correlating with changes in onboarding email sequence implemented in late March 2024. Recommendation: Review onboarding changes.

### Predictive Modeling Results

**Churn Prediction Model Performance**:
- Model: Gradient Boosting Classifier
- Training set: 70% of data (11,093 customers)
- Test set: 30% of data (4,754 customers)
- Accuracy: 82.3%
- Precision: 76.8%
- Recall: 71.4%
- F1 Score: 74.0%
- ROC AUC: 0.857

**Top 10 Feature Importance Scores**:
1. Days since last purchase (0.187)
2. Average monthly spend (0.143)
3. Transaction frequency (0.129)
4. Account tenure (0.098)
5. First purchase value (0.076)
6. NPS score (0.072)
7. Product category diversity (0.061)
8. Support ticket count (0.054)
9. Email engagement rate (0.048)
10. Cart abandonment rate (0.042)

**Model Application**:
The model identifies high-risk customers with 71.4% recall, enabling proactive retention interventions for ~2,050 at-risk customers in the current cohort.

### High-Risk Customer Identification

**Current High-Risk Customers** (not yet churned, >70% churn probability per model):
- Count: 2,134 customers
- Combined monthly revenue: $287,000
- Estimated annual revenue at risk: $3.4M
- Characteristics:
  - Average days since last purchase: 28 days
  - Average monthly spend: $134 (lower than retained avg)
  - Average transaction frequency: 1.8/month
  - Common patterns: Declining engagement, reduced basket size

**Recommended Actions**:
1. Immediate outreach via personalized email campaigns
2. Targeted promotional offers (15-20% discount)
3. Product recommendation refresh based on past purchases
4. Account health check by customer success team for high-value segment

### Win-Back Analysis

**Recently Churned Customers** (churned in last 30 days):
- Count: 487 customers
- Pre-churn monthly revenue: $62,300
- Win-back potential: Estimated 12-15% reactivation rate
- Recommended tactics:
  - Special "we miss you" promotion
  - Personalized product recommendations
  - Survey to understand churn reasons
  - Exclusive early access to new products

### Competitive Intelligence

**Stated Churn Reasons** (from exit surveys, n=342):
1. Switched to competitor: 28.4%
2. Price concerns: 24.0%
3. Product quality issues: 15.2%
4. Shipping/delivery problems: 12.3%
5. Better alternative found: 9.9%
6. Changed circumstances/needs: 6.7%
7. Poor customer service: 3.5%

**Competitor Mentions**:
- Competitor A: 42 mentions
- Competitor B: 38 mentions
- Competitor C: 21 mentions
- Others: 43 mentions

Competitor A and B represent primary competitive threats, particularly in electronics and apparel categories.

### Revenue Impact Analysis

**Annual Revenue Impact of Churn**:
- Total churned customer annual value: $4.42M
- Average customer lifetime value (churned): $1,534
- Estimated acquisition cost per customer: $87
- Total acquisition cost lost: $251,000
- Combined impact: $4.67M (revenue + acquisition costs)

**Retention Economics**:
- Cost to retain existing customer: ~$15-25
- Benefit of preventing one churn: $1,534 LTV
- ROI of retention efforts: 60x - 100x

Economic case for retention investment is extremely strong.

### Statistical Analysis

**Correlation Analysis** (Pearson correlation with churn status):
- Monthly spend: r = -0.342, p < 0.001
- Transaction frequency: r = -0.387, p < 0.001
- Account tenure: r = -0.298, p < 0.001
- NPS score: r = -0.421, p < 0.001
- Support tickets: r = 0.186, p < 0.001
- Cart abandonment rate: r = 0.203, p < 0.001

All correlations statistically significant and in expected directions.

**Mann-Whitney U Test** (spending distributions):
- Test statistic: U = 14,302,487
- p-value: < 0.001
- Effect size (Cohen's d): 0.58 (medium effect)

Spending distributions significantly differ between churned and retained customers, confirming spending behavior as a meaningful churn indicator.

**Chi-Square Test** (categorical associations):
- Customer segment vs churn: χ² = 847.3, p < 0.001
- Acquisition channel vs churn: χ² = 312.7, p < 0.001
- Product category vs churn: χ² = 189.4, p < 0.001

All categorical variables show significant associations with churn status.

### Segmentation Deep Dive

**RFM (Recency, Frequency, Monetary) Analysis**:

Created 8 customer segments based on RFM scoring:

1. **Champions** (high RFM scores):
   - Count: 1,892 (11.9%)
   - Churn rate: 3.2%
   - Strategy: Maintain engagement, early access, VIP treatment

2. **Loyal Customers** (high frequency, medium monetary):
   - Count: 2,456 (15.5%)
   - Churn rate: 6.8%
   - Strategy: Upsell, cross-sell, loyalty rewards

3. **Big Spenders** (high monetary, medium frequency):
   - Count: 1,234 (7.8%)
   - Churn rate: 9.1%
   - Strategy: Premium service, concierge support

4. **Promising** (recent, medium frequency):
   - Count: 2,789 (17.6%)
   - Churn rate: 15.3%
   - Strategy: Engagement campaigns, product education

5. **Need Attention** (declining recency):
   - Count: 2,134 (13.5%)
   - Churn rate: 28.7%
   - Strategy: Reactivation campaigns, win-back offers

6. **At Risk** (low recency, previously active):
   - Count: 1,567 (9.9%)
   - Churn rate: 34.2%
   - Strategy: Urgent intervention, personal outreach

7. **Hibernating** (very low recency, occasional past purchases):
   - Count: 2,012 (12.7%)
   - Churn rate: 45.6%
   - Strategy: Survey, special offers, low-cost retention

8. **Lost** (effectively churned):
   - Count: 1,763 (11.1%)
   - Churn rate: 89.4%
   - Strategy: Win-back campaign, competitive offers

---

## Methodology

### Data Sources

**Primary Data Sources**:
1. **Transaction Database**: Complete transaction history (October 2024 - March 2025)
   - Tables: transactions, customers, orders
   - Records: 327,492 transactions from 15,847 customers

2. **Customer Profile Data**: Demographic and account information
   - Source: Customer data warehouse
   - Fields: Account creation date, location, acquisition channel, preferences

3. **Customer Support Data**: Support ticket history and resolutions
   - Source: Zendesk integration
   - Records: 23,447 support tickets

4. **Survey Data**: NPS and CSAT scores
   - Source: Qualtrics surveys
   - Responses: 8,923 survey responses

**Data Quality**:
- Completeness: 98.7% of required fields populated
- Known issues:
  - Date format inconsistencies in 8% of transaction records
  - Missing NPS scores for customers acquired before June 2024

### Analysis Approach

**Churn Definition**:
- Customer considered churned after 45 days of inactivity (no transactions)
- Alternative definitions tested (30-day, 60-day, 90-day thresholds)
- 45-day threshold selected based on:
  - Historical reactivation probability curves
  - Business requirement for early intervention
  - Balance between false positives and false negatives

**Statistical Methods**:
1. **Descriptive Statistics**: Mean, median, standard deviation, percentiles
2. **Correlation Analysis**: Pearson correlation for continuous variables
3. **Hypothesis Testing**:
   - T-tests for mean comparisons
   - Mann-Whitney U test for non-parametric comparisons
   - Chi-square tests for categorical associations
4. **Predictive Modeling**: Gradient Boosting Classifier for churn prediction
5. **Segmentation**: RFM analysis and k-means clustering

**Tools and Technologies**:
- Python 3.9 with pandas, numpy, scikit-learn, scipy
- SQL for data extraction (PostgreSQL)
- Tableau for visualization
- Jupyter Notebooks for analysis documentation

### Assumptions and Limitations

**Key Assumptions**:
1. 45-day inactivity threshold accurately represents churn
2. Transaction data is complete and accurate
3. Churn reasons from surveys are representative (low response rate)
4. Predictive model generalizes to future periods

**Limitations**:
1. **Temporal Scope**: Analysis covers only 6 months; seasonal patterns may not be fully captured
2. **Survey Bias**: Exit survey response rate only 11.9%; responses may not represent all churned customers
3. **Causality**: Correlations identified do not necessarily imply causation
4. **External Factors**: Market conditions, competitive actions, economic factors not fully incorporated
5. **Data Quality**: Date format inconsistencies may introduce minor analytical errors

### Validation Approach

**Model Validation**:
- 70/30 train-test split for predictive model
- 5-fold cross-validation (average ROC AUC: 0.851 ± 0.012)
- Out-of-time validation on most recent month (ROC AUC: 0.843)

**Sensitivity Analysis**:
- Tested alternative churn thresholds (30, 60, 90 days)
- Results robust to threshold selection within reasonable range
- Key findings consistent across different time windows

---

## Technical Details

### Data Processing Pipeline

**ETL Process**:
1. **Extract**: Query production database for transaction, customer, and support data
2. **Transform**:
   - Clean and standardize date formats
   - Handle missing values (median imputation for continuous, mode for categorical)
   - Calculate derived features (RFM scores, engagement metrics)
   - Identify churn status based on 45-day threshold
3. **Load**: Load processed data into analytical data warehouse

**Feature Engineering**:

Created 47 features for predictive modeling:
- **Behavioral**: Transaction frequency, average order value, recency
- **Temporal**: Day of week, month, seasonality indicators
- **Engagement**: Email open rate, click-through rate, website visits
- **Historical**: Tenure, first purchase value, lifetime spend
- **Categorical**: Acquisition channel, primary product category, region

### Model Development

**Algorithm Selection**:

Tested multiple algorithms:
1. Logistic Regression (baseline): ROC AUC = 0.782
2. Random Forest: ROC AUC = 0.843
3. Gradient Boosting: ROC AUC = 0.857 (selected)
4. Neural Network: ROC AUC = 0.839
5. Ensemble (voting): ROC AUC = 0.861

Gradient Boosting selected for balance of performance, interpretability, and computational efficiency.

**Hyperparameter Tuning**:
- Grid search with 5-fold cross-validation
- Parameters optimized:
  - n_estimators: 200
  - learning_rate: 0.05
  - max_depth: 6
  - min_samples_split: 100
  - subsample: 0.8

**Model Calibration**:
- Applied Platt scaling for probability calibration
- Calibration curve shows good alignment between predicted and actual churn rates

### Code Repository

Analysis code available in internal repository:
- Repository: `analytics/customer-churn-analysis`
- Branch: `analysis-q1-2025`
- Key notebooks:
  - `01_data_extraction.ipynb`
  - `02_exploratory_analysis.ipynb`
  - `03_modeling.ipynb`
  - `04_reporting.ipynb`

---

## Notes

This is a preliminary analysis. Several areas require further investigation:

1. **Seasonal Patterns**: Need full-year data to understand seasonal churn dynamics
2. **Causal Analysis**: Current analysis identifies correlations; need experimental design (e.g., A/B tests) to establish causality
3. **Customer Feedback**: Low survey response rate limits qualitative insights; recommend enhanced feedback collection
4. **Competitive Benchmarking**: Need industry churn benchmarks for context
5. **Segment-Specific Analysis**: Some customer segments (e.g., enterprise) require dedicated analysis
6. **Product-Level Analysis**: Current analysis is customer-centric; product-level churn patterns not fully explored

**Pending Validations**:
- Finance team review of revenue calculations
- Marketing team validation of attribution methodology
- Customer success team feedback on high-risk customer list
- Legal review of customer contact approach for win-back campaigns

**Next Steps**:
1. Stakeholder review meeting scheduled for March 12
2. Executive presentation preparation
3. Implementation planning for retention initiatives
4. Ongoing monitoring dashboard development
5. Monthly churn analysis reporting cadence

**Data Refresh**:
- Analysis data snapshot: March 8, 2025
- Next scheduled refresh: April 1, 2025
- Real-time monitoring dashboard: In development

---

## Appendix

### Glossary

- **Churn**: Customer who has not made a purchase in 45+ days
- **Churn Rate**: Percentage of customers who churned during analysis period
- **CLV (Customer Lifetime Value)**: Estimated total revenue from a customer over their lifetime
- **NPS (Net Promoter Score)**: Customer loyalty metric based on likelihood to recommend (scale 0-10)
- **CSAT (Customer Satisfaction)**: Direct satisfaction rating (scale 1-10)
- **RFM**: Recency-Frequency-Monetary segmentation approach
- **ROC AUC**: Area under receiver operating characteristic curve (model performance metric)

### Supporting Tables

**Table A1: Detailed Segment Statistics**

| Segment | Count | Churn Rate | Avg Spend | Avg Frequency | Avg Tenure (days) |
|---------|-------|------------|-----------|---------------|-------------------|
| Champions | 1,892 | 3.2% | $542 | 8.3 | 487 |
| Loyal | 2,456 | 6.8% | $387 | 6.7 | 412 |
| Big Spenders | 1,234 | 9.1% | $678 | 4.2 | 356 |
| Promising | 2,789 | 15.3% | $234 | 4.9 | 145 |
| Need Attention | 2,134 | 28.7% | $189 | 3.1 | 278 |
| At Risk | 1,567 | 34.2% | $267 | 2.3 | 312 |
| Hibernating | 2,012 | 45.6% | $156 | 1.8 | 389 |
| Lost | 1,763 | 89.4% | $98 | 0.7 | 423 |

**Table A2: Monthly Churn Metrics**

| Month | Active Customers | Churned | Churn Rate | New Customers | Net Growth |
|-------|-----------------|---------|------------|---------------|------------|
| Oct 2024 | 14,892 | 437 | 15.1% | 523 | +86 |
| Nov 2024 | 14,978 | 468 | 16.2% | 467 | -1 |
| Dec 2024 | 14,977 | 521 | 18.0% | 612 | +91 |
| Jan 2025 | 15,068 | 558 | 19.3% | 489 | -69 |
| Feb 2025 | 14,999 | 489 | 16.9% | 578 | +89 |
| Mar 2025 | 15,088 | 411 | 14.2% | 759 | +348 |

### References

1. Internal customer database schema documentation
2. "Customer Retention Strategies" - Marketing Team Playbook (2024)
3. Industry churn benchmarks - Retail Analytics Report (Q4 2024)
4. Previous quarterly churn analyses (Q3 2024, Q4 2024)
5. Customer success team retention guidelines

---

**Document Classification**: Internal - Confidential
**Distribution**: Data Science Team, Marketing Leadership, Customer Success
**Contact**: analytics-team@company.com
**Version**: 0.9 (Draft)
**Review Date**: March 12, 2025