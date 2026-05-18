"""
Customer Churn Analysis Module

This module provides comprehensive statistical analysis, feature engineering, and predictive
modeling capabilities for customer churn analysis. It implements various analytical methods
including correlation analysis, statistical testing, predictive modeling, and visualization.

The analysis pipeline supports:
- Exploratory data analysis (EDA)
- Statistical hypothesis testing
- Feature engineering for ML models
- Churn prediction and scoring
- Cohort analysis and segmentation
- Time series analysis of customer behavior

Author: Analytics Team
Created: 2025-03-02
Last Modified: 2025-03-12
Version: 1.3.0

Dependencies:
    - pandas>=2.2.0
    - numpy>=1.26.0
    - scipy>=1.12.0
    - matplotlib>=3.8.0
    - seaborn>=0.13.0
    - scikit-learn>=1.4.0

Usage Example:
    >>> from analysis import compute_churn_rate, analyze_churn_factors
    >>> churn_rate = compute_churn_rate(df, churn_col='is_churned')
    >>> print(f"Overall churn rate: {churn_rate:.2%}")
    >>> factors = analyze_churn_factors(df)
    >>> print(factors['top_predictors'])
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy.stats import chi2_contingency, mannwhitneyu, spearmanr, pearsonr, kstest
from typing import Dict, List, Tuple, Optional, Union, Any
import warnings
import logging
from pathlib import Path
import sys
from collections import defaultdict
from datetime import datetime, timedelta

# Visualization imports
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.figure import Figure
from matplotlib.axes import Axes

# Machine learning imports
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure visualization defaults
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Global configuration
ALPHA = 0.05  # Significance level for statistical tests
RANDOM_STATE = 42
MIN_SAMPLE_SIZE = 30


class AnalysisError(Exception):
    """Custom exception for analysis errors."""
    pass


class InsufficientDataError(Exception):
    """Exception raised when data is insufficient for analysis."""
    pass


def compute_churn_rate(df: pd.DataFrame, churn_col: str = "is_churned",
                      group_by: Optional[str] = None) -> Union[float, pd.Series]:
    """
    Compute overall churn rate or churn rate by group.

    The churn rate is calculated as the proportion of churned customers
    in the dataset. This is a fundamental metric for understanding customer
    retention and business health.

    Args:
        df (pd.DataFrame): Input dataframe with churn labels
        churn_col (str): Name of column containing churn indicator (default: "is_churned")
        group_by (Optional[str]): Column name to group by for segmented analysis

    Returns:
        Union[float, pd.Series]: Overall churn rate or series of churn rates by group

    Raises:
        KeyError: If churn_col or group_by column doesn't exist
        ValueError: If churn_col is not binary (0/1 or True/False)

    Example:
        >>> df = pd.DataFrame({
        ...     'customer_id': range(100),
        ...     'is_churned': [0]*70 + [1]*30
        ... })
        >>> rate = compute_churn_rate(df)
        >>> print(f"Churn rate: {rate:.1%}")
        Churn rate: 30.0%

    Notes:
        - Churn column should contain binary values (0/1 or True/False)
        - Missing values in churn column are excluded from calculation
        - For grouped analysis, returns a pandas Series indexed by group values
    """
    logger.info(f"Computing churn rate (churn_col='{churn_col}', group_by={group_by})")

    # Validate churn column exists
    if churn_col not in df.columns:
        error_msg = f"Churn column '{churn_col}' not found. Available: {df.columns.tolist()}"
        logger.error(error_msg)
        raise KeyError(error_msg)

    # Check for missing values
    missing_count = df[churn_col].isna().sum()
    if missing_count > 0:
        logger.warning(f"Found {missing_count} missing values in churn column (will be excluded)")

    # Validate binary values
    unique_values = df[churn_col].dropna().unique()
    if not set(unique_values).issubset({0, 1, True, False}):
        error_msg = f"Churn column must be binary (0/1 or True/False), found: {unique_values}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Compute churn rate
    if group_by is None:
        # Overall churn rate
        churn_rate = df[churn_col].mean()
        total_customers = df[churn_col].notna().sum()
        churned_customers = df[churn_col].sum()

        logger.info(f"Overall churn rate: {churn_rate:.2%}")
        logger.info(f"Churned customers: {churned_customers}/{total_customers}")

        return float(churn_rate)

    else:
        # Churn rate by group
        if group_by not in df.columns:
            error_msg = f"Group column '{group_by}' not found"
            logger.error(error_msg)
            raise KeyError(error_msg)

        churn_rates = df.groupby(group_by)[churn_col].mean()

        logger.info(f"Churn rates by {group_by}:")
        for group, rate in churn_rates.items():
            logger.info(f"  {group}: {rate:.2%}")

        return churn_rates


def correlate_spend_churn(df: pd.DataFrame, spend_col: str = 'total_revenue',
                         churn_col: str = 'is_churned',
                         method: str = 'spearman') -> Dict[str, Any]:
    """
    Analyze correlation between customer spending and churn.

    This function implements multiple correlation methods to understand the
    relationship between customer spending patterns and churn behavior.
    Jordan's initial analysis plan suggested using Spearman correlation for
    robustness to outliers.

    Args:
        df (pd.DataFrame): Customer-level dataframe with spend and churn data
        spend_col (str): Name of column containing spend/revenue data
        churn_col (str): Name of column containing churn indicator
        method (str): Correlation method ('spearman', 'pearson', 'pointbiserial')

    Returns:
        Dict[str, Any]: Dictionary containing correlation coefficient, p-value,
                       and interpretation

    Raises:
        KeyError: If required columns don't exist
        ValueError: If method is not supported or data is insufficient

    Example:
        >>> result = correlate_spend_churn(df, method='spearman')
        >>> print(f"Correlation: {result['correlation']:.3f}")
        >>> print(f"P-value: {result['p_value']:.4f}")
        >>> print(f"Significant: {result['is_significant']}")

    Notes:
        - Spearman correlation is recommended for non-linear relationships
        - Pearson correlation assumes linear relationship and normal distribution
        - Point-biserial is appropriate when churn is truly binary
        - TODO: Jordan to confirm final correlation method for production analysis
    """
    logger.info(f"Computing correlation between {spend_col} and {churn_col} (method={method})")

    # Validate columns exist
    required_cols = [spend_col, churn_col]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        error_msg = f"Missing columns: {missing_cols}"
        logger.error(error_msg)
        raise KeyError(error_msg)

    # Remove rows with missing values
    df_clean = df[[spend_col, churn_col]].dropna()
    initial_rows = len(df)
    clean_rows = len(df_clean)

    if clean_rows < initial_rows:
        logger.warning(f"Dropped {initial_rows - clean_rows} rows with missing values")

    if clean_rows < MIN_SAMPLE_SIZE:
        raise InsufficientDataError(
            f"Insufficient data for correlation analysis: {clean_rows} rows (minimum: {MIN_SAMPLE_SIZE})"
        )

    # Compute correlation based on method
    result = {
        'method': method,
        'sample_size': clean_rows,
        'spend_mean': float(df_clean[spend_col].mean()),
        'spend_median': float(df_clean[spend_col].median()),
        'churn_rate': float(df_clean[churn_col].mean())
    }

    try:
        if method == 'spearman':
            # Spearman rank correlation (robust to outliers, handles non-linear monotonic relationships)
            correlation, p_value = spearmanr(df_clean[spend_col], df_clean[churn_col])

        elif method == 'pearson':
            # Pearson correlation (assumes linear relationship and normality)
            correlation, p_value = pearsonr(df_clean[spend_col], df_clean[churn_col])

        elif method == 'pointbiserial':
            # Point-biserial correlation (special case of Pearson for binary variable)
            from scipy.stats import pointbiserialr
            correlation, p_value = pointbiserialr(df_clean[churn_col], df_clean[spend_col])

        else:
            raise ValueError(f"Unsupported correlation method: {method}")

        result['correlation'] = float(correlation)
        result['p_value'] = float(p_value)
        result['is_significant'] = p_value < ALPHA

        # Interpret correlation strength
        abs_corr = abs(correlation)
        if abs_corr < 0.1:
            strength = "negligible"
        elif abs_corr < 0.3:
            strength = "weak"
        elif abs_corr < 0.5:
            strength = "moderate"
        elif abs_corr < 0.7:
            strength = "strong"
        else:
            strength = "very strong"

        result['strength'] = strength
        result['direction'] = "negative" if correlation < 0 else "positive"

        logger.info(f"Correlation: {correlation:.3f} (p={p_value:.4f})")
        logger.info(f"Interpretation: {strength} {result['direction']} correlation")
        logger.info(f"Statistically significant: {result['is_significant']}")

    except Exception as e:
        logger.error(f"Correlation computation failed: {str(e)}")
        raise AnalysisError(f"Failed to compute correlation: {str(e)}")

    return result


def analyze_churn_factors(df: pd.DataFrame, churn_col: str = 'is_churned',
                         feature_cols: Optional[List[str]] = None,
                         top_n: int = 10) -> Dict[str, Any]:
    """
    Comprehensive analysis of factors influencing customer churn.

    Performs univariate analysis of all potential churn predictors including:
    - Correlation analysis for continuous variables
    - Chi-square tests for categorical variables
    - T-tests and Mann-Whitney U tests for group comparisons
    - Feature importance ranking

    Args:
        df (pd.DataFrame): Customer-level dataframe
        churn_col (str): Name of churn indicator column
        feature_cols (Optional[List[str]]): List of feature columns to analyze
                                           (if None, uses all columns except churn)
        top_n (int): Number of top features to return in summary

    Returns:
        Dict[str, Any]: Dictionary containing analysis results and feature rankings
    """
    logger.info("Analyzing churn factors")

    # Determine feature columns
    if feature_cols is None:
        feature_cols = [col for col in df.columns if col != churn_col]
        logger.info(f"Analyzing all {len(feature_cols)} features")
    else:
        logger.info(f"Analyzing {len(feature_cols)} specified features")

    # Validate churn column
    if churn_col not in df.columns:
        raise KeyError(f"Churn column '{churn_col}' not found")

    results = {
        'churn_col': churn_col,
        'total_features': len(feature_cols),
        'sample_size': len(df),
        'churn_rate': float(df[churn_col].mean()),
        'numeric_features': {},
        'categorical_features': {},
        'feature_rankings': []
    }

    # Split into churned and non-churned groups
    churned = df[df[churn_col] == 1]
    not_churned = df[df[churn_col] == 0]

    logger.info(f"Churned customers: {len(churned)}")
    logger.info(f"Non-churned customers: {len(not_churned)}")

    # Analyze each feature
    for feature in feature_cols:
        if feature not in df.columns:
            logger.warning(f"Feature '{feature}' not found, skipping")
            continue

        try:
            if pd.api.types.is_numeric_dtype(df[feature]):
                # Numeric feature analysis
                feature_result = analyze_numeric_feature(
                    df, feature, churn_col, churned, not_churned
                )
                results['numeric_features'][feature] = feature_result

            else:
                # Categorical feature analysis
                feature_result = analyze_categorical_feature(
                    df, feature, churn_col
                )
                results['categorical_features'][feature] = feature_result

            # Add to rankings
            results['feature_rankings'].append({
                'feature': feature,
                'p_value': feature_result.get('p_value', 1.0),
                'effect_size': feature_result.get('effect_size', 0.0),
                'type': feature_result.get('type', 'unknown')
            })

        except Exception as e:
            logger.warning(f"Failed to analyze feature '{feature}': {str(e)}")
            continue

    # Sort features by p-value (most significant first)
    results['feature_rankings'].sort(key=lambda x: x['p_value'])

    # Get top features
    results['top_predictors'] = results['feature_rankings'][:top_n]

    logger.info(f"Analysis complete. Top {top_n} predictors:")
    for i, feat in enumerate(results['top_predictors'], 1):
        logger.info(f"  {i}. {feat['feature']} (p={feat['p_value']:.4f})")

    return results


def analyze_numeric_feature(df: pd.DataFrame, feature: str, churn_col: str,
                           churned: pd.DataFrame, not_churned: pd.DataFrame) -> Dict[str, Any]:
    """
    Analyze numeric feature's relationship with churn.

    Performs:
    - Descriptive statistics by churn group
    - T-test for mean difference
    - Mann-Whitney U test (non-parametric alternative)
    - Effect size calculation (Cohen's d)

    Args:
        df (pd.DataFrame): Full dataframe
        feature (str): Feature name
        churn_col (str): Churn column name
        churned (pd.DataFrame): Churned customers subset
        not_churned (pd.DataFrame): Non-churned customers subset

    Returns:
        Dict[str, Any]: Analysis results
    """
    result = {'type': 'numeric'}

    # Get clean data (no nulls)
    churned_values = churned[feature].dropna()
    not_churned_values = not_churned[feature].dropna()

    if len(churned_values) < MIN_SAMPLE_SIZE or len(not_churned_values) < MIN_SAMPLE_SIZE:
        result['error'] = 'Insufficient sample size'
        result['p_value'] = 1.0
        result['effect_size'] = 0.0
        return result

    # Descriptive statistics
    result['churned_mean'] = float(churned_values.mean())
    result['churned_median'] = float(churned_values.median())
    result['churned_std'] = float(churned_values.std())
    result['not_churned_mean'] = float(not_churned_values.mean())
    result['not_churned_median'] = float(not_churned_values.median())
    result['not_churned_std'] = float(not_churned_values.std())

    # T-test for mean difference
    from scipy.stats import ttest_ind
    t_stat, t_pvalue = ttest_ind(churned_values, not_churned_values, equal_var=False)
    result['t_statistic'] = float(t_stat)
    result['t_pvalue'] = float(t_pvalue)

    # Mann-Whitney U test (non-parametric)
    u_stat, u_pvalue = mannwhitneyu(churned_values, not_churned_values, alternative='two-sided')
    result['u_statistic'] = float(u_stat)
    result['u_pvalue'] = float(u_pvalue)

    # Use more conservative p-value
    result['p_value'] = max(t_pvalue, u_pvalue)

    # Cohen's d effect size
    pooled_std = np.sqrt((churned_values.std()**2 + not_churned_values.std()**2) / 2)
    if pooled_std > 0:
        cohens_d = (churned_values.mean() - not_churned_values.mean()) / pooled_std
        result['effect_size'] = abs(float(cohens_d))
    else:
        result['effect_size'] = 0.0

    # Correlation with churn
    corr, corr_pval = spearmanr(df[feature].dropna(), df.loc[df[feature].notna(), churn_col])
    result['correlation'] = float(corr)
    result['correlation_pvalue'] = float(corr_pval)

    return result


def analyze_categorical_feature(df: pd.DataFrame, feature: str,
                                churn_col: str) -> Dict[str, Any]:
    """
    Analyze categorical feature's relationship with churn using chi-square test.

    Args:
        df (pd.DataFrame): Full dataframe
        feature (str): Feature name
        churn_col (str): Churn column name

    Returns:
        Dict[str, Any]: Analysis results including chi-square statistic and p-value
    """
    result = {'type': 'categorical'}

    # Create contingency table
    contingency_table = pd.crosstab(df[feature], df[churn_col])

    # Chi-square test
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)

    result['chi2_statistic'] = float(chi2)
    result['p_value'] = float(p_value)
    result['degrees_of_freedom'] = int(dof)

    # Cramer's V effect size
    n = contingency_table.sum().sum()
    min_dim = min(contingency_table.shape) - 1
    cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 else 0
    result['effect_size'] = float(cramers_v)

    # Category-wise churn rates
    category_churn_rates = df.groupby(feature)[churn_col].mean().to_dict()
    result['category_churn_rates'] = {str(k): float(v) for k, v in category_churn_rates.items()}

    return result


def perform_cohort_analysis(df: pd.DataFrame, cohort_col: str = 'signup_month',
                            date_col: str = 'transaction_date',
                            customer_col: str = 'customer_id',
                            value_col: str = 'order_value') -> pd.DataFrame:
    """
    Perform cohort analysis to track customer behavior over time.

    Creates cohort retention and revenue matrices showing how customer
    cohorts behave over their lifecycle.

    Args:
        df (pd.DataFrame): Transaction-level dataframe
        cohort_col (str): Column defining cohort (e.g., signup month)
        date_col (str): Transaction date column
        customer_col (str): Customer ID column
        value_col (str): Transaction value column

    Returns:
        pd.DataFrame: Cohort analysis matrix
    """
    logger.info(f"Performing cohort analysis by {cohort_col}")

    # Ensure date column is datetime
    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        df[date_col] = pd.to_datetime(df[date_col])

    # Create period column (e.g., months since cohort start)
    df['cohort_period'] = (
        df[date_col].dt.to_period('M').astype(str)
    )

    # Count unique customers per cohort per period
    cohort_data = df.groupby([cohort_col, 'cohort_period']).agg({
        customer_col: 'nunique',
        value_col: 'sum'
    }).reset_index()

    cohort_data.columns = [cohort_col, 'period', 'customers', 'revenue']

    # Pivot to create cohort matrix
    cohort_matrix_customers = cohort_data.pivot(
        index=cohort_col, columns='period', values='customers'
    )

    cohort_matrix_revenue = cohort_data.pivot(
        index=cohort_col, columns='period', values='revenue'
    )

    logger.info(f"Cohort analysis complete. Cohorts: {len(cohort_matrix_customers)}")

    return cohort_matrix_customers


def calculate_customer_lifetime_value(df: pd.DataFrame,
                                      customer_col: str = 'customer_id',
                                      revenue_col: str = 'total_revenue',
                                      time_col: str = 'days_since_first_transaction',
                                      discount_rate: float = 0.1) -> pd.DataFrame:
    """
    Calculate Customer Lifetime Value (CLV) for each customer.

    CLV is calculated using historical transaction data and projected
    future value based on customer patterns.

    Args:
        df (pd.DataFrame): Customer-level aggregated dataframe
        customer_col (str): Customer ID column
        revenue_col (str): Total revenue column
        time_col (str): Customer age/tenure column
        discount_rate (float): Annual discount rate for NPV calculation

    Returns:
        pd.DataFrame: Dataframe with CLV calculations
    """
    logger.info("Calculating Customer Lifetime Value")

    clv_df = df[[customer_col, revenue_col, time_col]].copy()

    # Historical CLV (actual revenue)
    clv_df['historical_clv'] = clv_df[revenue_col]

    # Calculate average revenue per day
    clv_df['revenue_per_day'] = clv_df[revenue_col] / clv_df[time_col].replace(0, 1)

    # Project future value (simplified model - 1 year projection)
    projection_days = 365
    daily_discount = (1 + discount_rate) ** (1/365) - 1

    clv_df['projected_clv'] = clv_df['revenue_per_day'] * (
        (1 - (1 + daily_discount) ** -projection_days) / daily_discount
    )

    # Total CLV
    clv_df['total_clv'] = clv_df['historical_clv'] + clv_df['projected_clv']

    logger.info(f"Average CLV: ${clv_df['total_clv'].mean():.2f}")
    logger.info(f"Median CLV: ${clv_df['total_clv'].median():.2f}")

    return clv_df


def segment_customers(df: pd.DataFrame, method: str = 'rfm',
                     n_segments: int = 4) -> pd.DataFrame:
    """
    Segment customers using various methods.

    Supports:
    - RFM (Recency, Frequency, Monetary) segmentation
    - K-means clustering
    - Quantile-based segmentation

    Args:
        df (pd.DataFrame): Customer-level dataframe
        method (str): Segmentation method ('rfm', 'kmeans', 'quantile')
        n_segments (int): Number of segments to create

    Returns:
        pd.DataFrame: Dataframe with segment assignments
    """
    logger.info(f"Segmenting customers using {method} method ({n_segments} segments)")

    if method == 'rfm':
        return segment_rfm(df, n_segments)
    elif method == 'kmeans':
        return segment_kmeans(df, n_segments)
    elif method == 'quantile':
        return segment_quantile(df, n_segments)
    else:
        raise ValueError(f"Unsupported segmentation method: {method}")


def segment_rfm(df: pd.DataFrame, n_segments: int = 4) -> pd.DataFrame:
    """
    RFM (Recency, Frequency, Monetary) segmentation.

    Requires columns:
    - days_since_last_transaction (Recency)
    - transaction_count (Frequency)
    - total_revenue (Monetary)
    """
    required_cols = ['days_since_last_transaction', 'transaction_count', 'total_revenue']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise KeyError(f"Missing required columns for RFM: {missing}")

    df_rfm = df.copy()

    # Calculate RFM scores (1 to n_segments)
    # Recency: lower is better (recent customers)
    df_rfm['r_score'] = pd.qcut(df_rfm['days_since_last_transaction'], n_segments,
                                 labels=range(n_segments, 0, -1), duplicates='drop')

    # Frequency: higher is better
    df_rfm['f_score'] = pd.qcut(df_rfm['transaction_count'], n_segments,
                                 labels=range(1, n_segments + 1), duplicates='drop')

    # Monetary: higher is better
    df_rfm['m_score'] = pd.qcut(df_rfm['total_revenue'], n_segments,
                                 labels=range(1, n_segments + 1), duplicates='drop')

    # Composite RFM score
    df_rfm['rfm_score'] = (
        df_rfm['r_score'].astype(int) * 100 +
        df_rfm['f_score'].astype(int) * 10 +
        df_rfm['m_score'].astype(int)
    )

    # Create segment labels
    def label_rfm_segment(score):
        if score >= 333:
            return 'Champions'
        elif score >= 233:
            return 'Loyal'
        elif score >= 133:
            return 'Potential'
        else:
            return 'At Risk'

    df_rfm['segment'] = df_rfm['rfm_score'].apply(label_rfm_segment)

    logger.info("RFM segmentation complete")
    logger.info(f"Segment distribution:\n{df_rfm['segment'].value_counts()}")

    return df_rfm


def segment_kmeans(df: pd.DataFrame, n_segments: int = 4) -> pd.DataFrame:
    """K-means clustering segmentation."""
    from sklearn.cluster import KMeans

    # Select numeric features
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    # Remove ID columns
    feature_cols = [col for col in numeric_cols if 'id' not in col.lower()]

    # Prepare data
    X = df[feature_cols].fillna(df[feature_cols].median())

    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # K-means clustering
    kmeans = KMeans(n_clusters=n_segments, random_state=RANDOM_STATE, n_init=10)
    df['segment'] = kmeans.fit_predict(X_scaled)

    logger.info(f"K-means segmentation complete ({n_segments} clusters)")
    logger.info(f"Cluster sizes:\n{df['segment'].value_counts()}")

    return df


def segment_quantile(df: pd.DataFrame, n_segments: int = 4,
                    value_col: str = 'total_revenue') -> pd.DataFrame:
    """Simple quantile-based segmentation."""
    if value_col not in df.columns:
        raise KeyError(f"Column '{value_col}' not found")

    df['segment'] = pd.qcut(df[value_col], n_segments,
                            labels=[f'Segment_{i+1}' for i in range(n_segments)],
                            duplicates='drop')

    logger.info(f"Quantile segmentation complete on '{value_col}'")
    return df


def generate_summary_statistics(df: pd.DataFrame,
                                group_by: Optional[str] = None) -> pd.DataFrame:
    """
    Generate comprehensive summary statistics.

    Args:
        df (pd.DataFrame): Input dataframe
        group_by (Optional[str]): Column to group by

    Returns:
        pd.DataFrame: Summary statistics
    """
    logger.info("Generating summary statistics")

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if group_by is None:
        summary = df[numeric_cols].describe().T
        summary['median'] = df[numeric_cols].median()
        summary['null_count'] = df[numeric_cols].isnull().sum()
    else:
        summary = df.groupby(group_by)[numeric_cols].describe()

    return summary


def test_statistical_significance(group1: np.ndarray, group2: np.ndarray,
                                  test_type: str = 'auto') -> Dict[str, Any]:
    """
    Test statistical significance between two groups.

    Args:
        group1 (np.ndarray): First group data
        group2 (np.ndarray): Second group data
        test_type (str): Type of test ('auto', 't-test', 'mann-whitney')

    Returns:
        Dict[str, Any]: Test results
    """
    result = {}

    # Remove NaN values
    group1_clean = group1[~np.isnan(group1)]
    group2_clean = group2[~np.isnan(group2)]

    if len(group1_clean) < MIN_SAMPLE_SIZE or len(group2_clean) < MIN_SAMPLE_SIZE:
        result['error'] = 'Insufficient sample size'
        return result

    # Automatic test selection
    if test_type == 'auto':
        # Use Shapiro-Wilk test for normality
        from scipy.stats import shapiro
        _, p1 = shapiro(group1_clean[:5000])  # Limit to 5000 for performance
        _, p2 = shapiro(group2_clean[:5000])

        if p1 > 0.05 and p2 > 0.05:
            test_type = 't-test'
        else:
            test_type = 'mann-whitney'

    result['test_type'] = test_type

    if test_type == 't-test':
        from scipy.stats import ttest_ind
        stat, pval = ttest_ind(group1_clean, group2_clean, equal_var=False)
    else:  # mann-whitney
        stat, pval = mannwhitneyu(group1_clean, group2_clean, alternative='two-sided')

    result['statistic'] = float(stat)
    result['p_value'] = float(pval)
    result['is_significant'] = pval < ALPHA

    return result


def create_churn_prediction_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create engineered features for churn prediction model.

    Args:
        df (pd.DataFrame): Customer-level dataframe

    Returns:
        pd.DataFrame: Dataframe with engineered features
    """
    logger.info("Creating churn prediction features")

    df_features = df.copy()

    # Time-based features
    if 'days_since_last_transaction' in df.columns:
        df_features['recency_category'] = pd.cut(
            df['days_since_last_transaction'],
            bins=[0, 7, 30, 90, 365, float('inf')],
            labels=['very_recent', 'recent', 'medium', 'old', 'very_old']
        )

    # Spending behavior features
    if 'avg_order_value' in df.columns and 'transaction_count' in df.columns:
        df_features['spending_consistency'] = (
            df['std_order_value'] / df['avg_order_value']
        ).fillna(0)

    # Engagement features
    if 'transaction_frequency' in df.columns:
        df_features['engagement_level'] = pd.qcut(
            df['transaction_frequency'],
            q=3,
            labels=['low', 'medium', 'high'],
            duplicates='drop'
        )

    logger.info(f"Created {len(df_features.columns) - len(df.columns)} new features")

    return df_features


# Visualization functions

def plot_churn_rate_by_segment(df: pd.DataFrame, segment_col: str,
                               churn_col: str = 'is_churned',
                               figsize: Tuple[int, int] = (10, 6)) -> Figure:
    """Create bar plot of churn rate by segment."""
    fig, ax = plt.subplots(figsize=figsize)

    churn_by_segment = df.groupby(segment_col)[churn_col].mean().sort_values(ascending=False)

    churn_by_segment.plot(kind='bar', ax=ax, color='coral')
    ax.set_title('Churn Rate by Segment', fontsize=14, fontweight='bold')
    ax.set_xlabel(segment_col.replace('_', ' ').title(), fontsize=12)
    ax.set_ylabel('Churn Rate', fontsize=12)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.1%}'))
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    return fig


def plot_feature_distributions(df: pd.DataFrame, feature: str, churn_col: str = 'is_churned',
                               figsize: Tuple[int, int] = (12, 5)) -> Figure:
    """Create distribution plots comparing churned vs non-churned."""
    fig, axes = plt.subplots(1, 2, figsize=figsize)

    # Histogram
    df[df[churn_col] == 0][feature].hist(ax=axes[0], bins=30, alpha=0.6, label='Not Churned')
    df[df[churn_col] == 1][feature].hist(ax=axes[0], bins=30, alpha=0.6, label='Churned')
    axes[0].set_title(f'{feature} Distribution')
    axes[0].legend()

    # Box plot
    df.boxplot(column=feature, by=churn_col, ax=axes[1])
    axes[1].set_title(f'{feature} by Churn Status')

    plt.suptitle('')
    plt.tight_layout()
    return fig


if __name__ == "__main__":
    # Example usage
    print("Analysis Module - Example Usage")
    print("=" * 50)

    # Example: churn_rate = compute_churn_rate(df, 'is_churned')
    # Example: correlation = correlate_spend_churn(df, method='spearman')
    # Example: factors = analyze_churn_factors(df)
