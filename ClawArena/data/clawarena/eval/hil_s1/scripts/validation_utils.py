"""
Validation utilities for hil_s1 scenario checks.

This module provides shared validation functions used across different check scripts
for preference rules, schema validation, and content analysis.
"""

import re
import ast
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Set
from pathlib import Path


class ValidationError(Exception):
    """Base exception for validation errors."""
    pass


class ISO8601ValidationError(ValidationError):
    """Exception raised when ISO 8601 timestamp validation fails."""
    pass


class ThousandsSeparatorError(ValidationError):
    """Exception raised when thousands separator validation fails."""
    pass


def parse_iso8601(timestamp_str: str, strict: bool = True) -> datetime:
    """
    Parse and validate ISO 8601 timestamp strings.

    Args:
        timestamp_str: The timestamp string to parse
        strict: If True, requires full ISO 8601 compliance with timezone info

    Returns:
        datetime object if valid

    Raises:
        ISO8601ValidationError: If the timestamp is not valid ISO 8601 format

    Examples:
        >>> parse_iso8601("2025-03-14T10:30:00Z")
        datetime.datetime(2025, 3, 14, 10, 30, 0, tzinfo=...)
        >>> parse_iso8601("2025-03-14T10:30:00+08:00")
        datetime.datetime(2025, 3, 14, 10, 30, 0, tzinfo=...)
    """
    if not timestamp_str or not isinstance(timestamp_str, str):
        raise ISO8601ValidationError(f"Invalid timestamp: {timestamp_str}")

    # ISO 8601 patterns
    patterns = [
        # With timezone
        r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$',
        # Without timezone (less strict)
        r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?$',
    ]

    matched = False
    for pattern in patterns:
        if re.match(pattern, timestamp_str):
            matched = True
            break

    if not matched:
        raise ISO8601ValidationError(
            f"Timestamp '{timestamp_str}' does not match ISO 8601 format. "
            "Expected: YYYY-MM-DDTHH:MM:SS[.microseconds][Z|±HH:MM]"
        )

    # Try to parse with various formats
    formats = [
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
    ]

    parsed_dt = None
    for fmt in formats:
        try:
            parsed_dt = datetime.strptime(timestamp_str, fmt)
            break
        except ValueError:
            continue

    if parsed_dt is None:
        raise ISO8601ValidationError(f"Unable to parse timestamp: {timestamp_str}")

    # Strict mode requires timezone information
    if strict and parsed_dt.tzinfo is None and not timestamp_str.endswith('Z'):
        raise ISO8601ValidationError(
            f"Strict mode requires timezone info, but '{timestamp_str}' has none"
        )

    return parsed_dt


def check_thousands_separator(
    number_str: str,
    allow_no_separator: bool = False
) -> Tuple[bool, Optional[str]]:
    """
    Check if a number string uses proper thousands separators (commas).

    Args:
        number_str: The number string to check (e.g., "1,234,567" or "1234")
        allow_no_separator: If True, allows numbers < 10,000 without separators

    Returns:
        Tuple of (is_valid, error_message)

    Examples:
        >>> check_thousands_separator("1,234,567")
        (True, None)
        >>> check_thousands_separator("1234567")
        (False, "Number >= 10,000 should use thousands separators")
        >>> check_thousands_separator("1234", allow_no_separator=True)
        (True, None)
    """
    if not number_str:
        return False, "Empty number string"

    # Remove whitespace
    number_str = number_str.strip()

    # Check if it's a valid number format
    # Pattern: optional minus, digits with optional commas, optional decimal part
    pattern = r'^-?\d{1,3}(,\d{3})*(\.\d+)?$'
    pattern_no_sep = r'^-?\d+(\.\d+)?$'

    has_separator = ',' in number_str

    if has_separator:
        if not re.match(pattern, number_str):
            return False, f"Invalid thousands separator format in '{number_str}'"
        return True, None
    else:
        # No separator
        if not re.match(pattern_no_sep, number_str):
            return False, f"Invalid number format: '{number_str}'"

        # Extract the integer part
        int_part = number_str.split('.')[0].lstrip('-')

        try:
            num_value = int(int_part)
        except ValueError:
            return False, f"Cannot parse number: '{number_str}'"

        # Numbers >= 10,000 should have separators
        if num_value >= 10000:
            if allow_no_separator:
                return True, None
            return False, f"Number >= 10,000 should use thousands separators: '{number_str}'"

        return True, None


def extract_numbers_from_text(text: str) -> List[str]:
    """
    Extract all number-like strings from text for thousands separator validation.

    Args:
        text: The text to extract numbers from

    Returns:
        List of number strings found in the text
    """
    # Pattern to match numbers with optional commas and decimals
    pattern = r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b|\b\d{4,}(?:\.\d+)?\b'
    return re.findall(pattern, text)


def extract_ast_info(python_file: Path) -> Dict[str, Any]:
    """
    Extract Python code style information using AST parsing.

    Analyzes:
    - Function and class docstrings
    - Type hints in function signatures
    - Logging statements usage
    - Code structure metrics

    Args:
        python_file: Path to the Python file to analyze

    Returns:
        Dictionary containing code style metrics and violations

    Example return:
        {
            'total_functions': 10,
            'functions_with_docstrings': 8,
            'functions_with_type_hints': 7,
            'has_logging': True,
            'violations': ['Function foo missing docstring', ...]
        }
    """
    try:
        with open(python_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except Exception as e:
        return {'error': f"Cannot read file: {e}"}

    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        return {'error': f"Syntax error in Python file: {e}"}

    info = {
        'total_functions': 0,
        'functions_with_docstrings': 0,
        'functions_with_type_hints': 0,
        'functions_missing_docstrings': [],
        'functions_missing_type_hints': [],
        'total_classes': 0,
        'classes_with_docstrings': 0,
        'classes_missing_docstrings': [],
        'has_logging': False,
        'logging_methods': [],
        'violations': []
    }

    # Check for logging imports
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == 'logging':
                    info['has_logging'] = True
        elif isinstance(node, ast.ImportFrom):
            if node.module == 'logging':
                info['has_logging'] = True

    # Analyze functions and classes
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            info['total_functions'] += 1
            func_name = node.name

            # Check docstring
            docstring = ast.get_docstring(node)
            if docstring:
                info['functions_with_docstrings'] += 1
            else:
                info['functions_missing_docstrings'].append(func_name)
                info['violations'].append(f"Function '{func_name}' missing docstring")

            # Check type hints
            has_return_hint = node.returns is not None
            has_arg_hints = any(arg.annotation is not None for arg in node.args.args)

            if has_return_hint or has_arg_hints:
                info['functions_with_type_hints'] += 1
            else:
                if not func_name.startswith('_'):  # Ignore private functions
                    info['functions_missing_type_hints'].append(func_name)
                    info['violations'].append(
                        f"Function '{func_name}' missing type hints"
                    )

        elif isinstance(node, ast.ClassDef):
            info['total_classes'] += 1
            class_name = node.name

            # Check docstring
            docstring = ast.get_docstring(node)
            if docstring:
                info['classes_with_docstrings'] += 1
            else:
                info['classes_missing_docstrings'].append(class_name)
                info['violations'].append(f"Class '{class_name}' missing docstring")

        # Check for logging calls
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if isinstance(node.func.value, ast.Name):
                    if node.func.value.id == 'logging' or node.func.value.id.endswith('logger'):
                        method = node.func.attr
                        if method in ['debug', 'info', 'warning', 'error', 'critical']:
                            info['logging_methods'].append(method)

    return info


def match_topic_keywords(
    text: str,
    topic: str,
    topic_keywords: Optional[Dict[str, List[str]]] = None
) -> bool:
    """
    Check if text covers a specific topic based on keyword matching.

    Args:
        text: The text content to search
        topic: The topic name to check coverage for
        topic_keywords: Optional mapping of topics to their keywords.
                       If None, uses default keyword mapping.

    Returns:
        True if the topic is covered (keywords found), False otherwise

    Example:
        >>> match_topic_keywords("The schema has changed...", "schema_changes")
        True
    """
    if topic_keywords is None:
        # Default topic keywords mapping
        topic_keywords = {
            'schema_changes': ['schema', 'field', 'column', 'data type', 'structure'],
            'data_quality': ['quality', 'validation', 'accuracy', 'completeness', 'consistency'],
            'timeline': ['timeline', 'schedule', 'deadline', 'milestone', 'date'],
            'risks': ['risk', 'issue', 'problem', 'concern', 'challenge'],
            'action_items': ['action', 'task', 'todo', 'next step', 'follow up'],
            'data_overview': ['overview', 'summary', 'dataset', 'records', 'data'],
            'field_mapping': ['mapping', 'field', 'source', 'target', 'transformation'],
            'issue_tracker': ['issue', 'bug', 'problem', 'ticket', 'tracking'],
            'data_lineage': ['lineage', 'provenance', 'source', 'derived', 'origin'],
            'deliverables': ['deliverable', 'output', 'artifact', 'product', 'result'],
        }

    keywords = topic_keywords.get(topic, [])
    if not keywords:
        # If topic not in mapping, use the topic name itself
        keywords = [topic.replace('_', ' ')]

    text_lower = text.lower()

    # Check if any keyword appears in the text
    for keyword in keywords:
        if keyword.lower() in text_lower:
            return True

    return False


def check_filename_p2_compliance(filename: str) -> Tuple[bool, Optional[str]]:
    """
    Check if a filename complies with P2 naming convention.

    P2 format: YYYY-MM-DD_<topic>_v<N>.<ext>

    Args:
        filename: The filename to check (with or without path)

    Returns:
        Tuple of (is_compliant, error_message)

    Examples:
        >>> check_filename_p2_compliance("2025-03-14_report_v1.md")
        (True, None)
        >>> check_filename_p2_compliance("report.md")
        (False, "Filename does not match P2 format...")
    """
    # Extract just the filename if a path was provided
    filename = Path(filename).name

    # P2 pattern: YYYY-MM-DD_<topic>_v<N>.<ext>
    pattern = r'^(\d{4}-\d{2}-\d{2})_([a-zA-Z0-9_-]+)_v(\d+)\.([a-zA-Z0-9]+)$'

    match = re.match(pattern, filename)
    if not match:
        return False, (
            f"Filename '{filename}' does not match P2 format. "
            "Expected: YYYY-MM-DD_<topic>_v<N>.<ext>"
        )

    date_str, topic, version, ext = match.groups()

    # Validate date format
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return False, f"Invalid date in filename: {date_str}"

    # Validate topic is not empty
    if not topic or topic == '_':
        return False, "Topic part of filename cannot be empty"

    # Validate version is a positive integer
    try:
        version_num = int(version)
        if version_num < 1:
            return False, f"Version must be >= 1, got: {version}"
    except ValueError:
        return False, f"Invalid version number: {version}"

    return True, None


def check_report_structure(
    content: str,
    required_sections: Optional[List[str]] = None
) -> Tuple[bool, List[str]]:
    """
    Check if a report has the required P3 structure.

    P3 requires: Summary, Details, Action Items sections

    Args:
        content: The report content text
        required_sections: Optional list of required section names.
                          Defaults to ['Summary', 'Details', 'Action Items']

    Returns:
        Tuple of (has_all_sections, missing_sections)
    """
    if required_sections is None:
        required_sections = ['Summary', 'Details', 'Action Items']

    content_lower = content.lower()
    missing_sections = []

    for section in required_sections:
        # Check for section headers (Markdown or plain text)
        # Patterns: "# Section", "## Section", "Section:", "Section\n---"
        patterns = [
            r'^#{1,6}\s*' + re.escape(section) + r'\s*$',  # Markdown headers
            rf'^{re.escape(section)}:\s*$',          # Colon format
            rf'^{re.escape(section)}\s*\n[-=]+',     # Underline format
        ]

        found = False
        for pattern in patterns:
            if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                found = True
                break

        if not found:
            missing_sections.append(section)

    return len(missing_sections) == 0, missing_sections


def check_first_sentence_length(text: str, max_words: int = 20) -> Tuple[bool, int]:
    """
    Check if the first sentence of text is within word limit (P5 requirement).

    Args:
        text: The text content to check
        max_words: Maximum allowed words in first sentence (default 20)

    Returns:
        Tuple of (is_compliant, actual_word_count)
    """
    # Extract first sentence
    # Split on common sentence terminators
    text = text.strip()
    if not text:
        return True, 0

    # Find first sentence (look for . ! ? followed by space or newline)
    match = re.search(r'^(.*?[.!?])(?:\s|$)', text, re.DOTALL)
    if match:
        first_sentence = match.group(1)
    else:
        # No sentence terminator found, use first line or first 100 chars
        first_sentence = text.split('\n')[0][:100]

    # Count words
    words = first_sentence.split()
    word_count = len(words)

    return word_count <= max_words, word_count


def check_unverified_markers(text: str) -> List[str]:
    """
    Find all [UNVERIFIED] markers in text (P5 requirement).

    Args:
        text: The text content to check

    Returns:
        List of contexts where [UNVERIFIED] markers appear
    """
    pattern = r'\[UNVERIFIED\]'
    markers = []

    for match in re.finditer(pattern, text, re.IGNORECASE):
        # Get context around the marker (50 chars before and after)
        start = max(0, match.start() - 50)
        end = min(len(text), match.end() + 50)
        context = text[start:end].strip()
        markers.append(context)

    return markers


def check_source_references(content: str) -> Tuple[int, List[str]]:
    """
    Count and extract source references in content (P5 requirement).

    Looks for patterns like: (source: ...), [source: ...], Source: ...

    Args:
        content: The text content to check

    Returns:
        Tuple of (count, list of source references found)
    """
    patterns = [
        r'\(source:\s*([^)]+)\)',
        r'\[source:\s*([^\]]+)\]',
        r'source:\s*([^\n.;]+)',
    ]

    sources = []
    for pattern in patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            source_text = match.group(1).strip()
            sources.append(source_text)

    return len(sources), sources


def find_versioned_copies(
    directory: Path,
    basename: str,
    extension: Optional[str] = None
) -> List[Path]:
    """
    Find all versioned copies of a file in a directory.

    Looks for files matching: basename_v<N>.ext

    Args:
        directory: Directory to search in
        basename: Base name of the file (without version suffix)
        extension: Optional file extension to filter by

    Returns:
        List of Path objects for versioned files, sorted by version number
    """
    if not directory.exists() or not directory.is_dir():
        return []

    pattern = rf'^{re.escape(basename)}_v(\d+)'
    if extension:
        pattern += rf'\.{re.escape(extension.lstrip("."))}$'
    else:
        pattern += r'\.[a-zA-Z0-9]+$'

    versioned_files = []
    for file_path in directory.iterdir():
        if file_path.is_file():
            match = re.match(pattern, file_path.name)
            if match:
                version_num = int(match.group(1))
                versioned_files.append((version_num, file_path))

    # Sort by version number
    versioned_files.sort(key=lambda x: x[0])
    return [path for _, path in versioned_files]


def load_json_file(file_path: Path) -> Dict[str, Any]:
    """
    Load and parse a JSON file with error handling.

    Args:
        file_path: Path to the JSON file

    Returns:
        Parsed JSON data as dictionary

    Raises:
        ValidationError: If file cannot be read or parsed
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise ValidationError(f"File not found: {file_path}")
    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON in {file_path}: {e}")
    except Exception as e:
        raise ValidationError(f"Error reading {file_path}: {e}")


def get_latest_file_by_pattern(
    directory: Path,
    pattern: str
) -> Optional[Path]:
    """
    Get the most recently modified file matching a glob pattern.

    Args:
        directory: Directory to search in
        pattern: Glob pattern (e.g., "*.md", "report_*.json")

    Returns:
        Path to the latest file, or None if no matches found
    """
    if not directory.exists() or not directory.is_dir():
        return None

    matches = list(directory.glob(pattern))
    if not matches:
        return None

    # Sort by modification time, most recent first
    matches.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return matches[0]


def validate_date_format(date_str: str, format_str: str = "%Y-%m-%d") -> Tuple[bool, Optional[str]]:
    """
    Validate that a date string matches the expected format.

    Args:
        date_str: The date string to validate
        format_str: Expected date format (default: "%Y-%m-%d")

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        datetime.strptime(date_str, format_str)
        return True, None
    except ValueError as e:
        return False, f"Invalid date format '{date_str}': {e}"


def compare_date_strings(date1: str, date2: str, format_str: str = "%Y-%m-%d") -> int:
    """
    Compare two date strings.

    Args:
        date1: First date string
        date2: Second date string
        format_str: Date format (default: "%Y-%m-%d")

    Returns:
        -1 if date1 < date2, 0 if equal, 1 if date1 > date2

    Raises:
        ValidationError: If dates cannot be parsed
    """
    try:
        dt1 = datetime.strptime(date1, format_str)
        dt2 = datetime.strptime(date2, format_str)

        if dt1 < dt2:
            return -1
        elif dt1 > dt2:
            return 1
        else:
            return 0
    except ValueError as e:
        raise ValidationError(f"Cannot compare dates: {e}")
