# Schema Changelog

## Version History Overview

This document tracks all schema changes for the customer transaction database. The schema has evolved to support enhanced analytics capabilities and multi-channel transaction tracking. All changes are documented here with detailed migration notes and backward compatibility considerations.

## v2 (2025-03-07)

### Summary of Changes

Version 2 introduces significant enhancements to support omnichannel analytics. The primary addition is the `channel` field which enables business intelligence teams to analyze customer behavior across different transaction channels.

### New Fields

#### `channel` Column

- **Field Name**: `channel`
- **Data Type**: VARCHAR(20)
- **Nullable**: NO
- **Default Value**: None (must be specified)
- **Valid Values**:
  - `online` - Web-based transactions through the e-commerce platform
  - `in-store` - Physical retail location transactions
  - `mobile` - Mobile app transactions (iOS and Android)

**Business Justification**: The addition of the channel field was requested by the Analytics team on February 28, 2025, to enable cross-channel customer journey analysis. This field supports the Q2 2025 initiative to understand channel preference patterns and optimize the omnichannel customer experience.

**Implementation Details**: The channel field was added to all new transaction records starting March 7, 2025. Historical data (pre-v2) does not include this field, which creates a data completeness gap for historical channel analysis. The Data Engineering team is evaluating options for backfilling historical transactions based on payment method and device fingerprinting data.

### Fields Retained from v1

All fields from version 1 remain unchanged in version 2. There were **no field renames** in this version, maintaining full backward compatibility with existing queries and reporting tools.

- `transaction_id`: Unique transaction identifier (format: TXN-YYYYMMDD-XXXXXX)
- `customer_id`: Customer identifier linking to customer master table
- `date`: Transaction date (format varies - see Known Issues)
- `order_value`: Transaction amount in USD

### Schema Definition (v2)

```sql
CREATE TABLE transactions_v2 (
    transaction_id VARCHAR(30) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    date VARCHAR(20) NOT NULL,
    order_value DECIMAL(10,2) NOT NULL,
    channel VARCHAR(20) NOT NULL,
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    CONSTRAINT chk_channel CHECK (channel IN ('online', 'in-store', 'mobile'))
);
```

### Migration Notes

#### From v1 to v2

**Migration Date**: March 7, 2025
**Performed By**: Data Engineering Team (Lead: Sarah Chen)
**Downtime**: None (online schema evolution)

The migration from v1 to v2 was performed as an online schema change to avoid service disruption. The following steps were executed:

1. **Schema Alteration**: Added `channel` column to existing table
2. **Default Value Backfill**: Initially populated NULL values with 'online' as default (temporary measure)
3. **Application Update**: Updated transaction capture services to populate channel field
4. **Data Quality Check**: Validated channel distribution matches expected patterns
5. **NULL Cleanup**: Removed temporary default values and enforced NOT NULL constraint

**Post-Migration Validation**:
- Verified 100% channel field population for transactions after March 7, 2025 00:00:00 UTC
- Confirmed channel distribution: ~40% online, ~35% in-store, ~25% mobile (matches historical payment method distribution)
- Validated referential integrity with customer master table

#### Backward Compatibility

Version 2 maintains full backward compatibility with v1 queries as long as they do not explicitly reference the new `channel` field. Existing reporting dashboards and ETL pipelines that use `SELECT *` will automatically include the channel field, which may require updates to consuming applications.

**Recommended Actions for Consumers**:
- Update data models to include channel field
- Modify existing aggregations to group by channel where relevant
- Review and update unit tests that validate transaction record structure
- Update documentation and data dictionaries

### Breaking Changes

**None**. Version 2 is fully backward compatible. The addition of a new NOT NULL field only affects INSERT operations, not SELECT queries.

### Known Issues and Limitations

#### Date Format Inconsistency

Approximately 8% of transaction records in v2 use MM/DD/YYYY format instead of the standard YYYY-MM-DD format. This inconsistency was introduced during a system integration incident on March 12, 2025, when a legacy payment gateway was temporarily reactivated due to primary gateway maintenance.

**Impact**: Date parsing logic in consuming applications must handle both formats. Queries using direct string comparison or date range filters may produce incorrect results.

**Workaround**: Use robust date parsing functions (e.g., `STR_TO_DATE` with multiple format attempts, or application-level parsing with format detection).

**Resolution Status**: Data Engineering team has deprioritized cleanup due to Q1 2025 resource constraints. Planned for Q3 2025 data quality initiative.

#### Channel Validation

The channel field currently accepts only three predefined values. Future channel additions (e.g., 'partner', 'wholesale', 'api') will require schema changes and potential data migration.

**Design Decision**: Hard-coded CHECK constraint was chosen over lookup table for performance optimization. This decision may be revisited if channel types proliferate.

### Performance Impact

The addition of the channel field has minimal impact on query performance:

- **Index Strategy**: No additional indexes were created. Channel field is typically used in GROUP BY clauses rather than WHERE filters.
- **Storage Impact**: +20 bytes per record (VARCHAR(20) field)
- **Query Performance**: Aggregation queries grouping by channel show <5% performance degradation compared to v1 (measured on 10M record dataset)

### Data Quality Considerations

#### Channel Accuracy

Channel assignment is based on the transaction origination system:
- **Online**: Transactions from web application (identified by session source)
- **In-store**: Transactions from POS systems (identified by terminal ID prefix)
- **Mobile**: Transactions from mobile apps (identified by device ID pattern)

**Accuracy Rate**: 99.2% (validated through manual sampling, n=5000)

**Known Misclassification Scenarios**:
- Web-to-store transactions (buy online, pay in store) are classified as 'in-store'
- Mobile browser transactions may be misclassified as 'online' if user agent string is ambiguous
- Partner kiosk transactions are classified as 'in-store' (no distinct channel yet)

#### Data Completeness

- **v2 Records (post-March 7)**: 100% channel field population
- **v1 Records (pre-March 7)**: 0% channel field availability (field did not exist)
- **Transition Period (March 7, 00:00-02:00 UTC)**: 12% records missing channel data due to deployment rollout

### Analytics Use Cases

The channel field enables several new analytics capabilities:

1. **Channel Attribution Analysis**: Understand which channels drive the highest transaction value and customer lifetime value
2. **Cross-Channel Customer Journey**: Track customers who use multiple channels and identify conversion patterns
3. **Channel Performance Metrics**: Compare average order value, transaction frequency, and return rates across channels
4. **Channel Preference Segmentation**: Create customer segments based on channel usage patterns
5. **Operational Efficiency**: Analyze channel-specific cost structures and profitability

### Example Queries

#### Channel Distribution
```sql
SELECT
    channel,
    COUNT(*) as transaction_count,
    SUM(order_value) as total_value,
    AVG(order_value) as avg_order_value
FROM transactions_v2
WHERE date >= '2025-03-07'
GROUP BY channel
ORDER BY transaction_count DESC;
```

#### Customer Channel Preference
```sql
SELECT
    customer_id,
    channel,
    COUNT(*) as channel_usage_count,
    RANK() OVER (PARTITION BY customer_id ORDER BY COUNT(*) DESC) as channel_preference_rank
FROM transactions_v2
WHERE date >= '2025-03-07'
GROUP BY customer_id, channel;
```

#### Cross-Channel Customer Analysis
```sql
SELECT
    customer_id,
    COUNT(DISTINCT channel) as channels_used,
    SUM(order_value) as total_spend
FROM transactions_v2
WHERE date >= '2025-03-07'
GROUP BY customer_id
HAVING COUNT(DISTINCT channel) > 1
ORDER BY total_spend DESC;
```

### Testing and Validation

#### Test Coverage

The v2 schema was validated through comprehensive testing:

- **Unit Tests**: 47 test cases covering field validation, constraint enforcement, and data type validation
- **Integration Tests**: 23 test scenarios covering application-level transaction creation across all channels
- **Performance Tests**: Load testing with 1M concurrent transaction simulations (P95 latency: 45ms)
- **Data Quality Tests**: Automated validation of channel distribution, referential integrity, and format compliance

#### Test Results Summary

| Test Category | Pass Rate | Notes |
|--------------|-----------|-------|
| Schema Validation | 100% | All constraints properly enforced |
| Data Type Validation | 100% | Correct data types and precision |
| Referential Integrity | 100% | Foreign key constraints validated |
| Channel Constraint | 100% | Only valid channel values accepted |
| Date Format Validation | 92% | Known issue with 8% format inconsistency |
| Performance Benchmarks | 98% | Slight degradation in complex aggregations |

### Rollback Procedure

If issues arise with v2, the following rollback procedure can be executed:

1. **Stop Transaction Ingestion**: Pause new transaction writes
2. **Schema Rollback**: Drop `channel` column using `ALTER TABLE DROP COLUMN`
3. **Application Rollback**: Deploy v1 application code that does not reference channel
4. **Validation**: Verify v1 functionality and data integrity
5. **Resume Operations**: Re-enable transaction ingestion

**Estimated Rollback Time**: 30 minutes
**Data Loss Risk**: Minimal (channel data preserved in backups, can be restored)

### Future Enhancements

#### Planned for v3 (Q3 2025)

- Add `channel_subcategory` field to distinguish mobile app vs mobile web
- Implement channel attribution tracking for multi-touch journeys
- Add `channel_metadata` JSON field for extensible channel-specific attributes
- Create materialized view for channel performance metrics
- Add composite index on (date, channel) for optimized reporting queries

#### Under Consideration for v4

- Normalize channel data into separate channel_master table
- Add temporal validity tracking (effective_from, effective_to) for channel definitions
- Implement change data capture (CDC) for channel updates
- Add support for dynamic channel types without schema changes

## v1 (2024-11-15)

### Summary

Version 1 established the foundational transaction schema. This was the initial production release supporting basic transaction capture and reporting.

### Schema Definition (v1)

```sql
CREATE TABLE transactions_v1 (
    transaction_id VARCHAR(30) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    date VARCHAR(20) NOT NULL,
    order_value DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
```

### Field Definitions

#### `transaction_id`

- **Data Type**: VARCHAR(30)
- **Constraints**: PRIMARY KEY
- **Format**: TXN-YYYYMMDD-XXXXXX
- **Description**: Unique identifier for each transaction, combining date prefix and sequential number

#### `customer_id`

- **Data Type**: VARCHAR(20)
- **Constraints**: NOT NULL, FOREIGN KEY to customers table
- **Format**: CUST-XXXXX
- **Description**: References customer record in master customer table

#### `date`

- **Data Type**: VARCHAR(20)
- **Constraints**: NOT NULL
- **Format**: YYYY-MM-DD (intended, but not enforced)
- **Description**: Transaction date. Note: Format validation not enforced at schema level, leading to later format inconsistencies.

**Design Consideration**: VARCHAR was chosen over DATE type to accommodate edge cases in transaction date capture from various source systems. This decision later contributed to date format inconsistencies in v2.

#### `order_value`

- **Data Type**: DECIMAL(10,2)
- **Constraints**: NOT NULL
- **Format**: Up to 8 digits before decimal, 2 after
- **Description**: Transaction amount in USD. Currency conversion handled at application layer.

### Initial Deployment

**Deployment Date**: November 15, 2024
**Initial Load**: 2.3M historical transaction records migrated from legacy system
**Migration Duration**: 4 hours
**Validation**: 100% record count match, 99.7% data integrity validation

### v1 Known Issues

#### No Channel Tracking

Version 1 did not capture transaction channel information, limiting analytics capabilities. This was identified as a critical gap in Q4 2024 analytics review and drove the v2 enhancement.

#### Date Format Not Enforced

The use of VARCHAR(20) for date field without application-level format enforcement led to inconsistent date formats in the data. While most transactions used YYYY-MM-DD, approximately 3% of v1 transactions used alternative formats.

#### No Audit Trail

Version 1 did not include created_at, updated_at, or modified_by fields, limiting audit capabilities. This was acceptable for initial release but flagged for future enhancement.

### v1 Performance Characteristics

- **Average INSERT latency**: 12ms (P95: 18ms)
- **Average SELECT latency** (single record by PK): 2ms (P95: 5ms)
- **Complex aggregation queries** (30-day rolling sum by customer): 340ms (P95: 890ms)

### v1 to v2 Migration Lessons Learned

1. **Date Type Selection**: Should have used DATE type from beginning. VARCHAR provided no meaningful flexibility and introduced data quality issues.
2. **Extensibility**: Consider future enhancement needs during initial design. Adding channel field in v2 was straightforward but could have been anticipated.
3. **Testing**: More extensive testing of date format handling would have caught format inconsistency issues earlier.
4. **Documentation**: Initial documentation was sparse. Comprehensive changelog approach adopted in v2 proved valuable.

## Schema Evolution Principles

### Guiding Principles for Future Changes

1. **Backward Compatibility**: Prioritize non-breaking changes. When breaking changes are necessary, provide clear migration paths and adequate notice.
2. **Data Quality**: Enforce data quality constraints at schema level where possible (e.g., CHECK constraints, NOT NULL, data types).
3. **Performance**: Consider performance implications of schema changes. Add indexes strategically.
4. **Documentation**: Maintain comprehensive documentation of all changes, including business justification, technical implementation, and migration notes.
5. **Testing**: Require comprehensive test coverage for all schema changes before production deployment.
6. **Versioning**: Use clear version numbers. Major versions for breaking changes, minor versions for additive changes.

### Change Request Process

All schema changes must follow the established change request process:

1. **Proposal**: Submit RFC (Request for Comments) with business justification and technical design
2. **Review**: Data Architecture Board reviews and provides feedback
3. **Approval**: Requires sign-off from Data Engineering Lead, Analytics Lead, and Application Owner
4. **Implementation**: Data Engineering team implements with comprehensive testing
5. **Deployment**: Coordinated deployment with application updates and monitoring
6. **Validation**: Post-deployment validation and rollback readiness
7. **Documentation**: Update schema changelog and relevant documentation

### Change Categories

#### Non-Breaking Changes (Minor Version)

- Adding new nullable fields
- Adding new indexes
- Creating views
- Adding CHECK constraints that don't invalidate existing data
- Documentation updates

#### Breaking Changes (Major Version)

- Removing fields
- Renaming fields
- Changing data types (with few exceptions)
- Adding NOT NULL constraints to existing fields
- Changing constraint definitions

## Data Dictionary

### Complete Field Reference (v2)

| Field Name | Data Type | Nullable | Constraints | Description | Added in Version |
|------------|-----------|----------|-------------|-------------|------------------|
| transaction_id | VARCHAR(30) | NO | PRIMARY KEY | Unique transaction identifier | v1 |
| customer_id | VARCHAR(20) | NO | FOREIGN KEY | Customer identifier | v1 |
| date | VARCHAR(20) | NO | - | Transaction date (multiple formats) | v1 |
| order_value | DECIMAL(10,2) | NO | - | Transaction amount in USD | v1 |
| channel | VARCHAR(20) | NO | CHECK | Transaction channel (online, in-store, mobile) | v2 |

### Data Type Rationale

#### VARCHAR vs Specific Types

**VARCHAR(30) for transaction_id**: Chosen to accommodate format changes without schema migration. Transaction ID format is stable but potentially extensible.

**VARCHAR(20) for customer_id**: Allows for format evolution as customer identification systems change.

**VARCHAR(20) for date**: Originally chosen for flexibility across source systems. In retrospect, DATE type would have been better. Changing now would require major migration.

**VARCHAR(20) for channel**: Adequate for known channel types. Could have used ENUM but CHECK constraint provides similar functionality with more flexibility.

#### Numeric Precision

**DECIMAL(10,2) for order_value**: Supports transactions up to $99,999,999.99. Maximum observed transaction: $45,230.50. Precision chosen to support potential enterprise/wholesale transactions.

## Appendix

### Related Documentation

- **Data Architecture Standards**: `/docs/data-architecture/standards.md`
- **Database Change Management Process**: `/docs/processes/database-change-management.md`
- **Transaction Data Model**: `/docs/data-models/transaction-model.md`
- **ETL Pipeline Documentation**: `/docs/etl/transaction-ingestion.md`

### Contact Information

- **Data Engineering Team**: data-eng@company.com
- **Schema Change Requests**: schema-changes@company.com
- **Data Architecture Board**: data-arch-board@company.com

### Revision History

| Date | Author | Changes |
|------|--------|---------|
| 2025-03-07 | Sarah Chen | Added v2 schema documentation with channel field details |
| 2025-03-08 | Sarah Chen | Updated known issues section with date format inconsistency |
| 2025-03-10 | Michael Roberts | Added migration notes and rollback procedure |
| 2025-03-12 | Sarah Chen | Updated data quality metrics and analytics use cases |
| 2024-11-15 | David Kim | Initial v1 schema documentation |
| 2024-11-20 | David Kim | Added performance characteristics and deployment notes |

### Glossary

- **Channel**: The method/platform through which a customer completes a transaction
- **Transaction**: A completed purchase or order captured in the system
- **Schema Version**: A numbered iteration of the database schema with specific field definitions
- **Migration**: The process of moving from one schema version to another
- **Backward Compatibility**: Ability of new schema to work with existing queries/code
- **Data Quality**: Accuracy, completeness, consistency, and validity of data
- **Referential Integrity**: Consistency of relationships between tables (foreign keys)
- **CDC (Change Data Capture)**: Technique for tracking and propagating data changes
- **ETL (Extract, Transform, Load)**: Process of moving data from sources to data warehouse

### FAQ

**Q: Why wasn't the date field corrected in v2?**
A: Fixing the date format inconsistency would require a data migration of all historical records. Given resource constraints and the availability of workarounds, this was deprioritized in favor of new feature development. The date format cleanup is scheduled for Q3 2025.

**Q: Can I add custom channel types?**
A: No, the current CHECK constraint limits channel to 'online', 'in-store', and 'mobile'. Adding new channel types requires a schema change. If you have a need for additional channel types, submit a schema change request.

**Q: Is channel data available for historical (pre-v2) transactions?**
A: No, the channel field was added in v2 and only applies to transactions from March 7, 2025 onwards. Historical backfilling is under consideration but not yet scheduled.

**Q: What happens if I try to insert a transaction without a channel value?**
A: The NOT NULL constraint will cause the INSERT to fail. All transactions must specify a valid channel value.

**Q: Are there any performance indexes on the channel field?**
A: No dedicated indexes currently exist on the channel field. Most queries group by channel rather than filter by it, so index benefits would be limited. Index strategy is reviewed quarterly.

**Q: How do I handle the date format inconsistency in my queries?**
A: Use robust date parsing functions that can handle multiple formats, or convert dates at the application layer. Example: `STR_TO_DATE(date, '%Y-%m-%d')` with error handling for alternative formats.

**Q: Will v3 introduce breaking changes?**
A: Current v3 plans focus on additive changes (new fields, indexes) without breaking existing functionality. Any breaking changes would be clearly communicated with migration support.

**Q: How are mobile web vs mobile app transactions distinguished?**
A: Currently, both are classified as 'mobile' channel. Detailed distinction (mobile app vs mobile web) is planned for v3 using the proposed `channel_subcategory` field.

**Q: What's the process for proposing a schema change?**
A: Submit an RFC (Request for Comments) to the Data Architecture Board with business justification, technical design, and impact analysis. See Database Change Management Process documentation for details.

**Q: Are there any regulatory/compliance considerations for the transaction schema?**
A: Transaction data is subject to PCI DSS requirements (payment card data security). The schema itself does not store sensitive payment information (card numbers, CVV, etc.) which are managed in a separate secured system. Audit and retention requirements are documented separately.

---

**Document Version**: 2.1
**Last Updated**: March 12, 2025
**Next Review**: June 1, 2025
**Owner**: Data Engineering Team