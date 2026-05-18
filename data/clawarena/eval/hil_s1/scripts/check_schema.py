#!/usr/bin/env python3
"""
JSON Schema validation script for hil_s1 scenario.

This script validates JSON files against predefined schemas used in the hil_s1 scenario.
Supports 11 schema types: task_list, data_overview, schema_changes, field_mapping,
action_items, timeline, risk_assessment, issue_tracker, data_lineage,
project_panorama, and deliverables_manifest.

Usage:
    python check_schema.py --file FILE --schema SCHEMA_NAME
    python check_schema.py --file data.json --schema task_list --verbose
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone

try:
    import jsonschema
    from jsonschema import validate, ValidationError as JSONSchemaValidationError
    from jsonschema import Draft7Validator, Draft202012Validator
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


# Import validation utilities
from validation_utils import load_json_file, ValidationError


class SchemaValidator:
    """Validator for JSON schemas in hil_s1 scenario."""

    # Supported schema names
    SUPPORTED_SCHEMAS = {
        'task_list',
        'data_overview',
        'schema_changes',
        'field_mapping',
        'action_items',
        'timeline',
        'risk_assessment',
        'issue_tracker',
        'data_lineage',
        'project_panorama',
        'deliverables_manifest',
    }

    def __init__(self, schema_dir: Optional[Path] = None, verbose: bool = False):
        """
        Initialize the schema validator.

        Args:
            schema_dir: Directory containing schema JSON files.
                       If None, uses ./schemas/ relative to this script.
            verbose: If True, output detailed validation information
        """
        if schema_dir is None:
            script_dir = Path(__file__).parent
            schema_dir = script_dir / "schemas"

        self.schema_dir = schema_dir
        self.verbose = verbose
        self.schemas_cache: Dict[str, Dict[str, Any]] = {}

        if not HAS_JSONSCHEMA:
            print(
                "WARNING: jsonschema package not installed. "
                "Install with: pip install jsonschema",
                file=sys.stderr
            )

    def log(self, message: str, level: str = "INFO"):
        """Log a message if verbose mode is enabled."""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [{level}] {message}", file=sys.stderr)

    def load_schema(self, schema_name: str) -> Dict[str, Any]:
        """
        Load a JSON schema from disk.

        Args:
            schema_name: Name of the schema (e.g., 'task_list')

        Returns:
            Schema dictionary

        Raises:
            ValidationError: If schema cannot be loaded
        """
        if schema_name in self.schemas_cache:
            self.log(f"Using cached schema: {schema_name}", "DEBUG")
            return self.schemas_cache[schema_name]

        if schema_name not in self.SUPPORTED_SCHEMAS:
            raise ValidationError(
                f"Unsupported schema: {schema_name}. "
                f"Supported: {', '.join(sorted(self.SUPPORTED_SCHEMAS))}"
            )

        schema_file = self.schema_dir / f"{schema_name}.json"

        if not schema_file.exists():
            raise ValidationError(f"Schema file not found: {schema_file}")

        self.log(f"Loading schema from {schema_file}", "INFO")

        try:
            schema = load_json_file(schema_file)
            self.schemas_cache[schema_name] = schema
            return schema
        except Exception as e:
            raise ValidationError(f"Failed to load schema {schema_name}: {e}")

    def validate_data(
        self,
        data: Dict[str, Any],
        schema_name: str
    ) -> Tuple[bool, List[str]]:
        """
        Validate data against a schema.

        Args:
            data: The JSON data to validate
            schema_name: Name of the schema to validate against

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        self.log(f"Validating against schema: {schema_name}", "INFO")

        # Load schema
        try:
            schema = self.load_schema(schema_name)
        except ValidationError as e:
            return False, [str(e)]

        if not HAS_JSONSCHEMA:
            # Fallback to basic validation without jsonschema
            return self._basic_validate(data, schema, schema_name)

        # Use jsonschema for validation
        errors = []

        try:
            # Determine validator based on $schema field
            schema_version = schema.get('$schema', '')

            if '2020-12' in schema_version or '2019-09' in schema_version:
                validator_cls = Draft202012Validator
            else:
                validator_cls = Draft7Validator

            validator = validator_cls(schema)

            # Validate
            validation_errors = sorted(validator.iter_errors(data), key=lambda e: e.path)

            for error in validation_errors:
                path = '.'.join(str(p) for p in error.path) if error.path else 'root'
                errors.append(f"At '{path}': {error.message}")
                self.log(f"Validation error at {path}: {error.message}", "WARNING")

            if not errors:
                self.log("Validation successful", "INFO")
                return True, []
            else:
                self.log(f"Validation failed with {len(errors)} error(s)", "WARNING")
                return False, errors

        except Exception as e:
            self.log(f"Validation exception: {e}", "ERROR")
            return False, [f"Validation exception: {e}"]

    def _basic_validate(
        self,
        data: Dict[str, Any],
        schema: Dict[str, Any],
        schema_name: str
    ) -> Tuple[bool, List[str]]:
        """
        Basic validation without jsonschema library.

        Checks:
        - Required fields are present
        - Basic type checking
        - Enum value validation

        Args:
            data: The data to validate
            schema: The schema to validate against
            schema_name: Name of the schema

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        self.log("Using basic validation (jsonschema not available)", "WARNING")
        errors = []

        # Check type
        expected_type = schema.get('type')
        if expected_type:
            actual_type = type(data).__name__
            type_map = {
                'dict': 'object',
                'list': 'array',
                'str': 'string',
                'int': 'integer',
                'float': 'number',
                'bool': 'boolean',
                'NoneType': 'null'
            }
            actual_type_json = type_map.get(actual_type, actual_type)

            if expected_type != actual_type_json:
                errors.append(
                    f"Root type mismatch: expected {expected_type}, got {actual_type_json}"
                )
                return False, errors

        # Check required fields
        if isinstance(data, dict):
            required_fields = schema.get('required', [])
            properties = schema.get('properties', {})

            for field in required_fields:
                if field not in data:
                    errors.append(f"Missing required field: {field}")

            # Check each property
            for field, value in data.items():
                if field in properties:
                    field_schema = properties[field]
                    field_type = field_schema.get('type')

                    if field_type:
                        value_type = type(value).__name__
                        type_map = {
                            'dict': 'object',
                            'list': 'array',
                            'str': 'string',
                            'int': 'integer',
                            'float': 'number',
                            'bool': 'boolean',
                            'NoneType': 'null'
                        }
                        value_type_json = type_map.get(value_type, value_type)

                        # Handle integer/number flexibility
                        if field_type == 'number' and value_type_json == 'integer':
                            value_type_json = 'number'

                        # Support type as a list (e.g. ["array", "object"])
                        allowed_types = field_type if isinstance(field_type, list) else [field_type]
                        # Handle integer/number flexibility for list types
                        if 'number' in allowed_types and value_type_json == 'integer':
                            value_type_json = 'number'

                        if value_type_json not in allowed_types:
                            errors.append(
                                f"Field '{field}': expected {field_type}, got {value_type_json}"
                            )

                    # Check enum
                    if 'enum' in field_schema and value not in field_schema['enum']:
                        errors.append(
                            f"Field '{field}': value '{value}' not in allowed enum values"
                        )

        return len(errors) == 0, errors

    def validate_file(
        self,
        file_path: Path,
        schema_name: str
    ) -> Dict[str, Any]:
        """
        Validate a JSON file against a schema.

        Args:
            file_path: Path to the JSON file
            schema_name: Name of the schema to validate against

        Returns:
            Dictionary with validation results
        """
        self.log(f"Validating file: {file_path}", "INFO")

        result = {
            'file': str(file_path),
            'schema': schema_name,
            'validated_at': datetime.now(timezone.utc).isoformat(),
            'valid': False,
            'errors': [],
            'warnings': []
        }

        # Load data file
        try:
            data = load_json_file(file_path)
        except ValidationError as e:
            result['errors'].append(str(e))
            return result

        # Validate
        is_valid, errors = self.validate_data(data, schema_name)

        result['valid'] = is_valid
        result['errors'] = errors

        # Additional checks
        if is_valid:
            # Check for best practices
            warnings = self._check_best_practices(data, schema_name)
            result['warnings'] = warnings

        return result

    def _check_best_practices(
        self,
        data: Dict[str, Any],
        schema_name: str
    ) -> List[str]:
        """
        Check for best practices beyond schema validation.

        Args:
            data: The validated data
            schema_name: Name of the schema

        Returns:
            List of warning messages
        """
        warnings = []

        # Common checks for all schemas
        # Check for metadata fields
        metadata_fields = ['version', 'generated_at', 'updated_at', 'created_at']
        found_metadata = any(field in data for field in metadata_fields)

        if not found_metadata:
            warnings.append(
                "Consider adding metadata fields (version, generated_at, etc.)"
            )

        # Schema-specific checks
        if schema_name == 'task_list':
            tasks = data.get('tasks', [])
            if not tasks:
                warnings.append("Task list is empty")
            else:
                # Check for tasks without owners
                tasks_without_owners = [
                    t.get('id', 'unknown')
                    for t in tasks
                    if not t.get('owner')
                ]
                if tasks_without_owners:
                    warnings.append(
                        f"{len(tasks_without_owners)} task(s) without owner"
                    )

        elif schema_name == 'risk_assessment':
            risks = data.get('risks', [])
            high_severity_risks = [
                r for r in risks
                if r.get('severity', '').lower() in ['high', 'critical']
            ]
            if high_severity_risks:
                warnings.append(
                    f"{len(high_severity_risks)} high/critical severity risk(s) found"
                )

        elif schema_name == 'issue_tracker':
            issues = data.get('issues', [])
            open_issues = [
                i for i in issues
                if i.get('status', '').lower() in ['open', 'in_progress']
            ]
            if open_issues:
                warnings.append(f"{len(open_issues)} open issue(s)")

        elif schema_name == 'action_items':
            items = data.get('action_items', [])
            overdue_items = []

            for item in items:
                due_date = item.get('due')
                status = item.get('status', '').lower()

                if due_date and status not in ['completed', 'done']:
                    # Simple date comparison (assumes YYYY-MM-DD format)
                    try:
                        from datetime import datetime
                        due = datetime.strptime(due_date, "%Y-%m-%d")
                        if due < datetime.now():
                            overdue_items.append(item.get('id', 'unknown'))
                    except:
                        pass

            if overdue_items:
                warnings.append(f"{len(overdue_items)} potentially overdue action item(s)")

        return warnings

    def list_schemas(self) -> List[Dict[str, Any]]:
        """
        List all available schemas with metadata.

        Returns:
            List of schema metadata dictionaries
        """
        schemas_info = []

        for schema_name in sorted(self.SUPPORTED_SCHEMAS):
            info = {
                'name': schema_name,
                'file': str(self.schema_dir / f"{schema_name}.json"),
                'available': False
            }

            try:
                schema = self.load_schema(schema_name)
                info['available'] = True
                info['title'] = schema.get('title', schema_name)
                info['description'] = schema.get('description', '')
                info['schema_version'] = schema.get('$schema', 'unknown')
            except:
                pass

            schemas_info.append(info)

        return schemas_info


def main():
    """Main entry point for the check_schema script."""
    parser = argparse.ArgumentParser(
        description="Validate JSON files against hil_s1 schemas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Supported schemas:
  - task_list: Task tracking with owner, priority, due_date
  - data_overview: Dataset summary with record counts and date ranges
  - schema_changes: Version-to-version schema change documentation
  - field_mapping: Source-to-target field mappings
  - action_items: Action items with status tracking
  - timeline: Project milestones and timeline
  - risk_assessment: Risk identification and severity assessment
  - issue_tracker: Issue tracking with status and resolution
  - data_lineage: Dataset provenance and lineage tracking
  - project_panorama: High-level project overview
  - deliverables_manifest: Project deliverables catalog

Examples:
  # Validate a task list file
  python check_schema.py --file tasks.json --schema task_list

  # Validate with verbose output
  python check_schema.py --file data.json --schema data_overview --verbose

  # List all available schemas
  python check_schema.py --list-schemas

  # Validate and save results to file
  python check_schema.py --file risks.json --schema risk_assessment --output results.json
        """
    )

    parser.add_argument(
        '--file',
        type=Path,
        help="JSON file to validate"
    )
    parser.add_argument(
        '--schema',
        type=str,
        help="Schema name to validate against"
    )
    parser.add_argument(
        '--schema-dir',
        type=Path,
        help="Directory containing schema files (default: ./schemas/)"
    )
    parser.add_argument(
        '--list-schemas',
        action='store_true',
        help="List all available schemas and exit"
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
        help="Write validation results to JSON file"
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help="Output results in JSON format"
    )

    args = parser.parse_args()

    # Create validator
    validator = SchemaValidator(schema_dir=args.schema_dir, verbose=args.verbose)

    try:
        # List schemas mode
        if args.list_schemas:
            schemas = validator.list_schemas()

            if args.json:
                print(json.dumps(schemas, indent=2))
            else:
                print("\nAvailable Schemas:")
                print("=" * 70)
                for schema_info in schemas:
                    status = "✓" if schema_info['available'] else "✗"
                    print(f"\n{status} {schema_info['name']}")
                    if schema_info['available']:
                        print(f"  Title: {schema_info.get('title', 'N/A')}")
                        print(f"  File: {schema_info['file']}")

            sys.exit(0)

        # Validation mode
        if not args.file:
            parser.error("--file is required (or use --list-schemas)")

        if not args.schema:
            parser.error("--schema is required (or use --list-schemas)")

        if not args.file.exists():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)

        # Validate file
        result = validator.validate_file(args.file, args.schema)

        # Output results
        if args.json or args.output:
            output_json = json.dumps(result, indent=2)

            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(output_json)
                print(f"Results written to {args.output}")
            else:
                print(output_json)
        else:
            # Human-readable output
            print("\n" + "=" * 70)
            print("SCHEMA VALIDATION RESULTS")
            print("=" * 70)
            print(f"File: {result['file']}")
            print(f"Schema: {result['schema']}")
            print(f"Valid: {'✓ YES' if result['valid'] else '✗ NO'}")
            print()

            if result['errors']:
                print(f"Errors ({len(result['errors'])}):")
                for error in result['errors']:
                    print(f"  - {error}")
                print()

            if result['warnings']:
                print(f"Warnings ({len(result['warnings'])}):")
                for warning in result['warnings']:
                    print(f"  - {warning}")
                print()

            if result['valid'] and not result['warnings']:
                print("✓ Validation passed with no warnings")

        # Exit with appropriate code
        exit_code = 0 if result['valid'] else 1
        sys.exit(exit_code)

    except ValidationError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(2)


if __name__ == '__main__':
    main()
