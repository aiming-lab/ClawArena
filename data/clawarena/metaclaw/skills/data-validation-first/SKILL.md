---
name: data-validation-first
description: Use this skill before any data analysis, transformation, or modeling. Always inspect and validate the data before drawing conclusions or writing transformations.
category: data_analysis
---

# Data Validation First

Before writing any analysis code, understand the data:

```python
# Always run these first
df.shape          # rows x columns
df.dtypes         # column types
df.isnull().sum() # missing values per column
df.describe()     # statistics for numeric columns
df.head()         # sample rows
```

**Key questions:**
- Are there nulls in columns you'll join or filter on?
- Are numeric columns stored as strings? (parse_dates, astype)
- Are there unexpected duplicates (check primary key uniqueness)?
- Does the row count match your expectation from the source?

**Anti-pattern:** Running `.groupby().sum()` without first checking for nulls in the groupby key.
