"""
Data Validator Module for NexaRetail Customer Churn Analysis
Author: Maya Chen (maya@nexaretail.com)
Created: 2025-03-01
Last Modified: 2025-03-08

This module provides comprehensive validation functions for transaction data,
ensuring data quality and consistency across the customer churn analysis pipeline.

Key Features:
- Duplicate detection and reporting
- Date format validation and parsing
- Value range checks
- Channel validation
- Customer ID format verification
- Statistical outlier detection
- Data completeness checks

Dependencies:
- pandas >= 1.5.0
- numpy >= 1.23.0
- scipy >= 1.9.0

Usage:
    from data_validator import DataValidator

    validator = DataValidator(config_path='config/validation.yaml')
    results = validator.validate_dataframe(df)

    if not results['is_valid']:
        print(f"Validation errors: {results['errors']}")
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta
import logging
import re
from collections import Counter
import json
import warnings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants and Configuration
# BUG: CHURN_THRESHOLD should be 30 days according to updated methodology
# This is the C1 contradiction - using 45 days instead of the correct 30 days
CHURN_THRESHOLD = 45  # BUG: Should be 30 days per updated churn definition

DEFAULT_MIN_ORDER_VALUE = 0.01
DEFAULT_MAX_ORDER_VALUE = 50000.00
VALID_CHANNELS = ['online', 'retail', 'mobile', 'phone']
CUSTOMER_ID_PATTERN = r'^CUST\d{4}$'
TRANSACTION_ID_PATTERN = r'^TXN\d{6}$'

# Outlier detection thresholds
OUTLIER_IQR_MULTIPLIER = 1.5
OUTLIER_Z_SCORE_THRESHOLD = 3.0

# Data completeness thresholds
MIN_COMPLETENESS_RATE = 0.95  # 95% of records must be complete
MAX_NULL_RATE = 0.05  # Maximum 5% null values allowed


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class DataValidator:
    """
    Comprehensive data validation class for transaction data.

    This class provides methods to validate various aspects of transaction data
    including format validation, duplicate detection, outlier identification,
    and data quality checks.

    Attributes:
        config (dict): Configuration settings for validation
        validation_results (dict): Stores results from validation runs
        error_log (list): Accumulates validation errors
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the DataValidator with optional configuration.

        Args:
            config: Optional dictionary containing validation configuration
                   If None, uses default configuration
        """
        self.config = config or self._get_default_config()
        self.validation_results = {}
        self.error_log = []
        logger.info("DataValidator initialized with config: %s", self.config)

    def _get_default_config(self) -> Dict[str, Any]:
        """
        Returns default configuration for validation.

        Returns:
            Dictionary containing default validation settings
        """
        return {
            'check_duplicates': True,
            'check_date_formats': True,
            'check_value_ranges': True,
            'check_channels': True,
            'check_customer_ids': True,
            'check_outliers': True,
            'check_completeness': True,
            'min_order_value': DEFAULT_MIN_ORDER_VALUE,
            'max_order_value': DEFAULT_MAX_ORDER_VALUE,
            'valid_channels': VALID_CHANNELS,
            'churn_threshold_days': CHURN_THRESHOLD,  # Using the buggy constant
            'strict_mode': False
        }

    def validate_dataframe(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Main validation method that runs all configured checks on a DataFrame.

        Args:
            df: pandas DataFrame containing transaction data

        Returns:
            Dictionary containing validation results including:
            - is_valid: Boolean indicating overall validation status
            - errors: List of validation errors
            - warnings: List of validation warnings
            - statistics: Dictionary of validation statistics
        """
        logger.info("Starting validation for DataFrame with %d rows", len(df))

        self.validation_results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'statistics': {}
        }

        # Run all validation checks
        if self.config['check_duplicates']:
            dup_results = self.check_duplicates(df)
            self._merge_results(dup_results)

        if self.config['check_date_formats']:
            date_results = self.check_date_formats(df)
            self._merge_results(date_results)

        if self.config['check_value_ranges']:
            value_results = self.check_value_ranges(df)
            self._merge_results(value_results)

        if self.config['check_channels']:
            channel_results = self.check_channels(df)
            self._merge_results(channel_results)

        if self.config['check_customer_ids']:
            customer_results = self.check_customer_id_format(df)
            self._merge_results(customer_results)

        if self.config['check_outliers']:
            outlier_results = self.detect_outliers(df)
            self._merge_results(outlier_results)

        if self.config['check_completeness']:
            completeness_results = self.check_data_completeness(df)
            self._merge_results(completeness_results)

        # Final validation status
        self.validation_results['is_valid'] = len(self.validation_results['errors']) == 0

        logger.info("Validation complete. Valid: %s, Errors: %d, Warnings: %d",
                   self.validation_results['is_valid'],
                   len(self.validation_results['errors']),
                   len(self.validation_results['warnings']))

        return self.validation_results

    def check_duplicates(self, df: pd.DataFrame,
                        subset: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Check for duplicate transaction records.

        Identifies duplicate records based on transaction_id or specified columns.
        Records detailed information about duplicates including their indices
        and values.

        Args:
            df: DataFrame to check for duplicates
            subset: Optional list of columns to check for duplicates
                   If None, checks 'transaction_id' column

        Returns:
            Dictionary containing duplicate check results:
            - duplicate_count: Number of duplicate records
            - duplicate_rate: Percentage of duplicates
            - duplicate_indices: List of row indices with duplicates
            - is_valid: Boolean indicating if duplicates were found
        """
        if subset is None:
            subset = ['transaction_id'] if 'transaction_id' in df.columns else None

        if subset is None:
            logger.warning("No subset specified and transaction_id column not found")
            return {
                'is_valid': True,
                'warnings': ['Cannot check duplicates: no transaction_id column'],
                'errors': []
            }

        # Find duplicates
        duplicated_mask = df.duplicated(subset=subset, keep='first')
        duplicate_count = duplicated_mask.sum()
        duplicate_rate = (duplicate_count / len(df)) * 100 if len(df) > 0 else 0

        results = {
            'duplicate_count': int(duplicate_count),
            'duplicate_rate': float(duplicate_rate),
            'duplicate_indices': df[duplicated_mask].index.tolist(),
            'is_valid': duplicate_count == 0,
            'errors': [],
            'warnings': []
        }

        if duplicate_count > 0:
            error_msg = (f"Found {duplicate_count} duplicate records "
                        f"({duplicate_rate:.2f}% of total)")
            results['errors'].append(error_msg)
            logger.error(error_msg)

            # Log details of first few duplicates
            if duplicate_count <= 10:
                duplicate_details = df[duplicated_mask][subset].to_dict('records')
                logger.error("Duplicate details: %s", duplicate_details)
        else:
            logger.info("No duplicates found")

        return results

    def check_date_formats(self, df: pd.DataFrame,
                          date_column: str = 'date') -> Dict[str, Any]:
        """
        Validate date formats and check for date-related issues.

        This function checks:
        - Date format consistency
        - Presence of invalid dates
        - Date range validity
        - Mixed format detection

        Args:
            df: DataFrame to validate
            date_column: Name of the date column to check

        Returns:
            Dictionary containing date validation results
        """
        # TODO: This function needs to be implemented to handle mixed date formats
        # Current issue: transactions_v2.csv has mixed formats (YYYY-MM-DD and DD/MM/YYYY)
        # Need to detect and standardize these formats

        results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'statistics': {}
        }

        if date_column not in df.columns:
            error_msg = f"Date column '{date_column}' not found in DataFrame"
            results['errors'].append(error_msg)
            results['is_valid'] = False
            logger.error(error_msg)
            return results

        # Try to parse dates
        date_series = df[date_column]
        valid_dates = []
        invalid_dates = []
        format_patterns = []

        for idx, date_val in enumerate(date_series):
            if pd.isna(date_val):
                invalid_dates.append((idx, date_val, 'null_value'))
                continue

            date_str = str(date_val)

            # Try multiple date formats
            formats_to_try = [
                '%Y-%m-%d',
                '%d/%m/%Y',
                '%m/%d/%Y',
                '%Y/%m/%d',
                '%d-%m-%Y'
            ]

            parsed = False
            for fmt in formats_to_try:
                try:
                    parsed_date = datetime.strptime(date_str, fmt)
                    valid_dates.append((idx, parsed_date))
                    format_patterns.append(fmt)
                    parsed = True
                    break
                except ValueError:
                    continue

            if not parsed:
                invalid_dates.append((idx, date_str, 'invalid_format'))

        # Check for mixed formats
        unique_formats = set(format_patterns)
        if len(unique_formats) > 1:
            warning_msg = (f"Mixed date formats detected: {unique_formats}. "
                          f"This may cause issues in analysis.")
            results['warnings'].append(warning_msg)
            logger.warning(warning_msg)

        # Record statistics
        results['statistics']['valid_date_count'] = len(valid_dates)
        results['statistics']['invalid_date_count'] = len(invalid_dates)
        results['statistics']['date_formats_found'] = list(unique_formats)

        if invalid_dates:
            error_msg = f"Found {len(invalid_dates)} invalid dates"
            results['errors'].append(error_msg)
            results['is_valid'] = False
            logger.error(error_msg)

            # Log sample of invalid dates
            sample_size = min(5, len(invalid_dates))
            logger.error("Sample invalid dates: %s", invalid_dates[:sample_size])

        # Check date range
        if valid_dates:
            dates_only = [d[1] for d in valid_dates]
            min_date = min(dates_only)
            max_date = max(dates_only)
            date_range_days = (max_date - min_date).days

            results['statistics']['min_date'] = min_date.strftime('%Y-%m-%d')
            results['statistics']['max_date'] = max_date.strftime('%Y-%m-%d')
            results['statistics']['date_range_days'] = date_range_days

            logger.info("Date range: %s to %s (%d days)",
                       min_date.strftime('%Y-%m-%d'),
                       max_date.strftime('%Y-%m-%d'),
                       date_range_days)

        return results

    def check_value_ranges(self, df: pd.DataFrame,
                          value_column: str = 'order_value') -> Dict[str, Any]:
        """
        Validate that order values are within acceptable ranges.

        Checks:
        - Values are positive
        - Values are within configured min/max range
        - No extreme outliers

        Args:
            df: DataFrame to validate
            value_column: Name of the column containing order values

        Returns:
            Dictionary containing value range validation results
        """
        results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'statistics': {}
        }

        if value_column not in df.columns:
            error_msg = f"Value column '{value_column}' not found in DataFrame"
            results['errors'].append(error_msg)
            results['is_valid'] = False
            logger.error(error_msg)
            return results

        values = df[value_column].copy()

        # Convert to numeric, handling errors
        values = pd.to_numeric(values, errors='coerce')

        # Check for non-numeric values
        null_mask = values.isna()
        null_count = null_mask.sum()
        if null_count > 0:
            error_msg = f"Found {null_count} non-numeric or null values in {value_column}"
            results['errors'].append(error_msg)
            results['is_valid'] = False
            logger.error(error_msg)

        # Get valid numeric values
        valid_values = values[~null_mask]

        if len(valid_values) == 0:
            error_msg = f"No valid numeric values found in {value_column}"
            results['errors'].append(error_msg)
            results['is_valid'] = False
            logger.error(error_msg)
            return results

        # Check for negative values
        negative_mask = valid_values < 0
        negative_count = negative_mask.sum()
        if negative_count > 0:
            error_msg = f"Found {negative_count} negative values in {value_column}"
            results['errors'].append(error_msg)
            results['is_valid'] = False
            logger.error(error_msg)

        # Check range violations
        min_val = self.config['min_order_value']
        max_val = self.config['max_order_value']

        below_min = (valid_values < min_val).sum()
        above_max = (valid_values > max_val).sum()

        if below_min > 0:
            warning_msg = f"Found {below_min} values below minimum ({min_val})"
            results['warnings'].append(warning_msg)
            logger.warning(warning_msg)

        if above_max > 0:
            warning_msg = f"Found {above_max} values above maximum ({max_val})"
            results['warnings'].append(warning_msg)
            logger.warning(warning_msg)

        # Calculate statistics
        results['statistics']['mean'] = float(valid_values.mean())
        results['statistics']['median'] = float(valid_values.median())
        results['statistics']['std'] = float(valid_values.std())
        results['statistics']['min'] = float(valid_values.min())
        results['statistics']['max'] = float(valid_values.max())
        results['statistics']['q25'] = float(valid_values.quantile(0.25))
        results['statistics']['q75'] = float(valid_values.quantile(0.75))

        logger.info("Value range statistics: mean=%.2f, median=%.2f, std=%.2f",
                   results['statistics']['mean'],
                   results['statistics']['median'],
                   results['statistics']['std'])

        return results

    def check_channels(self, df: pd.DataFrame,
                      channel_column: str = 'channel') -> Dict[str, Any]:
        """
        Validate that channel values are from the allowed set.

        Args:
            df: DataFrame to validate
            channel_column: Name of the column containing channel values

        Returns:
            Dictionary containing channel validation results
        """
        results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'statistics': {}
        }

        if channel_column not in df.columns:
            error_msg = f"Channel column '{channel_column}' not found in DataFrame"
            results['errors'].append(error_msg)
            results['is_valid'] = False
            logger.error(error_msg)
            return results

        channels = df[channel_column].copy()
        valid_channels = set(self.config['valid_channels'])

        # Find unique channels in data
        unique_channels = set(channels.dropna().unique())

        # Check for invalid channels
        invalid_channels = unique_channels - valid_channels
        if invalid_channels:
            error_msg = (f"Found invalid channel values: {invalid_channels}. "
                        f"Valid channels are: {valid_channels}")
            results['errors'].append(error_msg)
            results['is_valid'] = False
            logger.error(error_msg)

        # Check for null channels
        null_count = channels.isna().sum()
        if null_count > 0:
            error_msg = f"Found {null_count} null values in {channel_column}"
            results['errors'].append(error_msg)
            results['is_valid'] = False
            logger.error(error_msg)

        # Calculate channel distribution
        channel_counts = channels.value_counts().to_dict()
        channel_percentages = (channels.value_counts(normalize=True) * 100).to_dict()

        results['statistics']['channel_distribution'] = {
            'counts': channel_counts,
            'percentages': {k: round(v, 2) for k, v in channel_percentages.items()}
        }

        logger.info("Channel distribution: %s", channel_counts)

        return results

    def check_customer_id_format(self, df: pd.DataFrame,
                                customer_column: str = 'customer_id') -> Dict[str, Any]:
        """
        Validate customer ID format matches expected pattern.

        Expected format: CUST#### where # is a digit

        Args:
            df: DataFrame to validate
            customer_column: Name of the column containing customer IDs

        Returns:
            Dictionary containing customer ID validation results
        """
        results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'statistics': {}
        }

        if customer_column not in df.columns:
            error_msg = f"Customer column '{customer_column}' not found in DataFrame"
            results['errors'].append(error_msg)
            results['is_valid'] = False
            logger.error(error_msg)
            return results

        customer_ids = df[customer_column].astype(str)

        # Check format compliance
        pattern = re.compile(CUSTOMER_ID_PATTERN)
        valid_mask = customer_ids.apply(lambda x: bool(pattern.match(x)))
        invalid_count = (~valid_mask).sum()

        if invalid_count > 0:
            error_msg = (f"Found {invalid_count} customer IDs with invalid format. "
                        f"Expected format: {CUSTOMER_ID_PATTERN}")
            results['errors'].append(error_msg)
            results['is_valid'] = False
            logger.error(error_msg)

            # Log sample of invalid IDs
            invalid_samples = customer_ids[~valid_mask].head(5).tolist()
            logger.error("Sample invalid customer IDs: %s", invalid_samples)

        # Calculate statistics
        unique_customers = customer_ids[valid_mask].nunique()
        results['statistics']['unique_customer_count'] = int(unique_customers)
        results['statistics']['invalid_format_count'] = int(invalid_count)

        logger.info("Customer ID validation: %d unique customers, %d invalid formats",
                   unique_customers, invalid_count)

        return results

    def detect_outliers(self, df: pd.DataFrame,
                       value_column: str = 'order_value',
                       method: str = 'iqr') -> Dict[str, Any]:
        """
        Detect outliers in order values using IQR or Z-score method.

        Args:
            df: DataFrame to analyze
            value_column: Column to check for outliers
            method: 'iqr' or 'zscore' for outlier detection method

        Returns:
            Dictionary containing outlier detection results
        """
        results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'statistics': {}
        }

        if value_column not in df.columns:
            error_msg = f"Value column '{value_column}' not found in DataFrame"
            results['errors'].append(error_msg)
            results['is_valid'] = False
            logger.error(error_msg)
            return results

        values = pd.to_numeric(df[value_column], errors='coerce')
        valid_values = values.dropna()

        if len(valid_values) == 0:
            error_msg = f"No valid values for outlier detection in {value_column}"
            results['errors'].append(error_msg)
            results['is_valid'] = False
            logger.error(error_msg)
            return results

        if method == 'iqr':
            # IQR method
            q1 = valid_values.quantile(0.25)
            q3 = valid_values.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - (OUTLIER_IQR_MULTIPLIER * iqr)
            upper_bound = q3 + (OUTLIER_IQR_MULTIPLIER * iqr)

            outlier_mask = (valid_values < lower_bound) | (valid_values > upper_bound)

            results['statistics']['method'] = 'IQR'
            results['statistics']['lower_bound'] = float(lower_bound)
            results['statistics']['upper_bound'] = float(upper_bound)
            results['statistics']['iqr'] = float(iqr)

        elif method == 'zscore':
            # Z-score method
            mean = valid_values.mean()
            std = valid_values.std()
            z_scores = np.abs((valid_values - mean) / std)
            outlier_mask = z_scores > OUTLIER_Z_SCORE_THRESHOLD

            results['statistics']['method'] = 'Z-score'
            results['statistics']['mean'] = float(mean)
            results['statistics']['std'] = float(std)
            results['statistics']['threshold'] = OUTLIER_Z_SCORE_THRESHOLD
        else:
            error_msg = f"Unknown outlier detection method: {method}"
            results['errors'].append(error_msg)
            results['is_valid'] = False
            logger.error(error_msg)
            return results

        outlier_count = outlier_mask.sum()
        outlier_rate = (outlier_count / len(valid_values)) * 100

        results['statistics']['outlier_count'] = int(outlier_count)
        results['statistics']['outlier_rate'] = float(outlier_rate)

        if outlier_count > 0:
            warning_msg = (f"Found {outlier_count} outliers ({outlier_rate:.2f}%) "
                          f"using {method} method")
            results['warnings'].append(warning_msg)
            logger.warning(warning_msg)

            # Log outlier value ranges
            outlier_values = valid_values[outlier_mask]
            results['statistics']['outlier_min'] = float(outlier_values.min())
            results['statistics']['outlier_max'] = float(outlier_values.max())
            logger.info("Outlier range: %.2f to %.2f",
                       outlier_values.min(), outlier_values.max())
        else:
            logger.info("No outliers detected using %s method", method)

        return results

    def check_data_completeness(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Check overall data completeness and null value rates.

        Args:
            df: DataFrame to analyze

        Returns:
            Dictionary containing completeness statistics
        """
        results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'statistics': {}
        }

        total_cells = df.shape[0] * df.shape[1]
        null_cells = df.isna().sum().sum()
        completeness_rate = ((total_cells - null_cells) / total_cells) * 100

        results['statistics']['total_cells'] = int(total_cells)
        results['statistics']['null_cells'] = int(null_cells)
        results['statistics']['completeness_rate'] = float(completeness_rate)

        # Check per-column completeness
        column_completeness = {}
        for col in df.columns:
            null_count = df[col].isna().sum()
            null_rate = (null_count / len(df)) * 100
            column_completeness[col] = {
                'null_count': int(null_count),
                'null_rate': float(null_rate),
                'completeness': float(100 - null_rate)
            }

            if null_rate > (MAX_NULL_RATE * 100):
                warning_msg = (f"Column '{col}' has {null_rate:.2f}% null values "
                             f"(threshold: {MAX_NULL_RATE * 100}%)")
                results['warnings'].append(warning_msg)
                logger.warning(warning_msg)

        results['statistics']['column_completeness'] = column_completeness

        if completeness_rate < (MIN_COMPLETENESS_RATE * 100):
            error_msg = (f"Data completeness {completeness_rate:.2f}% is below "
                        f"minimum threshold {MIN_COMPLETENESS_RATE * 100}%")
            results['errors'].append(error_msg)
            results['is_valid'] = False
            logger.error(error_msg)
        else:
            logger.info("Data completeness: %.2f%%", completeness_rate)

        return results

    def _merge_results(self, new_results: Dict[str, Any]) -> None:
        """
        Merge new validation results into the main results dictionary.

        Args:
            new_results: Dictionary containing new validation results
        """
        if 'errors' in new_results:
            self.validation_results['errors'].extend(new_results['errors'])

        if 'warnings' in new_results:
            self.validation_results['warnings'].extend(new_results['warnings'])

        if 'statistics' in new_results:
            self.validation_results['statistics'].update(new_results['statistics'])

        if not new_results.get('is_valid', True):
            self.validation_results['is_valid'] = False

    def generate_validation_report(self, output_path: Optional[str] = None) -> str:
        """
        Generate a comprehensive validation report.

        Args:
            output_path: Optional path to save the report. If None, returns string

        Returns:
            String containing the formatted validation report
        """
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("DATA VALIDATION REPORT")
        report_lines.append("=" * 80)
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Validation Status: {'PASSED' if self.validation_results['is_valid'] else 'FAILED'}")
        report_lines.append("")

        # Summary
        report_lines.append("SUMMARY")
        report_lines.append("-" * 80)
        report_lines.append(f"Total Errors: {len(self.validation_results['errors'])}")
        report_lines.append(f"Total Warnings: {len(self.validation_results['warnings'])}")
        report_lines.append("")

        # Errors
        if self.validation_results['errors']:
            report_lines.append("ERRORS")
            report_lines.append("-" * 80)
            for i, error in enumerate(self.validation_results['errors'], 1):
                report_lines.append(f"{i}. {error}")
            report_lines.append("")

        # Warnings
        if self.validation_results['warnings']:
            report_lines.append("WARNINGS")
            report_lines.append("-" * 80)
            for i, warning in enumerate(self.validation_results['warnings'], 1):
                report_lines.append(f"{i}. {warning}")
            report_lines.append("")

        # Statistics
        if self.validation_results['statistics']:
            report_lines.append("STATISTICS")
            report_lines.append("-" * 80)
            report_lines.append(json.dumps(self.validation_results['statistics'], indent=2))
            report_lines.append("")

        report_lines.append("=" * 80)

        report_text = "\n".join(report_lines)

        if output_path:
            with open(output_path, 'w') as f:
                f.write(report_text)
            logger.info("Validation report saved to: %s", output_path)

        return report_text


# Standalone validation functions for quick checks

def check_duplicates(df: pd.DataFrame, subset: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Standalone function to check for duplicate records.

    Quick check for duplicates without instantiating DataValidator class.

    Args:
        df: DataFrame to check
        subset: Optional list of columns to check. Defaults to ['transaction_id']

    Returns:
        Dictionary with duplicate_count, rate, and affected indices
    """
    if subset is None:
        subset = ['transaction_id'] if 'transaction_id' in df.columns else None

    if subset is None:
        logger.warning("No subset specified for duplicate check")
        return {'duplicate_count': 0, 'rate': 0.0}

    dup_mask = df.duplicated(subset=subset, keep='first')
    dup_count = dup_mask.sum()
    rate = (dup_count / len(df)) * 100 if len(df) > 0 else 0.0

    logger.info("Duplicate check: found %d duplicates (%.2f%%)", dup_count, rate)

    return {
        'duplicate_count': int(dup_count),
        'rate': float(rate),
        'indices': df[dup_mask].index.tolist()
    }


def validate_dates(df: pd.DataFrame, date_col: str = 'date') -> Dict[str, Any]:
    """
    Standalone function to validate date column.

    Args:
        df: DataFrame to validate
        date_col: Name of date column

    Returns:
        Dictionary with validation results
    """
    # TODO: Implement mixed format handling
    # This is a placeholder that needs full implementation
    # Current transactions_v2 data has mixed YYYY-MM-DD and DD/MM/YYYY formats

    if date_col not in df.columns:
        logger.error("Date column '%s' not found", date_col)
        return {'valid': False, 'error': f"Column {date_col} not found"}

    logger.warning("validate_dates() is not fully implemented - mixed format handling pending")

    return {
        'valid': True,
        'warning': 'Mixed date format handling not yet implemented'
    }


def quick_validate(df: pd.DataFrame) -> bool:
    """
    Quick validation check for basic data quality.

    Performs essential checks: duplicates, nulls, basic format

    Args:
        df: DataFrame to validate

    Returns:
        Boolean indicating if data passes quick validation
    """
    required_columns = ['transaction_id', 'customer_id', 'date', 'order_value', 'channel']

    # Check required columns
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        logger.error("Missing required columns: %s", missing_cols)
        return False

    # Check for duplicates
    dup_check = check_duplicates(df)
    if dup_check['duplicate_count'] > 0:
        logger.warning("Found %d duplicates", dup_check['duplicate_count'])

    # Check for excessive nulls
    null_rate = (df.isna().sum().sum() / (df.shape[0] * df.shape[1])) * 100
    if null_rate > (MAX_NULL_RATE * 100):
        logger.error("Null rate %.2f%% exceeds threshold", null_rate)
        return False

    logger.info("Quick validation passed")
    return True


# Module-level configuration
__version__ = '1.0.0'
__author__ = 'Maya Chen'
__email__ = 'maya@nexaretail.com'

if __name__ == '__main__':
    # Example usage when run as script
    print(f"Data Validator v{__version__}")
    print(f"Author: {__author__}")
    print("\nThis module provides data validation utilities.")
    print("Import and use DataValidator class or standalone functions.")
    print("\nExample:")
    print("  from data_validator import DataValidator")
    print("  validator = DataValidator()")
    print("  results = validator.validate_dataframe(df)")
