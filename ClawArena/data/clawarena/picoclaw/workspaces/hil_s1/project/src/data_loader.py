"""
Data Loader Module for Customer Churn Analysis

This module provides comprehensive functionality for loading, validating, and preprocessing
customer transaction and customer data for churn analysis. It handles multiple data formats,
performs extensive validation, and provides robust error handling.

The module is designed to work with the following primary datasets:
- transactions_v1.csv: Transaction-level data with order values and dates
- customers.csv: Customer demographic and activity data

Author: Data Engineering Team
Created: 2025-03-01
Last Modified: 2025-03-12
Version: 1.2.0

Dependencies:
    - pandas>=2.2.0
    - numpy>=1.26.0
    - python-dateutil>=2.8.2

Usage Example:
    >>> from data_loader import load_transactions, validate_dataframe
    >>> df = load_transactions("data/raw/transactions_v1.csv")
    >>> valid, errors = validate_dataframe(df)
    >>> if valid:
    ...     print("Data loaded successfully")
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import logging
import sys
from typing import Dict, List, Tuple, Optional, Union, Any
import warnings
from collections import defaultdict
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_loader.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class DataLoadError(Exception):
    """Custom exception for data loading errors."""
    pass


class DataValidationError(Exception):
    """Custom exception for data validation errors."""
    pass


class DateParseError(Exception):
    """Custom exception for date parsing errors."""
    pass


# Global configuration constants
DEFAULT_ENCODING = 'utf-8'
FALLBACK_ENCODINGS = ['latin-1', 'iso-8859-1', 'cp1252']
MAX_FILE_SIZE_MB = 500
CHUNK_SIZE = 10000
NULL_THRESHOLD = 0.5  # Maximum proportion of nulls allowed per column


def load_transactions(filepath: str, encoding: str = DEFAULT_ENCODING,
                     validate: bool = True, clean: bool = True) -> pd.DataFrame:
    """
    Load transaction data from CSV file with comprehensive validation and cleaning.

    This function loads transaction data and performs several preprocessing steps:
    1. File existence and size validation
    2. CSV parsing with encoding detection
    3. Column name standardization
    4. Data type inference and conversion
    5. Optional validation and cleaning

    Args:
        filepath (str): Path to the CSV file containing transaction data
        encoding (str): Character encoding of the file (default: utf-8)
        validate (bool): Whether to perform validation checks (default: True)
        clean (bool): Whether to perform automatic cleaning (default: True)

    Returns:
        pd.DataFrame: Loaded and processed transaction dataframe

    Raises:
        DataLoadError: If file cannot be loaded or parsed
        DataValidationError: If validation checks fail

    Example:
        >>> df = load_transactions("data/raw/transactions_v1.csv")
        >>> print(df.shape)
        (50000, 6)
        >>> print(df.columns.tolist())
        ['transaction_id', 'customer_id', 'date', 'revenue', 'product_id', 'quantity']

    Notes:
        - This function contains a known bug where the column name 'transaction_amount'
          is hardcoded but the actual CSV uses 'order_value'
        - The bug causes a KeyError when the rename operation fails silently
        - This needs to be fixed by updating the column mapping
    """
    logger.info(f"Loading transaction data from: {filepath}")

    # Validate file existence
    file_path = Path(filepath)
    if not file_path.exists():
        error_msg = f"File not found: {filepath}"
        logger.error(error_msg)
        raise DataLoadError(error_msg)

    # Check file size
    file_size_mb = file_path.stat().st_size / (1024 * 1024)
    logger.info(f"File size: {file_size_mb:.2f} MB")
    if file_size_mb > MAX_FILE_SIZE_MB:
        logger.warning(f"Large file detected ({file_size_mb:.2f} MB). Consider using chunked loading.")

    # Try loading with different encodings
    df = None
    encodings_to_try = [encoding] + FALLBACK_ENCODINGS

    for enc in encodings_to_try:
        try:
            logger.info(f"Attempting to load with encoding: {enc}")
            df = pd.read_csv(filepath, encoding=enc, low_memory=False)
            logger.info(f"Successfully loaded with encoding: {enc}")
            break
        except UnicodeDecodeError:
            logger.warning(f"Failed to load with encoding: {enc}")
            continue
        except Exception as e:
            logger.error(f"Unexpected error loading file: {str(e)}")
            raise DataLoadError(f"Failed to load file: {str(e)}")

    if df is None:
        raise DataLoadError("Could not load file with any supported encoding")

    # Log initial statistics
    logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    logger.info(f"Columns: {df.columns.tolist()}")
    logger.info(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    # BUG 1: Column name is hardcoded as 'transaction_amount' but actual CSV uses 'order_value'
    # This will fail silently if the column doesn't exist, or create incorrect mappings
    # The correct fix would be to use 'order_value' instead of 'transaction_amount'
    df = df.rename(columns={"transaction_amount": "revenue"})

    # Standardize column names to lowercase with underscores
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    logger.info(f"Standardized column names: {df.columns.tolist()}")

    # Perform validation if requested
    if validate:
        try:
            is_valid, validation_errors = validate_dataframe(df, data_type='transactions')
            if not is_valid:
                error_msg = f"Validation failed: {validation_errors}"
                logger.error(error_msg)
                if not clean:
                    raise DataValidationError(error_msg)
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            if not clean:
                raise

    # Perform cleaning if requested
    if clean:
        df = clean_transactions_dataframe(df)
        logger.info("Data cleaning completed")

    # Log final statistics
    logger.info(f"Final shape: {df.shape}")
    logger.info(f"Null counts:\n{df.isnull().sum()}")

    return df


def parse_dates(df: pd.DataFrame, date_col: str, infer_format: bool = False,
               dayfirst: bool = False) -> pd.DataFrame:
    """
    Parse date column in dataframe with flexible format support.

    This function attempts to parse dates from string format to datetime objects.
    It supports multiple date formats and provides robust error handling.

    Args:
        df (pd.DataFrame): Input dataframe containing date column
        date_col (str): Name of the column containing dates
        infer_format (bool): Whether to infer date format automatically
        dayfirst (bool): Whether to interpret first value as day (default: False)

    Returns:
        pd.DataFrame: Dataframe with parsed date column

    Raises:
        DateParseError: If dates cannot be parsed
        KeyError: If date_col does not exist in dataframe

    Example:
        >>> df = pd.DataFrame({'date': ['2024-01-15', '2024-01-16', '2024-01-17']})
        >>> df = parse_dates(df, 'date')
        >>> print(df['date'].dtype)
        datetime64[ns]

    Notes:
        - BUG 2: This function only handles the format "%Y-%m-%d" and will raise
          ValueError when encountering dates in other formats like "M/D/YYYY"
        - The fix requires adding support for multiple date formats or using
          pandas' flexible date parsing with errors='coerce'
        - This bug will cause the pipeline to fail on real-world messy data
    """
    logger.info(f"Parsing dates in column: {date_col}")

    # Validate column exists
    if date_col not in df.columns:
        error_msg = f"Column '{date_col}' not found in dataframe. Available columns: {df.columns.tolist()}"
        logger.error(error_msg)
        raise KeyError(error_msg)

    # Check if already datetime
    if pd.api.types.is_datetime64_any_dtype(df[date_col]):
        logger.info(f"Column '{date_col}' is already datetime type")
        return df

    # Log sample values before parsing
    logger.info(f"Sample date values before parsing:\n{df[date_col].head(10)}")

    # Count non-null values
    non_null_count = df[date_col].notna().sum()
    logger.info(f"Non-null date values: {non_null_count}/{len(df)}")

    # BUG 2: Only handles one specific date format
    # This will fail when dates are in format like "3/15/2024" or "15/03/2024"
    # The function needs to try multiple formats or use pd.to_datetime with flexible parsing
    try:
        df[date_col] = df[date_col].apply(
            lambda d: datetime.strptime(d, "%Y-%m-%d") if pd.notna(d) else pd.NaT
        )
        logger.info(f"Successfully parsed {non_null_count} dates")
    except (ValueError, TypeError) as e:
        error_msg = f"Date parsing failed: {str(e)}. Dates must be in YYYY-MM-DD format."
        logger.error(error_msg)
        logger.error(f"Failed on value: {df[date_col].iloc[0]}")
        raise DateParseError(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error during date parsing: {str(e)}"
        logger.error(error_msg)
        raise DateParseError(error_msg)

    # Log sample values after parsing
    logger.info(f"Sample date values after parsing:\n{df[date_col].head(10)}")

    # Validate date range
    if df[date_col].notna().any():
        min_date = df[date_col].min()
        max_date = df[date_col].max()
        logger.info(f"Date range: {min_date} to {max_date}")

        # Sanity check for reasonable date range
        current_year = datetime.now().year
        if min_date.year < 1900 or max_date.year > current_year + 1:
            logger.warning(f"Unusual date range detected: {min_date} to {max_date}")

    return df


def filter_active(df: pd.DataFrame, days: int = 30,
                 date_col: str = "last_active") -> pd.DataFrame:
    """
    Filter dataframe to include only active customers based on activity threshold.

    This function implements the business logic for identifying active vs churned customers.
    A customer is considered active if they have had activity within the specified number
    of days from the current date.

    Args:
        df (pd.DataFrame): Input dataframe with customer activity data
        days (int): Number of days to look back for activity (default: 30)
        date_col (str): Name of column containing last activity date (default: "last_active")

    Returns:
        pd.DataFrame: Filtered dataframe containing only active customers

    Raises:
        KeyError: If date_col does not exist in dataframe
        ValueError: If days is negative or date_col is not datetime type

    Example:
        >>> df = load_transactions("data/raw/transactions_v1.csv")
        >>> active_df = filter_active(df, days=30)
        >>> print(f"Active customers: {len(active_df)}")
        Active customers: 8532

    Notes:
        - Churn definition comes from Alex's business requirement (2025-03-03 meeting)
        - 30-day threshold is standard for subscription-based business model
        - This logic is correct and should not be modified without stakeholder approval
    """
    logger.info(f"Filtering for active customers (last {days} days)")

    # Validate inputs
    if days < 0:
        raise ValueError(f"Days parameter must be non-negative, got: {days}")

    if date_col not in df.columns:
        error_msg = f"Column '{date_col}' not found. Available: {df.columns.tolist()}"
        logger.error(error_msg)
        raise KeyError(error_msg)

    # Ensure date column is datetime type
    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        logger.warning(f"Column '{date_col}' is not datetime type. Attempting conversion...")
        try:
            df[date_col] = pd.to_datetime(df[date_col])
        except Exception as e:
            raise ValueError(f"Cannot convert '{date_col}' to datetime: {str(e)}")

    # Calculate cutoff date
    cutoff = pd.Timestamp.now() - pd.Timedelta(days=days)
    logger.info(f"Cutoff date: {cutoff}")

    # Log statistics before filtering
    initial_count = len(df)
    null_count = df[date_col].isna().sum()
    logger.info(f"Initial row count: {initial_count}")
    logger.info(f"Null dates: {null_count}")

    # Filter for active customers
    # Business logic: customer is active if last_active >= cutoff date
    active_df = df[df[date_col] >= cutoff].copy()

    # Log statistics after filtering
    final_count = len(active_df)
    churned_count = initial_count - final_count - null_count
    logger.info(f"Active customers: {final_count} ({final_count/initial_count*100:.1f}%)")
    logger.info(f"Churned customers: {churned_count} ({churned_count/initial_count*100:.1f}%)")
    logger.info(f"Null date customers: {null_count} ({null_count/initial_count*100:.1f}%)")

    return active_df


def validate_dataframe(df: pd.DataFrame, data_type: str = 'transactions',
                      strict: bool = False) -> Tuple[bool, List[str]]:
    """
    Perform comprehensive validation checks on dataframe.

    This function validates data quality, schema compliance, and business rules.
    It performs multiple validation checks and returns detailed error messages.

    Args:
        df (pd.DataFrame): Dataframe to validate
        data_type (str): Type of data ('transactions' or 'customers')
        strict (bool): Whether to apply strict validation rules

    Returns:
        Tuple[bool, List[str]]: (is_valid, list_of_error_messages)

    Example:
        >>> df = load_transactions("data/raw/transactions_v1.csv", validate=False)
        >>> is_valid, errors = validate_dataframe(df, data_type='transactions')
        >>> if not is_valid:
        ...     print("Validation errors:", errors)
    """
    logger.info(f"Validating dataframe (type: {data_type}, strict: {strict})")

    errors = []

    # Check 1: Empty dataframe
    if df.empty:
        errors.append("Dataframe is empty")
        return False, errors

    # Check 2: Required columns based on data type
    required_columns = {
        'transactions': ['transaction_id', 'customer_id', 'date'],
        'customers': ['customer_id', 'signup_date']
    }

    if data_type in required_columns:
        missing_cols = set(required_columns[data_type]) - set(df.columns)
        if missing_cols:
            errors.append(f"Missing required columns: {missing_cols}")

    # Check 3: Duplicate records
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        msg = f"Found {duplicate_count} duplicate rows"
        if strict:
            errors.append(msg)
        else:
            logger.warning(msg)

    # Check 4: Null value threshold
    null_percentages = df.isnull().sum() / len(df)
    high_null_cols = null_percentages[null_percentages > NULL_THRESHOLD]
    if not high_null_cols.empty:
        msg = f"Columns with >{NULL_THRESHOLD*100}% nulls: {high_null_cols.to_dict()}"
        if strict:
            errors.append(msg)
        else:
            logger.warning(msg)

    # Check 5: Data type validation for transactions
    if data_type == 'transactions':
        # Check for numeric amount column
        amount_cols = [col for col in df.columns if 'amount' in col or 'value' in col or 'revenue' in col]
        for col in amount_cols:
            if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
                errors.append(f"Column '{col}' should be numeric but is {df[col].dtype}")

        # Check for negative amounts
        for col in amount_cols:
            if col in df.columns:
                negative_count = (df[col] < 0).sum()
                if negative_count > 0:
                    msg = f"Found {negative_count} negative values in '{col}'"
                    if strict:
                        errors.append(msg)
                    else:
                        logger.warning(msg)

    # Check 6: ID column validation
    id_cols = [col for col in df.columns if 'id' in col]
    for col in id_cols:
        unique_count = df[col].nunique()
        total_count = df[col].notna().sum()
        if col == 'transaction_id' or col.endswith('_id'):
            # Primary keys should have high uniqueness
            if unique_count < total_count * 0.9:
                msg = f"Low uniqueness in '{col}': {unique_count}/{total_count}"
                logger.warning(msg)

    # Check 7: Date column validation
    date_cols = [col for col in df.columns if 'date' in col]
    for col in date_cols:
        if col in df.columns:
            if not pd.api.types.is_datetime64_any_dtype(df[col]):
                msg = f"Date column '{col}' is not datetime type (currently {df[col].dtype})"
                if strict:
                    errors.append(msg)
                else:
                    logger.warning(msg)

    is_valid = len(errors) == 0

    if is_valid:
        logger.info("Validation passed successfully")
    else:
        logger.error(f"Validation failed with {len(errors)} errors")
        for error in errors:
            logger.error(f"  - {error}")

    return is_valid, errors


def clean_transactions_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform comprehensive cleaning operations on transactions dataframe.

    Cleaning operations include:
    - Removing duplicate rows
    - Handling missing values
    - Standardizing data types
    - Removing outliers
    - Normalizing text fields

    Args:
        df (pd.DataFrame): Raw transactions dataframe

    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    logger.info("Starting data cleaning process")
    initial_rows = len(df)

    # Make a copy to avoid modifying original
    df_clean = df.copy()

    # Step 1: Remove exact duplicates
    duplicates_before = df_clean.duplicated().sum()
    if duplicates_before > 0:
        df_clean = df_clean.drop_duplicates()
        logger.info(f"Removed {duplicates_before} duplicate rows")

    # Step 2: Handle missing values in critical columns
    critical_cols = ['transaction_id', 'customer_id']
    for col in critical_cols:
        if col in df_clean.columns:
            missing_count = df_clean[col].isna().sum()
            if missing_count > 0:
                logger.warning(f"Dropping {missing_count} rows with missing '{col}'")
                df_clean = df_clean.dropna(subset=[col])

    # Step 3: Standardize ID formats
    id_cols = [col for col in df_clean.columns if 'id' in col.lower()]
    for col in id_cols:
        if df_clean[col].dtype == 'object':
            df_clean[col] = df_clean[col].astype(str).str.strip().str.upper()

    # Step 4: Clean amount/value columns
    amount_cols = [col for col in df_clean.columns
                   if any(term in col.lower() for term in ['amount', 'value', 'revenue', 'price'])]
    for col in amount_cols:
        if col in df_clean.columns:
            # Convert to numeric, coercing errors
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

            # Remove negative values (assuming refunds are handled separately)
            negative_count = (df_clean[col] < 0).sum()
            if negative_count > 0:
                logger.warning(f"Removing {negative_count} negative values from '{col}'")
                df_clean = df_clean[df_clean[col] >= 0]

            # Remove extreme outliers (beyond 99.9th percentile)
            if df_clean[col].notna().sum() > 0:
                upper_bound = df_clean[col].quantile(0.999)
                outliers = (df_clean[col] > upper_bound).sum()
                if outliers > 0:
                    logger.warning(f"Removing {outliers} outliers from '{col}' (>{upper_bound:.2f})")
                    df_clean = df_clean[df_clean[col] <= upper_bound]

    # Step 5: Standardize text columns
    text_cols = df_clean.select_dtypes(include=['object']).columns
    for col in text_cols:
        if col not in id_cols:  # Skip ID columns (already processed)
            df_clean[col] = df_clean[col].astype(str).str.strip()

    final_rows = len(df_clean)
    rows_removed = initial_rows - final_rows
    logger.info(f"Cleaning complete. Removed {rows_removed} rows ({rows_removed/initial_rows*100:.1f}%)")
    logger.info(f"Final row count: {final_rows}")

    return df_clean


def load_customers(filepath: str, encoding: str = DEFAULT_ENCODING) -> pd.DataFrame:
    """
    Load customer data from CSV file with validation and preprocessing.

    Args:
        filepath (str): Path to customers CSV file
        encoding (str): File encoding (default: utf-8)

    Returns:
        pd.DataFrame: Loaded customer dataframe

    Raises:
        DataLoadError: If file cannot be loaded
    """
    logger.info(f"Loading customer data from: {filepath}")

    try:
        df = pd.read_csv(filepath, encoding=encoding)
        logger.info(f"Loaded {len(df)} customers")

        # Standardize column names
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

        # Validate
        is_valid, errors = validate_dataframe(df, data_type='customers')
        if not is_valid:
            logger.warning(f"Customer data validation issues: {errors}")

        return df

    except Exception as e:
        error_msg = f"Failed to load customer data: {str(e)}"
        logger.error(error_msg)
        raise DataLoadError(error_msg)


def merge_transaction_customer_data(transactions_df: pd.DataFrame,
                                   customers_df: pd.DataFrame,
                                   how: str = 'left') -> pd.DataFrame:
    """
    Merge transaction and customer dataframes on customer_id.

    Args:
        transactions_df (pd.DataFrame): Transaction data
        customers_df (pd.DataFrame): Customer data
        how (str): Type of merge (default: 'left')

    Returns:
        pd.DataFrame: Merged dataframe
    """
    logger.info(f"Merging transactions and customers (how={how})")

    # Validate merge key exists
    if 'customer_id' not in transactions_df.columns:
        raise KeyError("'customer_id' not found in transactions dataframe")
    if 'customer_id' not in customers_df.columns:
        raise KeyError("'customer_id' not found in customers dataframe")

    initial_rows = len(transactions_df)

    # Perform merge
    merged_df = transactions_df.merge(customers_df, on='customer_id', how=how, suffixes=('_trans', '_cust'))

    final_rows = len(merged_df)
    logger.info(f"Merge complete: {initial_rows} -> {final_rows} rows")

    # Check for unmatched records
    if how == 'left':
        unmatched = merged_df[merged_df[customers_df.columns.difference(['customer_id'])[0]].isna()].shape[0]
        if unmatched > 0:
            logger.warning(f"Found {unmatched} transactions without matching customer records")

    return merged_df


def aggregate_customer_metrics(df: pd.DataFrame,
                               customer_id_col: str = 'customer_id',
                               amount_col: str = 'order_value',
                               date_col: str = 'date') -> pd.DataFrame:
    """
    Aggregate transaction-level data to customer-level metrics.

    Creates features for churn prediction including:
    - Total transaction count
    - Total revenue
    - Average order value
    - Days since last transaction
    - Transaction frequency

    Args:
        df (pd.DataFrame): Transaction-level dataframe
        customer_id_col (str): Name of customer ID column
        amount_col (str): Name of transaction amount column
        date_col (str): Name of transaction date column

    Returns:
        pd.DataFrame: Customer-level aggregated metrics
    """
    logger.info("Aggregating customer-level metrics")

    # Ensure date column is datetime
    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        df[date_col] = pd.to_datetime(df[date_col])

    # Calculate reference date (most recent transaction in dataset)
    reference_date = df[date_col].max()
    logger.info(f"Reference date for recency calculations: {reference_date}")

    # Aggregate metrics
    agg_dict = {
        amount_col: ['sum', 'mean', 'std', 'count'],
        date_col: ['min', 'max']
    }

    customer_metrics = df.groupby(customer_id_col).agg(agg_dict)

    # Flatten column names
    customer_metrics.columns = ['_'.join(col).strip() for col in customer_metrics.columns.values]
    customer_metrics = customer_metrics.reset_index()

    # Calculate derived metrics
    customer_metrics['days_since_last_transaction'] = (
        reference_date - customer_metrics[f'{date_col}_max']
    ).dt.days

    customer_metrics['days_since_first_transaction'] = (
        reference_date - customer_metrics[f'{date_col}_min']
    ).dt.days

    customer_metrics['transaction_frequency'] = (
        customer_metrics[f'{amount_col}_count'] /
        customer_metrics['days_since_first_transaction'].replace(0, 1)
    )

    # Rename for clarity
    rename_map = {
        f'{amount_col}_sum': 'total_revenue',
        f'{amount_col}_mean': 'avg_order_value',
        f'{amount_col}_std': 'std_order_value',
        f'{amount_col}_count': 'transaction_count',
        f'{date_col}_min': 'first_transaction_date',
        f'{date_col}_max': 'last_transaction_date'
    }
    customer_metrics = customer_metrics.rename(columns=rename_map)

    logger.info(f"Created customer metrics for {len(customer_metrics)} customers")
    logger.info(f"Metrics columns: {customer_metrics.columns.tolist()}")

    return customer_metrics


def detect_data_quality_issues(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Perform comprehensive data quality assessment.

    Returns dictionary with quality metrics and issues found.

    Args:
        df (pd.DataFrame): Dataframe to assess

    Returns:
        Dict[str, Any]: Dictionary containing quality metrics
    """
    logger.info("Detecting data quality issues")

    quality_report = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2,
        'duplicate_rows': df.duplicated().sum(),
        'columns_with_nulls': {},
        'columns_with_high_cardinality': {},
        'numeric_outliers': {},
        'data_types': df.dtypes.to_dict()
    }

    # Check for null values
    null_counts = df.isnull().sum()
    quality_report['columns_with_nulls'] = {
        col: {'count': int(count), 'percentage': count/len(df)*100}
        for col, count in null_counts.items() if count > 0
    }

    # Check for high cardinality in categorical columns
    for col in df.select_dtypes(include=['object']).columns:
        unique_count = df[col].nunique()
        if unique_count > len(df) * 0.5:
            quality_report['columns_with_high_cardinality'][col] = unique_count

    # Check for outliers in numeric columns
    for col in df.select_dtypes(include=[np.number]).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
        if outliers > 0:
            quality_report['numeric_outliers'][col] = {
                'count': int(outliers),
                'percentage': outliers/len(df)*100
            }

    logger.info(f"Quality assessment complete. Found issues in {len(quality_report['columns_with_nulls'])} columns")

    return quality_report


def export_processed_data(df: pd.DataFrame, filepath: str,
                         format: str = 'csv', compression: Optional[str] = None) -> None:
    """
    Export processed dataframe to file.

    Args:
        df (pd.DataFrame): Dataframe to export
        filepath (str): Output file path
        format (str): Output format ('csv', 'parquet', 'excel')
        compression (Optional[str]): Compression method ('gzip', 'bz2', 'zip')
    """
    logger.info(f"Exporting data to {filepath} (format={format})")

    output_path = Path(filepath)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        if format == 'csv':
            df.to_csv(filepath, index=False, compression=compression)
        elif format == 'parquet':
            df.to_parquet(filepath, index=False, compression=compression or 'snappy')
        elif format == 'excel':
            df.to_excel(filepath, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")

        logger.info(f"Export successful: {filepath}")

    except Exception as e:
        logger.error(f"Export failed: {str(e)}")
        raise


# Additional utility functions for data loading pipeline

def sample_dataframe(df: pd.DataFrame, n: int = None, frac: float = None,
                    random_state: int = 42) -> pd.DataFrame:
    """Sample rows from dataframe for testing/development."""
    if n is not None:
        return df.sample(n=min(n, len(df)), random_state=random_state)
    elif frac is not None:
        return df.sample(frac=frac, random_state=random_state)
    else:
        raise ValueError("Must specify either n or frac")


def get_column_statistics(df: pd.DataFrame, column: str) -> Dict[str, Any]:
    """Get comprehensive statistics for a single column."""
    stats = {
        'name': column,
        'dtype': str(df[column].dtype),
        'null_count': int(df[column].isna().sum()),
        'null_percentage': df[column].isna().sum() / len(df) * 100,
        'unique_count': int(df[column].nunique())
    }

    if pd.api.types.is_numeric_dtype(df[column]):
        stats.update({
            'mean': float(df[column].mean()),
            'median': float(df[column].median()),
            'std': float(df[column].std()),
            'min': float(df[column].min()),
            'max': float(df[column].max())
        })

    return stats


if __name__ == "__main__":
    # Example usage and testing
    print("Data Loader Module - Example Usage")
    print("=" * 50)

    # This would be used in practice:
    # df = load_transactions("data/raw/transactions_v1.csv")
    # df = parse_dates(df, 'date')
    # active_df = filter_active(df, days=30)
    # print(f"Loaded {len(active_df)} active customers")
