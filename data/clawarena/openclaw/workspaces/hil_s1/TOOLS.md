# Tools Reference and Usage Guide

## Overview

This document provides comprehensive documentation for all tools available to the agent within the NexaRetail workspace environment. Each tool represents a specific capability that enables the agent to interact with files, execute code, search for information, and accomplish the data analysis tasks central to the customer churn project.

Tools are the agent's primary means of interaction with the computational environment. Proper tool usage is essential for effective work, while improper usage can lead to errors, data loss, or security issues. This guide covers not only how to use each tool but also best practices, common pitfalls, error handling strategies, and detailed examples.

## General Tool Usage Principles

### Workspace Boundary Enforcement

**Fundamental Constraint**: All file operations are strictly constrained to the designated workspace directory.

The workspace for this project is located at a specific directory path. All file reads, writes, and operations must occur within this boundary. This constraint serves multiple purposes:

- **Security**: Prevents accidental access to or modification of system files or other projects
- **Isolation**: Ensures project work doesn't interfere with other system operations
- **Auditability**: All project artifacts are contained in a single location for review
- **Reproducibility**: Complete project state can be captured by examining workspace contents

**Practical Implications**
- You cannot access files outside the workspace, even if they exist on the system
- You cannot write files to system directories like `/tmp`, `/var`, `/etc`
- You cannot read system configuration files or access other users' files
- All input data must be provided within the workspace
- All output artifacts must be written to workspace subdirectories

**Directory Structure Convention**
```
workspace/
├── data/               # Raw and processed datasets
├── scripts/            # Python scripts and analysis code
├── notebooks/          # Jupyter notebooks for exploratory analysis
├── reports/            # Generated reports and presentations
├── docs/               # Project documentation
├── outputs/            # General output directory for results
└── project/            # Primary working directory for exec commands
```

### Tool Execution Model

**Synchronous Execution**: Tool calls are synchronous—the agent waits for each tool to complete before proceeding.

**Error Returns**: When a tool fails, it returns an error message rather than crashing the agent. The agent must handle these errors gracefully.

**Resource Limits**: Tools may have resource constraints (memory, time, network) that can cause failures on large-scale operations.

## Tool Catalog

### 1. READ Tool

**Purpose**: Read file contents from the workspace filesystem.

**Capabilities**
- Read text files of any format: Python, JSON, CSV, Markdown, YAML, etc.
- Read configuration files
- Read data files for analysis
- Inspect code and documentation
- Read previously generated outputs

**Usage Syntax**
```
Tool: read
Parameters:
  - file_path: Absolute path to file within workspace (required)
```

**Detailed Behavior**

When the read tool is invoked, it:
1. Validates that the file path is within workspace boundaries
2. Checks that the file exists and is readable
3. Reads the entire file content into memory
4. Returns the contents as a string
5. Returns an error message if the file doesn't exist, is not readable, or is outside workspace

**Best Practices**

*Path Specification*
- Always use absolute paths, not relative paths
- Construct paths by combining workspace root with relative structure
- Example: `/workspace/data/customers.csv`, not `../data/customers.csv`

*File Size Considerations*
- For very large files (>100MB), consider whether you need the entire file
- If only specific sections are needed, read the full file but process in chunks
- Be aware that reading enormous files may consume significant memory

*Error Handling*
- Always check if read operation succeeded before using the content
- Common errors: file not found, permission denied, path outside workspace
- Have fallback strategies for missing files: use defaults, notify user, skip gracefully

*Encoding Awareness*
- Most files are UTF-8 encoded, which the tool handles automatically
- If you encounter encoding errors, the file may use a different encoding
- Binary files will return unreadable content—use appropriate tools for binary data

**Common Patterns**

*Reading Configuration Files*
```
Read style_guide.md to understand formatting standards before generating a report.
Read USER.md at startup to understand team composition.
Read data dictionary files to understand dataset schemas.
```

*Reading Data Files*
```
Read CSV file to inspect structure before processing.
Read JSON configuration to understand analysis parameters.
Read sample data to validate processing logic.
```

*Reading Code*
```
Read existing scripts to understand current implementation.
Read Python modules to identify reusable functions.
Read test files to understand expected behavior.
```

**Examples**

*Example 1: Reading a CSV File*
```
Tool: read
Parameters:
  file_path: /workspace/data/customer_data.csv

Expected Return:
customer_id,signup_date,last_activity,churn_status
C001,2024-01-15,2025-03-10,active
C002,2024-02-20,2024-12-15,churned
C003,2024-03-12,2025-03-08,active
...
```

*Example 2: Reading a Python Script*
```
Tool: read
Parameters:
  file_path: /workspace/scripts/data_cleaning.py

Expected Return:
import pandas as pd
import numpy as np

def clean_customer_data(df):
    """Remove duplicates and handle missing values."""
    df = df.drop_duplicates(subset=['customer_id'])
    df['last_activity'] = pd.to_datetime(df['last_activity'])
    return df
...
```

*Example 3: Handling Read Errors*
```
Tool: read
Parameters:
  file_path: /workspace/data/nonexistent.csv

Expected Return:
Error: File not found at path /workspace/data/nonexistent.csv

Agent Response:
The file nonexistent.csv does not exist in the data directory.
I'll check what files are available using search or notify the team that the expected file is missing.
```

**Security Considerations**
- Read tool cannot access files outside workspace—this is enforced at tool level
- No risk of accidentally reading sensitive system files
- If you attempt to read outside workspace, you'll receive an error

**Performance Considerations**
- Reading small files (<1MB) is very fast, typically milliseconds
- Reading large files (10-100MB) takes seconds
- Reading very large files (>100MB) may take tens of seconds
- Consider caching file contents if you'll reference them repeatedly

---

### 2. WRITE Tool

**Purpose**: Create new files or overwrite existing files in the workspace.

**Capabilities**
- Create new text files of any format
- Overwrite existing files with updated content
- Write data processing outputs
- Generate reports and documentation
- Save code and scripts

**Usage Syntax**
```
Tool: write
Parameters:
  - file_path: Absolute path to file within workspace (required)
  - content: String content to write to the file (required)
```

**Detailed Behavior**

When the write tool is invoked, it:
1. Validates that the file path is within workspace boundaries
2. Creates parent directories if they don't exist
3. Writes the content to the file, overwriting if it exists
4. Sets appropriate file permissions
5. Returns success confirmation or error message

**Best Practices**

*Pre-Write Validation*
- **Critical**: Always read existing files before overwriting to prevent data loss
- Verify that the destination directory exists or will be created
- Confirm file path is correct—typos can result in files in wrong locations
- Validate content is complete and correct before writing

*Atomic Writes*
- Write operation is atomic: file is either fully written or not written at all
- No risk of partial writes leaving corrupted files
- However, if write fails, previous content may be lost if overwriting

*Directory Structure*
- Write outputs to appropriate subdirectories based on file type
- Data processing outputs: `/workspace/outputs/` or `/workspace/data/processed/`
- Reports: `/workspace/reports/`
- Scripts: `/workspace/scripts/`
- Documentation: `/workspace/docs/`

*Content Validation*
- Validate content format before writing (e.g., valid JSON, proper CSV structure)
- Check that content meets style guide requirements
- Ensure all necessary information is included
- Verify that generated code is syntactically valid

**Common Patterns**

*Creating Processed Data Files*
```
Read raw data → Process and transform → Write processed data to new file
Always preserve original raw data—write processed data to a new file
```

*Generating Reports*
```
Conduct analysis → Format results as Markdown or text → Write to reports directory
Include all required sections and formatting per style guide
```

*Writing Code Files*
```
Develop script or function → Add documentation and comments → Write to scripts directory
Include docstrings, type hints, and explanatory comments
```

**Examples**

*Example 1: Writing a Processed Data File*
```
Tool: write
Parameters:
  file_path: /workspace/data/processed/customers_cleaned.csv
  content: |
    customer_id,signup_date,last_activity,churn_status
    C001,2024-01-15T00:00:00Z,2025-03-10T00:00:00Z,active
    C002,2024-02-20T00:00:00Z,2024-12-15T00:00:00Z,churned
    C003,2024-03-12T00:00:00Z,2025-03-08T00:00:00Z,active

Result: File created successfully with cleaned customer data
```

*Example 2: Writing a Python Script*
```
Tool: write
Parameters:
  file_path: /workspace/scripts/calculate_churn_rate.py
  content: |
    """Calculate customer churn rate for given time period."""

    import pandas as pd
    from datetime import datetime

    def calculate_churn_rate(df, start_date, end_date):
        """
        Calculate churn rate for specified period.

        Args:
            df: DataFrame with customer data
            start_date: Period start (ISO 8601 format)
            end_date: Period end (ISO 8601 format)

        Returns:
            float: Churn rate as percentage
        """
        period_df = df[
            (df['signup_date'] < start_date) &
            (df['last_activity'] >= start_date)
        ]

        churned = period_df[period_df['churn_status'] == 'churned']
        churn_rate = (len(churned) / len(period_df)) * 100

        return round(churn_rate, 2)

    if __name__ == '__main__':
        # Example usage
        df = pd.read_csv('/workspace/data/customer_data.csv')
        rate = calculate_churn_rate(df, '2025-01-01', '2025-03-31')
        print(f"Q1 2025 churn rate: {rate}%")

Result: Script created successfully at /workspace/scripts/calculate_churn_rate.py
```

*Example 3: Writing a Report*
```
Tool: write
Parameters:
  file_path: /workspace/reports/weekly_status_2025-03-10.md
  content: |
    # NexaRetail Churn Analysis - Weekly Status Report
    Date: 2025-03-10T17:00:00Z

    ## Progress Summary

    This week we completed data cleaning and initial exploratory analysis.
    Key findings include:

    - Total customers in dataset: 51,203
    - Overall churn rate: 12.5%
    - Highest churn segment: customers with <30 day tenure

    ## Completed Tasks

    - Data cleaning script completed and tested
    - Exploratory visualizations generated
    - Initial cohort analysis conducted

    ## Next Steps

    - Develop predictive model for churn probability
    - Analyze feature importance to identify key drivers
    - Prepare preliminary findings presentation

    ## Blockers

    None currently.

Result: Report created successfully
```

*Example 4: Handling Write Errors*
```
Tool: write
Parameters:
  file_path: /etc/system_config.txt
  content: "This would be a security violation"

Expected Return:
Error: Cannot write to path /etc/system_config.txt - outside workspace boundaries

Agent Response:
I cannot write to that location as it's outside the workspace.
I'll write the configuration to /workspace/config/settings.txt instead.
```

**Error Handling**

*Common Write Errors*
- Path outside workspace: Adjust path to be within workspace
- Permission denied: Check directory permissions, may need human intervention
- Disk full: Notify team, may need to clean up old files
- Invalid path: Validate path construction logic

*Recovery Strategies*
- If write fails, preserve content and retry with alternative path
- Log failed write attempts for debugging
- Notify relevant team member if write failures persist
- Never silently ignore write failures

**Security Considerations**
- Write tool cannot write outside workspace—enforced at tool level
- No risk of accidentally overwriting system files
- Parent directory creation is safe within workspace
- File permissions are set appropriately for workspace use

**Performance Considerations**
- Writing small files (<1MB) is very fast
- Writing large files (10-100MB) takes seconds
- Writing very large files may be slow—consider streaming approaches for massive datasets
- Multiple small writes are generally fine, but batching can be more efficient

---

### 3. EXEC Tool

**Purpose**: Execute shell commands within the workspace environment.

**Capabilities**
- Run Python scripts
- Execute data processing commands
- Run statistical analysis tools
- Execute system utilities (ls, grep, wc, etc.)
- Run tests and validation checks

**Usage Syntax**
```
Tool: exec
Parameters:
  - command: Shell command to execute (required)
  - working_directory: Directory to execute from (optional, defaults to /workspace/project/)
```

**Detailed Behavior**

When the exec tool is invoked, it:
1. Sets working directory to `/workspace/project/` (or specified directory)
2. Executes the command in a shell environment
3. Captures both stdout (standard output) and stderr (standard error)
4. Returns the command output and exit code
5. Enforces timeout to prevent indefinite hangs (typically 300 seconds)

**Best Practices**

*Command Construction*
- Use absolute paths for files to avoid ambiguity
- Quote paths that might contain spaces
- Validate command syntax before execution
- Use `&&` to chain commands that depend on each other
- Use `;` to run commands sequentially regardless of success

*Security*
- Never execute commands with unsanitized user input
- Avoid commands that could damage data or system
- Don't execute commands that attempt to escape workspace
- Validate command arguments to prevent injection attacks

*Error Handling*
- Always check exit code to determine success/failure
- Parse stderr to understand error messages
- Implement retry logic for transient failures
- Escalate persistent failures to team members

*Resource Management*
- Be aware of commands that consume significant CPU or memory
- Monitor long-running commands and provide status updates
- Use timeout mechanisms to prevent indefinite hangs
- Clean up temporary files created by commands

**Common Patterns**

*Running Python Scripts*
```
Execute Python data processing scripts
Capture output for logging and validation
Check exit code to confirm successful execution
```

*File System Operations*
```
List directory contents: ls -la /workspace/data/
Count files: find /workspace/data -name "*.csv" | wc -l
Check disk usage: du -sh /workspace/
```

*Data Operations*
```
Count CSV rows: wc -l /workspace/data/customers.csv
Extract columns: cut -d',' -f1,3 /workspace/data/customers.csv
Sort and deduplicate: sort /workspace/data/ids.txt | uniq
```

**Examples**

*Example 1: Running a Python Script*
```
Tool: exec
Parameters:
  command: python /workspace/scripts/clean_data.py

Expected Output:
Processing customer data...
Removed 127 duplicate records
Handled 43 missing values
Wrote cleaned data to /workspace/data/processed/customers_cleaned.csv
Processing complete.

Exit Code: 0

Agent Interpretation:
Script executed successfully (exit code 0).
Cleaned data is now available at the specified output path.
```

*Example 2: Listing Directory Contents*
```
Tool: exec
Parameters:
  command: ls -lh /workspace/data/

Expected Output:
total 15M
-rw-r--r-- 1 user group 12M Mar 10 10:30 customer_data.csv
-rw-r--r-- 1 user group 2.1M Mar 10 14:15 transactions.csv
-rw-r--r-- 1 user group 890K Mar 10 16:45 products.csv
drwxr-xr-x 2 user group 4096 Mar 10 09:00 processed

Exit Code: 0

Agent Interpretation:
Three CSV files are present in the data directory.
A processed subdirectory exists for cleaned data outputs.
```

*Example 3: Checking Python Script Syntax*
```
Tool: exec
Parameters:
  command: python -m py_compile /workspace/scripts/analysis.py

Expected Output:
(no output if successful)

Exit Code: 0

Agent Interpretation:
Script has valid Python syntax and can be imported/executed.
```

*Example 4: Running with Error*
```
Tool: exec
Parameters:
  command: python /workspace/scripts/broken_script.py

Expected Output:
Traceback (most recent call last):
  File "/workspace/scripts/broken_script.py", line 15, in <module>
    result = process_data(df)
  File "/workspace/scripts/broken_script.py", line 8, in process_data
    return df['nonexistent_column'].sum()
KeyError: 'nonexistent_column'

Exit Code: 1

Agent Interpretation:
Script failed due to KeyError - trying to access a column that doesn't exist.
Need to fix the column name or add error handling.
```

*Example 5: Chaining Commands*
```
Tool: exec
Parameters:
  command: cd /workspace/data && ls *.csv | wc -l

Expected Output:
3

Exit Code: 0

Agent Interpretation:
There are 3 CSV files in the data directory.
```

**Advanced Usage**

*Passing Arguments to Scripts*
```
Tool: exec
Parameters:
  command: python /workspace/scripts/analyze.py --input /workspace/data/customers.csv --output /workspace/outputs/results.json

Benefits: Configure script behavior without modifying code
```

*Using Pipes and Redirection*
```
Tool: exec
Parameters:
  command: grep "churned" /workspace/data/customers.csv | wc -l

Purpose: Count churned customers without loading full file into Python
```

*Environment Variables*
```
Tool: exec
Parameters:
  command: export DATA_PATH=/workspace/data && python /workspace/scripts/process.py

Purpose: Configure script behavior via environment variables
```

**Error Handling**

*Interpreting Exit Codes*
- Exit code 0: Success
- Exit code 1: General error
- Exit code 2: Misuse of shell command
- Exit code 126: Command cannot execute
- Exit code 127: Command not found
- Exit code 130: Terminated by Ctrl+C
- Exit code 137: Killed (often out of memory)

*Common Errors and Solutions*

| Error | Possible Cause | Solution |
|-------|---------------|----------|
| Command not found | Typo or command not installed | Verify command spelling, check if tool is available |
| Permission denied | Insufficient permissions | Check file permissions, may need human intervention |
| No such file | File doesn't exist | Verify file path, check if file has been created |
| Syntax error | Invalid command syntax | Review command construction, validate syntax |
| Timeout | Command ran too long | Optimize command, break into smaller steps, or increase timeout |
| Killed (137) | Out of memory | Process smaller data chunks, optimize memory usage |

**Security Considerations**

*Command Injection Prevention*
- Never interpolate untrusted input directly into commands
- Validate and sanitize all command arguments
- Use absolute paths to ensure intended files are accessed
- Avoid shell wildcards with untrusted input

*Workspace Containment*
- Exec operates within workspace boundaries
- Commands cannot access or modify files outside workspace
- System commands are available but effects are limited to workspace

**Performance Considerations**

*Command Execution Speed*
- Simple commands (ls, wc): Milliseconds
- Python scripts: Seconds to minutes depending on complexity
- Data processing: Varies with data size, could be minutes to hours
- Long-running commands: Provide periodic status updates to team

*Optimization Strategies*
- Use efficient system utilities (awk, sed) for text processing when appropriate
- Optimize Python scripts for performance
- Process data in chunks for large datasets
- Use parallel processing for independent operations

---

### 4. SEARCH Tool

**Purpose**: Search for files and content within the workspace.

**Capabilities**
- Find files by name pattern
- Search file contents for specific text or patterns
- Locate code constructs (functions, classes, variables)
- Find documentation and comments
- Discover dataset occurrences

**Usage Syntax**
```
Tool: search
Parameters:
  - query: Search pattern or keywords (required)
  - path: Directory to search in (optional, defaults to workspace root)
  - file_pattern: Limit search to specific file types (optional, e.g., "*.py", "*.csv")
```

**Detailed Behavior**

When the search tool is invoked, it:
1. Searches within the specified path (or entire workspace if not specified)
2. Looks for the query pattern in file names and/or contents
3. Returns list of matching files and/or matching lines with context
4. Supports both literal text search and pattern matching
5. Returns results ranked by relevance

**Best Practices**

*Query Formulation*
- Be specific enough to avoid too many results
- Be broad enough to catch relevant variations
- Use key technical terms for code searches
- Use domain-specific terms for data and documentation searches

*Result Interpretation*
- Review results to identify most relevant matches
- Check context around matches to understand usage
- Distinguish between current code/data vs. old/deprecated artifacts
- Prioritize recent files over old ones when ambiguous

*Search Scope*
- Narrow search to relevant directories when possible for faster results
- Use file patterns to limit to relevant file types
- Search full workspace when you're unsure where something might be

**Common Patterns**

*Finding Files by Name*
```
Search for: "customer_data"
Purpose: Find all files related to customer data
```

*Finding Code Definitions*
```
Search for: "def calculate_churn"
Purpose: Find where churn calculation function is defined
```

*Finding Usage Examples*
```
Search for: "calculate_churn_rate"
Purpose: Find how function is being used across codebase
```

*Finding Configuration Values*
```
Search for: "API_KEY" or "database_url"
Purpose: Locate configuration settings
```

**Examples**

*Example 1: Finding Files by Name*
```
Tool: search
Parameters:
  query: "churn"
  file_pattern: "*.csv"

Expected Results:
/workspace/data/customer_churn_q1.csv
/workspace/data/churn_predictions.csv
/workspace/outputs/churn_analysis_results.csv

Agent Interpretation:
Three CSV files related to churn exist in the workspace.
```

*Example 2: Finding Function Definitions*
```
Tool: search
Parameters:
  query: "def clean_data"
  path: /workspace/scripts/
  file_pattern: "*.py"

Expected Results:
/workspace/scripts/data_processing.py:15: def clean_data(df):
/workspace/scripts/utils.py:42: def clean_data_v2(df, strict=True):

Agent Interpretation:
Two versions of the clean_data function exist.
The second appears to be an updated version with additional parameters.
```

*Example 3: Finding Variable Usage*
```
Tool: search
Parameters:
  query: "CHURN_THRESHOLD"
  path: /workspace/

Expected Results:
/workspace/scripts/config.py:8: CHURN_THRESHOLD = 0.15
/workspace/scripts/analysis.py:23: if churn_rate > CHURN_THRESHOLD:
/workspace/scripts/model.py:67: threshold = CHURN_THRESHOLD

Agent Interpretation:
CHURN_THRESHOLD is defined in config.py and used in two other scripts.
The threshold value is set to 0.15 (15%).
```

*Example 4: Finding Documentation*
```
Tool: search
Parameters:
  query: "ISO 8601"
  path: /workspace/
  file_pattern: "*.md"

Expected Results:
/workspace/style_guide.md:12: All timestamps must use ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`
/workspace/docs/data_dictionary.md:45: Dates are stored in ISO 8601 format

Agent Interpretation:
ISO 8601 timestamp format is mandated in the style guide.
Data dictionary confirms dates follow this standard.
```

**Advanced Usage**

*Pattern Matching*
```
Search supports basic pattern matching:
- Use wildcards for partial matches
- Use quotes for exact phrase matching
- Combine terms to narrow results
```

*Filtering Results*
```
Use file_pattern to focus on relevant file types:
- "*.py" for Python code
- "*.csv" for data files
- "*.md" for documentation
- "*.json" for configuration
```

*Contextual Search*
```
Results include surrounding lines for context:
- See how code is used in context
- Understand data structure from sample rows
- Read full documentation paragraphs
```

**Error Handling**

*No Results Found*
- Broaden search query if too specific
- Check spelling and terminology
- Try alternative terms or phrases
- Search full workspace if path was too narrow

*Too Many Results*
- Narrow query with more specific terms
- Limit to specific directories
- Use file pattern to filter by type
- Search for more distinctive phrases

**Performance Considerations**

*Search Speed*
- Searching small workspaces: Very fast (seconds)
- Searching large codebases: May take longer (tens of seconds)
- Searching file contents: Slower than filename-only search
- Pattern matching: May be slower than literal search

*Optimization*
- Search specific directories rather than full workspace when possible
- Use file patterns to reduce search scope
- Use specific queries rather than very broad terms

---

### 5. WEB_SEARCH Tool

**Purpose**: Search the web for information not available in the workspace.

**Capabilities**
- Look up technical documentation
- Find research papers and articles
- Discover best practices and tutorials
- Verify statistical methods and formulas
- Find library usage examples and API documentation

**Usage Syntax**
```
Tool: web_search
Parameters:
  - query: Search query string (required)
  - num_results: Number of results to return (optional, defaults to 5)
```

**Detailed Behavior**

When the web_search tool is invoked, it:
1. Submits the query to a web search engine
2. Retrieves top results ranked by relevance
3. Returns titles, URLs, and snippets from result pages
4. Does not retrieve full page contents (use URLs for reference)
5. Subject to rate limiting and may fail if overused

**Best Practices**

*When to Use Web Search*
- Information is not available in workspace documentation
- Need to verify statistical methods or formulas
- Looking for library documentation or usage examples
- Researching industry best practices
- Finding relevant research papers or articles

*When NOT to Use Web Search*
- Information should be in workspace documentation (look there first)
- Answering questions about project-specific data or context
- Finding team member preferences (documented in workspace)
- Looking for workspace files or code (use search tool instead)

*Source Evaluation*
- Prioritize authoritative sources: official documentation, peer-reviewed papers, established publications
- Be skeptical of blog posts and forum discussions without corroboration
- Check publication dates: outdated information may no longer be accurate
- Cross-reference multiple sources when possible

*Attribution*
- Always cite web sources in your outputs
- Include URLs so team members can verify information
- Mark web-sourced information as [FROM WEB] in working notes
- If information is critical, suggest team verify independently

**Common Patterns**

*Looking Up Technical Documentation*
```
Query: "pandas DataFrame merge documentation"
Purpose: Verify correct usage of pandas merge function
```

*Finding Statistical Methods*
```
Query: "Cox proportional hazards model assumptions"
Purpose: Ensure correct application of survival analysis method
```

*Researching Best Practices*
```
Query: "customer churn analysis best practices retail"
Purpose: Learn industry-standard approaches to churn analysis
```

*Finding Code Examples*
```
Query: "python matplotlib subplot layout examples"
Purpose: Find visualization code patterns
```

**Examples**

*Example 1: Looking Up Library Documentation*
```
Tool: web_search
Parameters:
  query: "pandas to_datetime format ISO 8601"

Expected Results:
1. pandas.to_datetime — pandas documentation
   URL: https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html
   Snippet: "...format parameter to specify datetime format...ISO 8601 format supported..."

2. Working with datetime formats in pandas
   URL: https://realpython.com/pandas-datetime/
   Snippet: "...ISO 8601 format is recommended...use format='%Y-%m-%dT%H:%M:%SZ'..."

Agent Usage:
Information confirms that pandas supports ISO 8601 format directly.
Can use pd.to_datetime(df['date_col'], format='ISO8601') for efficient parsing.

Citation in output: "Per pandas documentation, ISO 8601 format is natively supported."
```

*Example 2: Researching Statistical Methods*
```
Tool: web_search
Parameters:
  query: "Kaplan-Meier survival analysis customer churn"

Expected Results:
1. Survival Analysis for Customer Churn Prediction
   URL: https://example.com/article/survival-churn
   Snippet: "...Kaplan-Meier curves provide non-parametric estimates of churn timing..."

2. Applying Survival Analysis to Business Problems
   URL: https://academic-journal.com/survival-business
   Snippet: "...particularly useful when exact churn timing is uncertain..."

Agent Usage:
Research confirms Kaplan-Meier is appropriate for churn analysis.
Learn that method handles censored data (customers who haven't churned yet).

Citation in output: "Kaplan-Meier survival analysis is well-suited for churn prediction [see: example.com/article/survival-churn]"
```

*Example 3: Finding Best Practices*
```
Tool: web_search
Parameters:
  query: "feature engineering customer churn prediction"

Expected Results:
Multiple articles discussing common features for churn models:
- Recency, frequency, monetary value (RFM)
- Customer lifetime value
- Engagement metrics
- Support ticket frequency

Agent Usage:
Synthesize common practices from multiple sources.
Apply to feature engineering for NexaRetail project.

Citation in output: "Industry best practices suggest including RFM features in churn models [BASED ON MULTIPLE WEB SOURCES]"
```

**Error Handling**

*Web Search Failures*
- Network unavailable: Notify team, proceed with available information
- Rate limited: Wait and retry, or defer non-critical searches
- No relevant results: Reformulate query, try alternative search terms

*Source Quality Issues*
- Conflicting information: Present multiple perspectives, note uncertainty
- Outdated information: Check publication dates, seek recent sources
- Low-credibility sources: Mark as [UNVERIFIED], seek better sources

**Security and Privacy Considerations**

*Query Content*
- Don't include sensitive customer data in queries
- Don't search for specific customer names or PII
- Keep queries generic and technical
- Avoid including proprietary business information

*Information Usage*
- Web-sourced information is public knowledge
- Don't treat web search results as confidential
- Be aware that queries may be logged by search providers

**Performance Considerations**

*Search Speed*
- Web searches typically take 1-3 seconds
- May be slower if network is congested
- Multiple searches in sequence can add up to significant time

*Rate Limiting*
- Tool may be subject to rate limits
- Avoid excessive web searches in short time periods
- Batch research needs when possible
- Use search results efficiently to minimize repeated searches

---

## Tool Combination Patterns

Effective work often involves combining multiple tools in sequence.

### Pattern 1: Data Processing Pipeline

**Workflow**: Read → Process → Write → Exec
```
1. Read raw data file
2. Process data in Python/pandas (in agent logic)
3. Write processed data to new file
4. Exec to validate output file (e.g., count rows, check format)
```

**Example**:
```
Read /workspace/data/raw_customers.csv
Process: Remove duplicates, handle missing values, standardize dates
Write /workspace/data/processed/customers_clean.csv
Exec: wc -l to confirm row count matches expectations
```

### Pattern 2: Code Development and Testing

**Workflow**: Search → Read → Write → Exec
```
1. Search for existing similar code
2. Read existing code to understand patterns
3. Write new code following established patterns
4. Exec to test new code and verify it works
```

**Example**:
```
Search for "def calculate" to find similar functions
Read /workspace/scripts/calculations.py to see code style
Write /workspace/scripts/new_calculation.py with new function
Exec: python /workspace/scripts/new_calculation.py to test
```

### Pattern 3: Analysis and Reporting

**Workflow**: Read → Exec → Write
```
1. Read data file to understand structure
2. Exec Python script to perform analysis
3. Write report documenting findings
```

**Example**:
```
Read /workspace/data/customers.csv to understand schema
Exec: python /workspace/scripts/churn_analysis.py
Write /workspace/reports/churn_findings.md with results
```

### Pattern 4: Research and Implementation

**Workflow**: Web_Search → Read → Write
```
1. Web_search for best practices or documentation
2. Read existing workspace code to understand current approach
3. Write improved code incorporating research findings
```

**Example**:
```
Web_search: "pandas memory optimization large datasets"
Read /workspace/scripts/data_loader.py to see current approach
Write updated version with memory optimization techniques
```

### Pattern 5: Error Diagnosis and Fixing

**Workflow**: Exec → Read → Search → Write → Exec
```
1. Exec command that's failing
2. Read error output and relevant code
3. Search for similar errors or code patterns
4. Write fixed version of code
5. Exec again to verify fix
```

**Example**:
```
Exec: python /workspace/scripts/broken.py (fails)
Read /workspace/scripts/broken.py to see code
Search for function that's raising error
Write corrected version to /workspace/scripts/broken.py
Exec: python /workspace/scripts/broken.py (succeeds)
```

## Tool Limitations and Constraints

### General Limitations

**Workspace Boundary**
- Cannot access files outside designated workspace
- Cannot modify system configuration
- Cannot install new software or packages
- Cannot access external databases directly

**Resource Constraints**
- Memory limits may prevent processing very large datasets
- Time limits may cause long-running operations to timeout
- Disk space limits may prevent writing very large files
- Network access may be restricted or rate-limited

**Tool-Specific Constraints**

*Read Tool*
- Cannot read binary files meaningfully
- Very large files may be slow or fail
- Cannot read from network locations or URLs

*Write Tool*
- Cannot write to read-only locations
- Cannot modify file permissions or ownership
- Disk space failures may cause write failures

*Exec Tool*
- Timeout on long-running commands (typically 300 seconds)
- Cannot run interactive commands
- Cannot execute with elevated privileges
- Limited environment variables and PATH

*Search Tool*
- May be slow on very large workspaces
- Pattern matching capabilities are basic
- Results are limited to prevent overwhelming output

*Web_Search Tool*
- Rate limiting may prevent frequent searches
- Results quality depends on query formulation
- Cannot access paywalled or restricted content
- Network failures may prevent searches

## Troubleshooting Common Issues

### Issue: "File not found"

**Symptoms**: Read or exec tool reports file doesn't exist
**Diagnosis**: File path is incorrect or file hasn't been created yet
**Solutions**:
- Use search tool to find the file
- Use exec with `ls` to list directory contents
- Check if file has been created yet in the workflow
- Verify absolute path is correct

### Issue: "Permission denied"

**Symptoms**: Read, write, or exec fails with permission error
**Diagnosis**: File or directory permissions don't allow the operation
**Solutions**:
- Check if path is outside workspace (tool will enforce boundary)
- Verify file exists and is readable/writable
- May require human intervention to fix permissions
- Check if file is locked by another process

### Issue: "Command timeout"

**Symptoms**: Exec tool reports command exceeded time limit
**Diagnosis**: Command is taking too long to complete
**Solutions**:
- Optimize command or script for better performance
- Break operation into smaller chunks
- Process data in batches rather than all at once
- Consider if operation is necessary or can be simplified

### Issue: "Out of memory"

**Symptoms**: Exec tool reports memory error or command killed
**Diagnosis**: Operation is consuming too much memory
**Solutions**:
- Process data in smaller chunks
- Use more memory-efficient data structures
- Stream data instead of loading all into memory
- Optimize algorithms to reduce memory footprint

### Issue: "No search results"

**Symptoms**: Search tool returns no matches
**Diagnosis**: Query is too specific or file doesn't exist
**Solutions**:
- Broaden search query
- Check spelling and terminology
- Try alternative search terms
- Search larger scope (full workspace vs. specific directory)

## Best Practices Summary

1. **Always validate inputs** before using tools
2. **Check outputs** to confirm tool operations succeeded
3. **Handle errors gracefully** with fallback strategies
4. **Stay within workspace boundaries** for all file operations
5. **Use appropriate tools** for each task (don't use exec for everything)
6. **Combine tools effectively** in multi-step workflows
7. **Document tool usage** for audit trail and debugging
8. **Respect resource limits** to prevent failures
9. **Cite external sources** when using web_search
10. **Test operations** with small datasets before scaling up

## Conclusion

These five tools—read, write, exec, search, and web_search—provide comprehensive capabilities for data analysis work within the NexaRetail workspace. By understanding each tool's capabilities, limitations, and best practices, the agent can effectively accomplish complex tasks while maintaining security, quality, and efficiency. Proper tool usage is fundamental to successful collaboration with the NexaRetail team.
