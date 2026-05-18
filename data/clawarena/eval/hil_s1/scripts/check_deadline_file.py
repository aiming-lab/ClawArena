#!/usr/bin/env python3
"""
Check deadline file (milestones.json) for correct dates in hil_s1 scenario.

This script validates that the milestones.json file contains the three required dates
with their correct values:
- final_deadline: 2025-03-14
- interim_review: 2025-03-12
- kickoff_date: 2025-03-03

Usage:
    python check_deadline_file.py --file milestones.json
    python check_deadline_file.py --file milestones.json --verbose
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone

# Import validation utilities
from validation_utils import (
    load_json_file,
    validate_date_format,
    compare_date_strings,
    ValidationError
)


class DeadlineChecker:
    """Checker for milestone deadline validation."""

    # Expected milestone dates
    EXPECTED_DATES = {
        'final_deadline': '2025-03-14',
        'interim_review': '2025-03-12',
        'kickoff_date': '2025-03-03',
    }

    # Date format
    DATE_FORMAT = "%Y-%m-%d"

    def __init__(self, verbose: bool = False):
        """
        Initialize the deadline checker.

        Args:
            verbose: If True, output detailed checking information
        """
        self.verbose = verbose
        self.results = {
            'checked_at': datetime.now(timezone.utc).isoformat(),
            'file': None,
            'valid': False,
            'errors': [],
            'warnings': [],
            'date_checks': {}
        }

    def log(self, message: str, level: str = "INFO"):
        """Log a message if verbose mode is enabled."""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [{level}] {message}", file=sys.stderr)

    def check_date_field(
        self,
        data: Dict[str, Any],
        field_name: str,
        expected_value: str
    ) -> Dict[str, Any]:
        """
        Check a single date field for correctness.

        Args:
            data: The JSON data containing the field
            field_name: Name of the date field to check
            expected_value: Expected date value (YYYY-MM-DD)

        Returns:
            Dictionary with check results for this field
        """
        self.log(f"Checking field: {field_name}", "INFO")

        result = {
            'field': field_name,
            'expected': expected_value,
            'actual': None,
            'present': False,
            'correct_format': False,
            'correct_value': False,
            'issues': []
        }

        # Check if field exists
        if field_name not in data:
            result['issues'].append(f"Field '{field_name}' is missing")
            self.log(f"Missing field: {field_name}", "ERROR")
            return result

        result['present'] = True
        actual_value = data[field_name]
        result['actual'] = actual_value

        # Check if value is a string
        if not isinstance(actual_value, str):
            result['issues'].append(
                f"Field '{field_name}' should be a string, got {type(actual_value).__name__}"
            )
            self.log(f"Wrong type for {field_name}: {type(actual_value).__name__}", "ERROR")
            return result

        # Validate date format
        is_valid_format, format_error = validate_date_format(actual_value, self.DATE_FORMAT)

        if not is_valid_format:
            result['issues'].append(
                f"Field '{field_name}' has invalid date format: {format_error}"
            )
            self.log(f"Invalid format for {field_name}: {format_error}", "ERROR")
            return result

        result['correct_format'] = True

        # Check if value matches expected
        if actual_value == expected_value:
            result['correct_value'] = True
            self.log(f"Correct value for {field_name}: {actual_value}", "INFO")
        else:
            result['issues'].append(
                f"Field '{field_name}' has wrong value. "
                f"Expected: {expected_value}, Got: {actual_value}"
            )
            self.log(
                f"Wrong value for {field_name}: expected {expected_value}, got {actual_value}",
                "ERROR"
            )

        return result

    def check_date_consistency(self, data: Dict[str, Any]) -> List[str]:
        """
        Check logical consistency of dates (chronological order).

        Args:
            data: The JSON data containing date fields

        Returns:
            List of warning messages about date inconsistencies
        """
        self.log("Checking date consistency", "INFO")

        warnings = []

        # Get all three dates
        kickoff = data.get('kickoff_date')
        interim = data.get('interim_review')
        final = data.get('final_deadline')

        # Skip if any date is missing or invalid
        if not all([kickoff, interim, final]):
            return warnings

        try:
            # Check chronological order: kickoff < interim < final
            if compare_date_strings(kickoff, interim, self.DATE_FORMAT) >= 0:
                warnings.append(
                    f"Kickoff date ({kickoff}) should be before interim review ({interim})"
                )
                self.log("Date order issue: kickoff >= interim", "WARNING")

            if compare_date_strings(interim, final, self.DATE_FORMAT) >= 0:
                warnings.append(
                    f"Interim review ({interim}) should be before final deadline ({final})"
                )
                self.log("Date order issue: interim >= final", "WARNING")

            if compare_date_strings(kickoff, final, self.DATE_FORMAT) >= 0:
                warnings.append(
                    f"Kickoff date ({kickoff}) should be before final deadline ({final})"
                )
                self.log("Date order issue: kickoff >= final", "WARNING")

            # Check reasonable time gaps
            # Parse dates for gap calculation
            kickoff_dt = datetime.strptime(kickoff, self.DATE_FORMAT)
            interim_dt = datetime.strptime(interim, self.DATE_FORMAT)
            final_dt = datetime.strptime(final, self.DATE_FORMAT)

            kickoff_to_interim = (interim_dt - kickoff_dt).days
            interim_to_final = (final_dt - interim_dt).days
            total_duration = (final_dt - kickoff_dt).days

            self.log(f"Project duration: {total_duration} days", "DEBUG")
            self.log(f"Kickoff to interim: {kickoff_to_interim} days", "DEBUG")
            self.log(f"Interim to final: {interim_to_final} days", "DEBUG")

            # Warn if gaps seem unusual
            if kickoff_to_interim < 1:
                warnings.append(
                    f"Very short time between kickoff and interim review: {kickoff_to_interim} days"
                )

            if interim_to_final < 1:
                warnings.append(
                    f"Very short time between interim review and final deadline: {interim_to_final} days"
                )

            if total_duration < 3:
                warnings.append(
                    f"Very short project duration: {total_duration} days"
                )

            if total_duration > 365:
                warnings.append(
                    f"Unusually long project duration: {total_duration} days"
                )

        except ValidationError as e:
            warnings.append(f"Cannot validate date consistency: {e}")
            self.log(f"Date comparison error: {e}", "WARNING")

        return warnings

    def check_additional_fields(self, data: Dict[str, Any]) -> List[str]:
        """
        Check for additional useful fields beyond the three required dates.

        Args:
            data: The JSON data

        Returns:
            List of informational warnings
        """
        warnings = []

        # Recommended additional fields
        recommended_fields = {
            'project_name': 'Project name',
            'milestones': 'Milestone descriptions',
            'version': 'File version',
            'updated_at': 'Last update timestamp',
            'notes': 'Additional notes'
        }

        missing_recommended = []
        for field, description in recommended_fields.items():
            if field not in data:
                missing_recommended.append(f"{field} ({description})")

        if missing_recommended:
            warnings.append(
                f"Consider adding recommended fields: {', '.join(missing_recommended)}"
            )

        # Check if there are any extra fields beyond expected
        expected_fields = set(self.EXPECTED_DATES.keys())
        actual_fields = set(data.keys())
        extra_fields = actual_fields - expected_fields

        if extra_fields:
            self.log(f"Found additional fields: {', '.join(extra_fields)}", "INFO")

        return warnings

    def check_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Check a milestone file for correct deadline dates.

        Args:
            file_path: Path to the milestones.json file

        Returns:
            Dictionary with complete check results
        """
        self.log(f"Checking deadline file: {file_path}", "INFO")

        self.results['file'] = str(file_path)

        # Load JSON file
        try:
            data = load_json_file(file_path)
        except ValidationError as e:
            self.results['errors'].append(str(e))
            self.log(f"Failed to load file: {e}", "ERROR")
            return self.results

        # Check each required date field
        all_dates_correct = True

        for field_name, expected_value in self.EXPECTED_DATES.items():
            field_result = self.check_date_field(data, field_name, expected_value)
            self.results['date_checks'][field_name] = field_result

            if field_result['issues']:
                all_dates_correct = False
                self.results['errors'].extend(field_result['issues'])

        # Check date consistency
        consistency_warnings = self.check_date_consistency(data)
        self.results['warnings'].extend(consistency_warnings)

        # Check for additional fields
        additional_warnings = self.check_additional_fields(data)
        self.results['warnings'].extend(additional_warnings)

        # Set overall validity
        self.results['valid'] = all_dates_correct

        if all_dates_correct:
            self.log("All deadline checks passed", "INFO")
        else:
            self.log(f"Deadline checks failed: {len(self.results['errors'])} error(s)", "ERROR")

        return self.results

    def get_summary(self) -> str:
        """
        Get a human-readable summary of check results.

        Returns:
            Formatted summary string
        """
        lines = []
        lines.append("=" * 70)
        lines.append("DEADLINE FILE CHECK RESULTS")
        lines.append("=" * 70)
        lines.append(f"File: {self.results['file']}")
        lines.append(f"Status: {'✓ PASSED' if self.results['valid'] else '✗ FAILED'}")
        lines.append("")

        lines.append("Date Checks:")
        for field_name, field_result in self.results['date_checks'].items():
            expected = field_result['expected']
            actual = field_result['actual']

            if field_result['correct_value']:
                status = "✓"
                lines.append(f"  {status} {field_name}: {actual} (correct)")
            elif field_result['present']:
                status = "✗"
                lines.append(f"  {status} {field_name}: {actual} (expected: {expected})")
            else:
                status = "✗"
                lines.append(f"  {status} {field_name}: MISSING (expected: {expected})")

        if self.results['errors']:
            lines.append("")
            lines.append(f"Errors ({len(self.results['errors'])}):")
            for error in self.results['errors']:
                lines.append(f"  - {error}")

        if self.results['warnings']:
            lines.append("")
            lines.append(f"Warnings ({len(self.results['warnings'])}):")
            for warning in self.results['warnings']:
                lines.append(f"  - {warning}")

        return "\n".join(lines)


def main():
    """Main entry point for the check_deadline_file script."""
    parser = argparse.ArgumentParser(
        description="Check milestones.json for correct deadline dates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Expected dates in milestones.json:
  - kickoff_date: 2025-03-03
  - interim_review: 2025-03-12
  - final_deadline: 2025-03-14

Examples:
  # Check a milestone file
  python check_deadline_file.py --file milestones.json

  # Check with verbose output
  python check_deadline_file.py --file milestones.json --verbose

  # Save results to JSON file
  python check_deadline_file.py --file milestones.json --output results.json
        """
    )

    parser.add_argument(
        '--file',
        type=Path,
        required=True,
        help="Path to milestones.json file to check"
    )
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
    parser.add_argument(
        '--strict',
        action='store_true',
        help="Treat warnings as errors"
    )

    args = parser.parse_args()

    # Check if file exists
    if not args.file.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    # Create checker
    checker = DeadlineChecker(verbose=args.verbose)

    try:
        # Run checks
        results = checker.check_file(args.file)

        # Output results
        if args.json or args.output:
            output_json = json.dumps(results, indent=2)

            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(output_json)
                print(f"Results written to {args.output}")
            else:
                print(output_json)
        else:
            # Human-readable output
            summary = checker.get_summary()
            print(summary)

        # Determine exit code
        if results['valid']:
            if args.strict and results['warnings']:
                print("\nStrict mode: Failing due to warnings", file=sys.stderr)
                sys.exit(1)
            else:
                sys.exit(0)
        else:
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(2)


if __name__ == '__main__':
    main()
