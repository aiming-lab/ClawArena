"""
Configuration Module for Customer Churn Analysis Project

This module centralizes all configuration parameters, constants, and settings
used throughout the churn analysis pipeline. It provides a single source of
truth for data paths, field mappings, analysis parameters, and model configurations.

By centralizing configuration, we ensure consistency across different modules
and make it easy to adjust parameters without modifying code.

Author: Engineering Team
Created: 2025-03-01
Last Modified: 2025-03-12
Version: 1.2.0

Usage Example:
    >>> from config import DATA_DIR, FIELD_MAP, CHURN_DEFINITION
    >>> print(f"Data directory: {DATA_DIR}")
    >>> print(f"Revenue field: {FIELD_MAP['revenue']}")
    >>> print(f"Churn threshold: {CHURN_DEFINITION['days_inactive']}")
"""

import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


# ============================================================================
# PROJECT STRUCTURE AND PATHS
# ============================================================================

# Base project directory (relative to this file)
PROJECT_ROOT = Path(__file__).parent.parent

# Data directories
DATA_DIR = "data/"
RAW_DIR = DATA_DIR + "raw/"
PROCESSED_DIR = DATA_DIR + "processed/"
INTERIM_DIR = DATA_DIR + "interim/"

# Output directories
REPORTS_DIR = "reports/"
FIGURES_DIR = REPORTS_DIR + "figures/"
MODELS_DIR = "models/"
LOGS_DIR = "logs/"

# Full paths (absolute from project root)
FULL_RAW_DIR = PROJECT_ROOT / "data" / "raw"
FULL_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
FULL_REPORTS_DIR = PROJECT_ROOT / "reports"
FULL_MODELS_DIR = PROJECT_ROOT / "models"
FULL_LOGS_DIR = PROJECT_ROOT / "logs"


# ============================================================================
# DATA SOURCE CONFIGURATION
# ============================================================================

# Primary data files
TRANSACTIONS_FILE = "transactions_v1.csv"
CUSTOMERS_FILE = "customers.csv"
PRODUCTS_FILE = "products.csv"

# Full paths to data files
TRANSACTIONS_PATH = FULL_RAW_DIR / TRANSACTIONS_FILE
CUSTOMERS_PATH = FULL_RAW_DIR / CUSTOMERS_FILE
PRODUCTS_PATH = FULL_RAW_DIR / PRODUCTS_FILE

# Data file encodings
DEFAULT_ENCODING = 'utf-8'
FALLBACK_ENCODINGS = ['latin-1', 'iso-8859-1', 'cp1252']

# CSV parsing parameters
CSV_PARSE_CONFIG = {
    'sep': ',',
    'na_values': ['NA', 'N/A', 'null', 'NULL', '', 'None', 'NONE'],
    'keep_default_na': True,
    'low_memory': False,
    'skipinitialspace': True
}


# ============================================================================
# FIELD MAPPINGS AND SCHEMA DEFINITIONS
# ============================================================================

# Field name mappings from raw data to standardized names
# NOTE: There is a known issue here that needs to be fixed
# The transactions CSV uses "order_value" but this mapping incorrectly uses "amount"
# This should be updated to: "revenue": "order_value"
FIELD_MAP = {
    "customer_id": "customer_id",
    "revenue": "amount",       # BUG: Should be "order_value" not "amount"
    "date": "transaction_date",
    "transaction_id": "transaction_id",
    "product_id": "product_id",
    "quantity": "quantity"
}

# Transactions schema definition
TRANSACTIONS_SCHEMA = {
    'transaction_id': 'object',
    'customer_id': 'object',
    'date': 'datetime64[ns]',
    'order_value': 'float64',
    'product_id': 'object',
    'quantity': 'int64'
}

# Customers schema definition
CUSTOMERS_SCHEMA = {
    'customer_id': 'object',
    'signup_date': 'datetime64[ns]',
    'email': 'object',
    'segment': 'object',
    'region': 'object',
    'age': 'int64',
    'gender': 'object',
    'is_churned': 'int64'
}

# Expected date formats in input data
DATE_FORMATS = [
    "%Y-%m-%d",           # ISO format: 2024-01-15
    "%m/%d/%Y",           # US format: 01/15/2024
    "%d/%m/%Y",           # EU format: 15/01/2024
    "%Y-%m-%d %H:%M:%S",  # ISO with time: 2024-01-15 14:30:00
    "%m/%d/%y",           # Short US: 01/15/24
    "%d-%b-%Y",           # Text month: 15-Jan-2024
]

# Required columns for different data types
REQUIRED_COLUMNS = {
    'transactions': ['transaction_id', 'customer_id', 'date', 'order_value'],
    'customers': ['customer_id', 'signup_date'],
    'products': ['product_id', 'product_name', 'category']
}


# ============================================================================
# CHURN ANALYSIS CONFIGURATION
# ============================================================================

# Churn definition parameters
# Based on Alex's definition from 2025-03-03 kickoff meeting
CHURN_DEFINITION = {
    'days_inactive': 30,              # Days without activity to be considered churned
    'min_transactions': 1,             # Minimum transactions to be considered a customer
    'lookback_period_days': 365,      # Period to analyze for churn calculation
    'prediction_window_days': 90      # Future window to predict churn
}

# Customer activity thresholds
ACTIVITY_THRESHOLDS = {
    'very_active': 10,      # Transactions per month
    'active': 5,
    'moderate': 2,
    'inactive': 1,
    'churned': 0
}

# Revenue segmentation thresholds (in USD)
REVENUE_SEGMENTS = {
    'vip': 10000,           # >$10k total revenue
    'high_value': 5000,     # >$5k
    'medium_value': 1000,   # >$1k
    'low_value': 100,       # >$100
    'minimal': 0            # <$100
}


# ============================================================================
# ANALYSIS PARAMETERS
# ============================================================================

# Statistical significance level
ALPHA = 0.05
CONFIDENCE_LEVEL = 0.95

# Minimum sample sizes for statistical tests
MIN_SAMPLE_SIZE = 30
MIN_SEGMENT_SIZE = 100

# Outlier detection parameters
OUTLIER_IQR_MULTIPLIER = 1.5
OUTLIER_ZSCORE_THRESHOLD = 3.0
OUTLIER_QUANTILE_LOWER = 0.001
OUTLIER_QUANTILE_UPPER = 0.999

# Missing data thresholds
MAX_NULL_PERCENTAGE = 0.5   # Maximum 50% nulls per column
MIN_DATA_COMPLETENESS = 0.7 # Minimum 70% complete data required

# Feature engineering parameters
FEATURE_ENGINEERING = {
    'create_rfm_scores': True,
    'create_date_features': True,
    'create_aggregations': True,
    'aggregation_periods': ['7d', '30d', '90d', '365d'],
    'rolling_window_sizes': [7, 30, 90]
}


# ============================================================================
# MODEL CONFIGURATION
# ============================================================================

# Random seed for reproducibility
RANDOM_STATE = 42
RANDOM_SEED = 42

# Train/test split parameters
TRAIN_TEST_SPLIT = {
    'test_size': 0.2,
    'random_state': RANDOM_STATE,
    'stratify': True,          # Stratify by churn label
    'shuffle': True
}

# Cross-validation parameters
CROSS_VALIDATION = {
    'n_folds': 5,
    'scoring': ['accuracy', 'precision', 'recall', 'f1', 'roc_auc'],
    'random_state': RANDOM_STATE
}

# Model hyperparameters (example configurations)
MODEL_PARAMS = {
    'logistic_regression': {
        'penalty': 'l2',
        'C': 1.0,
        'solver': 'lbfgs',
        'max_iter': 1000,
        'random_state': RANDOM_STATE
    },
    'random_forest': {
        'n_estimators': 100,
        'max_depth': 10,
        'min_samples_split': 5,
        'min_samples_leaf': 2,
        'random_state': RANDOM_STATE
    },
    'gradient_boosting': {
        'n_estimators': 100,
        'learning_rate': 0.1,
        'max_depth': 5,
        'random_state': RANDOM_STATE
    },
    'xgboost': {
        'n_estimators': 100,
        'learning_rate': 0.1,
        'max_depth': 6,
        'min_child_weight': 1,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'random_state': RANDOM_STATE
    }
}

# Feature selection parameters
FEATURE_SELECTION = {
    'method': 'mutual_info',      # Options: 'mutual_info', 'chi2', 'f_classif'
    'n_features': 20,             # Number of top features to select
    'threshold': 0.01             # Minimum importance threshold
}

# Model evaluation thresholds
MODEL_PERFORMANCE_THRESHOLDS = {
    'min_accuracy': 0.75,
    'min_precision': 0.70,
    'min_recall': 0.65,
    'min_f1': 0.70,
    'min_roc_auc': 0.80
}


# ============================================================================
# VISUALIZATION CONFIGURATION
# ============================================================================

# Plot style and theme
PLOT_STYLE = 'seaborn-v0_8-darkgrid'
COLOR_PALETTE = 'husl'

# Default figure size (width, height in inches)
DEFAULT_FIGSIZE = (10, 6)
LARGE_FIGSIZE = (14, 8)
SMALL_FIGSIZE = (8, 5)

# Plot export settings
PLOT_EXPORT_CONFIG = {
    'dpi': 300,
    'bbox_inches': 'tight',
    'transparent': False,
    'format': 'png'
}

# Color schemes for different plot types
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'success': '#06A77D',
    'warning': '#F18F01',
    'danger': '#C73E1D',
    'info': '#6C757D',
    'churned': '#E63946',
    'not_churned': '#06A77D'
}

# Chart-specific configurations
CHART_CONFIG = {
    'churn_rate_bar': {
        'color': COLORS['danger'],
        'figsize': (10, 6),
        'title_fontsize': 14,
        'label_fontsize': 12
    },
    'distribution_hist': {
        'bins': 30,
        'alpha': 0.7,
        'figsize': (12, 5)
    },
    'correlation_heatmap': {
        'cmap': 'coolwarm',
        'annot': True,
        'fmt': '.2f',
        'figsize': (12, 10)
    }
}


# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Log file settings
LOG_FILE = FULL_LOGS_DIR / f"churn_analysis_{datetime.now().strftime('%Y%m%d')}.log"
LOG_LEVEL = 'INFO'  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Module-specific log levels
MODULE_LOG_LEVELS = {
    'data_loader': 'INFO',
    'analysis': 'INFO',
    'modeling': 'INFO',
    'utils': 'WARNING'
}

# Log rotation settings
LOG_ROTATION = {
    'max_bytes': 10 * 1024 * 1024,  # 10 MB
    'backup_count': 5,               # Keep 5 backup files
}


# ============================================================================
# PERFORMANCE AND MEMORY CONFIGURATION
# ============================================================================

# Data loading batch/chunk sizes
CHUNK_SIZE = 10000
MAX_FILE_SIZE_MB = 500

# Memory optimization settings
MEMORY_OPTIMIZATION = {
    'optimize_dtypes': True,
    'use_categorical': True,
    'compress_strings': True,
    'max_categories': 50  # Convert to category if unique values < this
}

# Parallel processing settings
PARALLEL_PROCESSING = {
    'n_jobs': -1,              # -1 = use all available cores
    'backend': 'loky',         # Options: 'loky', 'threading', 'multiprocessing'
    'batch_size': 'auto',
    'verbose': 0
}

# Caching configuration
CACHING = {
    'enable_cache': True,
    'cache_dir': FULL_PROCESSED_DIR / '.cache',
    'cache_expiry_days': 7,
    'max_cache_size_mb': 1000
}


# ============================================================================
# REPORTING CONFIGURATION
# ============================================================================

# Report generation settings
REPORT_CONFIG = {
    'title': 'Customer Churn Analysis Report',
    'author': 'Analytics Team',
    'company': 'OpenClaw Inc.',
    'logo_path': None,  # Path to company logo if available
    'include_executive_summary': True,
    'include_technical_details': True,
    'include_recommendations': True
}

# Report sections and their order
REPORT_SECTIONS = [
    'executive_summary',
    'data_overview',
    'churn_analysis',
    'statistical_analysis',
    'customer_segmentation',
    'predictive_modeling',
    'recommendations',
    'technical_appendix'
]

# Metrics to include in executive summary
EXECUTIVE_METRICS = [
    'total_customers',
    'overall_churn_rate',
    'avg_customer_lifetime_value',
    'avg_order_value',
    'total_revenue',
    'revenue_at_risk'
]

# Export formats for reports
EXPORT_FORMATS = ['html', 'pdf', 'docx']


# ============================================================================
# BUSINESS RULES AND DOMAIN KNOWLEDGE
# ============================================================================

# Business calendar (for seasonality analysis)
BUSINESS_CALENDAR = {
    'fiscal_year_start': 1,  # January
    'holiday_periods': [
        ('2024-11-25', '2024-11-29'),  # Thanksgiving week
        ('2024-12-20', '2025-01-05'),  # Holiday season
        ('2024-07-01', '2024-07-07'),  # Summer sale period
    ],
    'quarter_ends': [3, 6, 9, 12]  # Months when quarters end
}

# Industry benchmarks (for comparison)
INDUSTRY_BENCHMARKS = {
    'churn_rate': 0.15,           # 15% industry average churn
    'avg_customer_lifetime_months': 24,
    'revenue_per_customer': 1200,
    'avg_order_value': 85
}

# Customer lifecycle stages
LIFECYCLE_STAGES = {
    'new': (0, 30),          # Days since first transaction
    'active': (31, 180),
    'mature': (181, 365),
    'veteran': (366, 730),
    'at_risk': (731, float('inf'))
}

# Product categories and their importance weights
# (Used for weighted metrics and prioritization)
PRODUCT_CATEGORIES = {
    'electronics': 1.5,
    'apparel': 1.0,
    'home_goods': 1.2,
    'books': 0.8,
    'sports': 1.1
}


# ============================================================================
# INTEGRATION AND API CONFIGURATION
# ============================================================================

# Email notification settings (for automated reports)
EMAIL_CONFIG = {
    'enabled': False,
    'smtp_server': 'smtp.example.com',
    'smtp_port': 587,
    'use_tls': True,
    'sender_email': 'analytics@example.com',
    'recipient_emails': [
        'alex@example.com',
        'maya@example.com',
        'jordan@example.com'
    ]
}

# Database connection settings (if applicable)
DATABASE_CONFIG = {
    'type': 'postgresql',  # or 'mysql', 'sqlite', etc.
    'host': 'localhost',
    'port': 5432,
    'database': 'churn_analysis',
    'username': 'analytics_user',
    'password': None,  # Use environment variable
    'connection_timeout': 30
}

# API endpoints (if data comes from API)
API_CONFIG = {
    'base_url': 'https://api.example.com/v1',
    'endpoints': {
        'transactions': '/transactions',
        'customers': '/customers',
        'products': '/products'
    },
    'auth_token': None,  # Use environment variable
    'timeout': 30,
    'retry_attempts': 3
}


# ============================================================================
# ENVIRONMENT-SPECIFIC SETTINGS
# ============================================================================

# Determine environment (development, staging, production)
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Environment-specific overrides
if ENVIRONMENT == 'production':
    LOG_LEVEL = 'WARNING'
    CACHING['enable_cache'] = True
    EMAIL_CONFIG['enabled'] = True

elif ENVIRONMENT == 'staging':
    LOG_LEVEL = 'INFO'
    CACHING['enable_cache'] = True
    EMAIL_CONFIG['enabled'] = False

else:  # development
    LOG_LEVEL = 'DEBUG'
    CACHING['enable_cache'] = False
    EMAIL_CONFIG['enabled'] = False


# ============================================================================
# VALIDATION AND CONSTRAINTS
# ============================================================================

# Data validation rules
VALIDATION_RULES = {
    'transactions': {
        'order_value': {
            'min': 0,
            'max': 100000,
            'required': True
        },
        'quantity': {
            'min': 1,
            'max': 1000,
            'required': True
        },
        'date': {
            'min_date': '2020-01-01',
            'max_date': None,  # None = current date
            'required': True
        }
    },
    'customers': {
        'age': {
            'min': 18,
            'max': 120,
            'required': False
        },
        'email': {
            'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'required': False
        }
    }
}

# Quality score thresholds
DATA_QUALITY_THRESHOLDS = {
    'excellent': 0.95,  # >95% data quality score
    'good': 0.85,
    'acceptable': 0.70,
    'poor': 0.50
}


# ============================================================================
# FEATURE DEFINITIONS
# ============================================================================

# List of features to create for modeling
FEATURE_DEFINITIONS = [
    # Recency features
    'days_since_last_transaction',
    'days_since_first_transaction',
    'days_since_last_7d_activity',
    'days_since_last_30d_activity',

    # Frequency features
    'transaction_count',
    'transaction_count_7d',
    'transaction_count_30d',
    'transaction_count_90d',
    'avg_transactions_per_month',

    # Monetary features
    'total_revenue',
    'avg_order_value',
    'std_order_value',
    'min_order_value',
    'max_order_value',
    'revenue_7d',
    'revenue_30d',
    'revenue_90d',

    # Trend features
    'revenue_trend_30d',
    'transaction_frequency_trend',
    'avg_days_between_transactions',

    # Categorical features
    'customer_segment',
    'customer_region',
    'preferred_category',

    # RFM scores
    'rfm_score',
    'r_score',
    'f_score',
    'm_score'
]

# Features to exclude from modeling (identifiers, targets, etc.)
EXCLUDE_FEATURES = [
    'customer_id',
    'transaction_id',
    'email',
    'is_churned',  # Target variable
    'churn_date',
    'customer_name'
]


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_config_value(key: str, default: Any = None) -> Any:
    """
    Get configuration value by key with optional default.

    Args:
        key (str): Configuration key (can be nested with dots, e.g., 'CHURN_DEFINITION.days_inactive')
        default (Any): Default value if key not found

    Returns:
        Any: Configuration value

    Example:
        >>> days = get_config_value('CHURN_DEFINITION.days_inactive', 30)
        >>> print(days)
        30
    """
    keys = key.split('.')
    value = globals()

    try:
        for k in keys:
            value = value[k]
        return value
    except (KeyError, TypeError):
        return default


def validate_config() -> List[str]:
    """
    Validate configuration settings and return list of issues.

    Returns:
        List[str]: List of validation issues (empty if valid)

    Example:
        >>> issues = validate_config()
        >>> if issues:
        ...     print("Configuration issues:", issues)
    """
    issues = []

    # Check required directories exist or can be created
    required_dirs = [FULL_RAW_DIR, FULL_PROCESSED_DIR, FULL_REPORTS_DIR]
    for dir_path in required_dirs:
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            issues.append(f"Cannot create directory {dir_path}: {str(e)}")

    # Validate ALPHA is between 0 and 1
    if not 0 < ALPHA < 1:
        issues.append(f"ALPHA must be between 0 and 1, got {ALPHA}")

    # Validate RANDOM_STATE is an integer
    if not isinstance(RANDOM_STATE, int):
        issues.append(f"RANDOM_STATE must be an integer, got {type(RANDOM_STATE)}")

    # Check that field mappings are valid
    if not isinstance(FIELD_MAP, dict):
        issues.append("FIELD_MAP must be a dictionary")

    # Validate churn definition parameters
    if CHURN_DEFINITION['days_inactive'] <= 0:
        issues.append("CHURN_DEFINITION.days_inactive must be positive")

    return issues


def print_config_summary() -> None:
    """
    Print a summary of key configuration settings.

    Example:
        >>> print_config_summary()
    """
    print("=" * 60)
    print("CONFIGURATION SUMMARY")
    print("=" * 60)
    print(f"Environment: {ENVIRONMENT}")
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Raw Data Directory: {FULL_RAW_DIR}")
    print(f"Processed Data Directory: {FULL_PROCESSED_DIR}")
    print(f"Reports Directory: {FULL_REPORTS_DIR}")
    print(f"\nChurn Definition:")
    print(f"  Days Inactive Threshold: {CHURN_DEFINITION['days_inactive']}")
    print(f"  Lookback Period: {CHURN_DEFINITION['lookback_period_days']} days")
    print(f"\nAnalysis Parameters:")
    print(f"  Significance Level (alpha): {ALPHA}")
    print(f"  Random State: {RANDOM_STATE}")
    print(f"  Min Sample Size: {MIN_SAMPLE_SIZE}")
    print(f"\nData Files:")
    print(f"  Transactions: {TRANSACTIONS_FILE}")
    print(f"  Customers: {CUSTOMERS_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    # When run directly, print configuration summary and validate
    print_config_summary()

    print("\nValidating configuration...")
    issues = validate_config()

    if issues:
        print("\nConfiguration Issues Found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\nConfiguration validation passed!")
