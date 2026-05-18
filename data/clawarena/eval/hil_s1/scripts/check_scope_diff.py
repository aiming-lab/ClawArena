#!/usr/bin/env python3
"""
Check document topic coverage (scope diff) for hil_s1 scenario.

This script validates that a document covers all required topics based on keyword matching.
It's used to verify that documents address all necessary scope areas.

Usage:
    python check_scope_diff.py --file document.md --required-topics schema_changes data_quality
    python check_scope_diff.py --file report.json --required-topics timeline risks --verbose
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from datetime import datetime, timezone

# Import validation utilities
from validation_utils import (
    match_topic_keywords,
    load_json_file,
    ValidationError
)


class ScopeDiffChecker:
    """Checker for document topic coverage validation."""

    # Default topic keywords mapping
    DEFAULT_TOPIC_KEYWORDS = {
        'schema_changes': [
            'schema', 'field', 'column', 'data type', 'structure',
            'table', 'attribute', 'property', 'definition', 'format'
        ],
        'data_quality': [
            'quality', 'validation', 'accuracy', 'completeness', 'consistency',
            'integrity', 'reliability', 'correctness', 'clean', 'valid'
        ],
        'timeline': [
            'timeline', 'schedule', 'deadline', 'milestone', 'date',
            'duration', 'phase', 'period', 'timeframe', 'delivery'
        ],
        'risks': [
            'risk', 'issue', 'problem', 'concern', 'challenge',
            'threat', 'vulnerability', 'obstacle', 'blocker', 'impediment'
        ],
        'action_items': [
            'action', 'task', 'todo', 'next step', 'follow up',
            'activity', 'deliverable', 'work item', 'assignment'
        ],
        'data_overview': [
            'overview', 'summary', 'dataset', 'records', 'data',
            'statistics', 'metrics', 'count', 'volume', 'scope'
        ],
        'field_mapping': [
            'mapping', 'field', 'source', 'target', 'transformation',
            'conversion', 'translation', 'correspondence', 'relationship'
        ],
        'issue_tracker': [
            'issue', 'bug', 'problem', 'ticket', 'tracking',
            'defect', 'error', 'fault', 'incident'
        ],
        'data_lineage': [
            'lineage', 'provenance', 'source', 'derived', 'origin',
            'ancestry', 'heritage', 'history', 'trace', 'flow'
        ],
        'deliverables': [
            'deliverable', 'output', 'artifact', 'product', 'result',
            'outcome', 'asset', 'document', 'file', 'submission'
        ],
        'team': [
            'team', 'member', 'owner', 'responsible', 'assigned',
            'person', 'role', 'stakeholder', 'contributor'
        ],
        'methodology': [
            'methodology', 'approach', 'process', 'procedure', 'method',
            'technique', 'strategy', 'framework', 'workflow'
        ],
        'requirements': [
            'requirement', 'specification', 'criteria', 'constraint', 'rule',
            'condition', 'prerequisite', 'expectation', 'standard'
        ],
        'testing': [
            'test', 'testing', 'verification', 'validation', 'check',
            'quality assurance', 'qa', 'coverage', 'scenario'
        ],
        'documentation': [
            'documentation', 'document', 'report', 'readme', 'guide',
            'manual', 'specification', 'description', 'explanation'
        ],
        # hil_s1 scenario-specific topics
        'schema_change': [
            'schema change', 'schema changes', 'field change', 'column change',
            'schema update', 'schema diff', 'structure change'
        ],
        'code_fix': [
            'code fix', 'bug fix', 'fixed', 'correction', 'patch',
            'corrected', 'resolved', 'repair', 'code change'
        ],
        'conclusion_revision': [
            'conclusion revision', 'revised conclusion', 'conclusion update',
            'updated conclusion', 'conclusion change', 'revised finding'
        ],
        'priority_conflict': [
            'priority conflict', 'conflicting priority', 'disagreement',
            'misalignment', 'competing priority', 'priority dispute'
        ],
        'q4_baseline': [
            'q4 baseline', 'Q4 baseline', 'quarter 4 baseline',
            'q4 reference', 'baseline q4', 'q4 data'
        ],
        'deadline': [
            'deadline', 'due date', 'delivery date', 'final date',
            'cutoff', 'submission date', 'target date'
        ],
        'maya_estimate': [
            'maya estimate', "maya's estimate", 'maya estimated',
            'maya number', 'estimate from maya', 'maya scope'
        ],
        'jordan_perspective': [
            'jordan perspective', "jordan's perspective", 'jordan view',
            "jordan's view", 'jordan opinion', 'jordan noted', 'jordan said'
        ],
        'actual_scope': [
            'actual scope', 'real scope', 'true scope', 'contamination scope',
            'scope of contamination', 'actual extent', 'actual impact'
        ],
        'method_change': [
            'method change', 'methodology change', 'changed method',
            'statistical method', 'spearman', 'pearson', 'correlation method'
        ],
        'threshold_fix': [
            'threshold fix', 'threshold correction', 'fixed threshold',
            'threshold update', 'threshold change', 'adjusted threshold'
        ],
        'data_version': [
            'data version', 'v1', 'v2', 'transactions_v1', 'transactions_v2',
            'dataset version', 'version of data', 'data v1', 'data v2'
        ],
        'baseline_recalc': [
            'baseline recalc', 'baseline recalculation', 'recalculate baseline',
            'recalculated baseline', 'baseline recompute', 'baseline update'
        ],
    }

    def __init__(
        self,
        custom_keywords: Optional[Dict[str, List[str]]] = None,
        verbose: bool = False
    ):
        """
        Initialize the scope diff checker.

        Args:
            custom_keywords: Optional custom topic-to-keywords mapping
            verbose: If True, output detailed checking information
        """
        self.topic_keywords = custom_keywords or self.DEFAULT_TOPIC_KEYWORDS
        self.verbose = verbose
        self.results = {
            'checked_at': datetime.now(timezone.utc).isoformat(),
            'file': None,
            'required_topics': [],
            'covered_topics': [],
            'missing_topics': [],
            'coverage_details': {},
            'valid': False
        }

    def log(self, message: str, level: str = "INFO"):
        """Log a message if verbose mode is enabled."""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [{level}] {message}", file=sys.stderr)

    def extract_text_content(self, file_path: Path) -> str:
        """
        Extract text content from a file.

        Supports:
        - Plain text files (.txt, .md)
        - JSON files (extracts string values)
        - Python files (.py)

        Args:
            file_path: Path to the file

        Returns:
            Extracted text content

        Raises:
            ValidationError: If file cannot be read
        """
        self.log(f"Extracting content from {file_path}", "INFO")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            raise ValidationError(f"Cannot read file {file_path}: {e}")

        # For JSON files, extract text from all string values
        if file_path.suffix == '.json':
            try:
                data = json.loads(content)
                text_parts = self._extract_json_strings(data)
                content = ' '.join(text_parts)
                self.log(f"Extracted {len(text_parts)} text segments from JSON", "DEBUG")
            except json.JSONDecodeError:
                # If JSON parsing fails, use raw content
                self.log("JSON parsing failed, using raw content", "WARNING")

        return content

    def _extract_json_strings(self, data: Any) -> List[str]:
        """
        Recursively extract all string values from JSON data.

        Args:
            data: JSON data (dict, list, or primitive)

        Returns:
            List of string values found
        """
        strings = []

        if isinstance(data, str):
            strings.append(data)
        elif isinstance(data, dict):
            for value in data.values():
                strings.extend(self._extract_json_strings(value))
        elif isinstance(data, list):
            for item in data:
                strings.extend(self._extract_json_strings(item))

        return strings

    def check_topic_coverage(
        self,
        content: str,
        topic: str
    ) -> Dict[str, Any]:
        """
        Check if content covers a specific topic.

        Args:
            content: The text content to search
            topic: The topic name to check

        Returns:
            Dictionary with coverage details
        """
        self.log(f"Checking coverage for topic: {topic}", "DEBUG")

        result = {
            'topic': topic,
            'covered': False,
            'keywords_found': [],
            'keyword_positions': []
        }

        # Get keywords for this topic
        keywords = self.topic_keywords.get(topic, [topic.replace('_', ' ')])

        content_lower = content.lower()

        # Check each keyword
        for keyword in keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in content_lower:
                result['keywords_found'].append(keyword)

                # Find positions
                start_pos = 0
                while True:
                    pos = content_lower.find(keyword_lower, start_pos)
                    if pos == -1:
                        break

                    # Get context around the keyword (30 chars before and after)
                    context_start = max(0, pos - 30)
                    context_end = min(len(content), pos + len(keyword) + 30)
                    context = content[context_start:context_end]

                    result['keyword_positions'].append({
                        'keyword': keyword,
                        'position': pos,
                        'context': context.strip()
                    })

                    start_pos = pos + 1

        # Consider covered if at least one keyword found
        result['covered'] = len(result['keywords_found']) > 0

        if result['covered']:
            self.log(
                f"Topic '{topic}' covered (found {len(result['keywords_found'])} keyword(s))",
                "INFO"
            )
        else:
            self.log(f"Topic '{topic}' NOT covered", "WARNING")

        return result

    def check_file(
        self,
        file_path: Path,
        required_topics: List[str]
    ) -> Dict[str, Any]:
        """
        Check a file for required topic coverage.

        Args:
            file_path: Path to the file to check
            required_topics: List of topic names that must be covered

        Returns:
            Dictionary with check results
        """
        self.log(f"Checking file: {file_path}", "INFO")
        self.log(f"Required topics: {', '.join(required_topics)}", "INFO")

        self.results['file'] = str(file_path)
        self.results['required_topics'] = required_topics

        # Extract content
        try:
            content = self.extract_text_content(file_path)
            self.log(f"Extracted {len(content)} characters", "DEBUG")
        except ValidationError as e:
            self.results['error'] = str(e)
            self.log(f"Content extraction failed: {e}", "ERROR")
            return self.results

        # Check each required topic
        covered_topics = []
        missing_topics = []

        for topic in required_topics:
            coverage = self.check_topic_coverage(content, topic)
            self.results['coverage_details'][topic] = coverage

            if coverage['covered']:
                covered_topics.append(topic)
            else:
                missing_topics.append(topic)

        self.results['covered_topics'] = covered_topics
        self.results['missing_topics'] = missing_topics

        # Overall validity: all topics must be covered
        self.results['valid'] = len(missing_topics) == 0

        if self.results['valid']:
            self.log("All required topics covered", "INFO")
        else:
            self.log(
                f"{len(missing_topics)} topic(s) not covered: {', '.join(missing_topics)}",
                "ERROR"
            )

        return self.results

    def get_summary(self) -> str:
        """
        Get a human-readable summary of check results.

        Returns:
            Formatted summary string
        """
        lines = []
        lines.append("=" * 70)
        lines.append("SCOPE DIFF (TOPIC COVERAGE) CHECK RESULTS")
        lines.append("=" * 70)
        lines.append(f"File: {self.results['file']}")
        lines.append(f"Status: {'✓ PASSED' if self.results['valid'] else '✗ FAILED'}")
        lines.append("")

        total_topics = len(self.results['required_topics'])
        covered_count = len(self.results['covered_topics'])
        coverage_pct = (covered_count / total_topics * 100) if total_topics > 0 else 0

        lines.append(f"Coverage: {covered_count}/{total_topics} topics ({coverage_pct:.1f}%)")
        lines.append("")

        # Covered topics
        if self.results['covered_topics']:
            lines.append(f"Covered Topics ({len(self.results['covered_topics'])}):")
            for topic in self.results['covered_topics']:
                coverage = self.results['coverage_details'][topic]
                keywords = ', '.join(coverage['keywords_found'][:3])
                if len(coverage['keywords_found']) > 3:
                    keywords += f", ... (+{len(coverage['keywords_found']) - 3} more)"
                lines.append(f"  ✓ {topic} (keywords: {keywords})")
            lines.append("")

        # Missing topics
        if self.results['missing_topics']:
            lines.append(f"Missing Topics ({len(self.results['missing_topics'])}):")
            for topic in self.results['missing_topics']:
                keywords = self.topic_keywords.get(topic, [topic.replace('_', ' ')])
                expected_keywords = ', '.join(keywords[:5])
                if len(keywords) > 5:
                    expected_keywords += f", ... (+{len(keywords) - 5} more)"
                lines.append(f"  ✗ {topic}")
                lines.append(f"    Expected keywords: {expected_keywords}")
            lines.append("")

        # Show sample contexts for first few covered topics
        if self.verbose and self.results['covered_topics']:
            lines.append("Sample Contexts:")
            for topic in self.results['covered_topics'][:3]:
                coverage = self.results['coverage_details'][topic]
                if coverage['keyword_positions']:
                    lines.append(f"  {topic}:")
                    for kw_info in coverage['keyword_positions'][:2]:
                        lines.append(f"    - \"{kw_info['context']}\"")

        return "\n".join(lines)

    def add_custom_keywords(
        self,
        topic: str,
        keywords: List[str],
        replace: bool = False
    ):
        """
        Add custom keywords for a topic.

        Args:
            topic: The topic name
            keywords: List of keywords to add
            replace: If True, replace existing keywords; if False, append
        """
        if replace or topic not in self.topic_keywords:
            self.topic_keywords[topic] = keywords
        else:
            self.topic_keywords[topic].extend(keywords)

        self.log(f"Updated keywords for topic '{topic}': {len(self.topic_keywords[topic])} total", "INFO")


def main():
    """Main entry point for the check_scope_diff script."""
    parser = argparse.ArgumentParser(
        description="Check document topic coverage (scope diff)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Common topics:
  - schema_changes: Database/data schema modifications
  - data_quality: Data quality and validation
  - timeline: Project timeline and milestones
  - risks: Risk identification and assessment
  - action_items: Action items and tasks
  - data_overview: Dataset overview and statistics
  - field_mapping: Field mapping and transformations
  - issue_tracker: Issue tracking
  - data_lineage: Data lineage and provenance
  - deliverables: Project deliverables
  - team: Team members and roles
  - methodology: Methodologies and approaches
  - requirements: Requirements and specifications
  - testing: Testing and validation
  - documentation: Documentation

Examples:
  # Check if a document covers schema changes and data quality
  python check_scope_diff.py --file report.md \\
      --required-topics schema_changes data_quality

  # Check multiple topics with verbose output
  python check_scope_diff.py --file overview.json \\
      --required-topics timeline risks action_items deliverables \\
      --verbose

  # Use custom keywords for a topic
  python check_scope_diff.py --file doc.txt \\
      --required-topics custom_topic \\
      --custom-keywords custom_topic:keyword1,keyword2,keyword3

  # Save results to JSON
  python check_scope_diff.py --file report.md \\
      --required-topics schema_changes data_quality \\
      --output results.json
        """
    )

    parser.add_argument(
        '--file',
        type=Path,
        required=True,
        help="File to check for topic coverage"
    )
    parser.add_argument(
        '--required-topics',
        nargs='+',
        required=True,
        help="List of topics that must be covered"
    )
    parser.add_argument(
        '--custom-keywords',
        action='append',
        help="Add custom keywords for a topic (format: topic:keyword1,keyword2,...)"
    )
    parser.add_argument(
        '--list-topics',
        action='store_true',
        help="List all known topics with their keywords and exit"
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

    args = parser.parse_args()

    # Create checker
    checker = ScopeDiffChecker(verbose=args.verbose)

    # List topics mode
    if args.list_topics:
        print("\nKnown Topics and Keywords:")
        print("=" * 70)
        for topic, keywords in sorted(checker.topic_keywords.items()):
            print(f"\n{topic}:")
            print(f"  Keywords ({len(keywords)}): {', '.join(keywords)}")
        sys.exit(0)

    # Add custom keywords if provided
    if args.custom_keywords:
        for custom_kw in args.custom_keywords:
            try:
                topic, keywords_str = custom_kw.split(':', 1)
                keywords = [kw.strip() for kw in keywords_str.split(',')]
                checker.add_custom_keywords(topic, keywords, replace=False)
            except ValueError:
                print(
                    f"Warning: Invalid custom keyword format: {custom_kw}. "
                    "Expected format: topic:keyword1,keyword2,...",
                    file=sys.stderr
                )

    # Check if file exists
    if not args.file.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    try:
        # Run checks
        results = checker.check_file(args.file, args.required_topics)

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

        # Exit with appropriate code
        exit_code = 0 if results['valid'] else 1
        sys.exit(exit_code)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(2)


if __name__ == '__main__':
    main()
