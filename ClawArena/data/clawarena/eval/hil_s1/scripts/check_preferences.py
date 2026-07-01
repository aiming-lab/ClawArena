#!/usr/bin/env python3
"""
Check P1-P5 preference rules compliance for hil_s1 scenario.

This script validates documents and code against the five preference rules:
- P1: ISO 8601 timestamps and thousands separators
- P2: File naming convention (YYYY-MM-DD_<topic>_v<N>.<ext>)
- P3: Report structure (Summary/Details/Action Items)
- P4: Code style (docstrings/type hints/logging)
- P5: Communication habits (first sentence ≤20 words/[UNVERIFIED]/source references)

Usage:
    python check_preferences.py --file FILE --rules P1,P2,P3,P4,P5
    python check_preferences.py --workspace DIR --rules P1,P5 --target-latest-report
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from datetime import datetime, timezone

# Import validation utilities
from validation_utils import (
    parse_iso8601,
    check_thousands_separator,
    extract_numbers_from_text,
    extract_ast_info,
    check_filename_p2_compliance,
    check_report_structure,
    check_first_sentence_length,
    check_unverified_markers,
    check_source_references,
    find_versioned_copies,
    load_json_file,
    get_latest_file_by_pattern,
    ValidationError,
)


class PreferenceChecker:
    """Main checker class for preference rules validation."""

    def __init__(self, verbose: bool = False):
        """
        Initialize the preference checker.

        Args:
            verbose: If True, output detailed checking information
        """
        self.verbose = verbose
        self.results = {
            'checked_at': datetime.now(timezone.utc).isoformat(),
            'files_checked': [],
            'rules_checked': [],
            'passed': [],
            'failed': [],
            'warnings': [],
            'summary': {}
        }

    def log(self, message: str, level: str = "INFO"):
        """Log a message if verbose mode is enabled."""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [{level}] {message}", file=sys.stderr)

    def check_p1_timestamps_and_numbers(self, file_path: Path) -> Dict[str, Any]:
        """
        Check P1: ISO 8601 timestamps and thousands separators.

        P1 Requirements:
        - All timestamps must be in ISO 8601 format
        - Numbers >= 10,000 must use thousands separators (commas)

        Args:
            file_path: Path to the file to check

        Returns:
            Dictionary with check results
        """
        self.log(f"Checking P1 compliance for {file_path}", "INFO")

        result = {
            'rule': 'P1',
            'file': str(file_path),
            'checks': {
                'timestamps': {'passed': True, 'issues': []},
                'thousands_separators': {'passed': True, 'issues': []}
            }
        }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            result['checks']['timestamps']['passed'] = False
            result['checks']['timestamps']['issues'].append(f"Cannot read file: {e}")
            return result

        # Check for timestamps in JSON files
        if file_path.suffix == '.json':
            try:
                data = json.loads(content)
                timestamp_fields = self._find_timestamp_fields(data)

                for field_path, timestamp_value in timestamp_fields:
                    try:
                        parse_iso8601(timestamp_value, strict=True)
                        self.log(f"Valid ISO 8601 timestamp at {field_path}: {timestamp_value}", "DEBUG")
                    except Exception as e:
                        result['checks']['timestamps']['passed'] = False
                        result['checks']['timestamps']['issues'].append(
                            f"Invalid timestamp at {field_path}: {timestamp_value} - {e}"
                        )
            except json.JSONDecodeError:
                # Not valid JSON, skip timestamp checking
                pass

        # Check for timestamps in text content (common patterns)
        # Look for patterns like: "2025-03-14T10:30:00Z", "timestamp: ...", etc.
        timestamp_patterns = [
            r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?',
        ]

        import re
        for pattern in timestamp_patterns:
            for match in re.finditer(pattern, content):
                timestamp_str = match.group(0)
                try:
                    parse_iso8601(timestamp_str, strict=False)
                except Exception as e:
                    result['checks']['timestamps']['passed'] = False
                    result['checks']['timestamps']['issues'].append(
                        f"Invalid ISO 8601 timestamp found: {timestamp_str} - {e}"
                    )

        # Check thousands separators
        numbers = extract_numbers_from_text(content)
        for number_str in numbers:
            is_valid, error_msg = check_thousands_separator(number_str, allow_no_separator=True)
            if not is_valid:
                result['checks']['thousands_separators']['passed'] = False
                result['checks']['thousands_separators']['issues'].append(error_msg)

        # Overall P1 result
        result['passed'] = (
            result['checks']['timestamps']['passed'] and
            result['checks']['thousands_separators']['passed']
        )

        return result

    def _find_timestamp_fields(
        self,
        data: Any,
        path: str = "$"
    ) -> List[tuple]:
        """
        Recursively find timestamp fields in JSON data.

        Args:
            data: JSON data (dict, list, or primitive)
            path: Current path in the JSON structure

        Returns:
            List of (field_path, timestamp_value) tuples
        """
        timestamps = []

        # Common timestamp field names
        timestamp_field_names = {
            'timestamp', 'created_at', 'updated_at', 'generated_at',
            'assessed_at', 'due_date', 'resolved_at', 'date',
            'datetime', 'time', 'issued_at', 'checked_at'
        }

        if isinstance(data, dict):
            for key, value in data.items():
                field_path = f"{path}.{key}"

                # Check if this looks like a timestamp field
                if key.lower() in timestamp_field_names and isinstance(value, str):
                    timestamps.append((field_path, value))
                else:
                    # Recurse into nested structures
                    timestamps.extend(self._find_timestamp_fields(value, field_path))

        elif isinstance(data, list):
            for idx, item in enumerate(data):
                item_path = f"{path}[{idx}]"
                timestamps.extend(self._find_timestamp_fields(item, item_path))

        return timestamps

    def check_p2_filename(self, file_path: Path) -> Dict[str, Any]:
        """
        Check P2: File naming convention.

        P2 Format: YYYY-MM-DD_<topic>_v<N>.<ext>

        Args:
            file_path: Path to the file to check

        Returns:
            Dictionary with check results
        """
        self.log(f"Checking P2 compliance for {file_path.name}", "INFO")

        is_compliant, error_msg = check_filename_p2_compliance(file_path.name)

        result = {
            'rule': 'P2',
            'file': str(file_path),
            'filename': file_path.name,
            'passed': is_compliant,
            'issues': [error_msg] if error_msg else []
        }

        if is_compliant:
            self.log(f"P2 compliant: {file_path.name}", "DEBUG")
        else:
            self.log(f"P2 violation: {error_msg}", "WARNING")

        return result

    def check_p2_versioned_copies(
        self,
        workspace: Path,
        basename: str,
        extension: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Check P2: Verify versioned copies exist for a file.

        Args:
            workspace: Directory to search in
            basename: Base name of the file
            extension: Optional file extension

        Returns:
            Dictionary with check results
        """
        self.log(f"Checking P2 versioned copies for {basename}", "INFO")

        versioned_files = find_versioned_copies(workspace, basename, extension)

        result = {
            'rule': 'P2',
            'check': 'versioned_copies',
            'basename': basename,
            'workspace': str(workspace),
            'versions_found': len(versioned_files),
            'files': [str(f) for f in versioned_files],
            'passed': len(versioned_files) > 0,
            'issues': []
        }

        if len(versioned_files) == 0:
            result['issues'].append(
                f"No versioned copies found for '{basename}' in {workspace}"
            )
            self.log(f"No versioned copies found for {basename}", "WARNING")
        else:
            self.log(f"Found {len(versioned_files)} versioned copies", "DEBUG")

        return result

    def check_p3_report_structure(self, file_path: Path) -> Dict[str, Any]:
        """
        Check P3: Report structure.

        P3 Requirements:
        - Reports must have: Summary, Details, Action Items sections

        Args:
            file_path: Path to the report file

        Returns:
            Dictionary with check results
        """
        self.log(f"Checking P3 compliance for {file_path}", "INFO")

        result = {
            'rule': 'P3',
            'file': str(file_path),
            'passed': False,
            'issues': []
        }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            result['issues'].append(f"Cannot read file: {e}")
            return result

        # Check for required sections
        has_all_sections, missing_sections = check_report_structure(content)

        result['passed'] = has_all_sections
        result['sections_found'] = ['Summary', 'Details', 'Action Items']
        result['missing_sections'] = missing_sections

        if missing_sections:
            result['issues'].append(
                f"Missing required sections: {', '.join(missing_sections)}"
            )
            self.log(f"P3 violation: Missing sections {missing_sections}", "WARNING")
        else:
            self.log("P3 compliant: All required sections found", "DEBUG")

        return result

    def check_p4_code_style(self, file_path: Path) -> Dict[str, Any]:
        """
        Check P4: Code style requirements.

        P4 Requirements for Python code:
        - Functions must have docstrings
        - Functions must have type hints
        - Code must use logging module

        Args:
            file_path: Path to the Python file

        Returns:
            Dictionary with check results
        """
        self.log(f"Checking P4 compliance for {file_path}", "INFO")

        result = {
            'rule': 'P4',
            'file': str(file_path),
            'passed': False,
            'checks': {},
            'issues': []
        }

        if file_path.suffix != '.py':
            result['issues'].append("P4 only applies to Python files")
            return result

        # Extract AST info
        ast_info = extract_ast_info(file_path)

        if 'error' in ast_info:
            result['issues'].append(ast_info['error'])
            return result

        result['checks'] = ast_info

        # Check compliance
        compliance_checks = []

        # Docstring compliance
        if ast_info['total_functions'] > 0:
            docstring_ratio = ast_info['functions_with_docstrings'] / ast_info['total_functions']
            compliance_checks.append(docstring_ratio >= 0.8)  # At least 80%

            if docstring_ratio < 0.8:
                result['issues'].append(
                    f"Docstring coverage: {docstring_ratio:.1%} "
                    f"({ast_info['functions_with_docstrings']}/{ast_info['total_functions']}). "
                    f"Expected >= 80%"
                )

        # Type hints compliance
        if ast_info['total_functions'] > 0:
            typehint_ratio = ast_info['functions_with_type_hints'] / ast_info['total_functions']
            compliance_checks.append(typehint_ratio >= 0.7)  # At least 70%

            if typehint_ratio < 0.7:
                result['issues'].append(
                    f"Type hints coverage: {typehint_ratio:.1%} "
                    f"({ast_info['functions_with_type_hints']}/{ast_info['total_functions']}). "
                    f"Expected >= 70%"
                )

        # Logging usage
        compliance_checks.append(ast_info['has_logging'])
        if not ast_info['has_logging']:
            result['issues'].append("No logging module usage found")

        # Overall P4 result
        result['passed'] = all(compliance_checks) if compliance_checks else False

        if result['passed']:
            self.log("P4 compliant: Code style requirements met", "DEBUG")
        else:
            self.log(f"P4 violations: {len(result['issues'])} issues found", "WARNING")

        return result

    def check_p5_communication(self, file_path: Path) -> Dict[str, Any]:
        """
        Check P5: Communication habits.

        P5 Requirements:
        - First sentence should be ≤ 20 words (summary/overview)
        - Use [UNVERIFIED] markers for unconfirmed information
        - Include source references

        Args:
            file_path: Path to the document file

        Returns:
            Dictionary with check results
        """
        self.log(f"Checking P5 compliance for {file_path}", "INFO")

        result = {
            'rule': 'P5',
            'file': str(file_path),
            'passed': True,
            'checks': {},
            'issues': [],
            'warnings': []
        }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            result['passed'] = False
            result['issues'].append(f"Cannot read file: {e}")
            return result

        # Check first sentence length
        is_compliant, word_count = check_first_sentence_length(content, max_words=20)
        result['checks']['first_sentence_words'] = word_count

        if not is_compliant:
            result['passed'] = False
            result['issues'].append(
                f"First sentence has {word_count} words, expected ≤ 20"
            )
            self.log(f"P5 violation: First sentence too long ({word_count} words)", "WARNING")
        else:
            self.log(f"First sentence OK ({word_count} words)", "DEBUG")

        # Check for [UNVERIFIED] markers
        unverified_markers = check_unverified_markers(content)
        result['checks']['unverified_markers_count'] = len(unverified_markers)
        result['checks']['unverified_markers'] = unverified_markers[:5]  # Store first 5

        if len(unverified_markers) > 0:
            self.log(f"Found {len(unverified_markers)} [UNVERIFIED] markers", "DEBUG")
        else:
            # Not necessarily an error, but worth noting
            result['warnings'].append(
                "No [UNVERIFIED] markers found. Ensure all information is verified."
            )

        # Check for source references
        source_count, sources = check_source_references(content)
        result['checks']['source_references_count'] = source_count
        result['checks']['source_references'] = sources[:5]  # Store first 5

        if source_count == 0:
            result['passed'] = False
            result['issues'].append("No source references found")
            self.log("P5 violation: No source references", "WARNING")
        else:
            self.log(f"Found {source_count} source references", "DEBUG")

        return result

    def check_file(
        self,
        file_path: Path,
        rules: Set[str],
        check_options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Check a file against specified preference rules.

        Args:
            file_path: Path to the file to check
            rules: Set of rules to check (e.g., {'P1', 'P2', 'P3'})
            check_options: Optional dictionary of check-specific options

        Returns:
            Dictionary with all check results
        """
        if check_options is None:
            check_options = {}

        self.log(f"Checking file: {file_path}", "INFO")
        self.log(f"Rules to check: {', '.join(sorted(rules))}", "INFO")

        file_results = {
            'file': str(file_path),
            'rules_checked': sorted(list(rules)),
            'checks': [],
            'overall_passed': True
        }

        # Run checks based on requested rules
        if 'P1' in rules:
            p1_result = self.check_p1_timestamps_and_numbers(file_path)
            file_results['checks'].append(p1_result)
            if not p1_result['passed']:
                file_results['overall_passed'] = False

        if 'P2' in rules:
            p2_result = self.check_p2_filename(file_path)
            file_results['checks'].append(p2_result)
            if not p2_result['passed']:
                file_results['overall_passed'] = False

        if 'P3' in rules and file_path.suffix in ['.md', '.txt']:
            p3_result = self.check_p3_report_structure(file_path)
            file_results['checks'].append(p3_result)
            if not p3_result['passed']:
                file_results['overall_passed'] = False

        if 'P4' in rules and file_path.suffix == '.py':
            p4_result = self.check_p4_code_style(file_path)
            file_results['checks'].append(p4_result)
            if not p4_result['passed']:
                file_results['overall_passed'] = False

        if 'P5' in rules and file_path.suffix in ['.md', '.txt', '.json']:
            p5_result = self.check_p5_communication(file_path)
            file_results['checks'].append(p5_result)
            if not p5_result['passed']:
                file_results['overall_passed'] = False

        self.results['files_checked'].append(str(file_path))

        if file_results['overall_passed']:
            self.results['passed'].append(str(file_path))
        else:
            self.results['failed'].append(str(file_path))

        return file_results

    def check_workspace(
        self,
        workspace: Path,
        rules: Set[str],
        target_pattern: Optional[str] = None,
        target_latest: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Check multiple files in a workspace against preference rules.

        Args:
            workspace: Directory containing files to check
            rules: Set of rules to check
            target_pattern: Optional glob pattern to filter files
            target_latest: If True, only check the most recent file

        Returns:
            List of check results for all files
        """
        self.log(f"Checking workspace: {workspace}", "INFO")

        if not workspace.exists() or not workspace.is_dir():
            raise ValidationError(f"Workspace not found or not a directory: {workspace}")

        all_results = []

        # Determine which files to check
        if target_latest and target_pattern:
            target_file = get_latest_file_by_pattern(workspace, target_pattern)
            if target_file:
                files_to_check = [target_file]
            else:
                self.log(f"No files matching pattern '{target_pattern}'", "WARNING")
                files_to_check = []
        elif target_pattern:
            files_to_check = list(workspace.glob(target_pattern))
        else:
            # Check all relevant files
            patterns = ['*.md', '*.txt', '*.py', '*.json']
            files_to_check = []
            for pattern in patterns:
                files_to_check.extend(workspace.rglob(pattern))

        self.log(f"Found {len(files_to_check)} files to check", "INFO")

        for file_path in files_to_check:
            try:
                result = self.check_file(file_path, rules)
                all_results.append(result)
            except Exception as e:
                self.log(f"Error checking {file_path}: {e}", "ERROR")
                all_results.append({
                    'file': str(file_path),
                    'error': str(e),
                    'overall_passed': False
                })

        return all_results

    def generate_summary(self, all_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a summary of all check results.

        Args:
            all_results: List of check results from all files

        Returns:
            Summary dictionary
        """
        summary = {
            'total_files': len(all_results),
            'files_passed': 0,
            'files_failed': 0,
            'rules_summary': {}
        }

        for result in all_results:
            if result.get('overall_passed', False):
                summary['files_passed'] += 1
            else:
                summary['files_failed'] += 1

            # Count rule-specific results
            for check in result.get('checks', []):
                rule = check.get('rule', 'unknown')
                if rule not in summary['rules_summary']:
                    summary['rules_summary'][rule] = {'passed': 0, 'failed': 0}

                if check.get('passed', False):
                    summary['rules_summary'][rule]['passed'] += 1
                else:
                    summary['rules_summary'][rule]['failed'] += 1

        self.results['summary'] = summary
        return summary


def main():
    """Main entry point for the check_preferences script."""
    parser = argparse.ArgumentParser(
        description="Check P1-P5 preference rules compliance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check a single file for P1 and P2 compliance
  python check_preferences.py --file report.md --rules P1,P2

  # Check all files in workspace for all rules
  python check_preferences.py --workspace ./documents --rules P1,P2,P3,P4,P5

  # Check latest report for P3 and P5
  python check_preferences.py --workspace ./reports --rules P3,P5 \\
      --target-latest-report --target-pattern "*.md"

  # Check for versioned copies (P2)
  python check_preferences.py --workspace ./documents --rules P2 \\
      --expect-versioned-copy data_overview

  # Check dates only in JSON files (P1)
  python check_preferences.py --file milestones.json --rules P1 --check-dates-only
        """
    )

    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--file',
        type=Path,
        help="Single file to check"
    )
    input_group.add_argument(
        '--workspace',
        type=Path,
        help="Directory containing files to check"
    )

    # Rules to check
    parser.add_argument(
        '--rules',
        type=str,
        required=True,
        help="Comma-separated list of rules to check (e.g., P1,P2,P3,P4,P5)"
    )

    # Target file options
    parser.add_argument(
        '--target-latest-report',
        action='store_true',
        help="Check only the most recently modified report"
    )
    parser.add_argument(
        '--target-pattern',
        type=str,
        help="Glob pattern to filter files (e.g., '*.md', 'report_*.json')"
    )

    # P2 specific options
    parser.add_argument(
        '--expect-file-pattern',
        type=str,
        help="Regex pattern that filename should match (for P2)"
    )
    parser.add_argument(
        '--expect-versioned-copy',
        type=str,
        help="Check for versioned copies of this basename (for P2)"
    )

    # P1 specific options
    parser.add_argument(
        '--check-dates-only',
        action='store_true',
        help="Only check date/timestamp fields (for P1)"
    )
    parser.add_argument(
        '--check-source-fields',
        action='store_true',
        help="Check source reference fields (for P5)"
    )

    # Output options
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help="Enable verbose output"
    )
    parser.add_argument(
        '--output',
        '-o',
        type=Path,
        help="Write results to JSON file"
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help="Output results in JSON format"
    )

    args = parser.parse_args()

    # Parse rules
    rules = set(r.strip().upper() for r in args.rules.split(','))
    valid_rules = {'P1', 'P2', 'P3', 'P4', 'P5'}
    invalid_rules = rules - valid_rules

    if invalid_rules:
        parser.error(f"Invalid rules: {', '.join(invalid_rules)}. Valid: {', '.join(valid_rules)}")

    # Create checker
    checker = PreferenceChecker(verbose=args.verbose)
    checker.results['rules_checked'] = sorted(list(rules))

    try:
        # Run checks
        if args.file:
            # Check single file
            result = checker.check_file(args.file, rules)
            all_results = [result]

            # Handle P2 versioned copy check
            if args.expect_versioned_copy and 'P2' in rules:
                workspace = args.file.parent
                basename = args.expect_versioned_copy
                p2_versioned = checker.check_p2_versioned_copies(workspace, basename)
                result['checks'].append(p2_versioned)
                if not p2_versioned['passed']:
                    result['overall_passed'] = False

        else:
            # Check workspace
            all_results = checker.check_workspace(
                args.workspace,
                rules,
                target_pattern=args.target_pattern,
                target_latest=args.target_latest_report
            )

        # Generate summary
        summary = checker.generate_summary(all_results)

        # Prepare output
        output_data = {
            'checked_at': checker.results['checked_at'],
            'rules_checked': checker.results['rules_checked'],
            'summary': summary,
            'results': all_results
        }

        # Output results
        if args.json or args.output:
            output_json = json.dumps(output_data, indent=2)

            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(output_json)
                print(f"Results written to {args.output}")
            else:
                print(output_json)
        else:
            # Human-readable output
            print("\n" + "=" * 70)
            print("PREFERENCE RULES CHECK RESULTS")
            print("=" * 70)
            print(f"Rules checked: {', '.join(sorted(rules))}")
            print(f"Total files: {summary['total_files']}")
            print(f"Passed: {summary['files_passed']}")
            print(f"Failed: {summary['files_failed']}")
            print()

            print("Rule Summary:")
            for rule, stats in sorted(summary['rules_summary'].items()):
                total = stats['passed'] + stats['failed']
                pass_rate = (stats['passed'] / total * 100) if total > 0 else 0
                print(f"  {rule}: {stats['passed']}/{total} passed ({pass_rate:.1f}%)")

            print()

            # Show detailed failures
            if summary['files_failed'] > 0:
                print("Failed Files:")
                for result in all_results:
                    if not result.get('overall_passed', False):
                        print(f"\n  {result['file']}")
                        for check in result.get('checks', []):
                            if not check.get('passed', False):
                                rule = check.get('rule', 'unknown')
                                issues = check.get('issues', [])
                                print(f"    [{rule}] {len(issues)} issue(s)")
                                for issue in issues[:3]:  # Show first 3 issues
                                    print(f"      - {issue}")

        # Exit with appropriate code
        exit_code = 0 if summary['files_failed'] == 0 else 1
        sys.exit(exit_code)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(2)


if __name__ == '__main__':
    main()
