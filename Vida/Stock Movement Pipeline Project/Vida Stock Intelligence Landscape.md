---
title: Vida Stock Intelligence Landscape
date created: Tuesday, 23rd September 2025
date modified: Tuesday, 23rd September 2025
tags:
  - Vida
  - Database
  - Plan
  - Stock_Movement
  - SQL
  - SQ
aliases:
  - Database Intelligence Plan
  - Stock Movement Databas Setup Intel
---
-----

# 🧭Vida Stock Intelligence Landscape

What follows is a high-level strategic consolidation of the entire data terrain, organized by domain, source, and tactical function. This is the command center view — the vantage point from which we’ll architect the fortress.

## I. 🏪 Store Metadata & Identifier Reconciliation

Source Files

Role

Notes

VidaStoresCurrentDisgisticsNaming.xlsx<br>VidaOtherStoresDisgisticsNaming.xlsx<br>VidanNewStoresDisgisticsNaming.xlsx

Canonical store registry

Fragmented VID codes, inconsistent naming across Digistics and GAAP

COS workbook screenshot

Final reporting layer

Aggregates purchases, transfers, sales, closing stock, wastage

Strategic Objective: Normalize store identifiers, assign internal UUIDs, enable cross-system joins.

## II. 📦 Stock Item Registry & Metadata

Source Files

Role

Notes

VidaStockItemMatrixDigisticsInventoryWD.xlsx

Item registry

VE codes, GAAP codes, pack size, supplier, cost, status

Stock_Listing.xlsx

Store-level stock snapshot

Useful for retention logic and archival triggers

Strategic Objective: Build unified item_registry, reconcile VE/GAAP/PLU codes, enrich with metadata.

## III. 📅 Daily Operational Reports

Source Files

Domain

Notes

VidaPurchaseExportDaily.xlsx

Purchases

Supplier, item, quantity, cost

VidaTransferExportDaily.xlsx

Transfers

Inter-store movement

VidaWastageSummaryDaily.xlsx

Wastage

Loss tracking

VidaTurnoverPerStoreExcl.xlsx

Sales excl export

Revenue lens

VidaStockCostPriceVariance.xlsx

Cost drift

Price anomalies

Strategic Objective: Normalize ingestion, timestamped records, validate against recipes and GRVs.

## IV. 📆 Monthly Digistics Reports

Source Files

Domain

Notes

DigisticsSalesPerTransaction.xlsx

Transaction-level sales

Item-level breakdown

DigisticsSalesRands&CasesPerStore.xlsx

Volume/value reconciliation

Store-level consumption

Strategic Objective: Build monthly_sales_summary, validate against daily records, detect drift.

## V. 🧾 GRV & Supplier Compliance

Source Files

Domain

Notes

GRV per Supplier Export.xlsx

Goods received

Supplier, item, quantity, cost, store

Strategic Objective: Build grv_records, cross-check against purchases, score compliance.

## VI. 🍽️ Menu Items & Recipe Components

Source Files

Domain

Notes

Recipes_Menu_Items_min.xlsx

Menu registry

PLU codes, names, categories, prices

Recipe_Stock_Items_min.xlsx

Recipe components

Item codes, quantities, units, yield factors

Strategic Objective: Link menu items to stock items, model theoretical GP, validate consumption.

## VII. 🧮 COS Calculation Logic

Source Files

Domain

Notes

COS Base calculation sheets.xlsx

Formula logic

GP, shrinkage, theoretical vs actual cost, aggregation cadence

Strategic Objective: Reverse-engineer COS formulas into SQL/Python logic, validate reporting layer, automate GP overlays.

🧱 COS Summary View (Draft)

```sql
CREATE VIEW cos_summary AS
SELECT
  store_id,
  report_date,
  total_sales,
  total_purchases,
  total_transfers_in,
  total_transfers_out,
  total_wastage,
  closing_stock_value,
  theoretical_cost,
  actual_cost,
  gross_profit,
  gp_percentage,
  shrinkage_value,
  shrinkage_percentage
FROM ...
JOIN logic derived from COS base sheets
WHERE ...
```
This view will be powered by joins across:

purchases, transfers, sales_excl, wastage, closing_stock

menu_items, recipe_components

item_registry, store_registry 

🧱 ARCHITECTURAL STRATEGY

🔗 Core Tables

store_registry

item_registry

menu_items

recipe_components

purchases, transfers, wastage, sales, grv_records

monthly_sales_summary

cos_summary (output layer)

## ⚙️ ETL Principles

Modular, timestamped ingestion

Identifier reconciliation (VID, GAAP, VE, PLU)

Audit trails and anomaly flagging

Retention logic for archival (OneDrive cold layer)

## 📊 Analytical Views

COS reporting with theoretical overlays

GP modeling per store/item/day

Compliance dashboards

Pilferage and shrinkage detection

## 🧠 STRATEGIC OUTCOMES

Less time cleaning, more time analyzing

Operational truth across all stores

Anomaly detection that protects margin

Scalable architecture ready for automation and upgrades🧠 Strategic Outcomes

✅ COS reporting with theoretical overlays

✅ GP modeling per store/item/day

✅ Compliance dashboards

✅ Pilferage and shrinkage detection

✅ Retention logic for archival

✅ Automation-ready architecture

The war table is complete. The terrain is mapped. The sources are catalogued. The logic is visible.From here, we move into schema blueprinting, ETL design, and reporting layer construction.The schema is forming — when you're ready, we pour the first slab of your fortress.

Command center is online. Ready to break ground, Commander. Let’s build.

