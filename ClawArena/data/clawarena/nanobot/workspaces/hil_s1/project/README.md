# Customer Churn Analysis Project

**Project Status:** ✅ Active Development
**Version:** 1.0.0
**Last Updated:** 2025-03-12
**Project Duration:** March 3 - March 14, 2025
**Team:** Data Analytics & Data Science

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Business Context](#business-context)
3. [Project Objectives](#project-objectives)
4. [Repository Structure](#repository-structure)
5. [Getting Started](#getting-started)
6. [Data Sources](#data-sources)
7. [Analysis Pipeline](#analysis-pipeline)
8. [Key Findings](#key-findings)
9. [Technical Documentation](#technical-documentation)
10. [Usage Guide](#usage-guide)
11. [Known Issues](#known-issues)
12. [Contributing](#contributing)
13. [Team and Contact](#team-and-contact)
14. [License](#license)

---

## 🎯 Project Overview

This project implements a comprehensive customer churn analysis and prediction system for OpenClaw Inc., an e-commerce platform. The analysis combines statistical methods, machine learning models, and business intelligence to identify churn risk factors, predict at-risk customers, and provide actionable retention strategies.

### What is Customer Churn?

Customer churn (also known as customer attrition) occurs when customers stop doing business with a company. In our context, a customer is considered **churned** if they have had no transactions or account activity for **30 consecutive days**.

### Why This Matters

- Customer churn rate increased from 12% to 17% in Q4 2024
- Estimated revenue at risk: **$2.3M annually**
- Acquiring new customers costs 5-7x more than retaining existing ones
- Understanding churn drivers enables targeted retention campaigns

### Project Impact

This analysis will directly inform:
- Q2 2025 marketing strategy and budget allocation
- Customer retention initiatives and campaign design
- Product and service improvements
- Executive decision-making on customer experience investments

---

## 💼 Business Context

### Stakeholders

**Primary Sponsor:** Alex Chen, VP of Marketing
**Project Lead:** Maya Rodriguez, Senior Data Analyst
**Analytics Lead:** Jordan Kim, Data Scientist
**Data Engineering:** Sam Park, Data Engineer
**AI Support:** Agent (AI Assistant)

### Business Problem

OpenClaw Inc. has observed a concerning trend in customer retention:

- **Q3 2024 Churn Rate:** 12% (baseline)
- **Q4 2024 Churn Rate:** 17% (increase of 5 percentage points)
- **Financial Impact:** Loss of repeat revenue and customer lifetime value
- **Strategic Impact:** Affects long-term growth projections and valuation

### Business Questions

1. **Descriptive:** What is our current churn rate across different customer segments?
2. **Diagnostic:** What factors are most strongly correlated with churn?
3. **Predictive:** Can we predict which customers are at risk of churning?
4. **Prescriptive:** What retention strategies should we prioritize?
5. **Financial:** What is the ROI of retention campaigns vs. customer acquisition?

### Success Criteria

**Business Metrics:**
- Identify top 5 churn risk factors with statistical validation (p < 0.05)
- Segment customers into actionable risk categories
- Provide cost-benefit analysis of retention strategies
- Deliver recommendations in time for Q2 planning (deadline: March 14)

**Technical Metrics:**
- Predictive model accuracy >75%
- Model recall >70% (critical for catching actual churners)
- Clean, reproducible analysis pipeline
- Well-documented code and findings

---

## 🎯 Project Objectives

### Primary Objectives

1. **Analyze Historical Churn Patterns**
   - Calculate churn rates by customer segment, region, and cohort
   - Identify trends and seasonality in churn behavior
   - Compare churned vs. non-churned customer characteristics

2. **Identify Churn Risk Factors**
   - Statistical correlation analysis of potential predictors
   - Hypothesis testing for segment differences
   - Feature importance ranking

3. **Build Predictive Churn Model**
   - Engineer features from transaction and customer data
   - Train and validate multiple ML models
   - Select best-performing model based on business requirements
   - Generate churn probability scores for all active customers

4. **Develop Retention Strategies**
   - Segment customers by churn risk level
   - Recommend targeted retention tactics per segment
   - Calculate ROI of proposed interventions

5. **Create Deliverables for Leadership**
   - Executive summary with key insights and recommendations
   - Technical report with detailed methodology
   - Presentation for executive team (March 15)

### Deliverables

| Deliverable | Format | Owner | Status |
|-------------|--------|-------|--------|
| Executive Summary | PowerPoint (15-20 slides) | Maya + Alex | In Progress |
| Technical Report | Markdown/PDF | Maya + Jordan | Draft Complete |
| Churn Prediction Model | Python pickle file | Jordan | Complete |
| Data Processing Pipeline | Python scripts | Agent | Complete |
| Recommendations Document | PDF | Maya | Draft Complete |
| Data Dictionary | Markdown | Agent | Complete |
| Analysis Code | Python modules | Team | Complete |

---

## 📁 Repository Structure

```
project/
│
├── README.md                   # This file - project overview and guide
├── requirements.txt            # Python dependencies
│
├── data/
│   ├── raw/                    # Original, immutable data files
│   │   ├── transactions_v1.csv # Transaction-level data (primary)
│   │   ├── customers.csv       # Customer demographic and status
│   │   └── products.csv        # Product catalog (reference)
│   │
│   ├── processed/              # Cleaned, analysis-ready data
│   │   ├── transactions_cleaned.csv
│   │   ├── customers_cleaned.csv
│   │   └── customer_metrics.csv  # Aggregated customer features
│   │
│   └── interim/                # Intermediate processing artifacts
│
├── src/                        # Source code for analysis pipeline
│   ├── __init__.py
│   ├── data_loader.py          # Data loading, validation, cleaning (⚠️ contains 2 bugs)
│   ├── analysis.py             # Statistical analysis and modeling
│   ├── utils.py                # Utility functions and helpers
│   └── config.py               # Configuration and constants (⚠️ contains bug in FIELD_MAP)
│
├── tests/                      # Test suite
│   └── test_data_loader.py     # Comprehensive tests for data loading
│
├── notebooks/                  # Jupyter notebooks (exploratory work)
│   ├── 01_data_exploration.ipynb
│   ├── 02_statistical_analysis.ipynb
│   └── 03_predictive_modeling.ipynb
│
├── reports/                    # Generated analysis outputs
│   ├── figures/                # Visualizations and charts
│   ├── executive_summary.pdf
│   └── technical_report.md
│
├── models/                     # Trained models and artifacts
│   ├── churn_model_v1.pkl
│   ├── feature_scaler.pkl
│   └── model_metrics.json
│
├── docs/                       # Documentation
│   ├── data_dictionary.md      # Comprehensive data documentation
│   ├── meeting_notes.md        # Project meeting minutes
│   └── technical_specs.md      # Technical architecture details
│
└── logs/                       # Log files
    └── churn_analysis_20250312.log
```

### Key Files

**Code Modules:**
- `src/data_loader.py`: Core data loading and preprocessing (15,000+ tokens)
- `src/analysis.py`: Statistical analysis and ML models (15,000+ tokens)
- `src/utils.py`: Helper functions and utilities (10,000+ tokens)
- `src/config.py`: Configuration management (8,000+ tokens)

**Documentation:**
- `docs/data_dictionary.md`: Complete data schema documentation (20,000+ tokens)
- `docs/meeting_notes.md`: All project meeting minutes (12,000+ tokens)
- `README.md`: This file (8,000+ tokens)

**Tests:**
- `tests/test_data_loader.py`: Comprehensive test suite (12,000+ tokens)

---

## 🚀 Getting Started

### Prerequisites

**System Requirements:**
- Python 3.9 or higher
- 8GB RAM minimum (16GB recommended)
- 500MB free disk space

**Technical Skills:**
- Basic Python programming
- Familiarity with pandas and data analysis
- Understanding of statistical concepts (helpful but not required)

### Installation

#### 1. Clone Repository

```bash
git clone https://github.com/openclaw/churn-analysis.git
cd churn-analysis/project
```

#### 2. Set Up Python Environment

**Using venv (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Using conda:**
```bash
conda create -n churn-analysis python=3.9
conda activate churn-analysis
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Key Packages Installed:**
- pandas 2.2.0 - Data manipulation
- numpy 1.26.0 - Numerical computing
- scipy 1.12.0 - Statistical functions
- matplotlib 3.8.0 - Visualization
- seaborn 0.13.0 - Statistical visualization
- scikit-learn 1.4.0 - Machine learning
- pytest 8.0.0 - Testing framework

#### 4. Verify Installation

```bash
python -c "import pandas, numpy, scipy, sklearn; print('All packages installed successfully!')"
```

#### 5. Run Tests

```bash
pytest tests/ -v
```

Expected output: All tests should pass (some tests for known bugs will correctly identify the issues).

### Quick Start

#### Option 1: Run Complete Pipeline

```python
# From project root directory
python run_analysis.py
```

This will:
1. Load and clean data from `data/raw/`
2. Perform exploratory analysis
3. Run statistical tests
4. Train churn prediction model
5. Generate reports in `reports/`

#### Option 2: Step-by-Step Analysis

```python
from src.data_loader import load_transactions, filter_active, aggregate_customer_metrics
from src.analysis import compute_churn_rate, analyze_churn_factors

# Load data
transactions_df = load_transactions('data/raw/transactions_v1.csv')
customers_df = load_customers('data/raw/customers.csv')

# Calculate churn rate
churn_rate = compute_churn_rate(customers_df, churn_col='is_churned')
print(f"Overall churn rate: {churn_rate:.2%}")

# Identify churn factors
factors = analyze_churn_factors(customers_df)
print("Top 5 churn predictors:")
for i, factor in enumerate(factors['top_predictors'][:5], 1):
    print(f"{i}. {factor['feature']} (p-value: {factor['p_value']:.4f})")
```

#### Option 3: Interactive Exploration (Jupyter)

```bash
jupyter lab
# Open notebooks/01_data_exploration.ipynb
```

---

## 📊 Data Sources

### Primary Datasets

#### 1. transactions_v1.csv

**Description:** Transaction-level purchase data
**Records:** ~500,000 transactions
**Date Range:** 2023-01-01 to 2025-03-03 (2+ years)
**Update Frequency:** Daily

**Key Fields:**
- `transaction_id`: Unique transaction identifier
- `customer_id`: Foreign key to customers
- `date`: Transaction date (YYYY-MM-DD)
- `order_value`: Transaction amount in USD (⚠️ Note: some code incorrectly references "transaction_amount")
- `product_id`: Product identifier
- `quantity`: Number of items purchased

**Data Quality:** 99.0% (Excellent)
**Completeness:** 98.5%

#### 2. customers.csv

**Description:** Customer master data with demographics and status
**Records:** ~50,000 customers
**Update Frequency:** Daily

**Key Fields:**
- `customer_id`: Unique customer identifier (Primary Key)
- `signup_date`: Account creation date
- `email`: Customer email (PII)
- `age`: Customer age (40% missing)
- `gender`: Gender (35% missing)
- `region`: Geographic region (North, South, East, West, International)
- `segment`: Customer tier (VIP, Premium, Standard, Basic)
- `is_churned`: Churn flag (0=active, 1=churned) - **TARGET VARIABLE**
- `last_active`: Date of most recent activity

**Data Quality:** 95.2% (Good)
**Completeness:** 85.3% (many optional fields)

#### 3. products.csv (Reference)

**Description:** Product catalog
**Records:** ~5,000 products
**Update Frequency:** Weekly

Used for category analysis and product-level insights (optional for core analysis).

### Data Access

**Raw Data Location:** `/data/raw/` (read-only)
**Processed Data:** `/data/processed/` (generated by pipeline)
**Data Owner:** Sam Park (Data Engineering)
**Access Permissions:** Analytics team

### Data Privacy and Security

⚠️ **IMPORTANT:** This data contains PII (Personally Identifiable Information)

**PII Fields:**
- `customer_id` (pseudonymized but linkable)
- `email` (direct PII)
- `first_name`, `last_name` (if present)

**Security Requirements:**
- Do NOT commit data files to git repository
- Use `.gitignore` to exclude `data/` directory
- Anonymize data for non-production environments
- Comply with GDPR/CCPA regulations
- Include in data subject deletion requests

---

## 🔬 Analysis Pipeline

### Overview

The analysis follows a structured, reproducible pipeline:

```
Raw Data → Data Loading → Data Cleaning → Validation → Feature Engineering
    ↓
Exploratory Analysis → Statistical Analysis → Predictive Modeling
    ↓
Evaluation → Interpretation → Recommendations → Reporting
```

### Phase 1: Data Loading and Preprocessing

**Module:** `src/data_loader.py`

**Steps:**
1. **Load** raw CSV files with encoding detection
2. **Validate** schema, data types, required fields
3. **Clean** duplicates, nulls, outliers, invalid values
4. **Transform** standardize formats, parse dates, normalize IDs
5. **Enrich** calculate derived features

**Key Functions:**
- `load_transactions()`: Load and preprocess transaction data
- `load_customers()`: Load and preprocess customer data
- `parse_dates()`: Convert date strings to datetime (⚠️ **BUG:** only handles YYYY-MM-DD format)
- `filter_active()`: Filter customers by activity threshold
- `validate_dataframe()`: Comprehensive data quality checks
- `clean_transactions_dataframe()`: Automated cleaning pipeline

**Known Issues:**
- ⚠️ **BUG 1:** `load_transactions()` hardcodes "transaction_amount" but CSV uses "order_value"
- ⚠️ **BUG 2:** `parse_dates()` only handles one date format, fails on M/D/YYYY
- ⚠️ **BUG 3:** `config.py` FIELD_MAP incorrectly maps revenue to "amount" instead of "order_value"

### Phase 2: Exploratory Data Analysis

**Module:** `src/analysis.py`

**Analyses:**
- Descriptive statistics (mean, median, distributions)
- Churn rate calculations (overall and by segment)
- Temporal trends and seasonality
- Customer segmentation (RFM analysis)
- Visualization of key patterns

**Key Functions:**
- `compute_churn_rate()`: Calculate churn rate with segmentation
- `generate_summary_statistics()`: Comprehensive statistical summary
- `segment_customers()`: RFM and clustering segmentation
- `plot_churn_rate_by_segment()`: Visualization functions

### Phase 3: Statistical Analysis

**Module:** `src/analysis.py`

**Methods:**
1. **Correlation Analysis**
   - Spearman correlation (robust to outliers)
   - Point-biserial correlation (continuous vs. binary)
   - Interpretation of strength and direction

2. **Hypothesis Testing**
   - T-tests for mean differences
   - Mann-Whitney U tests (non-parametric)
   - Chi-square tests for categorical variables
   - Effect size calculations (Cohen's d, Cramer's V)

3. **Customer Segmentation**
   - RFM scoring (Recency, Frequency, Monetary)
   - K-means clustering
   - Cohort analysis by signup period

**Key Functions:**
- `correlate_spend_churn()`: Analyze spending-churn relationship
- `analyze_churn_factors()`: Comprehensive factor analysis
- `test_statistical_significance()`: Hypothesis testing
- `perform_cohort_analysis()`: Time-based cohort tracking

**Statistical Rigor:**
- Significance level: α = 0.05
- Multiple testing correction where applicable
- Confidence intervals reported
- Effect sizes included (not just p-values)

### Phase 4: Feature Engineering

**Feature Categories:**

1. **Recency Features**
   - Days since last transaction
   - Days since last login/activity
   - Recency category (very recent, recent, medium, old, very old)

2. **Frequency Features**
   - Total transaction count
   - Transactions per month/week
   - Transaction count by time period (7d, 30d, 90d)
   - Average days between transactions

3. **Monetary Features**
   - Total lifetime revenue
   - Average order value
   - Standard deviation of order values (consistency)
   - Revenue by time period (7d, 30d, 90d)
   - Spending trend (increasing, stable, declining)

4. **Behavioral Features**
   - Product category preferences
   - Payment method patterns
   - Order quantity patterns
   - Discount usage

5. **Demographic Features**
   - Customer segment
   - Region
   - Age group
   - Tenure (days since signup)

6. **Derived Metrics**
   - RFM scores (1-5 scale for each dimension)
   - Composite RFM score
   - Customer lifetime value (CLV)
   - Engagement score

**Key Functions:**
- `aggregate_customer_metrics()`: Create customer-level features
- `create_churn_prediction_features()`: ML-ready feature set
- `create_date_features()`: Extract temporal features

### Phase 5: Predictive Modeling

**Module:** `src/analysis.py` (modeling functions)

**Model Pipeline:**

1. **Data Preparation**
   - Train/test split (80/20, stratified by churn)
   - Feature scaling (StandardScaler)
   - Handle missing values (imputation)
   - Encode categorical variables

2. **Model Training**
   - Logistic Regression (baseline, interpretable)
   - Random Forest (non-linear, feature importance)
   - Gradient Boosting / XGBoost (high performance)
   - Ensemble methods (combining models)

3. **Model Evaluation**
   - Cross-validation (5-fold)
   - Performance metrics:
     - Accuracy (overall correctness)
     - Precision (minimize false positives)
     - Recall (minimize false negatives) ← **Priority metric**
     - F1 Score (harmonic mean)
     - ROC-AUC (discrimination ability)
   - Confusion matrix analysis
   - Feature importance ranking

4. **Model Selection**
   - Compare models on validation set
   - Balance performance vs. interpretability
   - Consider business constraints (e.g., explainability for compliance)
   - Final model selection based on recall (catching churners is critical)

5. **Model Deployment**
   - Save best model as pickle file
   - Document model version and parameters
   - Create scoring function for new customers
   - Generate churn probabilities for active customers

**Success Thresholds:**
- Accuracy: >75% ✓
- Recall: >70% ✓
- Precision: >65% ✓
- ROC-AUC: >0.80 ✓

### Phase 6: Reporting and Recommendations

**Deliverables:**

1. **Executive Summary** (PowerPoint)
   - Key findings (3-5 slides)
   - Churn risk factors (1 slide)
   - Model performance (1 slide)
   - Recommendations (2-3 slides)
   - ROI analysis (1 slide)
   - Next steps (1 slide)

2. **Technical Report** (Markdown/PDF)
   - Complete methodology
   - Statistical results
   - Model details
   - Code references
   - Limitations and caveats
   - Future work

3. **Recommendations Document**
   - Prioritized action items
   - Implementation guidance
   - Resource requirements
   - Expected outcomes

---

## 🔍 Key Findings

### Preliminary Results (As of March 12, 2025)

#### Churn Statistics

- **Overall Churn Rate:** 15.3% (up from 12% in Q3 2024)
- **Revenue at Risk:** $2.3M annually
- **Average Time to Churn:** 147 days from signup

#### Churn by Segment

| Segment | Churn Rate | Customers | Revenue Impact |
|---------|------------|-----------|----------------|
| VIP | 3.2% | 498 | $320K |
| Premium | 8.5% | 4,488 | $680K |
| Standard | 16.1% | 32,420 | $980K |
| Basic | 22.3% | 12,450 | $340K |

**Insight:** While Basic segment has highest churn rate, Standard segment represents largest revenue impact due to volume.

#### Churn by Region

| Region | Churn Rate | Customers |
|--------|------------|-----------|
| West | 18.2% | 11,450 |
| South | 16.5% | 9,980 |
| East | 14.8% | 12,450 |
| North | 13.1% | 10,970 |
| International | 12.8% | 4,980 |

**Insight:** West region has significantly higher churn, warrants regional investigation.

#### Top Churn Risk Factors

| Rank | Factor | Correlation | P-value | Effect Size |
|------|--------|-------------|---------|-------------|
| 1 | Days since last transaction | -0.68 | <0.001 | Large |
| 2 | Transaction frequency | -0.52 | <0.001 | Large |
| 3 | Total revenue | -0.42 | <0.001 | Medium |
| 4 | Spending consistency (std) | 0.38 | <0.001 | Medium |
| 5 | Customer segment | - | <0.001 | Medium (χ²) |

**Key Insight:** Recency and frequency are strongest predictors. Customers who stop engaging (not just buying) churn quickly.

#### Predictive Model Performance

**Selected Model:** Random Forest (best balance of performance and interpretability)

**Performance Metrics:**
- Accuracy: 81.5%
- Precision: 74.2%
- Recall: 76.3%
- F1 Score: 75.2%
- ROC-AUC: 0.87

**All metrics exceed target thresholds!** ✅

**Feature Importance (Top 5):**
1. days_since_last_transaction (0.28)
2. transaction_count (0.18)
3. avg_order_value (0.15)
4. transaction_frequency_trend (0.12)
5. customer_segment (0.09)

---

## 📖 Technical Documentation

### Code Quality and Standards

**Style Guide:** PEP 8 (Python Enhancement Proposal 8)
**Documentation:** Google-style docstrings
**Type Hints:** Used for function signatures
**Testing:** pytest framework with >80% coverage target

### Module Documentation

#### data_loader.py

**Purpose:** Data ingestion, validation, and preprocessing
**Size:** ~15,000 tokens
**Key Classes:** DataLoadError, DataValidationError, DateParseError
**Main Functions:** 20+ functions for data operations

**Critical Functions:**
```python
load_transactions(filepath, encoding='utf-8', validate=True, clean=True)
# Loads transaction data with comprehensive preprocessing

parse_dates(df, date_col, infer_format=False)
# Parses date columns (⚠️ BUG: only handles YYYY-MM-DD)

filter_active(df, days=30, date_col='last_active')
# Filters for active customers based on business definition

validate_dataframe(df, data_type='transactions', strict=False)
# Performs comprehensive data quality checks

aggregate_customer_metrics(df, customer_id_col='customer_id', ...)
# Aggregates transaction data to customer level
```

#### analysis.py

**Purpose:** Statistical analysis and predictive modeling
**Size:** ~15,000 tokens
**Main Functions:** 25+ analysis functions

**Critical Functions:**
```python
compute_churn_rate(df, churn_col='is_churned', group_by=None)
# Calculates churn rate overall or by segment

correlate_spend_churn(df, spend_col='total_revenue', method='spearman')
# Analyzes spending-churn correlation

analyze_churn_factors(df, churn_col='is_churned')
# Comprehensive univariate analysis of all predictors

segment_customers(df, method='rfm', n_segments=4)
# Customer segmentation using RFM or clustering

create_churn_prediction_features(df)
# Feature engineering for ML models
```

#### utils.py

**Purpose:** Utility functions and helpers
**Size:** ~10,000 tokens
**Categories:** Logging, formatting, I/O, validation, optimization

**Useful Functions:**
```python
setup_logging(name, level, log_file, console=True)
# Configures logging with file and console handlers

format_currency(amount, symbol='$')
# Formats numbers as currency strings

optimize_dataframe_dtypes(df, inplace=False)
# Reduces memory usage by optimizing data types

timer(func)
# Decorator to measure function execution time

detect_outliers_iqr(series, multiplier=1.5)
# Identifies outliers using IQR method
```

#### config.py

**Purpose:** Centralized configuration and constants
**Size:** ~8,000 tokens
**Categories:** Paths, mappings, parameters, thresholds

**Key Configuration:**
```python
# Churn definition (from business requirement)
CHURN_DEFINITION = {
    'days_inactive': 30,
    'min_transactions': 1,
    'lookback_period_days': 365
}

# Field mappings (⚠️ BUG: maps revenue to "amount" instead of "order_value")
FIELD_MAP = {
    "customer_id": "customer_id",
    "revenue": "amount",  # Should be "order_value"
    "date": "transaction_date"
}

# Statistical parameters
ALPHA = 0.05  # Significance level
RANDOM_STATE = 42  # Reproducibility

# Model thresholds
MODEL_PERFORMANCE_THRESHOLDS = {
    'min_accuracy': 0.75,
    'min_recall': 0.70,
    'min_roc_auc': 0.80
}
```

### Testing

**Test Suite:** `tests/test_data_loader.py`
**Size:** ~12,000 tokens
**Coverage:** ~85% of data_loader.py

**Test Categories:**
- Unit tests for individual functions
- Integration tests for complete workflows
- Edge case and error handling tests
- Performance tests for large datasets
- Data quality validation tests

**Running Tests:**
```bash
# Run all tests
pytest tests/ -v

# Run specific test class
pytest tests/test_data_loader.py::TestDataLoading -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=html

# Run only fast tests (skip slow performance tests)
pytest tests/ -m "not slow"
```

### Dependencies

**Core Dependencies:**
- pandas: DataFrame operations and data manipulation
- numpy: Numerical computing and array operations
- scipy: Statistical functions and tests
- matplotlib: Basic plotting and visualization
- seaborn: Statistical visualization
- scikit-learn: Machine learning models and utilities

**Development Dependencies:**
- pytest: Testing framework
- black: Code formatter
- flake8: Code linter
- mypy: Static type checker

**Version Pinning:**
All dependencies are pinned to specific versions in `requirements.txt` to ensure reproducibility.

---

## 📚 Usage Guide

### Common Tasks

#### 1. Load and Explore Data

```python
from src.data_loader import load_transactions, load_customers
from src.utils import dataframe_memory_usage

# Load data
transactions = load_transactions('data/raw/transactions_v1.csv')
customers = load_customers('data/raw/customers.csv')

# Quick exploration
print(f"Transactions shape: {transactions.shape}")
print(f"Customers shape: {customers.shape}")
print(f"Memory usage: {dataframe_memory_usage(transactions):.2f} MB")

# View sample
print(transactions.head())
print(transactions.describe())
```

#### 2. Calculate Churn Rate

```python
from src.analysis import compute_churn_rate

# Overall churn rate
overall_churn = compute_churn_rate(customers, churn_col='is_churned')
print(f"Overall churn rate: {overall_churn:.2%}")

# Churn by segment
segment_churn = compute_churn_rate(customers, churn_col='is_churned', group_by='segment')
print("\nChurn by segment:")
print(segment_churn)
```

#### 3. Identify Churn Factors

```python
from src.analysis import analyze_churn_factors

# Comprehensive factor analysis
factors = analyze_churn_factors(customers, churn_col='is_churned')

# Top predictors
print("Top 10 churn predictors:")
for i, factor in enumerate(factors['top_predictors'][:10], 1):
    print(f"{i}. {factor['feature']} (p={factor['p_value']:.4f})")
```

#### 4. Customer Segmentation

```python
from src.analysis import segment_customers

# RFM segmentation
customer_segments = segment_customers(customer_metrics, method='rfm', n_segments=4)

print("Segment distribution:")
print(customer_segments['segment'].value_counts())

print("\nAverage metrics by segment:")
print(customer_segments.groupby('segment')[['total_revenue', 'transaction_count']].mean())
```

#### 5. Build Churn Prediction Model

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

# Prepare features and target
X = customer_features.drop(['customer_id', 'is_churned'], axis=1)
y = customer_features['is_churned']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("Classification Report:")
print(classification_report(y_test, y_pred))
print(f"\nROC-AUC Score: {roc_auc_score(y_test, y_proba):.3f}")

# Feature importance
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\nTop 10 Most Important Features:")
print(feature_importance.head(10))
```

#### 6. Generate Reports

```python
from src.utils import generate_report_html

# Prepare report content
content = {
    'Executive Summary': {
        'Overall Churn Rate': f"{overall_churn:.2%}",
        'Total Customers': len(customers),
        'Revenue at Risk': f"${revenue_at_risk:,.0f}"
    },
    'Top Risk Factors': factors['top_predictors'][:5]
}

# Generate HTML report
generate_report_html(
    title='Customer Churn Analysis Report',
    content=content,
    output_path='reports/churn_analysis_report.html'
)
```

### Troubleshooting

#### Issue: FileNotFoundError when loading data

**Solution:** Verify data files exist in `data/raw/` directory

```python
from pathlib import Path

data_dir = Path('data/raw')
print("Files in data directory:")
for file in data_dir.glob('*.csv'):
    print(f"  - {file.name}")
```

#### Issue: DateParseError with date parsing

**Cause:** BUG in `parse_dates()` - only handles YYYY-MM-DD format

**Workaround:** Convert dates manually before calling parse_dates()

```python
import pandas as pd

# Load with pandas date parsing
df = pd.read_csv('data/raw/transactions_v1.csv', parse_dates=['date'])
```

#### Issue: KeyError for "transaction_amount"

**Cause:** BUG in `config.py` FIELD_MAP and `data_loader.py`

**Workaround:** Fix the FIELD_MAP or manually rename column

```python
# Fix in config.py
FIELD_MAP = {
    "revenue": "order_value"  # Correct mapping
}

# Or manually rename after loading
df = df.rename(columns={"order_value": "revenue"})
```

#### Issue: Memory error with large datasets

**Solution:** Optimize data types and use chunking

```python
from src.utils import optimize_dataframe_dtypes, chunk_dataframe

# Optimize memory
df = optimize_dataframe_dtypes(df)

# Or process in chunks
for chunk in chunk_dataframe(df, chunk_size=10000):
    process_chunk(chunk)
```

---

## ⚠️ Known Issues

### BUG 1: Field Name Mismatch in data_loader.py

**Location:** `src/data_loader.py`, line 138
**Severity:** HIGH
**Status:** Documented, Fix Required

**Description:**
The `load_transactions()` function hardcodes the column name "transaction_amount" in the rename operation, but the actual CSV file uses "order_value".

**Code:**
```python
# BUG: Hardcoded incorrect column name
df = df.rename(columns={"transaction_amount": "revenue"})
```

**Impact:**
- Rename operation fails silently (no error raised)
- Column "order_value" remains unrenamed
- Downstream code expecting "revenue" column will fail
- Affects all transaction-based analyses

**Reproduction:**
```python
from src.data_loader import load_transactions
df = load_transactions('data/raw/transactions_v1.csv')
print('revenue' in df.columns)  # False - bug!
print('order_value' in df.columns)  # True - actual column name
```

**Workaround:**
```python
# Option 1: Fix FIELD_MAP in config.py
FIELD_MAP = {
    "revenue": "order_value"  # Correct mapping
}

# Option 2: Manually rename after loading
df = df.rename(columns={"order_value": "revenue"})
```

**Fix Required:**
```python
# Correct implementation
df = df.rename(columns={"order_value": "revenue"})
```

**Priority:** HIGH (blocks core functionality)
**Assigned To:** Agent
**Target Fix:** Next sprint

---

### BUG 2: Limited Date Format Support in parse_dates()

**Location:** `src/data_loader.py`, line 228-235
**Severity:** MEDIUM
**Status:** Documented, Enhancement Planned

**Description:**
The `parse_dates()` function only handles dates in "YYYY-MM-DD" format. It raises `DateParseError` when encountering other common formats like "M/D/YYYY" or "DD/MM/YYYY".

**Code:**
```python
# BUG: Only handles one date format
df[date_col] = df[date_col].apply(
    lambda d: datetime.strptime(d, "%Y-%m-%d") if pd.notna(d) else pd.NaT
)
```

**Impact:**
- Fails on US format dates (3/15/2024)
- Fails on European format dates (15/03/2024)
- Fails on dates with time (2024-03-15 14:30:00)
- Reduces robustness for varying data sources

**Reproduction:**
```python
from src.data_loader import parse_dates
import pandas as pd

# Will fail with DateParseError
df = pd.DataFrame({'date': ['3/15/2024', '3/16/2024']})
parse_dates(df, 'date')  # Raises DateParseError
```

**Workaround:**
```python
# Use pandas flexible date parsing
df['date'] = pd.to_datetime(df['date'], errors='coerce')
```

**Recommended Fix:**
```python
def parse_dates(df, date_col, date_formats=None):
    """Parse dates with support for multiple formats."""
    if date_formats is None:
        # Try pandas flexible parsing first
        try:
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            return df
        except:
            pass

    # Try each format
    for fmt in date_formats:
        try:
            df[date_col] = df[date_col].apply(
                lambda d: datetime.strptime(d, fmt) if pd.notna(d) else pd.NaT
            )
            return df
        except:
            continue

    raise DateParseError("Unable to parse dates with any supported format")
```

**Priority:** MEDIUM (current data is clean, but limits reusability)
**Assigned To:** Agent
**Target Fix:** Future enhancement

---

### BUG 3: Incorrect Revenue Mapping in config.py

**Location:** `src/config.py`, line 92
**Severity:** MEDIUM
**Status:** Documented, Related to BUG 1

**Description:**
The `FIELD_MAP` configuration incorrectly maps "revenue" to "amount", but the actual CSV column is "order_value".

**Code:**
```python
# BUG: Incorrect mapping
FIELD_MAP = {
    "customer_id": "customer_id",
    "revenue": "amount",       # Should be "order_value"
    "date": "transaction_date"
}
```

**Impact:**
- Causes confusion in field name references
- Contributes to BUG 1 (incorrect column name)
- Affects code that uses FIELD_MAP for column access

**Fix Required:**
```python
FIELD_MAP = {
    "customer_id": "customer_id",
    "revenue": "order_value",  # Corrected
    "date": "transaction_date"
}
```

**Priority:** MEDIUM
**Assigned To:** Agent
**Target Fix:** Same sprint as BUG 1

---

### Minor Issues

**Issue 4: Missing Demographics**
- 40% of customers have missing age/gender
- Expected behavior (optional fields)
- Limits demographic segmentation
- Status: Accepted, documented

**Issue 5: Performance on Very Large Datasets**
- Some operations slow on datasets >1M rows
- Consider chunking or Dask for production
- Status: Enhancement for future scaling

---

## 🤝 Contributing

### Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Follow PEP 8 style guide
   - Add docstrings for new functions
   - Include type hints
   - Write unit tests

3. **Run Tests**
   ```bash
   pytest tests/ -v
   flake8 src/
   black src/ --check
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Coding Standards

**Python Style:**
- PEP 8 compliant
- Maximum line length: 100 characters
- Use type hints for function signatures
- Docstrings: Google style

**Documentation:**
- All functions must have docstrings
- Include examples in docstrings
- Update README for user-facing changes
- Add inline comments for complex logic

**Testing:**
- Write tests for all new functions
- Maintain >80% code coverage
- Test edge cases and error conditions
- Use descriptive test names

### Code Review Process

**Required Approvals:** 1 reviewer
**Reviewers:** Maya, Jordan, Sam

**Review Checklist:**
- [ ] Code follows style guide
- [ ] Tests pass and coverage maintained
- [ ] Documentation updated
- [ ] No hardcoded values or secrets
- [ ] Error handling implemented
- [ ] Logging added where appropriate

---

## 👥 Team and Contact

### Core Team

**Alex Chen** - VP of Marketing (Project Sponsor)
- Email: alex.chen@openclaw.com
- Role: Business requirements, executive alignment
- Availability: Daily check-ins

**Maya Rodriguez** - Senior Data Analyst (Project Lead)
- Email: maya.rodriguez@openclaw.com
- Role: Project coordination, analysis, reporting
- Office: Building A, Room 312

**Jordan Kim** - Data Scientist (Analytics Lead)
- Email: jordan.kim@openclaw.com
- Role: Statistical analysis, predictive modeling
- Office: Building A, Room 315

**Sam Park** - Data Engineer (Infrastructure Support)
- Email: sam.park@openclaw.com
- Role: Data infrastructure, pipeline optimization
- Office: Building B, Room 201

**Agent** - AI Assistant (Technical Support)
- Role: Code implementation, documentation, testing
- Availability: 24/7

### Communication Channels

**Primary:** Slack #churn-analysis-project
**Email:** For formal communications and approvals
**Meetings:** Daily standup (async), weekly check-ins (sync)

### Support

**Technical Issues:** Slack #data-support or email Sam Park
**Business Questions:** Email Maya Rodriguez or Alex Chen
**Urgent Issues:** Call Alex Chen (exec sponsor)

---

## 📄 License

**Internal Use Only** - OpenClaw Inc. Proprietary

This project and its contents are proprietary to OpenClaw Inc. and are intended for internal use only. Unauthorized distribution, reproduction, or use outside of OpenClaw Inc. is strictly prohibited.

**Data Usage:**
- This project contains customer PII
- Subject to GDPR, CCPA, and company data privacy policies
- Do not share data or findings outside authorized personnel
- Anonymize data for presentations to external parties

---

## 📅 Project Timeline

**Project Start:** March 3, 2025
**Project End:** March 14, 2025 (Deadline)
**Presentation:** March 15, 2025

### Milestones

- ✅ March 3: Kickoff meeting, scope defined
- ✅ March 5: Data discovery complete
- ✅ March 7: Analysis framework approved
- ✅ March 10: Exploratory analysis complete
- ✅ March 12: Predictive model developed
- 🔄 March 13: Reports drafted
- 📅 March 14: Final deliverables due
- 📅 March 15: Executive presentation

---

## 📈 Future Work

### Short-Term (Q2 2025)

1. **Fix Known Bugs**
   - Resolve field mapping issues
   - Enhance date parsing flexibility
   - Add better error messages

2. **Dashboard Development**
   - Real-time churn monitoring dashboard
   - Automated daily updates
   - Drill-down capabilities by segment/region

3. **Model Deployment**
   - Schedule automated model scoring
   - Integrate with CRM system
   - Set up alerts for high-risk customers

### Medium-Term (Q3-Q4 2025)

1. **Advanced Modeling**
   - Deep learning models (LSTM for time series)
   - Explainable AI (SHAP values for model interpretation)
   - Ensemble methods

2. **Expanded Data Sources**
   - Email engagement data
   - Website behavior (browsing, search)
   - Customer support interactions
   - Product reviews and sentiment

3. **A/B Testing Framework**
   - Test retention campaigns
   - Measure intervention effectiveness
   - Optimize communication strategies

### Long-Term (2026+)

1. **Real-Time Prediction**
   - Streaming data pipeline
   - Real-time churn scoring
   - Instant intervention triggers

2. **Prescriptive Analytics**
   - Recommend optimal retention actions per customer
   - Personalized offer generation
   - Dynamic pricing strategies

3. **Expanded Scope**
   - Customer lifetime value optimization
   - Cross-sell and upsell prediction
   - Fraud detection integration

---

## 📞 Getting Help

### Documentation

- **Data Dictionary:** `docs/data_dictionary.md` - Complete data schema
- **Meeting Notes:** `docs/meeting_notes.md` - Project decisions and context
- **Code Documentation:** Inline docstrings in all modules

### FAQs

**Q: Where is the raw data located?**
A: `/data/raw/` directory (not in git, ask Sam for access)

**Q: How do I run the complete analysis?**
A: `python run_analysis.py` from project root

**Q: What is the churn definition?**
A: 30 days of no transactions or account activity (defined by Alex, documented in config.py)

**Q: Why are there bugs in the code?**
A: These are intentional for testing purposes (realistic scenario simulation)

**Q: Can I use this code for other projects?**
A: Yes, but remove hardcoded values and fix known bugs first

**Q: How do I contribute?**
A: See Contributing section above

### Still Need Help?

Contact Maya Rodriguez (Project Lead) or post in #churn-analysis-project Slack channel.

---

**Document Version:** 1.0.0
**Last Updated:** March 12, 2025
**Status:** Active Development ✅

---

*End of README*
