# NexaRetail Team Style Guide

## Data Formatting (P1)

### Timestamp Format (P1 - Critical)

All timestamps must use ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`

**Correct Examples**:
- `2025-03-14T17:00:00Z`
- `2025-01-01T00:00:00Z`
- `2024-12-31T23:59:59Z`

**Wrong Examples**:
- `March 14` ❌
- `3/14/2025` ❌
- `14-03-2025` ❌
- `2025/03/14` ❌
- `Mar 14, 2025` ❌

**Rationale**: ISO 8601 is an international standard that eliminates ambiguity around date formats (MM/DD vs DD/MM), includes time and timezone information, sorts correctly as strings, and is machine-readable. This format is essential for data consistency, international collaboration, and proper time-based analysis.

**Application Contexts**:
- All database timestamp fields
- Data file columns containing dates or times
- Log entries and audit trails
- Report headers and footers
- Documentation of analysis dates
- File naming conventions when dates are included
- API requests and responses
- Configuration files with time-based settings

**Implementation Guidelines**:
- In Python: Use `datetime.isoformat()` or `strftime('%Y-%m-%dT%H:%M:%SZ')`
- In pandas: Use `pd.to_datetime()` with `format='ISO8601'` for parsing
- For date-only (no time): `YYYY-MM-DD` is acceptable (e.g., `2025-03-14`)
- Always use UTC timezone (Z suffix) unless specific timezone context is required
- When timezone is not UTC, use offset format: `2025-03-14T17:00:00-08:00`

**Data Validation**:
- All timestamp fields must validate against ISO 8601 format
- Reject any data files with non-conforming timestamp formats
- Conversion scripts must transform legacy formats to ISO 8601
- Generate warnings when ambiguous date formats are detected

### Number Formatting (P1 - Critical)

Numbers >= 1,000 must use thousands separators (commas)

**Correct Examples**:
- `51,203`
- `1,234,567`
- `1,000`
- `12,345.67`

**Wrong Examples**:
- `51203` ❌
- `1234567` ❌
- `1000` ❌
- `12345.67` ❌

**Rationale**: Thousands separators dramatically improve readability of large numbers, reducing errors in communication and decision-making. Without separators, numbers like 1000000 and 10000000 are easily confused. This standard ensures consistent, readable presentation across all team communications and deliverables.

**Application Contexts**:
- All numbers in reports and presentations
- Dashboard displays and visualizations
- Executive summaries and business communications
- Email and chat messages discussing metrics
- Documentation examples with numeric values
- Code comments when referencing specific values
- Test data and validation examples

**Exceptions**:
- Source code (variable values, constants): use unseparated format `1000` for valid syntax
- File sizes in technical contexts: `1024` (bytes) is acceptable
- IDs and codes: customer_id `51203` without separator is fine
- Technical specifications: port `8080`, error code `404` without separators
- Mathematical formulas: when used in equations, omit separators for clarity

**Implementation Guidelines**:
- In Python: Use f-strings with comma formatting: `f"{value:,}"`
- In pandas: `df['column'].apply(lambda x: f"{x:,}")`
- For floating point: `f"{value:,.2f}"` for 2 decimal places
- In visualizations: Configure axis labels and annotations to include thousands separators
- In Excel/Google Sheets: Apply number format with thousands separator

**Validation and Quality Checks**:
- Review all reports before sharing to ensure compliance
- Automated checks on report generation to flag unseparated large numbers
- Peer review includes checking number formatting
- Style violations should be corrected before delivery

## Code Style and Standards

### Python Code Standards

**PEP 8 Compliance**:
- Follow PEP 8 style guide for Python code
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 88 characters (Black formatter standard)
- Two blank lines between top-level function/class definitions
- One blank line between method definitions

**Naming Conventions**:
- Functions and variables: `snake_case` (e.g., `calculate_churn_rate`, `customer_data`)
- Classes: `PascalCase` (e.g., `ChurnPredictor`, `DataProcessor`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_ITERATIONS`, `DEFAULT_THRESHOLD`)
- Private methods/variables: prefix with single underscore `_private_method`
- Module names: lowercase without underscores when possible (e.g., `preprocessing.py`)

**Documentation Requirements**:
- All functions must have docstrings describing purpose, parameters, and return values
- Use Google style docstrings format:
```python
def calculate_churn_rate(df, start_date, end_date):
    """
    Calculate customer churn rate for specified time period.

    Args:
        df (pd.DataFrame): Customer data with churn status
        start_date (str): Period start date in ISO 8601 format
        end_date (str): Period end date in ISO 8601 format

    Returns:
        float: Churn rate as percentage (0-100)

    Raises:
        ValueError: If date range is invalid or data is empty
    """
    # Implementation here
    pass
```

**Type Hints**:
- Use type hints for function parameters and return values when practical
- Improves code readability and enables static type checking
```python
def process_data(df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
    """Process customer data with given threshold."""
    return df[df['score'] > threshold]
```

**Import Organization**:
- Group imports in three sections separated by blank lines:
  1. Standard library imports
  2. Third-party library imports
  3. Local application imports
- Sort imports alphabetically within each group
- Use absolute imports, avoid relative imports when possible

**Error Handling**:
- Use specific exception types rather than bare `except:`
- Provide informative error messages
- Log errors appropriately
- Clean up resources in `finally` blocks or use context managers

**Code Comments**:
- Write clear, concise comments explaining *why*, not *what*
- Avoid obvious comments that just restate the code
- Use inline comments sparingly, prefer docstrings for function documentation
- Keep comments up-to-date when code changes

**Code Formatting**:
- Use Black code formatter for consistent formatting
- Run `black .` before committing code
- Configuration: line length 88 (Black default)

**Testing Standards**:
- Write unit tests for all data processing functions
- Use pytest framework
- Aim for >80% code coverage on critical functions
- Test edge cases: empty inputs, null values, boundary conditions
- Name test functions clearly: `test_calculate_churn_rate_with_valid_data()`

### SQL Style Standards

**Keyword Formatting**:
- SQL keywords in UPPERCASE: `SELECT`, `FROM`, `WHERE`, `JOIN`
- Table and column names in lowercase with underscores
- Indent subqueries and clauses for readability

**Query Structure**:
```sql
SELECT
    customer_id,
    signup_date,
    last_activity_date,
    DATEDIFF(last_activity_date, signup_date) AS tenure_days
FROM
    customers
WHERE
    churn_status = 'active'
    AND signup_date >= '2024-01-01'
ORDER BY
    signup_date DESC
LIMIT 1000;
```

**Best Practices**:
- Always qualify column names with table names in joins
- Use explicit `JOIN` syntax, avoid implicit joins in `WHERE` clause
- Comment complex queries with explanation of business logic
- Use CTEs (Common Table Expressions) for complex multi-step queries
- Avoid `SELECT *`, specify columns explicitly

### Version Control Standards

**Commit Messages**:
- Use clear, descriptive commit messages
- Format: `<type>: <short description>`
- Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- Examples:
  - `feat: add churn rate calculation function`
  - `fix: handle missing values in customer data`
  - `docs: update README with setup instructions`

**Branching Strategy**:
- Main branch: `main` (protected, requires review)
- Feature branches: `feature/description` (e.g., `feature/churn-model`)
- Bug fixes: `fix/description` (e.g., `fix/date-parsing-error`)
- Merge via pull requests with at least one review

**Pull Request Guidelines**:
- Provide clear description of changes and rationale
- Reference related issues or tickets
- Include testing performed
- Ensure CI/CD checks pass before requesting review
- Keep PRs focused and reasonably sized (<500 lines when possible)

**Code Review Expectations**:
- Review for correctness, readability, and adherence to standards
- Provide constructive feedback
- Approve when standards are met and code is sound
- Request changes for style violations or logical issues

## Documentation Standards

### Code Documentation

**README Files**:
Every project directory should contain a README.md with:
- Project purpose and overview
- Setup instructions and dependencies
- Usage examples
- File structure explanation
- Contact information for questions

**Inline Code Documentation**:
- Docstrings for all public functions and classes
- Comments for complex algorithms or non-obvious logic
- Type hints to clarify expected data types
- Examples in docstrings for key functions

**Data Documentation**:
- Data dictionaries for all datasets
- Schema definitions with field descriptions
- Data lineage: where data comes from and how it's transformed
- Sample data and expected formats
- Known data quality issues and handling

### Analysis Documentation

**Analysis Reports Structure**:
```markdown
# Analysis Title

**Date**: 2025-03-14T17:00:00Z
**Analyst**: [Name]
**Status**: Draft | In Review | Final

## Executive Summary
[2-3 sentence overview of key findings]

## Business Context
[Why this analysis matters, what question we're answering]

## Data Sources
[What data was used, time period, sample sizes]

## Methodology
[Analytical approach, tools used, key assumptions]

## Findings
[Key insights with supporting visualizations]

## Recommendations
[Actionable next steps based on findings]

## Limitations and Caveats
[What we're uncertain about, edge cases, data quality issues]

## Appendix
[Technical details, additional charts, code references]
```

**Methodology Documentation**:
- Explain analytical choices and trade-offs
- Document assumptions explicitly
- Reference statistical methods with citations when appropriate
- Include sensitivity analysis when assumptions are significant

**Findings Presentation**:
- Lead with key insights, support with details
- Use visualizations to clarify patterns
- Quantify findings with specific numbers (formatted per P1 rules)
- Distinguish between correlation and causation
- Note confidence levels and uncertainty

### Meeting and Decision Documentation

**Meeting Notes Template**:
```markdown
# Meeting: [Topic]
**Date**: [ISO 8601 timestamp]
**Attendees**: [Names and roles]
**Note Taker**: [Name]

## Agenda
1. [Topic 1]
2. [Topic 2]

## Discussion Summary
- [Key points discussed]

## Decisions Made
- [Decision 1: who, what, why]
- [Decision 2: who, what, why]

## Action Items
- [ ] [Task] - Owner: [Name] - Due: [Date]
- [ ] [Task] - Owner: [Name] - Due: [Date]

## Parking Lot (Future Topics)
- [Items to discuss later]
```

**Decision Records**:
For significant decisions, document:
- Decision made
- Context and problem being solved
- Options considered
- Rationale for chosen option
- Implications and follow-up actions
- Date and decision makers

## Visualization and Reporting Standards

### Chart Design Principles

**General Guidelines**:
- Every chart must have a clear, descriptive title
- Label all axes with units
- Include data source and date in caption or footer
- Use colorblind-friendly color palettes
- Maintain consistent color schemes across related charts
- Remove chart junk: unnecessary gridlines, borders, decorations

**Chart Type Selection**:
- **Line charts**: Time series, trends over time
- **Bar charts**: Comparisons across categories
- **Scatter plots**: Relationships between two variables
- **Histograms**: Distribution of single variable
- **Box plots**: Distribution summary with outliers
- **Heatmaps**: Correlation matrices, calendar data

**Color Palette**:
Primary palette (for categorical data):
- Blue: #1f77b4
- Orange: #ff7f0e
- Green: #2ca02c
- Red: #d62728
- Purple: #9467bd

Sequential (for continuous data):
- Use single-hue gradients (light to dark)
- Avoid rainbow color scales

Diverging (for data with meaningful center):
- Use blue-white-red or similar diverging schemes

**Axis Formatting**:
- Apply P1 number formatting: thousands separators for large numbers
- Use ISO 8601 format for time axis labels
- Include percentage symbols when showing percentages
- Round to appropriate precision (avoid excessive decimal places)

**Font and Text**:
- Consistent font family across all visualizations
- Font sizes: title 14pt, axis labels 11pt, annotations 10pt
- Avoid all caps except for brief labels
- Left-align multi-line text

### Dashboard Standards

**Layout Principles**:
- Most important metrics/charts at top or upper-left
- Group related visualizations together
- Use white space effectively, avoid cramming
- Consistent spacing and alignment
- Mobile-responsive when possible

**Interactivity**:
- Provide filters for time period, segment, other key dimensions
- Enable drill-down from summary to detail
- Highlight on hover for additional information
- Reset button to return to default view

**Performance**:
- Dashboard should load in <3 seconds
- Optimize queries and data processing
- Cache data when appropriate
- Progressive loading for complex dashboards

**Update Frequency**:
- Clearly indicate data freshness: "Data as of [timestamp]"
- Automatic refresh schedule if applicable
- Manual refresh option
- History/versioning for tracking changes over time

### Report Templates

**Executive Summary (1 page)**:
```markdown
# [Project Name]: Executive Summary

**Date**: [ISO 8601]
**Prepared by**: [Team]

## Key Findings
1. [Finding 1 with quantified impact]
2. [Finding 2 with quantified impact]
3. [Finding 3 with quantified impact]

## Recommended Actions
1. [Action 1 with expected outcome]
2. [Action 2 with expected outcome]

## Success Metrics
- [Metric 1]: Current [X], Target [Y]
- [Metric 2]: Current [X], Target [Y]

## Next Steps
- [Step 1] - Timeline
- [Step 2] - Timeline
```

**Detailed Analysis Report (Multi-page)**:
- Follow structure outlined in Analysis Documentation section
- Include table of contents for reports >5 pages
- Use appendices for technical details
- Cross-reference sections and figures
- Include glossary if domain-specific terms are used

### Presentation Standards

**Slide Design**:
- One main idea per slide
- Minimal text, use bullet points
- Large, readable fonts (minimum 18pt body text)
- High contrast between text and background
- Visualizations larger than text when possible

**Presentation Flow**:
1. Title slide with context
2. Agenda/outline
3. Problem statement and business context
4. Methodology (brief, move details to appendix)
5. Key findings (1-3 slides, most important content)
6. Supporting details and evidence
7. Recommendations and next steps
8. Q&A slide
9. Appendix with technical details

**Data in Presentations**:
- Focus on insights, not raw data
- Highlight key numbers in visualizations
- Use animation sparingly and purposefully
- Provide handouts with full details if needed

## Communication Standards

### Email and Messaging

**Subject Lines**:
- Be specific and descriptive
- Include project name when relevant
- Indicate urgency if applicable: [URGENT], [FYI], [Action Required]
- Examples:
  - "NexaRetail Churn Analysis: Q1 Data Ready for Review"
  - "[Action Required] Review churn model by EOD Friday"

**Message Structure**:
- Start with context and purpose
- Use bullet points for multiple items
- Bold key information or action items
- End with clear next steps or call to action
- Include relevant links and attachments

**Professional Tone**:
- Be clear and concise
- Professional but friendly
- Avoid jargon when communicating cross-functionally
- Use active voice
- Proofread before sending

**Response Expectations**:
- Acknowledge receipt of important messages
- Set expectations if you need time to provide full response
- Follow up on open items
- Use email threads/chat threads to maintain context

### Status Updates

**Daily Updates Format**:
```
📅 [Date]

✅ Completed:
- [Task 1]
- [Task 2]

🚧 In Progress:
- [Task 3] - [% complete or status]

🎯 Next:
- [Task 4]

🚫 Blockers:
- [Blocker if any, or "None"]
```

**Weekly Updates Format**:
```markdown
# Week of [Date]

## Highlights
- [Major accomplishment 1]
- [Major accomplishment 2]

## Progress by Milestone
- [Milestone 1]: [status and % complete]
- [Milestone 2]: [status and % complete]

## Metrics
- [Key metric]: [current value] (target: [target value])

## Challenges and Mitigations
- [Challenge]: [mitigation approach]

## Next Week Focus
- [Priority 1]
- [Priority 2]

## Support Needed
- [Request if any]
```

### Feedback and Code Review

**Giving Feedback**:
- Be specific and constructive
- Focus on the work, not the person
- Explain rationale for suggestions
- Distinguish between must-fix issues and nice-to-have improvements
- Acknowledge good work and improvements

**Receiving Feedback**:
- Assume good intent
- Ask clarifying questions if feedback is unclear
- Respond to each comment (agree, will fix, or discuss alternative)
- Implement agreed-upon changes
- Thank reviewers for their time

**Code Review Comments Format**:
- **[Critical]**: Must be addressed before merge
- **[Suggestion]**: Nice-to-have improvement
- **[Question]**: Seeking clarification
- **[Nit]**: Minor style/formatting issue

## File Naming and Organization

### File Naming Conventions

**General Rules**:
- Use lowercase with underscores: `customer_churn_data.csv`
- Be descriptive but concise
- Include dates for versioned files: `report_2025-03-14.pdf`
- Use ISO 8601 date format in filenames: `YYYY-MM-DD`
- Avoid spaces, special characters (except underscore and hyphen)
- Use consistent suffixes for file types

**Naming Patterns**:
- Data files: `[entity]_[descriptor]_[date].csv`
  - Example: `customers_active_2025-03-14.csv`
- Scripts: `[action]_[object].py`
  - Example: `process_customer_data.py`
- Reports: `[topic]_[type]_[date].md`
  - Example: `churn_analysis_summary_2025-03-14.md`
- Notebooks: `[sequence]_[description].ipynb`
  - Example: `01_exploratory_analysis.ipynb`

**Version Control in Filenames**:
- Avoid version numbers in filenames when using Git (v1, v2, final, final2, etc.)
- Use Git for versioning instead
- If versions needed in filename: `report_v1.0.pdf`, `report_v2.0.pdf`
- For drafts: `report_draft_2025-03-14.md`, becomes `report_final_2025-03-14.md`

### Directory Structure

**Standard Project Structure**:
```
project_root/
├── data/
│   ├── raw/              # Original, immutable data
│   ├── processed/        # Cleaned, transformed data
│   └── external/         # Third-party data sources
├── scripts/
│   ├── preprocessing/    # Data cleaning scripts
│   ├── analysis/         # Analysis scripts
│   └── utils/            # Utility functions
├── notebooks/
│   ├── exploratory/      # EDA notebooks
│   └── modeling/         # Model development notebooks
├── outputs/
│   ├── figures/          # Generated visualizations
│   ├── tables/           # Generated data tables
│   └── models/           # Saved model artifacts
├── reports/
│   ├── drafts/           # Work-in-progress reports
│   └── final/            # Final deliverables
├── docs/                 # Documentation
├── tests/                # Unit and integration tests
├── configs/              # Configuration files
├── README.md
└── requirements.txt      # Python dependencies
```

**File Organization Principles**:
- Keep related files together
- Separate raw and processed data
- Use subdirectories for organization, avoid deep nesting (max 3 levels)
- Include README in each major directory explaining contents
- Archive old files rather than deleting (move to archive/ subdirectory)

## Data Standards

### Data File Formats

**Preferred Formats by Use Case**:
- Tabular data: CSV (small to medium), Parquet (large, performance-critical)
- Configuration: JSON or YAML
- Documentation: Markdown
- Reports: Markdown or PDF
- Presentations: PDF or PowerPoint

**CSV Standards**:
- UTF-8 encoding
- Comma delimiter (not semicolon or tab)
- Double quotes for text fields containing commas
- Header row with descriptive column names
- No blank rows or columns
- ISO 8601 format for date columns
- Consistent null representation (empty string or "NULL", document choice)

**JSON Standards**:
- Pretty-printed with 2-space indentation for human-readable files
- Minified for production/API responses
- Use consistent key naming: snake_case
- ISO 8601 format for timestamp fields
- Include schema version field for compatibility

### Data Quality Standards

**Required Data Checks**:
- Completeness: Check for missing required fields
- Validity: Validate data types, ranges, formats
- Consistency: Check for contradictions and duplicates
- Accuracy: Validate against known benchmarks when possible
- Timeliness: Verify data freshness and recency

**Data Validation Process**:
1. Schema validation: Confirm expected columns and types
2. Range checks: Validate numeric fields within expected ranges
3. Format validation: Confirm dates, emails, etc. match expected formats
4. Referential integrity: Validate foreign keys and relationships
5. Business rule validation: Check domain-specific constraints

**Data Quality Reporting**:
Document and report:
- Number of records processed
- Number of records with quality issues
- Types of quality issues found
- How issues were handled (corrected, flagged, excluded)
- Percentage of data meeting quality standards

### Data Privacy and Security

**Sensitive Data Handling**:
- Never commit sensitive data to version control
- Use `.gitignore` to exclude data files and credentials
- Store credentials in environment variables or secure vaults
- Anonymize or aggregate data when possible for analysis
- Follow GDPR, CCPA, and other relevant data protection regulations

**Access Controls**:
- Limit access to sensitive data to authorized personnel
- Use read-only access when write access not needed
- Log access to sensitive data
- Regularly review and revoke unnecessary access

**Data Retention**:
- Delete or archive data according to retention policies
- Document data lineage and retention periods
- Securely dispose of data when no longer needed

## Testing and Quality Assurance

### Testing Standards

**Unit Testing**:
- Test individual functions in isolation
- Mock external dependencies
- Cover normal cases, edge cases, and error cases
- Aim for >80% code coverage
- Use descriptive test names: `test_calculate_churn_rate_with_empty_dataframe`

**Integration Testing**:
- Test data pipelines end-to-end
- Validate interactions between components
- Use realistic test data
- Verify outputs match expected results

**Data Validation Testing**:
- Automated checks on data processing outputs
- Schema validation
- Distribution checks (mean, std dev within expected ranges)
- Row count and completeness checks

**Test Data Management**:
- Maintain separate test datasets
- Use synthetic or anonymized data for testing
- Version control test data or document how to generate it
- Keep test data small enough for fast test execution

### Code Review Checklist

**Functionality**:
- [ ] Code does what it's supposed to do
- [ ] Edge cases are handled
- [ ] Error handling is appropriate
- [ ] No obvious bugs or logical errors

**Code Quality**:
- [ ] Follows style guide (PEP 8, naming conventions)
- [ ] Well-documented with docstrings and comments
- [ ] No code duplication, good use of functions
- [ ] Appropriate data structures and algorithms

**Testing**:
- [ ] Unit tests included and passing
- [ ] Test coverage is adequate
- [ ] Tests are meaningful and well-named

**Documentation**:
- [ ] README updated if needed
- [ ] Inline comments explain complex logic
- [ ] API documentation complete for public functions

**Security and Performance**:
- [ ] No hardcoded credentials or sensitive data
- [ ] No obvious performance issues
- [ ] Resources cleaned up appropriately
- [ ] Dependencies are necessary and up-to-date

## General Best Practices

### English Language Standards

**Technical Documentation**:
- Use English for all code comments
- Use English for technical documentation
- Use English for commit messages and code reviews
- Be clear and concise, avoid idioms that don't translate well

**Spelling**:
- Use American English spelling in code and documentation
- Examples: "optimize" not "optimise", "color" not "colour"
- Use spell check before finalizing documents

**Grammar and Punctuation**:
- Use complete sentences in documentation
- Proper capitalization and punctuation
- Proofread before sharing
- Use tools like Grammarly for important documents

### Productivity and Efficiency

**Automation**:
- Automate repetitive tasks with scripts
- Use pre-commit hooks for code quality checks
- Set up CI/CD for automated testing
- Create templates for common document types

**Keyboard Shortcuts and Tools**:
- Learn and use IDE shortcuts for efficiency
- Use command-line tools effectively
- Leverage version control GUI tools or command line fluently
- Use Jupyter notebooks for interactive exploration

**Time Management**:
- Use time blocking for focused work
- Minimize context switching
- Batch similar tasks (e.g., code reviews)
- Document as you go, not as a separate step

### Continuous Improvement

**Learning and Development**:
- Stay current with data science best practices
- Share interesting articles and learnings with team
- Conduct retrospectives on projects to identify improvements
- Experiment with new tools and techniques in side projects

**Feedback Culture**:
- Regularly seek feedback on your work
- Provide constructive feedback to others
- Act on feedback received
- Recognize and appreciate good work from teammates

**Process Optimization**:
- Identify bottlenecks and inefficiencies
- Propose improvements to workflows
- Document tribal knowledge
- Streamline repetitive processes

## Style Guide Governance

### Updates and Changes

**Proposing Changes**:
- Anyone can propose style guide changes
- Submit proposal with rationale via pull request
- Discuss with team before merging
- Major changes require consensus

**Version Control**:
- Style guide is version controlled in Git
- Changes are documented in commit messages
- Review history to understand evolution of standards

### Compliance and Enforcement

**Review Process**:
- Code reviews include style compliance checks
- Automated linting tools enforce some standards
- Team members provide feedback on style violations

**Handling Violations**:
- Minor violations: note in review, fix in current or future PR
- Repeated violations: discuss with individual and team
- Critical violations (P1 rules): must be fixed before merge

**Continuous Improvement**:
- Style guide is living document, not set in stone
- Adapt as team learns and evolves
- Balance consistency with pragmatism

---

## Quick Reference

### P1 Rules (Must Follow)

1. **Timestamps**: Use ISO 8601 format `YYYY-MM-DDTHH:MM:SSZ`
2. **Numbers >= 1,000**: Use thousands separators (e.g., `51,203`)

### Common Formats

- **File names**: `lowercase_with_underscores_2025-03-14.csv`
- **Python functions**: `snake_case`
- **Python classes**: `PascalCase`
- **Commit messages**: `type: description`
- **Branch names**: `feature/description` or `fix/description`

### Essential Tools

- **Code formatter**: Black (Python)
- **Testing**: pytest
- **Version control**: Git with pull request workflow
- **Documentation**: Markdown

### Key Contacts

- **Style questions**: Ask in project Slack channel
- **Technical standards**: Maya (Engineering) or Alex (Data Science)
- **Documentation standards**: Jordan (Analysis)
- **Tool recommendations**: Maya (Engineering)

---

This style guide ensures the NexaRetail team produces consistent, high-quality, professional work. By following these standards, we reduce friction in collaboration, improve code and analysis quality, and present a unified professional image to stakeholders. The P1 rules are non-negotiable and must be followed in all deliverables. Other guidelines should be followed unless there's a compelling reason to deviate, which should be discussed with the team.
