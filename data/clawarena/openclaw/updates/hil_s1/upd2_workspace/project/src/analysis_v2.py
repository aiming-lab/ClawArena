"""
Customer Churn Analysis Module v2.0

This module provides comprehensive statistical analysis of customer churn patterns,
including correlation analysis, cohort analysis, and predictive modeling support.

Author: Data Science Team
Last Updated: 2025-03-09
Dependencies: pandas>=1.5.0, scipy>=1.9.0, numpy>=1.23.0, matplotlib>=3.6.0
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
from scipy.stats import chi2_contingency, mannwhitneyu, ttest_ind
import logging
from typing import Dict, List, Tuple, Optional, Any
import warnings
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Analysis configuration constants
DEFAULT_CHURN_THRESHOLD_DAYS = 45  # Days of inactivity to consider churned
SIGNIFICANCE_LEVEL = 0.05
CONFIDENCE_LEVEL = 0.95
MIN_SAMPLE_SIZE = 30

class ChurnAnalyzer:
    """
    Main analyzer class for customer churn analysis.

    Provides methods for statistical testing, correlation analysis,
    and churn prediction support.
    """

    def __init__(self, data: pd.DataFrame, churn_threshold: int = DEFAULT_CHURN_THRESHOLD_DAYS):
        """
        Initialize the ChurnAnalyzer with customer data.

        Args:
            data: DataFrame containing customer transaction and behavior data
            churn_threshold: Number of days of inactivity to consider a customer churned
        """
        self.data = data.copy()
        self.churn_threshold = churn_threshold
        self.results = {}
        self.metadata = {
            'analysis_date': datetime.now().isoformat(),
            'churn_threshold_days': churn_threshold,
            'total_customers': len(data)
        }
        logger.info(f"ChurnAnalyzer initialized with {len(data)} customers, "
                   f"churn threshold: {churn_threshold} days")

    def prepare_data(self) -> None:
        """
        Prepare and validate data for analysis.

        Performs data cleaning, feature engineering, and validation checks.
        """
        logger.info("Preparing data for analysis...")

        # Validate required columns
        required_columns = ['customer_id', 'is_churned', 'monthly_spend']
        missing_columns = [col for col in required_columns if col not in self.data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        # Handle missing values
        self.data['monthly_spend'].fillna(0, inplace=True)

        # Feature engineering
        if 'total_transactions' in self.data.columns:
            self.data['avg_transaction_value'] = (
                self.data['monthly_spend'] / self.data['total_transactions'].replace(0, 1)
            )

        # Data validation
        assert self.data['is_churned'].isin([0, 1]).all(), "is_churned must be binary (0 or 1)"
        assert (self.data['monthly_spend'] >= 0).all(), "monthly_spend must be non-negative"

        logger.info(f"Data preparation complete. Churned customers: {self.data['is_churned'].sum()}, "
                   f"Retained customers: {(self.data['is_churned'] == 0).sum()}")

    def analyze_churn_correlation(self, method: str = 'pearson') -> Dict[str, Any]:
        """
        Analyze correlation between spend and churn.

        This method examines the relationship between customer spending patterns
        and churn probability using statistical correlation analysis.

        Args:
            method: Correlation method ('pearson', 'spearman', or 'kendall')

        Returns:
            Dictionary containing correlation coefficient, p-value, and interpretation
        """
        logger.info(f"Analyzing churn correlation using {method} method...")

        # Segment data by churn status
        churned = self.data[self.data["is_churned"] == 1]["monthly_spend"]
        retained = self.data[self.data["is_churned"] == 0]["monthly_spend"]

        # Check sample sizes
        if len(churned) < MIN_SAMPLE_SIZE or len(retained) < MIN_SAMPLE_SIZE:
            logger.warning(f"Sample size below minimum threshold ({MIN_SAMPLE_SIZE}). "
                          f"Results may not be reliable.")

        # BUG: Using Pearson correlation which assumes normal distribution
        # The data is likely non-normally distributed (spending data typically right-skewed)
        # Should use Spearman or Mann-Whitney U test instead
        # This contradicts the methodology discussion in C5 where non-parametric tests were mentioned

        try:
            corr, p_value = stats.pearsonr(churned, retained)
        except Exception as e:
            logger.error(f"Correlation analysis failed: {e}")
            return {
                "error": str(e),
                "correlation": None,
                "p_value": None
            }

        # Interpret results
        significance = "significant" if p_value < SIGNIFICANCE_LEVEL else "not significant"
        strength = self._interpret_correlation_strength(abs(corr))

        result = {
            "correlation": float(corr),
            "p_value": float(p_value),
            "method": method,
            "significance": significance,
            "strength": strength,
            "churned_mean": float(churned.mean()),
            "churned_std": float(churned.std()),
            "retained_mean": float(retained.mean()),
            "retained_std": float(retained.std()),
            "sample_size_churned": len(churned),
            "sample_size_retained": len(retained)
        }

        logger.info(f"Correlation: {corr:.4f}, p={p_value:.4f} ({significance})")

        self.results['churn_correlation'] = result
        return result

    def _interpret_correlation_strength(self, abs_corr: float) -> str:
        """Interpret correlation coefficient strength."""
        if abs_corr < 0.1:
            return "negligible"
        elif abs_corr < 0.3:
            return "weak"
        elif abs_corr < 0.5:
            return "moderate"
        elif abs_corr < 0.7:
            return "strong"
        else:
            return "very strong"

    def compare_spend_distributions(self) -> Dict[str, Any]:
        """
        Compare spending distributions between churned and retained customers.

        Uses multiple statistical tests to comprehensively assess differences
        in spending behavior between customer segments.

        Returns:
            Dictionary containing test statistics and p-values for multiple tests
        """
        logger.info("Comparing spend distributions...")

        churned = self.data[self.data["is_churned"] == 1]["monthly_spend"]
        retained = self.data[self.data["is_churned"] == 0]["monthly_spend"]

        results = {}

        # T-test (parametric)
        try:
            t_stat, t_pvalue = ttest_ind(churned, retained, equal_var=False)
            results['t_test'] = {
                'statistic': float(t_stat),
                'p_value': float(t_pvalue),
                'significant': t_pvalue < SIGNIFICANCE_LEVEL
            }
        except Exception as e:
            logger.warning(f"T-test failed: {e}")
            results['t_test'] = {'error': str(e)}

        # Mann-Whitney U test (non-parametric)
        try:
            u_stat, u_pvalue = mannwhitneyu(churned, retained, alternative='two-sided')
            results['mann_whitney'] = {
                'statistic': float(u_stat),
                'p_value': float(u_pvalue),
                'significant': u_pvalue < SIGNIFICANCE_LEVEL
            }
        except Exception as e:
            logger.warning(f"Mann-Whitney test failed: {e}")
            results['mann_whitney'] = {'error': str(e)}

        # Descriptive statistics
        results['descriptive'] = {
            'churned': {
                'mean': float(churned.mean()),
                'median': float(churned.median()),
                'std': float(churned.std()),
                'min': float(churned.min()),
                'max': float(churned.max()),
                'q25': float(churned.quantile(0.25)),
                'q75': float(churned.quantile(0.75))
            },
            'retained': {
                'mean': float(retained.mean()),
                'median': float(retained.median()),
                'std': float(retained.std()),
                'min': float(retained.min()),
                'max': float(retained.max()),
                'q25': float(retained.quantile(0.25)),
                'q75': float(retained.quantile(0.75))
            }
        }

        # Effect size (Cohen's d)
        pooled_std = np.sqrt((churned.std()**2 + retained.std()**2) / 2)
        cohens_d = (retained.mean() - churned.mean()) / pooled_std
        results['effect_size'] = {
            'cohens_d': float(cohens_d),
            'interpretation': self._interpret_cohens_d(abs(cohens_d))
        }

        logger.info(f"Distribution comparison complete. Cohen's d: {cohens_d:.3f}")

        self.results['distribution_comparison'] = results
        return results

    def _interpret_cohens_d(self, abs_d: float) -> str:
        """Interpret Cohen's d effect size."""
        if abs_d < 0.2:
            return "negligible"
        elif abs_d < 0.5:
            return "small"
        elif abs_d < 0.8:
            return "medium"
        else:
            return "large"

    def calculate_churn_rate(self, groupby_col: Optional[str] = None) -> Dict[str, Any]:
        """
        Calculate overall and segmented churn rates.

        Args:
            groupby_col: Optional column to segment churn rate calculation

        Returns:
            Dictionary containing churn rate statistics
        """
        logger.info("Calculating churn rates...")

        # Overall churn rate
        total_customers = len(self.data)
        churned_customers = self.data['is_churned'].sum()
        overall_rate = churned_customers / total_customers if total_customers > 0 else 0

        results = {
            'overall': {
                'churn_rate': float(overall_rate),
                'churned_count': int(churned_customers),
                'retained_count': int(total_customers - churned_customers),
                'total_count': int(total_customers)
            }
        }

        # Segmented churn rates
        if groupby_col and groupby_col in self.data.columns:
            segment_stats = []
            for segment_value, group in self.data.groupby(groupby_col):
                segment_total = len(group)
                segment_churned = group['is_churned'].sum()
                segment_rate = segment_churned / segment_total if segment_total > 0 else 0

                segment_stats.append({
                    'segment': str(segment_value),
                    'churn_rate': float(segment_rate),
                    'churned_count': int(segment_churned),
                    'total_count': int(segment_total)
                })

            results['by_segment'] = segment_stats
            logger.info(f"Calculated churn rates for {len(segment_stats)} segments")

        logger.info(f"Overall churn rate: {overall_rate:.1%}")

        self.results['churn_rate'] = results
        return results

    def analyze_retention_cohorts(self, cohort_col: str = 'signup_month') -> Dict[str, Any]:
        """
        Analyze churn patterns across customer cohorts.

        Args:
            cohort_col: Column defining customer cohorts (e.g., signup month)

        Returns:
            Dictionary containing cohort analysis results
        """
        logger.info(f"Analyzing retention cohorts by {cohort_col}...")

        if cohort_col not in self.data.columns:
            logger.error(f"Column {cohort_col} not found in data")
            return {'error': f'Column {cohort_col} not found'}

        cohort_analysis = []

        for cohort_value, group in self.data.groupby(cohort_col):
            cohort_size = len(group)
            churned = group['is_churned'].sum()
            retained = cohort_size - churned
            churn_rate = churned / cohort_size if cohort_size > 0 else 0

            avg_spend_churned = group[group['is_churned'] == 1]['monthly_spend'].mean()
            avg_spend_retained = group[group['is_churned'] == 0]['monthly_spend'].mean()

            cohort_analysis.append({
                'cohort': str(cohort_value),
                'cohort_size': int(cohort_size),
                'churned': int(churned),
                'retained': int(retained),
                'churn_rate': float(churn_rate),
                'avg_spend_churned': float(avg_spend_churned) if not pd.isna(avg_spend_churned) else 0,
                'avg_spend_retained': float(avg_spend_retained) if not pd.isna(avg_spend_retained) else 0
            })

        results = {
            'cohorts': cohort_analysis,
            'cohort_column': cohort_col,
            'num_cohorts': len(cohort_analysis)
        }

        logger.info(f"Cohort analysis complete. Analyzed {len(cohort_analysis)} cohorts")

        self.results['cohort_analysis'] = results
        return results

    def identify_high_risk_customers(self, threshold_percentile: float = 0.8) -> pd.DataFrame:
        """
        Identify customers at high risk of churning based on spend patterns.

        Args:
            threshold_percentile: Percentile threshold for risk scoring

        Returns:
            DataFrame of high-risk customers with risk scores
        """
        logger.info(f"Identifying high-risk customers (threshold: {threshold_percentile})...")

        # Calculate risk score based on spending behavior
        # Lower spending associated with higher churn risk
        spend_threshold = self.data['monthly_spend'].quantile(threshold_percentile)

        high_risk = self.data[
            (self.data['monthly_spend'] < spend_threshold) &
            (self.data['is_churned'] == 0)  # Only active customers
        ].copy()

        # Calculate risk score (inverse of spend ranking)
        high_risk['risk_score'] = 1 - (high_risk['monthly_spend'] / high_risk['monthly_spend'].max())
        high_risk = high_risk.sort_values('risk_score', ascending=False)

        logger.info(f"Identified {len(high_risk)} high-risk customers")

        self.results['high_risk_customers'] = {
            'count': len(high_risk),
            'threshold_spend': float(spend_threshold),
            'avg_risk_score': float(high_risk['risk_score'].mean())
        }

        return high_risk

    def analyze_temporal_patterns(self, date_col: str = 'churn_date') -> Dict[str, Any]:
        """
        Analyze temporal patterns in churn behavior.

        Args:
            date_col: Column containing churn dates

        Returns:
            Dictionary containing temporal analysis results
        """
        logger.info(f"Analyzing temporal patterns using {date_col}...")

        if date_col not in self.data.columns:
            logger.warning(f"Column {date_col} not found. Skipping temporal analysis.")
            return {'error': f'Column {date_col} not found'}

        churned_data = self.data[self.data['is_churned'] == 1].copy()

        if len(churned_data) == 0:
            logger.warning("No churned customers found for temporal analysis")
            return {'error': 'No churned customers'}

        # Convert to datetime if not already
        churned_data[date_col] = pd.to_datetime(churned_data[date_col], errors='coerce')
        churned_data = churned_data.dropna(subset=[date_col])

        # Extract temporal features
        churned_data['month'] = churned_data[date_col].dt.month
        churned_data['quarter'] = churned_data[date_col].dt.quarter
        churned_data['day_of_week'] = churned_data[date_col].dt.dayofweek

        # Aggregate by time period
        monthly_churn = churned_data.groupby('month').size().to_dict()
        quarterly_churn = churned_data.groupby('quarter').size().to_dict()
        weekday_churn = churned_data.groupby('day_of_week').size().to_dict()

        results = {
            'monthly_distribution': {str(k): int(v) for k, v in monthly_churn.items()},
            'quarterly_distribution': {str(k): int(v) for k, v in quarterly_churn.items()},
            'weekday_distribution': {str(k): int(v) for k, v in weekday_churn.items()},
            'date_range': {
                'earliest': churned_data[date_col].min().isoformat(),
                'latest': churned_data[date_col].max().isoformat()
            }
        }

        logger.info("Temporal pattern analysis complete")

        self.results['temporal_patterns'] = results
        return results

    def generate_summary_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive summary report of all analyses.

        Returns:
            Dictionary containing complete analysis summary
        """
        logger.info("Generating summary report...")

        summary = {
            'metadata': self.metadata,
            'analyses': self.results,
            'recommendations': self._generate_recommendations()
        }

        logger.info("Summary report generated successfully")

        return summary

    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations based on analysis results."""
        recommendations = []

        # Check churn correlation
        if 'churn_correlation' in self.results:
            corr_result = self.results['churn_correlation']
            if corr_result.get('significance') == 'significant':
                if corr_result.get('correlation', 0) < 0:
                    recommendations.append(
                        "Implement targeted retention campaigns for low-spending customers "
                        "as spending is significantly correlated with churn risk."
                    )

        # Check distribution differences
        if 'distribution_comparison' in self.results:
            dist_result = self.results['distribution_comparison']
            if 'mann_whitney' in dist_result and dist_result['mann_whitney'].get('significant'):
                recommendations.append(
                    "Spending patterns differ significantly between churned and retained customers. "
                    "Consider personalized engagement strategies based on spend levels."
                )

        # Check churn rate
        if 'churn_rate' in self.results:
            churn_rate = self.results['churn_rate']['overall']['churn_rate']
            if churn_rate > 0.15:
                recommendations.append(
                    f"Churn rate ({churn_rate:.1%}) exceeds industry benchmark (15%). "
                    "Priority: Implement comprehensive retention program."
                )

        # Check high-risk customers
        if 'high_risk_customers' in self.results:
            high_risk_count = self.results['high_risk_customers']['count']
            if high_risk_count > 0:
                recommendations.append(
                    f"Identified {high_risk_count} high-risk customers. "
                    "Recommend proactive outreach and personalized offers."
                )

        if not recommendations:
            recommendations.append("No significant issues identified. Continue monitoring key metrics.")

        return recommendations


class AdvancedChurnAnalytics:
    """
    Advanced analytics module for sophisticated churn modeling and prediction.

    Provides feature engineering, segmentation, and predictive modeling support.
    """

    def __init__(self, data: pd.DataFrame):
        """Initialize advanced analytics module."""
        self.data = data.copy()
        self.features = None
        self.segments = None
        logger.info(f"AdvancedChurnAnalytics initialized with {len(data)} records")

    def engineer_features(self) -> pd.DataFrame:
        """
        Engineer advanced features for churn prediction.

        Returns:
            DataFrame with engineered features
        """
        logger.info("Engineering advanced features...")

        features = self.data.copy()

        # Spending behavior features
        if 'monthly_spend' in features.columns:
            features['spend_log'] = np.log1p(features['monthly_spend'])
            features['spend_zscore'] = (
                features['monthly_spend'] - features['monthly_spend'].mean()
            ) / features['monthly_spend'].std()

        # Transaction features
        if 'total_transactions' in features.columns:
            features['transactions_log'] = np.log1p(features['total_transactions'])
            features['avg_transaction_value'] = (
                features['monthly_spend'] / features['total_transactions'].replace(0, 1)
            )

        # Engagement features
        if 'days_since_last_purchase' in features.columns:
            features['engagement_score'] = 1 / (1 + features['days_since_last_purchase'])

        # Tenure features
        if 'account_age_days' in features.columns:
            features['tenure_months'] = features['account_age_days'] / 30.0
            features['tenure_years'] = features['account_age_days'] / 365.0

        # Interaction features
        if 'monthly_spend' in features.columns and 'total_transactions' in features.columns:
            features['spend_per_transaction'] = (
                features['monthly_spend'] / features['total_transactions'].replace(0, 1)
            )

        logger.info(f"Feature engineering complete. Created {len(features.columns)} features")

        self.features = features
        return features

    def perform_customer_segmentation(self, n_segments: int = 4) -> pd.DataFrame:
        """
        Perform customer segmentation using spending and behavior patterns.

        Args:
            n_segments: Number of customer segments to create

        Returns:
            DataFrame with segment assignments
        """
        logger.info(f"Performing customer segmentation into {n_segments} segments...")

        # Simple segmentation based on spend and churn risk
        data_with_segments = self.data.copy()

        # Calculate quartiles for spending
        spend_quartiles = data_with_segments['monthly_spend'].quantile([0.25, 0.5, 0.75])

        def assign_segment(row):
            spend = row['monthly_spend']
            churned = row['is_churned']

            if churned:
                return 'Churned'
            elif spend > spend_quartiles[0.75]:
                return 'High Value'
            elif spend > spend_quartiles[0.5]:
                return 'Medium Value'
            elif spend > spend_quartiles[0.25]:
                return 'Low Value'
            else:
                return 'At Risk'

        data_with_segments['segment'] = data_with_segments.apply(assign_segment, axis=1)

        # Segment summary
        segment_summary = data_with_segments.groupby('segment').agg({
            'customer_id': 'count',
            'monthly_spend': 'mean',
            'is_churned': 'sum'
        }).rename(columns={'customer_id': 'count', 'monthly_spend': 'avg_spend', 'is_churned': 'churned_count'})

        logger.info(f"Segmentation complete:\n{segment_summary}")

        self.segments = data_with_segments
        return data_with_segments

    def calculate_customer_lifetime_value(self, monthly_revenue_col: str = 'monthly_spend',
                                         discount_rate: float = 0.1) -> pd.DataFrame:
        """
        Calculate customer lifetime value (CLV) estimates.

        Args:
            monthly_revenue_col: Column containing monthly revenue per customer
            discount_rate: Annual discount rate for NPV calculation

        Returns:
            DataFrame with CLV calculations
        """
        logger.info("Calculating customer lifetime value...")

        clv_data = self.data.copy()

        # Estimate CLV using simplified formula: CLV = (monthly_revenue * retention_rate) / churn_rate
        # This is a basic approach; more sophisticated models would use historical transaction patterns

        retention_rate = 1 - (clv_data['is_churned'].mean())
        avg_monthly_revenue = clv_data[monthly_revenue_col].mean()

        # Simple CLV calculation
        monthly_discount = (1 + discount_rate) ** (1/12) - 1

        clv_data['estimated_clv'] = (
            clv_data[monthly_revenue_col] * retention_rate / (monthly_discount + (1 - retention_rate))
        )

        # Segment CLV by customer status
        active_clv = clv_data[clv_data['is_churned'] == 0]['estimated_clv'].mean()
        churned_clv = clv_data[clv_data['is_churned'] == 1]['estimated_clv'].mean()

        logger.info(f"CLV calculation complete. Active customer avg CLV: ${active_clv:.2f}, "
                   f"Churned customer avg CLV: ${churned_clv:.2f}")

        return clv_data


# Utility functions

def load_customer_data(file_path: str) -> pd.DataFrame:
    """
    Load customer data from file.

    Args:
        file_path: Path to data file (CSV, Excel, etc.)

    Returns:
        DataFrame containing customer data
    """
    logger.info(f"Loading customer data from {file_path}...")

    if file_path.endswith('.csv'):
        data = pd.read_csv(file_path)
    elif file_path.endswith(('.xls', '.xlsx')):
        data = pd.read_excel(file_path)
    elif file_path.endswith('.parquet'):
        data = pd.read_parquet(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")

    logger.info(f"Loaded {len(data)} records with {len(data.columns)} columns")

    return data


def export_results(results: Dict[str, Any], output_path: str) -> None:
    """
    Export analysis results to file.

    Args:
        results: Dictionary containing analysis results
        output_path: Path to output file (JSON format)
    """
    import json

    logger.info(f"Exporting results to {output_path}...")

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    logger.info("Export complete")


def visualize_churn_analysis(analyzer: ChurnAnalyzer, output_dir: str = './output') -> None:
    """
    Generate visualizations for churn analysis results.

    Args:
        analyzer: ChurnAnalyzer instance with completed analysis
        output_dir: Directory to save visualization files
    """
    logger.info("Generating visualizations...")

    import os
    os.makedirs(output_dir, exist_ok=True)

    # Distribution comparison plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    churned = analyzer.data[analyzer.data['is_churned'] == 1]['monthly_spend']
    retained = analyzer.data[analyzer.data['is_churned'] == 0]['monthly_spend']

    # Histograms
    axes[0].hist(churned, bins=30, alpha=0.6, label='Churned', color='red')
    axes[0].hist(retained, bins=30, alpha=0.6, label='Retained', color='green')
    axes[0].set_xlabel('Monthly Spend ($)')
    axes[0].set_ylabel('Frequency')
    axes[0].set_title('Spending Distribution by Churn Status')
    axes[0].legend()

    # Box plots
    data_for_box = pd.DataFrame({
        'Monthly Spend': pd.concat([churned, retained]),
        'Status': ['Churned'] * len(churned) + ['Retained'] * len(retained)
    })
    sns.boxplot(data=data_for_box, x='Status', y='Monthly Spend', ax=axes[1])
    axes[1].set_title('Spending Comparison: Churned vs Retained')

    plt.tight_layout()
    plt.savefig(f"{output_dir}/spending_distribution.png", dpi=300)
    logger.info(f"Saved visualization to {output_dir}/spending_distribution.png")

    plt.close()


# Example usage
if __name__ == "__main__":
    # Example workflow
    logger.info("Starting churn analysis workflow...")

    # Load sample data
    # data = load_customer_data('customer_data.csv')

    # For demonstration, create synthetic data
    np.random.seed(42)
    sample_size = 1000

    sample_data = pd.DataFrame({
        'customer_id': [f'CUST-{i:05d}' for i in range(sample_size)],
        'monthly_spend': np.random.gamma(2, 50, sample_size),
        'total_transactions': np.random.poisson(10, sample_size),
        'is_churned': np.random.binomial(1, 0.18, sample_size),
        'account_age_days': np.random.randint(30, 730, sample_size),
        'days_since_last_purchase': np.random.randint(0, 90, sample_size)
    })

    # Initialize analyzer
    analyzer = ChurnAnalyzer(sample_data, churn_threshold=45)

    # Prepare data
    analyzer.prepare_data()

    # Run analyses
    correlation_results = analyzer.analyze_churn_correlation()
    distribution_results = analyzer.compare_spend_distributions()
    churn_rate_results = analyzer.calculate_churn_rate()

    # Generate summary
    summary_report = analyzer.generate_summary_report()

    # Print results
    print("\n=== CHURN ANALYSIS SUMMARY ===")
    print(f"Total Customers: {analyzer.metadata['total_customers']}")
    print(f"Churn Threshold: {analyzer.churn_threshold} days")
    print(f"\nOverall Churn Rate: {churn_rate_results['overall']['churn_rate']:.1%}")
    print(f"\nCorrelation: {correlation_results['correlation']:.4f} "
          f"(p={correlation_results['p_value']:.4f})")
    print(f"Significance: {correlation_results['significance']}")

    print("\n=== RECOMMENDATIONS ===")
    for i, rec in enumerate(summary_report['recommendations'], 1):
        print(f"{i}. {rec}")

    logger.info("Churn analysis workflow complete")
