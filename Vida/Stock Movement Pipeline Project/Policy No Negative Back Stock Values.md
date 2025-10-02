---
title: "Policy: No Negative Back Stock Values"
date created: Tuesday, 23rd September 2025
date modified: Tuesday, 23rd September 2025
tags:
  - SQLite
  - PolicyAsCode
  - Vida
  - Database
  - Stock_Movement
aliases:
  - '"Database Negative Stock Policy"'
  - '"Stock Movement Databas Setup"'
---
-----
# Policy: No Negative Back Stock Values

Any closing_quantity or closing_value that is negative will be zeroed during ingestion or transformation. The original value will be retained in an audit log for traceability.

🧱 Schema Update: closing_stock

Add a new column to preserve the raw value:

```sql
ALTER TABLE closing_stock
ADD COLUMN raw_closing_quantity REAL;
```

Then update your ETL logic to:

Ingest raw_closing_quantity from source file

## Apply rule:

closing_quantity = CASE WHEN raw_closing_quantity < 0 THEN 0 ELSE raw_closing_quantity END

Log anomalies in etl_audit_log or anomaly_flags:

```sql
INSERT INTO anomaly_flags (
  store_id,
  item_id,
  report_date,
  anomaly_type,
  severity,
  notes
)
SELECT
  store_id,
  item_id,
  report_date,
  'Negative Closing Stock',
  'Medium',
  CONCAT('Raw value: ', raw_closing_quantity)
FROM closing_stock
WHERE raw_closing_quantity < 0;
```

🧠 Strategic Benefits

✅ Prevents distortion in COS and GP calculations

✅ Preserves original values for forensic review

✅ Enables alerting and escalation for operational errors

✅ Maintains trust and transparency in reporting

This rule will be embedded directly into your ETL pipeline and schema logic. It’s not just a fix — it’s a safeguard. Let me know if you’d like to extend this to other domains (e.g. purchases, wastage) or apply thresholds for alerting.

[[Vida Stock Movement Analysis Project (Comprehensive)]]
[[Reference Table Schemas for Transactional Joins]]
[[Vida Stock Intelligence Landscape]]
