#!/usr/bin/env python3
"""
Scratch Analysis Script - DEPRECATED
=====================================

This is an old exploratory analysis script from early 2024.
DO NOT USE - This was Jordan's initial exploration and has been
replaced by the proper pipeline.

Author: Jordan Chen
Created: 2024-02-14
Last Modified: 2024-03-08
Status: ABANDONED - DO NOT USE
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
import sys
import os
from typing import List, Dict, Tuple, Optional
import json
from pathlib import Path

# Suppress warnings for exploratory work
warnings.filterwarnings('ignore')

# Set random seed for reproducibility (though this doesn't matter anymore)
np.random.seed(42)

# Configure pandas display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', 50)

# Plotting style configuration
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ============================================================================
# CONFIGURATION SECTION
# ============================================================================

# These paths are probably wrong now, don't use this script
DATA_DIR = "/home/analytics/data/raw/"
OUTPUT_DIR = "/home/analytics/scratch_output/"
TEMP_DIR = "/tmp/jordan_scratch/"

# Old database config that's probably outdated
DB_CONFIG = {
    'host': 'old-db-server.nexaretail.internal',
    'port': 5432,
    'database': 'customer_data_2023',
    'user': 'jordan',
    'password': 'REDACTED'  # Obviously don't actually store passwords like this
}

# Random parameters I was experimenting with
ANALYSIS_PARAMS = {
    'churn_threshold_days': 60,  # Was trying different thresholds
    'lookback_window': 180,
    'min_customer_age': 30,
    'outlier_std_threshold': 3.0,
    'correlation_threshold': 0.15,
    'test_split': 0.3
}

# Visualization settings
VIZ_CONFIG = {
    'figure_size': (14, 10),
    'dpi': 100,
    'color_churned': '#e74c3c',
    'color_active': '#2ecc71',
    'color_neutral': '#95a5a6'
}

# ============================================================================
# UTILITY FUNCTIONS - Probably buggy, don't trust these
# ============================================================================

def load_customer_data(file_path: str) -> pd.DataFrame:
    """
    Load customer data from CSV.

    NOTE: This function has issues with date parsing and probably won't work
    with the current data format. Use the proper pipeline instead.
    """
    print(f"Loading customer data from {file_path}...")

    try:
        df = pd.read_csv(file_path)

        # Attempt to parse dates - this is messy and unreliable
        date_columns = ['signup_date', 'last_active', 'created_at', 'updated_at']
        for col in date_columns:
            if col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                except Exception as e:
                    print(f"Warning: Failed to parse {col}: {e}")

        print(f"Loaded {len(df)} rows, {len(df.columns)} columns")
        return df

    except Exception as e:
        print(f"ERROR loading data: {e}")
        return pd.DataFrame()


def calculate_churn_label(df: pd.DataFrame, threshold_days: int = 60) -> pd.DataFrame:
    """
    Calculate churn label based on inactivity.

    WARNING: This logic is probably wrong. I was experimenting with different
    approaches and never validated this properly. Use the production pipeline.
    """
    df = df.copy()

    # Calculate days since last activity
    reference_date = datetime.now()
    df['days_inactive'] = (reference_date - df['last_active']).dt.days

    # Label as churned if inactive for more than threshold
    df['churned'] = df['days_inactive'] > threshold_days

    # Some random additional conditions I was testing
    # (These don't make sense and should be ignored)
    df.loc[df['monthly_spend'] == 0, 'churned'] = True
    df.loc[df['support_tickets'] > 10, 'churned'] = True  # This is silly

    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and preprocess data.

    NOTE: This is a mess of random transformations. Don't use this.
    """
    print("Cleaning data...")
    original_rows = len(df)

    # Remove duplicates (but which columns define a duplicate? Who knows!)
    df = df.drop_duplicates()

    # Drop rows with missing critical fields
    # (But is this the right approach? Probably not.)
    critical_fields = ['customer_id', 'signup_date']
    df = df.dropna(subset=critical_fields)

    # Fill missing values with questionable defaults
    df['monthly_spend'] = df['monthly_spend'].fillna(0)
    df['support_tickets'] = df['support_tickets'].fillna(0)
    df['last_active'] = df['last_active'].fillna(df['signup_date'])

    # Remove outliers using a crude method
    # (This is probably too aggressive and loses important data)
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        mean = df[col].mean()
        std = df[col].std()
        df = df[np.abs(df[col] - mean) <= (3 * std)]

    rows_removed = original_rows - len(df)
    print(f"Removed {rows_removed} rows ({rows_removed/original_rows*100:.1f}%)")

    return df


def calculate_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineer features for analysis.

    WARNING: These features are ad-hoc and not validated.
    Many probably don't make sense or have bugs.
    """
    df = df.copy()

    # Customer lifetime in days
    df['customer_lifetime_days'] = (datetime.now() - df['signup_date']).dt.days

    # Days since last activity
    df['days_since_active'] = (datetime.now() - df['last_active']).dt.days

    # Activity ratio (probably meaningless)
    df['activity_ratio'] = df['days_since_active'] / (df['customer_lifetime_days'] + 1)

    # Spend per day (questionable utility)
    df['spend_per_day'] = df['monthly_spend'] / 30

    # Support intensity (tickets per month of lifetime)
    df['support_intensity'] = df['support_tickets'] / (df['customer_lifetime_days'] / 30 + 1)

    # Random categorical encoding that's probably wrong
    plan_type_map = {'basic': 1, 'standard': 2, 'premium': 3}
    df['plan_type_numeric'] = df['plan_type'].map(plan_type_map).fillna(0)

    # Some weird interaction terms I was testing
    df['spend_x_lifetime'] = df['monthly_spend'] * df['customer_lifetime_days']
    df['tickets_x_inactivity'] = df['support_tickets'] * df['days_since_active']

    # Handle infinite values and NaNs that these calculations might create
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.fillna(0)

    return df


def exploratory_analysis(df: pd.DataFrame) -> None:
    """
    Print some basic statistics.

    This is just random exploration, not a real analysis.
    """
    print("\n" + "="*80)
    print("EXPLORATORY ANALYSIS - SCRATCH WORK")
    print("="*80)

    print("\nDataset shape:", df.shape)
    print("\nColumn types:")
    print(df.dtypes)

    print("\nBasic statistics:")
    print(df.describe())

    print("\nMissing values:")
    print(df.isnull().sum())

    if 'churned' in df.columns:
        print("\nChurn distribution:")
        print(df['churned'].value_counts())
        print(f"\nChurn rate: {df['churned'].mean()*100:.2f}%")

    if 'plan_type' in df.columns:
        print("\nPlan type distribution:")
        print(df['plan_type'].value_counts())

    # Print correlations with churn (if it exists)
    if 'churned' in df.columns:
        print("\nCorrelations with churn:")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        correlations = df[numeric_cols].corrwith(df['churned'].astype(int))
        print(correlations.sort_values(ascending=False))


def plot_churn_analysis(df: pd.DataFrame, output_dir: str) -> None:
    """
    Create some exploratory plots.

    NOTE: These visualizations are rough drafts and not production-quality.
    The plots probably have issues and shouldn't be used for real reporting.
    """
    if 'churned' not in df.columns:
        print("No churn label found, skipping plots")
        return

    os.makedirs(output_dir, exist_ok=True)

    # Plot 1: Churn by plan type (if available)
    if 'plan_type' in df.columns:
        plt.figure(figsize=VIZ_CONFIG['figure_size'])
        churn_by_plan = df.groupby('plan_type')['churned'].mean() * 100
        churn_by_plan.plot(kind='bar', color=VIZ_CONFIG['color_churned'])
        plt.title('Churn Rate by Plan Type (Draft - Do Not Use)', fontsize=16)
        plt.ylabel('Churn Rate (%)', fontsize=12)
        plt.xlabel('Plan Type', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'churn_by_plan_DRAFT.png'), dpi=VIZ_CONFIG['dpi'])
        plt.close()

    # Plot 2: Distribution of days inactive
    if 'days_since_active' in df.columns:
        plt.figure(figsize=VIZ_CONFIG['figure_size'])

        churned = df[df['churned'] == True]['days_since_active']
        active = df[df['churned'] == False]['days_since_active']

        plt.hist([active, churned], bins=50, label=['Active', 'Churned'],
                 color=[VIZ_CONFIG['color_active'], VIZ_CONFIG['color_churned']],
                 alpha=0.7)
        plt.xlabel('Days Since Last Active', fontsize=12)
        plt.ylabel('Number of Customers', fontsize=12)
        plt.title('Inactivity Distribution (Draft)', fontsize=16)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'inactivity_dist_DRAFT.png'), dpi=VIZ_CONFIG['dpi'])
        plt.close()

    # Plot 3: Scatter plot of spend vs lifetime (messy)
    if 'monthly_spend' in df.columns and 'customer_lifetime_days' in df.columns:
        plt.figure(figsize=VIZ_CONFIG['figure_size'])

        churned_df = df[df['churned'] == True]
        active_df = df[df['churned'] == False]

        plt.scatter(active_df['customer_lifetime_days'], active_df['monthly_spend'],
                   alpha=0.3, c=VIZ_CONFIG['color_active'], label='Active', s=20)
        plt.scatter(churned_df['customer_lifetime_days'], churned_df['monthly_spend'],
                   alpha=0.3, c=VIZ_CONFIG['color_churned'], label='Churned', s=20)

        plt.xlabel('Customer Lifetime (days)', fontsize=12)
        plt.ylabel('Monthly Spend ($)', fontsize=12)
        plt.title('Spend vs Lifetime (Messy Draft)', fontsize=16)
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'spend_vs_lifetime_DRAFT.png'), dpi=VIZ_CONFIG['dpi'])
        plt.close()

    # Plot 4: Correlation heatmap (probably too many features)
    plt.figure(figsize=(12, 10))
    numeric_cols = df.select_dtypes(include=[np.number]).columns[:15]  # Just take first 15
    correlation_matrix = df[numeric_cols].corr()
    sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                center=0, square=True, linewidths=1)
    plt.title('Feature Correlations (Draft - Incomplete)', fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'correlation_heatmap_DRAFT.png'), dpi=VIZ_CONFIG['dpi'])
    plt.close()

    print(f"\nDraft plots saved to {output_dir}")


def segment_analysis(df: pd.DataFrame) -> None:
    """
    Analyze different customer segments.

    This is incomplete and the segmentation logic is questionable.
    """
    print("\n" + "="*80)
    print("SEGMENT ANALYSIS - INCOMPLETE")
    print("="*80)

    if 'churned' not in df.columns:
        print("No churn data available")
        return

    # Segment by plan type
    if 'plan_type' in df.columns:
        print("\nChurn by Plan Type:")
        for plan in df['plan_type'].unique():
            plan_df = df[df['plan_type'] == plan]
            churn_rate = plan_df['churned'].mean() * 100
            count = len(plan_df)
            print(f"  {plan}: {churn_rate:.1f}% (n={count})")

    # Segment by customer lifetime (arbitrary buckets)
    if 'customer_lifetime_days' in df.columns:
        print("\nChurn by Customer Age:")

        df['age_bucket'] = pd.cut(df['customer_lifetime_days'],
                                   bins=[0, 90, 180, 365, 730, 10000],
                                   labels=['0-3mo', '3-6mo', '6-12mo', '1-2yr', '2yr+'])

        for bucket in df['age_bucket'].cat.categories:
            bucket_df = df[df['age_bucket'] == bucket]
            if len(bucket_df) > 0:
                churn_rate = bucket_df['churned'].mean() * 100
                count = len(bucket_df)
                print(f"  {bucket}: {churn_rate:.1f}% (n={count})")

    # Segment by spend level (made up thresholds)
    if 'monthly_spend' in df.columns:
        print("\nChurn by Spend Level:")

        df['spend_bucket'] = pd.cut(df['monthly_spend'],
                                     bins=[0, 30, 60, 100, 10000],
                                     labels=['Low', 'Medium', 'High', 'Very High'])

        for bucket in df['spend_bucket'].cat.categories:
            bucket_df = df[df['spend_bucket'] == bucket]
            if len(bucket_df) > 0:
                churn_rate = bucket_df['churned'].mean() * 100
                count = len(bucket_df)
                print(f"  {bucket}: {churn_rate:.1f}% (n={count})")


def cohort_analysis_attempt(df: pd.DataFrame) -> None:
    """
    Attempt at cohort analysis - INCOMPLETE AND PROBABLY WRONG.

    I started this but never finished it. The logic is incomplete
    and probably has bugs. Don't use this.
    """
    print("\n" + "="*80)
    print("COHORT ANALYSIS ATTEMPT - INCOMPLETE")
    print("="*80)

    if 'signup_date' not in df.columns:
        print("No signup date available")
        return

    # Create cohort month
    df['cohort_month'] = df['signup_date'].dt.to_period('M')

    # Calculate cohort index (months since signup)
    # This logic is probably wrong
    df['cohort_index'] = ((datetime.now().year - df['signup_date'].dt.year) * 12 +
                          (datetime.now().month - df['signup_date'].dt.month))

    # Try to create a cohort table (incomplete)
    cohort_data = df.groupby(['cohort_month', 'cohort_index'])['customer_id'].count()

    print("\nCohort data shape:", cohort_data.shape)
    print("\nSample cohort data (probably wrong):")
    print(cohort_data.head(20))

    # TODO: Actually calculate retention rates
    # TODO: Create cohort visualization
    # TODO: Fix the logic above

    print("\n[This analysis is incomplete and abandoned]")


def quick_model_experiment(df: pd.DataFrame) -> None:
    """
    Quick and dirty model experiment.

    WARNING: This is NOT production-quality modeling. It's full of issues:
    - No proper train/test split validation
    - No feature scaling
    - No hyperparameter tuning
    - Probably data leakage
    - Not cross-validated

    DO NOT USE FOR ACTUAL PREDICTIONS.
    """
    print("\n" + "="*80)
    print("QUICK MODEL EXPERIMENT - NOT FOR PRODUCTION")
    print("="*80)

    if 'churned' not in df.columns:
        print("No churn label for modeling")
        return

    # Try to import sklearn (might not be installed)
    try:
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import accuracy_score, precision_score, recall_score
    except ImportError:
        print("sklearn not available, skipping model experiment")
        return

    # Select features (arbitrary selection)
    feature_cols = ['customer_lifetime_days', 'days_since_active', 'monthly_spend',
                   'support_tickets', 'plan_type_numeric']

    # Check if features exist
    available_features = [col for col in feature_cols if col in df.columns]

    if len(available_features) < 3:
        print("Not enough features available for modeling")
        return

    print(f"\nUsing features: {available_features}")

    # Prepare data (no scaling or proper preprocessing)
    X = df[available_features].fillna(0)
    y = df['churned'].astype(int)

    # Split data (arbitrary split, no stratification consideration)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # Train a basic logistic regression (no tuning)
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate metrics (basic, no confidence intervals)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)

    print(f"\nQuick Model Results (NOT VALIDATED):")
    print(f"  Accuracy:  {accuracy:.3f}")
    print(f"  Precision: {precision:.3f}")
    print(f"  Recall:    {recall:.3f}")

    # Print feature coefficients (raw, not interpreted correctly)
    print(f"\nRaw Coefficients (don't read too much into these):")
    for feature, coef in zip(available_features, model.coef_[0]):
        print(f"  {feature}: {coef:.4f}")

    print("\nREMINDER: This is not a proper model. Don't use these results.")


def random_experiments(df: pd.DataFrame) -> None:
    """
    Random stuff I was trying.

    This function is a collection of random experiments and tests.
    Nothing here is validated or useful.
    """
    print("\n" + "="*80)
    print("RANDOM EXPERIMENTS - IGNORE THIS")
    print("="*80)

    # Experiment 1: What if we use 45-day threshold instead?
    if 'days_since_active' in df.columns:
        threshold_45 = (df['days_since_active'] > 45).mean() * 100
        threshold_60 = (df['days_since_active'] > 60).mean() * 100
        threshold_90 = (df['days_since_active'] > 90).mean() * 100

        print(f"\nChurn rates with different thresholds:")
        print(f"  45 days: {threshold_45:.2f}%")
        print(f"  60 days: {threshold_60:.2f}%")
        print(f"  90 days: {threshold_90:.2f}%")

    # Experiment 2: What about customers with zero spend?
    if 'monthly_spend' in df.columns:
        zero_spend = df[df['monthly_spend'] == 0]
        print(f"\nCustomers with zero spend: {len(zero_spend)} ({len(zero_spend)/len(df)*100:.1f}%)")
        if 'churned' in df.columns and len(zero_spend) > 0:
            print(f"Churn rate for zero spend: {zero_spend['churned'].mean()*100:.2f}%")

    # Experiment 3: Support ticket extremes
    if 'support_tickets' in df.columns:
        high_support = df[df['support_tickets'] > 5]
        print(f"\nCustomers with 5+ tickets: {len(high_support)} ({len(high_support)/len(df)*100:.1f}%)")
        if 'churned' in df.columns and len(high_support) > 0:
            print(f"Churn rate for high support: {high_support['churned'].mean()*100:.2f}%")

    # Experiment 4: Recent signups
    if 'signup_date' in df.columns:
        recent_cutoff = datetime.now() - timedelta(days=90)
        recent_signups = df[df['signup_date'] > recent_cutoff]
        print(f"\nCustomers signed up in last 90 days: {len(recent_signups)}")
        if 'churned' in df.columns and len(recent_signups) > 0:
            print(f"Early churn rate: {recent_signups['churned'].mean()*100:.2f}%")


# ============================================================================
# MAIN EXECUTION - This whole thing is a mess, don't run it
# ============================================================================

def main():
    """
    Main execution function.

    DO NOT RUN THIS SCRIPT. It's outdated, buggy, and has been replaced
    by the proper production pipeline. This is kept for historical reference
    only (and should probably be deleted).
    """
    print("="*80)
    print("SCRATCH ANALYSIS SCRIPT - DEPRECATED")
    print("="*80)
    print("\nWARNING: This script is outdated and should not be used!")
    print("Use the production pipeline instead.")
    print("\nThis script contains:")
    print("  - Outdated file paths")
    print("  - Unvalidated logic")
    print("  - Questionable methodologies")
    print("  - No error handling")
    print("  - Hardcoded parameters that don't make sense")
    print("\nIf you're seeing this, you probably want to look at:")
    print("  - project/src/churn_pipeline.py (production code)")
    print("  - project/notebooks/churn_analysis.ipynb (validated analysis)")
    print("\nExiting without doing anything...")
    print("="*80)

    return

    # ---- EVERYTHING BELOW THIS POINT IS UNREACHABLE ----
    # (Left here for historical reference, but won't execute)

    # Try to load data (file probably doesn't exist)
    customer_file = os.path.join(DATA_DIR, "customers.csv")
    df = load_customer_data(customer_file)

    if df.empty:
        print("Failed to load data, exiting")
        return

    # Clean data (questionable approach)
    df = clean_data(df)

    # Calculate features (ad-hoc and unvalidated)
    df = calculate_features(df)

    # Calculate churn label (wrong threshold)
    df = calculate_churn_label(df, threshold_days=ANALYSIS_PARAMS['churn_threshold_days'])

    # Run exploratory analysis
    exploratory_analysis(df)

    # Create plots
    plot_churn_analysis(df, OUTPUT_DIR)

    # Segment analysis
    segment_analysis(df)

    # Cohort analysis (incomplete)
    cohort_analysis_attempt(df)

    # Model experiment (not production-ready)
    quick_model_experiment(df)

    # Random experiments
    random_experiments(df)

    print("\n" + "="*80)
    print("SCRATCH ANALYSIS COMPLETE")
    print("="*80)
    print("\nREMINDER: These are rough exploratory results only.")
    print("Do not use for decision-making or reporting.")
    print("See production pipeline for validated analysis.")


if __name__ == "__main__":
    main()


# ============================================================================
# ABANDONED FUNCTIONS - Code graveyard
# ============================================================================

def attempt_clustering(df):
    """
    Tried to cluster customers but never finished.
    KMeans, DBSCAN, hierarchical? Never decided.
    Also no feature scaling which would make this useless anyway.
    """
    pass


def time_series_analysis_idea(df):
    """
    Wanted to look at trends over time but the data structure
    isn't right for this and I never figured out how to reshape it.
    """
    pass


def build_fancy_dashboard(df):
    """
    Thought about making an interactive dashboard with plotly
    but realized this should be in Tableau instead.
    Started but never finished.
    """
    pass


def calculate_customer_lifetime_value(df):
    """
    CLV calculation - started but the formula is incomplete
    and probably wrong. Also need accounting input on revenue recognition.
    """
    pass


def competitor_churn_comparison():
    """
    Wanted to benchmark against competitor data but we don't have
    access to that information so this is impossible.
    """
    pass


# More abandoned ideas:
# - A/B test analysis for retention campaigns (no test data)
# - Geographic churn analysis (no good location data)
# - Seasonal pattern detection (need more historical data)
# - Customer journey mapping (would need behavioral event data)
# - NPS correlation with churn (NPS data not accessible from this script)
# - Feature usage correlation (product analytics in separate system)

# TODO (that will never be done):
# - Fix date parsing issues
# - Validate churn calculation logic
# - Add proper error handling
# - Document functions properly
# - Add unit tests (lol)
# - Refactor into modules
# - Update to use production database
# - Make plots production-quality
# - Complete cohort analysis
# - Build proper model pipeline
# - Add command-line arguments
# - Containerize with Docker
# - Set up CI/CD
# - Write documentation
#
# OR... just use the proper production pipeline that already does all this.

# Notes to self:
# - This script got way too long and messy
# - Should have used a notebook instead
# - Need to learn better software engineering practices
# - Next time, don't hardcode everything
# - Remember to delete scratch files when done (oops)
