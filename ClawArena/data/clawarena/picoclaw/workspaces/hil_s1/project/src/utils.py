"""
Utility Functions Module

This module provides common utility functions used across the churn analysis project.
It includes helpers for file I/O, data formatting, logging, configuration management,
and general-purpose utilities that support the main analysis pipeline.

Author: Engineering Team
Created: 2025-03-01
Last Modified: 2025-03-12
Version: 1.1.0

Dependencies:
    - pandas>=2.2.0
    - numpy>=1.26.0
    - pyyaml>=6.0.1

Usage Example:
    >>> from utils import format_currency, setup_logging, read_config
    >>> logger = setup_logging('my_module')
    >>> config = read_config('config.yaml')
    >>> formatted = format_currency(1234.56)
    >>> print(formatted)
    $1,234.56
"""

import os
import sys
import json
import yaml
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Tuple
import pandas as pd
import numpy as np
from functools import wraps
import time
import hashlib
import pickle
import warnings


# Global constants
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DEFAULT_LOG_LEVEL = logging.INFO


def setup_logging(name: str = __name__,
                 level: int = DEFAULT_LOG_LEVEL,
                 log_file: Optional[str] = None,
                 console: bool = True) -> logging.Logger:
    """
    Set up logging configuration with file and console handlers.

    Args:
        name (str): Logger name (usually __name__ from calling module)
        level (int): Logging level (e.g., logging.INFO, logging.DEBUG)
        log_file (Optional[str]): Path to log file (if None, no file logging)
        console (bool): Whether to output to console

    Returns:
        logging.Logger: Configured logger instance

    Example:
        >>> logger = setup_logging('data_pipeline', level=logging.DEBUG)
        >>> logger.info("Pipeline started")
        >>> logger.debug("Processing batch 1")
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    # Console handler
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler
    if log_file:
        # Ensure directory exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def read_config(config_path: str, format: str = 'auto') -> Dict[str, Any]:
    """
    Read configuration from YAML or JSON file.

    Args:
        config_path (str): Path to configuration file
        format (str): File format ('yaml', 'json', or 'auto' to detect)

    Returns:
        Dict[str, Any]: Configuration dictionary

    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If format is unsupported or file is malformed

    Example:
        >>> config = read_config('config.yaml')
        >>> database_url = config['database']['url']
        >>> api_key = config['api']['key']
    """
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    # Auto-detect format from extension
    if format == 'auto':
        if config_path.suffix in ['.yaml', '.yml']:
            format = 'yaml'
        elif config_path.suffix == '.json':
            format = 'json'
        else:
            raise ValueError(f"Cannot auto-detect format for extension: {config_path.suffix}")

    # Read file
    with open(config_path, 'r') as f:
        if format == 'yaml':
            config = yaml.safe_load(f)
        elif format == 'json':
            config = json.load(f)
        else:
            raise ValueError(f"Unsupported format: {format}")

    return config


def write_config(config: Dict[str, Any], config_path: str, format: str = 'auto') -> None:
    """
    Write configuration dictionary to YAML or JSON file.

    Args:
        config (Dict[str, Any]): Configuration dictionary
        config_path (str): Path to output file
        format (str): File format ('yaml', 'json', or 'auto' to detect)

    Example:
        >>> config = {'database': {'host': 'localhost', 'port': 5432}}
        >>> write_config(config, 'config.yaml')
    """
    config_path = Path(config_path)

    # Auto-detect format from extension
    if format == 'auto':
        if config_path.suffix in ['.yaml', '.yml']:
            format = 'yaml'
        elif config_path.suffix == '.json':
            format = 'json'
        else:
            raise ValueError(f"Cannot auto-detect format for extension: {config_path.suffix}")

    # Ensure directory exists
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Write file
    with open(config_path, 'w') as f:
        if format == 'yaml':
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        elif format == 'json':
            json.dump(config, f, indent=2)


def format_currency(amount: float, currency: str = 'USD', symbol: str = '$') -> str:
    """
    Format numeric amount as currency string.

    Args:
        amount (float): Numeric amount
        currency (str): Currency code (for reference/logging)
        symbol (str): Currency symbol to use

    Returns:
        str: Formatted currency string

    Example:
        >>> format_currency(1234.56)
        '$1,234.56'
        >>> format_currency(1000000)
        '$1,000,000.00'
    """
    if pd.isna(amount):
        return "N/A"

    return f"{symbol}{amount:,.2f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format decimal value as percentage string.

    Args:
        value (float): Decimal value (e.g., 0.15 for 15%)
        decimals (int): Number of decimal places

    Returns:
        str: Formatted percentage string

    Example:
        >>> format_percentage(0.1534)
        '15.3%'
        >>> format_percentage(0.1534, decimals=2)
        '15.34%'
    """
    if pd.isna(value):
        return "N/A"

    return f"{value * 100:.{decimals}f}%"


def format_number(value: Union[int, float], decimals: int = 0,
                 use_separator: bool = True) -> str:
    """
    Format number with thousand separators.

    Args:
        value (Union[int, float]): Numeric value
        decimals (int): Number of decimal places
        use_separator (bool): Whether to use thousand separator

    Returns:
        str: Formatted number string

    Example:
        >>> format_number(1234567)
        '1,234,567'
        >>> format_number(1234.5678, decimals=2)
        '1,234.57'
    """
    if pd.isna(value):
        return "N/A"

    if use_separator:
        return f"{value:,.{decimals}f}"
    else:
        return f"{value:.{decimals}f}"


def ensure_dir(directory: Union[str, Path]) -> Path:
    """
    Ensure directory exists, create if it doesn't.

    Args:
        directory (Union[str, Path]): Directory path

    Returns:
        Path: Path object for the directory

    Example:
        >>> ensure_dir('data/processed')
        PosixPath('data/processed')
    """
    dir_path = Path(directory)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def get_timestamp(format: str = '%Y%m%d_%H%M%S') -> str:
    """
    Get current timestamp as formatted string.

    Args:
        format (str): strftime format string

    Returns:
        str: Formatted timestamp

    Example:
        >>> timestamp = get_timestamp()
        >>> print(timestamp)
        20250312_143052
    """
    return datetime.now().strftime(format)


def timer(func):
    """
    Decorator to measure function execution time.

    Example:
        >>> @timer
        ... def slow_function():
        ...     time.sleep(2)
        ...     return "done"
        >>> result = slow_function()
        Function 'slow_function' executed in 2.00 seconds
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time

        logger = logging.getLogger(func.__module__)
        logger.info(f"Function '{func.__name__}' executed in {execution_time:.2f} seconds")

        return result

    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Decorator to retry function on failure.

    Args:
        max_attempts (int): Maximum number of retry attempts
        delay (float): Initial delay between retries (seconds)
        backoff (float): Multiplier for delay after each attempt

    Example:
        >>> @retry(max_attempts=3, delay=1.0)
        ... def unstable_api_call():
        ...     # Code that might fail
        ...     return make_api_request()
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            logger = logging.getLogger(func.__module__)

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        logger.error(f"Function '{func.__name__}' failed after {max_attempts} attempts")
                        raise

                    logger.warning(
                        f"Function '{func.__name__}' failed (attempt {attempt}/{max_attempts}): {str(e)}"
                    )
                    logger.info(f"Retrying in {current_delay:.1f} seconds...")
                    time.sleep(current_delay)
                    current_delay *= backoff

        return wrapper
    return decorator


def compute_hash(data: Union[str, bytes], algorithm: str = 'md5') -> str:
    """
    Compute hash of data using specified algorithm.

    Args:
        data (Union[str, bytes]): Data to hash
        algorithm (str): Hash algorithm ('md5', 'sha1', 'sha256')

    Returns:
        str: Hexadecimal hash string

    Example:
        >>> compute_hash("hello world")
        '5eb63bbbe01eeed093cb22bb8f5acdc3'
    """
    if isinstance(data, str):
        data = data.encode('utf-8')

    if algorithm == 'md5':
        hasher = hashlib.md5()
    elif algorithm == 'sha1':
        hasher = hashlib.sha1()
    elif algorithm == 'sha256':
        hasher = hashlib.sha256()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    hasher.update(data)
    return hasher.hexdigest()


def save_pickle(obj: Any, filepath: str) -> None:
    """
    Save Python object to pickle file.

    Args:
        obj (Any): Object to save
        filepath (str): Path to output file

    Example:
        >>> model = train_model(data)
        >>> save_pickle(model, 'models/trained_model.pkl')
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, 'wb') as f:
        pickle.dump(obj, f)

    logger = logging.getLogger(__name__)
    logger.info(f"Object saved to {filepath}")


def load_pickle(filepath: str) -> Any:
    """
    Load Python object from pickle file.

    Args:
        filepath (str): Path to pickle file

    Returns:
        Any: Loaded object

    Example:
        >>> model = load_pickle('models/trained_model.pkl')
        >>> predictions = model.predict(test_data)
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"Pickle file not found: {filepath}")

    with open(filepath, 'rb') as f:
        obj = pickle.load(f)

    logger = logging.getLogger(__name__)
    logger.info(f"Object loaded from {filepath}")

    return obj


def dataframe_memory_usage(df: pd.DataFrame, detailed: bool = False) -> Union[float, pd.Series]:
    """
    Calculate memory usage of dataframe.

    Args:
        df (pd.DataFrame): Input dataframe
        detailed (bool): If True, return per-column usage; if False, return total

    Returns:
        Union[float, pd.Series]: Total memory in MB or series of per-column usage

    Example:
        >>> memory_mb = dataframe_memory_usage(df)
        >>> print(f"Dataframe uses {memory_mb:.2f} MB")
    """
    memory_bytes = df.memory_usage(deep=True)

    if detailed:
        return memory_bytes / 1024**2  # Convert to MB
    else:
        return memory_bytes.sum() / 1024**2


def optimize_dataframe_dtypes(df: pd.DataFrame, inplace: bool = False) -> pd.DataFrame:
    """
    Optimize dataframe memory usage by converting to appropriate dtypes.

    Converts:
    - int64 to smaller int types where possible
    - float64 to float32 where possible
    - object to category for low-cardinality columns

    Args:
        df (pd.DataFrame): Input dataframe
        inplace (bool): Whether to modify dataframe in place

    Returns:
        pd.DataFrame: Optimized dataframe

    Example:
        >>> optimized_df = optimize_dataframe_dtypes(df)
        >>> print(f"Memory saved: {original_mb - optimized_mb:.2f} MB")
    """
    if not inplace:
        df = df.copy()

    logger = logging.getLogger(__name__)
    initial_memory = dataframe_memory_usage(df)

    # Optimize integers
    int_cols = df.select_dtypes(include=['int64']).columns
    for col in int_cols:
        col_min = df[col].min()
        col_max = df[col].max()

        if col_min >= 0:
            if col_max < 255:
                df[col] = df[col].astype(np.uint8)
            elif col_max < 65535:
                df[col] = df[col].astype(np.uint16)
            elif col_max < 4294967295:
                df[col] = df[col].astype(np.uint32)
        else:
            if col_min > np.iinfo(np.int8).min and col_max < np.iinfo(np.int8).max:
                df[col] = df[col].astype(np.int8)
            elif col_min > np.iinfo(np.int16).min and col_max < np.iinfo(np.int16).max:
                df[col] = df[col].astype(np.int16)
            elif col_min > np.iinfo(np.int32).min and col_max < np.iinfo(np.int32).max:
                df[col] = df[col].astype(np.int32)

    # Optimize floats
    float_cols = df.select_dtypes(include=['float64']).columns
    for col in float_cols:
        df[col] = df[col].astype(np.float32)

    # Convert low-cardinality object columns to category
    object_cols = df.select_dtypes(include=['object']).columns
    for col in object_cols:
        num_unique = df[col].nunique()
        num_total = len(df[col])

        if num_unique / num_total < 0.5:  # Less than 50% unique values
            df[col] = df[col].astype('category')

    final_memory = dataframe_memory_usage(df)
    memory_saved = initial_memory - final_memory

    logger.info(f"Memory optimization: {initial_memory:.2f} MB -> {final_memory:.2f} MB")
    logger.info(f"Saved: {memory_saved:.2f} MB ({memory_saved/initial_memory*100:.1f}%)")

    return df


def chunk_dataframe(df: pd.DataFrame, chunk_size: int = 10000):
    """
    Generator to iterate over dataframe in chunks.

    Args:
        df (pd.DataFrame): Input dataframe
        chunk_size (int): Number of rows per chunk

    Yields:
        pd.DataFrame: Chunk of dataframe

    Example:
        >>> for chunk in chunk_dataframe(large_df, chunk_size=5000):
        ...     process_chunk(chunk)
    """
    for i in range(0, len(df), chunk_size):
        yield df.iloc[i:i + chunk_size]


def detect_outliers_iqr(series: pd.Series, multiplier: float = 1.5) -> pd.Series:
    """
    Detect outliers using IQR method.

    Args:
        series (pd.Series): Input numeric series
        multiplier (float): IQR multiplier (default 1.5 for standard outliers)

    Returns:
        pd.Series: Boolean series indicating outliers

    Example:
        >>> outliers = detect_outliers_iqr(df['revenue'])
        >>> print(f"Found {outliers.sum()} outliers")
    """
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR

    return (series < lower_bound) | (series > upper_bound)


def detect_outliers_zscore(series: pd.Series, threshold: float = 3.0) -> pd.Series:
    """
    Detect outliers using z-score method.

    Args:
        series (pd.Series): Input numeric series
        threshold (float): Z-score threshold (default 3.0)

    Returns:
        pd.Series: Boolean series indicating outliers

    Example:
        >>> outliers = detect_outliers_zscore(df['transaction_amount'])
        >>> df_clean = df[~outliers]
    """
    z_scores = np.abs((series - series.mean()) / series.std())
    return z_scores > threshold


def calculate_missing_percentage(df: pd.DataFrame) -> pd.Series:
    """
    Calculate percentage of missing values for each column.

    Args:
        df (pd.DataFrame): Input dataframe

    Returns:
        pd.Series: Percentage of missing values per column

    Example:
        >>> missing_pct = calculate_missing_percentage(df)
        >>> high_missing = missing_pct[missing_pct > 10]
        >>> print(f"Columns with >10% missing: {high_missing}")
    """
    return (df.isnull().sum() / len(df) * 100).sort_values(ascending=False)


def impute_missing_values(df: pd.DataFrame, strategy: str = 'mean',
                         columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Impute missing values using specified strategy.

    Args:
        df (pd.DataFrame): Input dataframe
        strategy (str): Imputation strategy ('mean', 'median', 'mode', 'zero')
        columns (Optional[List[str]]): Specific columns to impute (if None, all numeric)

    Returns:
        pd.DataFrame: Dataframe with imputed values

    Example:
        >>> df_imputed = impute_missing_values(df, strategy='median')
    """
    df = df.copy()

    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()

    for col in columns:
        if col not in df.columns:
            warnings.warn(f"Column '{col}' not found, skipping")
            continue

        if strategy == 'mean':
            fill_value = df[col].mean()
        elif strategy == 'median':
            fill_value = df[col].median()
        elif strategy == 'mode':
            fill_value = df[col].mode()[0] if not df[col].mode().empty else 0
        elif strategy == 'zero':
            fill_value = 0
        else:
            raise ValueError(f"Unsupported strategy: {strategy}")

        df[col].fillna(fill_value, inplace=True)

    return df


def create_date_features(df: pd.DataFrame, date_col: str,
                        features: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Extract date features from datetime column.

    Args:
        df (pd.DataFrame): Input dataframe
        date_col (str): Name of datetime column
        features (Optional[List[str]]): List of features to extract
                                       (if None, extracts common features)

    Returns:
        pd.DataFrame: Dataframe with added date features

    Example:
        >>> df = create_date_features(df, 'transaction_date')
        >>> print(df[['transaction_date', 'year', 'month', 'day_of_week']])
    """
    df = df.copy()

    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        df[date_col] = pd.to_datetime(df[date_col])

    if features is None:
        features = ['year', 'month', 'day', 'day_of_week', 'quarter', 'is_weekend']

    prefix = date_col.replace('_date', '').replace('date', '')
    if prefix:
        prefix += '_'

    if 'year' in features:
        df[f'{prefix}year'] = df[date_col].dt.year

    if 'month' in features:
        df[f'{prefix}month'] = df[date_col].dt.month

    if 'day' in features:
        df[f'{prefix}day'] = df[date_col].dt.day

    if 'day_of_week' in features:
        df[f'{prefix}day_of_week'] = df[date_col].dt.dayofweek

    if 'quarter' in features:
        df[f'{prefix}quarter'] = df[date_col].dt.quarter

    if 'is_weekend' in features:
        df[f'{prefix}is_weekend'] = df[date_col].dt.dayofweek.isin([5, 6]).astype(int)

    return df


def validate_dataframe_schema(df: pd.DataFrame, expected_schema: Dict[str, str]) -> Tuple[bool, List[str]]:
    """
    Validate dataframe against expected schema.

    Args:
        df (pd.DataFrame): Dataframe to validate
        expected_schema (Dict[str, str]): Dictionary mapping column names to expected dtypes

    Returns:
        Tuple[bool, List[str]]: (is_valid, list_of_errors)

    Example:
        >>> schema = {'customer_id': 'object', 'revenue': 'float64', 'date': 'datetime64[ns]'}
        >>> is_valid, errors = validate_dataframe_schema(df, schema)
        >>> if not is_valid:
        ...     print("Schema errors:", errors)
    """
    errors = []

    # Check for missing columns
    expected_cols = set(expected_schema.keys())
    actual_cols = set(df.columns)
    missing_cols = expected_cols - actual_cols

    if missing_cols:
        errors.append(f"Missing columns: {missing_cols}")

    # Check data types
    for col, expected_dtype in expected_schema.items():
        if col in df.columns:
            actual_dtype = str(df[col].dtype)
            if actual_dtype != expected_dtype:
                errors.append(f"Column '{col}': expected {expected_dtype}, got {actual_dtype}")

    is_valid = len(errors) == 0
    return is_valid, errors


def generate_report_html(title: str, content: Dict[str, Any],
                        output_path: str) -> None:
    """
    Generate simple HTML report from content dictionary.

    Args:
        title (str): Report title
        content (Dict[str, Any]): Report content (sections and data)
        output_path (str): Path to save HTML file

    Example:
        >>> content = {
        ...     'Summary': {'Total Customers': 10000, 'Churn Rate': '15.3%'},
        ...     'Metrics': {'Revenue': '$1,234,567', 'AOV': '$125.50'}
        ... }
        >>> generate_report_html('Churn Analysis Report', content, 'reports/report.html')
    """
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #333; }}
            h2 {{ color: #666; margin-top: 30px; }}
            table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #4CAF50; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <p>Generated: {timestamp}</p>
        {content_html}
    </body>
    </html>
    """

    content_html = ""
    for section, data in content.items():
        content_html += f"<h2>{section}</h2>\n"

        if isinstance(data, dict):
            content_html += "<table>\n"
            content_html += "<tr><th>Metric</th><th>Value</th></tr>\n"
            for key, value in data.items():
                content_html += f"<tr><td>{key}</td><td>{value}</td></tr>\n"
            content_html += "</table>\n"
        elif isinstance(data, pd.DataFrame):
            content_html += data.to_html()
        else:
            content_html += f"<p>{data}</p>\n"

    html = html_template.format(
        title=title,
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        content_html=content_html
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        f.write(html)

    logger = logging.getLogger(__name__)
    logger.info(f"HTML report generated: {output_path}")


def parallel_apply(df: pd.DataFrame, func, n_jobs: int = -1) -> pd.Series:
    """
    Apply function to dataframe in parallel (requires joblib).

    Args:
        df (pd.DataFrame): Input dataframe
        func: Function to apply
        n_jobs (int): Number of parallel jobs (-1 for all CPUs)

    Returns:
        pd.Series: Result of applying function

    Example:
        >>> result = parallel_apply(df, lambda row: expensive_function(row), n_jobs=4)
    """
    try:
        from joblib import Parallel, delayed
    except ImportError:
        warnings.warn("joblib not installed, falling back to sequential apply")
        return df.apply(func, axis=1)

    results = Parallel(n_jobs=n_jobs)(
        delayed(func)(row) for _, row in df.iterrows()
    )

    return pd.Series(results, index=df.index)


# Environment and system utilities

def get_system_info() -> Dict[str, Any]:
    """
    Get system information for debugging and logging.

    Returns:
        Dict[str, Any]: System information including Python version, OS, etc.
    """
    import platform

    return {
        'python_version': sys.version,
        'platform': platform.platform(),
        'processor': platform.processor(),
        'machine': platform.machine(),
        'pandas_version': pd.__version__,
        'numpy_version': np.__version__
    }


def check_dependencies(required: Dict[str, str]) -> Tuple[bool, List[str]]:
    """
    Check if required package versions are installed.

    Args:
        required (Dict[str, str]): Dictionary of package names to minimum versions

    Returns:
        Tuple[bool, List[str]]: (all_satisfied, list_of_issues)

    Example:
        >>> required = {'pandas': '2.0.0', 'numpy': '1.24.0'}
        >>> satisfied, issues = check_dependencies(required)
        >>> if not satisfied:
        ...     print("Dependency issues:", issues)
    """
    from packaging import version
    import importlib

    issues = []

    for package, min_version in required.items():
        try:
            mod = importlib.import_module(package)
            installed_version = mod.__version__

            if version.parse(installed_version) < version.parse(min_version):
                issues.append(
                    f"{package}: installed {installed_version}, required >={min_version}"
                )
        except ImportError:
            issues.append(f"{package}: not installed (required >={min_version})")

    all_satisfied = len(issues) == 0
    return all_satisfied, issues


if __name__ == "__main__":
    # Example usage
    print("Utility Functions Module")
    print("=" * 50)

    # Set up logging example
    logger = setup_logging('utils_test')
    logger.info("Logger initialized")

    # Formatting examples
    print(f"Currency: {format_currency(1234567.89)}")
    print(f"Percentage: {format_percentage(0.1534)}")
    print(f"Number: {format_number(1234567)}")
    print(f"Timestamp: {get_timestamp()}")
