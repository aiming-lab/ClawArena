"""
Test Suite for Data Loader Module

This comprehensive test suite validates the functionality of the data_loader module,
including data loading, validation, cleaning, and transformation operations.

The tests are organized into several test classes:
- TestDataLoading: Tests for basic data loading functionality
- TestDateParsing: Tests for date parsing with various formats
- TestDataValidation: Tests for data validation logic
- TestDataCleaning: Tests for data cleaning operations
- TestFilteringAndAggregation: Tests for filtering and aggregation functions

Author: QA Team
Created: 2025-03-02
Last Modified: 2025-03-12
Version: 1.0.0

Dependencies:
    - pytest>=8.0.0
    - pandas>=2.2.0
    - numpy>=1.26.0

Usage:
    Run all tests:
        $ pytest tests/test_data_loader.py -v

    Run specific test class:
        $ pytest tests/test_data_loader.py::TestDataLoading -v

    Run with coverage:
        $ pytest tests/test_data_loader.py --cov=src.data_loader --cov-report=html
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import sys
import tempfile
import shutil

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from data_loader import (
    load_transactions,
    parse_dates,
    filter_active,
    validate_dataframe,
    clean_transactions_dataframe,
    load_customers,
    merge_transaction_customer_data,
    aggregate_customer_metrics,
    detect_data_quality_issues,
    DataLoadError,
    DataValidationError,
    DateParseError
)


# ============================================================================
# TEST FIXTURES
# ============================================================================

@pytest.fixture
def sample_transactions_df():
    """
    Create a sample transactions dataframe for testing.

    Returns:
        pd.DataFrame: Sample transactions data
    """
    data = {
        'transaction_id': [f'T{i:04d}' for i in range(1, 101)],
        'customer_id': [f'C{i%20:03d}' for i in range(1, 101)],
        'date': pd.date_range(start='2024-01-01', periods=100, freq='D'),
        'order_value': np.random.uniform(10, 500, 100),
        'product_id': [f'P{i%10:02d}' for i in range(1, 101)],
        'quantity': np.random.randint(1, 10, 100)
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_customers_df():
    """
    Create a sample customers dataframe for testing.

    Returns:
        pd.DataFrame: Sample customer data
    """
    data = {
        'customer_id': [f'C{i:03d}' for i in range(20)],
        'signup_date': pd.date_range(start='2023-01-01', periods=20, freq='ME'),
        'email': [f'customer{i}@example.com' for i in range(20)],
        'segment': np.random.choice(['Premium', 'Standard', 'Basic'], 20),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 20),
        'age': np.random.randint(18, 70, 20),
        'gender': np.random.choice(['M', 'F', 'Other'], 20)
    }
    return pd.DataFrame(data)


@pytest.fixture
def temp_data_dir():
    """
    Create a temporary directory for test data files.

    Yields:
        Path: Path to temporary directory
    """
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_csv_file(sample_transactions_df, temp_data_dir):
    """
    Create a sample CSV file for testing file loading.

    Args:
        sample_transactions_df: Sample dataframe fixture
        temp_data_dir: Temporary directory fixture

    Returns:
        Path: Path to created CSV file
    """
    csv_path = temp_data_dir / 'test_transactions.csv'
    sample_transactions_df.to_csv(csv_path, index=False)
    return csv_path


@pytest.fixture
def sample_df_with_nulls():
    """
    Create a dataframe with missing values for testing validation.

    Returns:
        pd.DataFrame: Dataframe with nulls
    """
    data = {
        'transaction_id': ['T001', 'T002', None, 'T004', 'T005'],
        'customer_id': ['C001', None, 'C003', 'C004', 'C005'],
        'date': ['2024-01-01', '2024-01-02', '2024-01-03', None, '2024-01-05'],
        'order_value': [100.0, None, 300.0, 400.0, None],
        'quantity': [1, 2, None, 4, 5]
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_df_with_duplicates(sample_transactions_df):
    """
    Create a dataframe with duplicate rows for testing cleaning.

    Args:
        sample_transactions_df: Sample dataframe fixture

    Returns:
        pd.DataFrame: Dataframe with duplicates
    """
    # Add duplicate rows
    duplicates = sample_transactions_df.head(10).copy()
    df_with_dupes = pd.concat([sample_transactions_df, duplicates], ignore_index=True)
    return df_with_dupes


# ============================================================================
# TEST CLASS: Data Loading
# ============================================================================

class TestDataLoading:
    """Test suite for data loading functionality."""

    def test_load_transactions_success(self, sample_csv_file):
        """Test successful loading of transactions from CSV file."""
        df = load_transactions(str(sample_csv_file), validate=False, clean=False)

        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert 'transaction_id' in df.columns
        assert 'customer_id' in df.columns

    def test_load_transactions_file_not_found(self):
        """Test that FileNotFoundError is raised for missing file."""
        with pytest.raises(DataLoadError, match="File not found"):
            load_transactions('/nonexistent/path/file.csv')

    def test_load_transactions_encoding_fallback(self, temp_data_dir):
        """Test encoding fallback mechanism for non-UTF8 files."""
        # Create a file with latin-1 encoding
        csv_path = temp_data_dir / 'latin1_file.csv'
        data = "transaction_id,customer_id,date,amount\nT001,C001,2024-01-01,100\n"

        with open(csv_path, 'w', encoding='latin-1') as f:
            f.write(data)

        # Should successfully load with fallback encoding
        df = load_transactions(str(csv_path), validate=False, clean=False)
        assert len(df) == 1

    def test_load_transactions_with_validation(self, sample_csv_file):
        """Test loading with validation enabled."""
        df = load_transactions(str(sample_csv_file), validate=True, clean=False)
        assert isinstance(df, pd.DataFrame)

    def test_load_transactions_with_cleaning(self, sample_csv_file):
        """Test loading with cleaning enabled."""
        df = load_transactions(str(sample_csv_file), validate=False, clean=True)
        assert isinstance(df, pd.DataFrame)
        # Check that cleaning was applied (no duplicates)
        assert df.duplicated().sum() == 0

    def test_load_customers_success(self, sample_customers_df, temp_data_dir):
        """Test successful loading of customer data."""
        csv_path = temp_data_dir / 'customers.csv'
        sample_customers_df.to_csv(csv_path, index=False)

        df = load_customers(str(csv_path))
        assert isinstance(df, pd.DataFrame)
        assert len(df) == len(sample_customers_df)
        assert 'customer_id' in df.columns

    def test_column_name_standardization(self, temp_data_dir):
        """Test that column names are standardized (lowercase, underscores)."""
        # Create CSV with mixed case column names
        data = pd.DataFrame({
            'Transaction ID': ['T001'],
            'Customer ID': ['C001'],
            'Order Date': ['2024-01-01'],
            'Order Value': [100]
        })
        csv_path = temp_data_dir / 'mixed_case.csv'
        data.to_csv(csv_path, index=False)

        df = load_transactions(str(csv_path), validate=False, clean=False)

        # Check that columns are lowercase with underscores
        assert 'transaction_id' in df.columns
        assert 'customer_id' in df.columns
        assert 'order_date' in df.columns
        assert 'order_value' in df.columns


# ============================================================================
# TEST CLASS: Date Parsing
# ============================================================================

class TestDateParsing:
    """Test suite for date parsing functionality."""

    def test_parse_dates_success(self):
        """Test successful parsing of dates in YYYY-MM-DD format."""
        df = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02', '2024-01-03']
        })

        result_df = parse_dates(df, 'date')

        assert pd.api.types.is_datetime64_any_dtype(result_df['date'])
        assert result_df['date'].notna().all()

    def test_parse_dates_with_nulls(self):
        """Test parsing dates with null values."""
        df = pd.DataFrame({
            'date': ['2024-01-01', None, '2024-01-03']
        })

        result_df = parse_dates(df, 'date')

        assert pd.api.types.is_datetime64_any_dtype(result_df['date'])
        assert result_df['date'].isna().sum() == 1

    def test_parse_dates_column_not_found(self):
        """Test that KeyError is raised for missing column."""
        df = pd.DataFrame({'other_col': [1, 2, 3]})

        with pytest.raises(KeyError, match="not found in dataframe"):
            parse_dates(df, 'date')

    def test_parse_dates_already_datetime(self):
        """Test that already-datetime columns are handled correctly."""
        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=3)
        })

        result_df = parse_dates(df, 'date')

        assert pd.api.types.is_datetime64_any_dtype(result_df['date'])
        assert len(result_df) == 3

    def test_parse_dates_invalid_format_raises_error(self):
        """
        Test that invalid date formats raise DateParseError.

        This test validates the BUG in parse_dates function where it only
        handles YYYY-MM-DD format and fails on other formats like M/D/YYYY.
        """
        df = pd.DataFrame({
            'date': ['3/15/2024', '3/16/2024', '3/17/2024']  # US format
        })

        # This should raise DateParseError due to the bug
        with pytest.raises(DateParseError, match="Date parsing failed"):
            parse_dates(df, 'date')

    def test_parse_dates_mixed_formats(self):
        """Test parsing with mixed date formats (should fail with current implementation)."""
        df = pd.DataFrame({
            'date': ['2024-01-01', '1/2/2024', '2024-01-03']  # Mixed formats
        })

        # Current implementation will fail on mixed formats
        with pytest.raises(DateParseError):
            parse_dates(df, 'date')

    def test_parse_dates_validates_range(self):
        """Test that unreasonable date ranges generate warnings."""
        df = pd.DataFrame({
            'date': ['1800-01-01', '2024-01-01', '2030-01-01']
        })

        # Should parse but may log warnings about unusual dates
        result_df = parse_dates(df, 'date')
        assert pd.api.types.is_datetime64_any_dtype(result_df['date'])


# ============================================================================
# TEST CLASS: Data Validation
# ============================================================================

class TestDataValidation:
    """Test suite for data validation functionality."""

    def test_validate_dataframe_valid_transactions(self, sample_transactions_df):
        """Test validation passes for valid transactions dataframe."""
        is_valid, errors = validate_dataframe(sample_transactions_df, data_type='transactions')

        assert is_valid is True
        assert len(errors) == 0

    def test_validate_dataframe_empty(self):
        """Test validation fails for empty dataframe."""
        df = pd.DataFrame()
        is_valid, errors = validate_dataframe(df)

        assert is_valid is False
        assert any('empty' in error.lower() for error in errors)

    def test_validate_dataframe_missing_required_columns(self):
        """Test validation fails when required columns are missing."""
        df = pd.DataFrame({
            'customer_id': ['C001', 'C002'],
            # Missing 'transaction_id' and 'date'
        })

        is_valid, errors = validate_dataframe(df, data_type='transactions')

        assert is_valid is False
        assert any('missing' in error.lower() for error in errors)

    def test_validate_dataframe_with_duplicates(self, sample_df_with_duplicates):
        """Test validation detects duplicate rows."""
        is_valid, errors = validate_dataframe(sample_df_with_duplicates, strict=True)

        assert is_valid is False
        assert any('duplicate' in error.lower() for error in errors)

    def test_validate_dataframe_high_null_percentage(self, sample_df_with_nulls):
        """Test validation detects columns with high null percentages."""
        is_valid, errors = validate_dataframe(sample_df_with_nulls, strict=True)

        # With strict=True, should fail on high null percentage
        assert is_valid is False

    def test_validate_dataframe_negative_amounts(self):
        """Test validation detects negative transaction amounts."""
        df = pd.DataFrame({
            'transaction_id': ['T001', 'T002', 'T003'],
            'customer_id': ['C001', 'C002', 'C003'],
            'date': pd.date_range('2024-01-01', periods=3),
            'order_value': [100, -50, 200]  # Negative value
        })

        is_valid, errors = validate_dataframe(df, data_type='transactions', strict=True)

        assert is_valid is False
        assert any('negative' in error.lower() for error in errors)

    def test_validate_dataframe_customers(self, sample_customers_df):
        """Test validation for customers dataframe."""
        is_valid, errors = validate_dataframe(sample_customers_df, data_type='customers')

        assert is_valid is True
        assert len(errors) == 0

    def test_validate_dataframe_wrong_data_types(self):
        """Test validation detects incorrect data types."""
        df = pd.DataFrame({
            'transaction_id': ['T001', 'T002'],
            'customer_id': ['C001', 'C002'],
            'date': pd.date_range('2024-01-01', periods=2),
            'order_value': ['not_a_number', 'also_not']  # Should be numeric
        })

        is_valid, errors = validate_dataframe(df, data_type='transactions')

        assert is_valid is False
        assert any('numeric' in error.lower() for error in errors)


# ============================================================================
# TEST CLASS: Data Cleaning
# ============================================================================

class TestDataCleaning:
    """Test suite for data cleaning functionality."""

    def test_clean_removes_duplicates(self, sample_df_with_duplicates):
        """Test that cleaning removes duplicate rows."""
        initial_count = len(sample_df_with_duplicates)
        duplicate_count = sample_df_with_duplicates.duplicated().sum()

        cleaned_df = clean_transactions_dataframe(sample_df_with_duplicates)

        assert len(cleaned_df) == initial_count - duplicate_count
        assert cleaned_df.duplicated().sum() == 0

    def test_clean_removes_nulls_in_critical_columns(self, sample_df_with_nulls):
        """Test that cleaning removes rows with nulls in critical columns."""
        cleaned_df = clean_transactions_dataframe(sample_df_with_nulls)

        # Should have removed rows with null customer_id or transaction_id
        assert cleaned_df['customer_id'].notna().all()
        assert cleaned_df['transaction_id'].notna().all()

    def test_clean_standardizes_id_formats(self):
        """Test that cleaning standardizes ID column formats."""
        df = pd.DataFrame({
            'transaction_id': ['  t001  ', 'T002', 't003'],
            'customer_id': ['c001', 'C002  ', '  C003'],
            'date': pd.date_range('2024-01-01', periods=3),
            'order_value': [100, 200, 300]
        })

        cleaned_df = clean_transactions_dataframe(df)

        # IDs should be uppercase and trimmed
        assert all(cleaned_df['transaction_id'].str.isupper())
        assert all(cleaned_df['customer_id'].str.isupper())
        assert not any(cleaned_df['transaction_id'].str.contains('  '))

    def test_clean_converts_amounts_to_numeric(self):
        """Test that cleaning converts amount columns to numeric."""
        df = pd.DataFrame({
            'transaction_id': ['T001', 'T002', 'T003'],
            'customer_id': ['C001', 'C002', 'C003'],
            'date': pd.date_range('2024-01-01', periods=3),
            'order_value': ['100', '200.50', '300']  # String amounts
        })

        cleaned_df = clean_transactions_dataframe(df)

        assert pd.api.types.is_numeric_dtype(cleaned_df['order_value'])

    def test_clean_removes_negative_amounts(self):
        """Test that cleaning removes negative transaction amounts."""
        df = pd.DataFrame({
            'transaction_id': ['T001', 'T002', 'T003', 'T004'],
            'customer_id': ['C001', 'C002', 'C003', 'C004'],
            'date': pd.date_range('2024-01-01', periods=4),
            'order_value': [100, -50, 200, -30]
        })

        cleaned_df = clean_transactions_dataframe(df)

        assert all(cleaned_df['order_value'] >= 0)
        assert len(cleaned_df) == 2  # Should have only 2 positive values

    def test_clean_removes_outliers(self):
        """Test that cleaning removes extreme outliers."""
        df = pd.DataFrame({
            'transaction_id': [f'T{i:03d}' for i in range(100)],
            'customer_id': [f'C{i:03d}' for i in range(100)],
            'date': pd.date_range('2024-01-01', periods=100),
            'order_value': [100] * 99 + [1000000]  # One extreme outlier
        })

        cleaned_df = clean_transactions_dataframe(df)

        # Extreme outlier should be removed
        assert cleaned_df['order_value'].max() < 1000000

    def test_clean_preserves_data_integrity(self, sample_transactions_df):
        """Test that cleaning preserves data integrity for valid records."""
        initial_valid_count = len(sample_transactions_df)

        cleaned_df = clean_transactions_dataframe(sample_transactions_df)

        # All valid records should be preserved
        assert len(cleaned_df) == initial_valid_count
        assert set(cleaned_df.columns) == set(sample_transactions_df.columns)


# ============================================================================
# TEST CLASS: Filtering and Aggregation
# ============================================================================

class TestFilteringAndAggregation:
    """Test suite for filtering and aggregation operations."""

    def test_filter_active_customers(self):
        """Test filtering for active customers based on activity threshold."""
        df = pd.DataFrame({
            'customer_id': ['C001', 'C002', 'C003', 'C004'],
            'last_active': [
                pd.Timestamp.now() - pd.Timedelta(days=10),  # Active
                pd.Timestamp.now() - pd.Timedelta(days=45),  # Inactive
                pd.Timestamp.now() - pd.Timedelta(days=5),   # Active
                pd.Timestamp.now() - pd.Timedelta(days=100)  # Inactive
            ]
        })

        active_df = filter_active(df, days=30)

        assert len(active_df) == 2
        assert 'C001' in active_df['customer_id'].values
        assert 'C003' in active_df['customer_id'].values

    def test_filter_active_custom_threshold(self):
        """Test filtering with custom activity threshold."""
        df = pd.DataFrame({
            'customer_id': ['C001', 'C002', 'C003'],
            'last_active': [
                pd.Timestamp.now() - pd.Timedelta(days=5),
                pd.Timestamp.now() - pd.Timedelta(days=10),
                pd.Timestamp.now() - pd.Timedelta(days=15)
            ]
        })

        # With 7-day threshold
        active_df = filter_active(df, days=7)
        assert len(active_df) == 1

        # With 20-day threshold
        active_df = filter_active(df, days=20)
        assert len(active_df) == 3

    def test_filter_active_column_not_found(self):
        """Test that KeyError is raised when date column is missing."""
        df = pd.DataFrame({
            'customer_id': ['C001', 'C002']
        })

        with pytest.raises(KeyError, match="not found"):
            filter_active(df, days=30)

    def test_filter_active_negative_days(self):
        """Test that ValueError is raised for negative days parameter."""
        df = pd.DataFrame({
            'customer_id': ['C001'],
            'last_active': [pd.Timestamp.now()]
        })

        with pytest.raises(ValueError, match="non-negative"):
            filter_active(df, days=-10)

    def test_aggregate_customer_metrics(self, sample_transactions_df):
        """Test aggregation of transaction data to customer-level metrics."""
        result_df = aggregate_customer_metrics(
            sample_transactions_df,
            customer_id_col='customer_id',
            amount_col='order_value',
            date_col='date'
        )

        assert 'total_revenue' in result_df.columns
        assert 'avg_order_value' in result_df.columns
        assert 'transaction_count' in result_df.columns
        assert 'days_since_last_transaction' in result_df.columns

        # Should have one row per unique customer
        expected_customers = sample_transactions_df['customer_id'].nunique()
        assert len(result_df) == expected_customers

    def test_aggregate_customer_metrics_calculations(self):
        """Test that aggregated metrics are calculated correctly."""
        df = pd.DataFrame({
            'customer_id': ['C001', 'C001', 'C002'],
            'order_value': [100, 200, 150],
            'date': pd.date_range('2024-01-01', periods=3)
        })

        result_df = aggregate_customer_metrics(df)

        # Check C001 metrics
        c001_row = result_df[result_df['customer_id'] == 'C001'].iloc[0]
        assert c001_row['total_revenue'] == 300
        assert c001_row['avg_order_value'] == 150
        assert c001_row['transaction_count'] == 2

    def test_merge_transaction_customer_data(self, sample_transactions_df, sample_customers_df):
        """Test merging transaction and customer dataframes."""
        merged_df = merge_transaction_customer_data(
            sample_transactions_df,
            sample_customers_df,
            how='left'
        )

        assert len(merged_df) >= len(sample_transactions_df)
        # Should have columns from both dataframes
        assert 'transaction_id' in merged_df.columns
        assert 'segment' in merged_df.columns
        assert 'region' in merged_df.columns

    def test_merge_missing_key_column(self, sample_transactions_df):
        """Test that merge raises error when key column is missing."""
        customers_df = pd.DataFrame({
            'cust_id': ['C001', 'C002'],  # Wrong column name
            'segment': ['Premium', 'Standard']
        })

        with pytest.raises(KeyError, match="customer_id"):
            merge_transaction_customer_data(sample_transactions_df, customers_df)


# ============================================================================
# TEST CLASS: Data Quality
# ============================================================================

class TestDataQuality:
    """Test suite for data quality assessment."""

    def test_detect_data_quality_issues(self, sample_transactions_df):
        """Test detection of data quality issues."""
        quality_report = detect_data_quality_issues(sample_transactions_df)

        assert 'total_rows' in quality_report
        assert 'total_columns' in quality_report
        assert 'duplicate_rows' in quality_report
        assert 'columns_with_nulls' in quality_report

        assert quality_report['total_rows'] == len(sample_transactions_df)
        assert quality_report['total_columns'] == len(sample_transactions_df.columns)

    def test_detect_quality_issues_with_nulls(self, sample_df_with_nulls):
        """Test that quality assessment detects null values."""
        quality_report = detect_data_quality_issues(sample_df_with_nulls)

        assert len(quality_report['columns_with_nulls']) > 0

        # Check that null percentages are calculated correctly
        for col, stats in quality_report['columns_with_nulls'].items():
            assert 'count' in stats
            assert 'percentage' in stats

    def test_detect_quality_issues_outliers(self):
        """Test that quality assessment detects outliers."""
        df = pd.DataFrame({
            'order_value': [100] * 99 + [10000]  # One outlier
        })

        quality_report = detect_data_quality_issues(df)

        assert 'numeric_outliers' in quality_report
        assert 'order_value' in quality_report['numeric_outliers']

    def test_detect_quality_high_cardinality(self):
        """Test detection of high-cardinality categorical columns."""
        df = pd.DataFrame({
            'customer_id': [f'C{i:04d}' for i in range(1000)],
            'unique_field': [f'value_{i}' for i in range(1000)]  # All unique
        })

        quality_report = detect_data_quality_issues(df)

        assert 'columns_with_high_cardinality' in quality_report
        assert len(quality_report['columns_with_high_cardinality']) > 0


# ============================================================================
# TEST CLASS: Error Handling
# ============================================================================

class TestErrorHandling:
    """Test suite for error handling and edge cases."""

    def test_load_transactions_handles_corrupt_csv(self, temp_data_dir):
        """Test handling of corrupted CSV files."""
        csv_path = temp_data_dir / 'corrupt.csv'

        # Create a malformed CSV
        with open(csv_path, 'w') as f:
            f.write("col1,col2\nvalue1\n")  # Missing column value

        # Should handle gracefully
        df = load_transactions(str(csv_path), validate=False, clean=False)
        assert isinstance(df, pd.DataFrame)

    def test_parse_dates_handles_empty_strings(self):
        """Test that empty strings in date column are handled."""
        df = pd.DataFrame({
            'date': ['2024-01-01', '', '2024-01-03']
        })

        # Empty strings should be converted to NaT
        result_df = parse_dates(df, 'date')
        assert pd.api.types.is_datetime64_any_dtype(result_df['date'])

    def test_filter_active_handles_null_dates(self):
        """Test that null dates are handled in active filtering."""
        df = pd.DataFrame({
            'customer_id': ['C001', 'C002', 'C003'],
            'last_active': [
                pd.Timestamp.now(),
                None,
                pd.Timestamp.now() - pd.Timedelta(days=10)
            ]
        })

        active_df = filter_active(df, days=30)

        # Should handle null date gracefully
        assert isinstance(active_df, pd.DataFrame)


# ============================================================================
# TEST CLASS: Integration Tests
# ============================================================================

class TestIntegration:
    """Integration tests for end-to-end workflows."""

    def test_full_pipeline_load_validate_clean(self, sample_csv_file):
        """Test complete pipeline: load -> validate -> clean."""
        # Load data
        df = load_transactions(str(sample_csv_file), validate=False, clean=False)
        assert len(df) > 0

        # Validate
        is_valid, errors = validate_dataframe(df, data_type='transactions')
        assert is_valid

        # Clean
        cleaned_df = clean_transactions_dataframe(df)
        assert len(cleaned_df) > 0
        assert cleaned_df.duplicated().sum() == 0

    def test_pipeline_with_date_parsing(self, sample_csv_file):
        """Test pipeline including date parsing."""
        df = load_transactions(str(sample_csv_file), validate=False, clean=False)

        # Parse dates
        df = parse_dates(df, 'date')
        assert pd.api.types.is_datetime64_any_dtype(df['date'])

        # Filter active
        df['last_active'] = df['date']
        active_df = filter_active(df, days=365)
        assert len(active_df) > 0

    def test_pipeline_aggregation_workflow(self, sample_csv_file):
        """Test pipeline with aggregation workflow."""
        df = load_transactions(str(sample_csv_file), validate=False, clean=True)
        df = parse_dates(df, 'date')

        # Aggregate to customer level
        customer_metrics = aggregate_customer_metrics(df)
        assert len(customer_metrics) > 0
        assert 'total_revenue' in customer_metrics.columns


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

class TestPerformance:
    """Performance and scalability tests."""

    def test_load_large_dataset_performance(self, temp_data_dir):
        """Test loading performance with larger dataset."""
        # Create a larger dataset
        large_df = pd.DataFrame({
            'transaction_id': [f'T{i:06d}' for i in range(10000)],
            'customer_id': [f'C{i%1000:04d}' for i in range(10000)],
            'date': pd.date_range('2023-01-01', periods=10000, freq='h'),
            'order_value': np.random.uniform(10, 500, 10000)
        })

        csv_path = temp_data_dir / 'large_transactions.csv'
        large_df.to_csv(csv_path, index=False)

        # Time the loading
        import time
        start_time = time.time()
        df = load_transactions(str(csv_path), validate=False, clean=False)
        end_time = time.time()

        execution_time = end_time - start_time

        assert len(df) == 10000
        assert execution_time < 10  # Should complete within 10 seconds

    def test_aggregation_performance(self):
        """Test aggregation performance with many customers."""
        # Create dataset with many customers
        df = pd.DataFrame({
            'customer_id': [f'C{i%5000:04d}' for i in range(50000)],
            'order_value': np.random.uniform(10, 500, 50000),
            'date': pd.date_range('2023-01-01', periods=50000, freq='h')
        })

        import time
        start_time = time.time()
        customer_metrics = aggregate_customer_metrics(df)
        end_time = time.time()

        execution_time = end_time - start_time

        assert len(customer_metrics) > 0
        assert execution_time < 30  # Should complete within 30 seconds


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
