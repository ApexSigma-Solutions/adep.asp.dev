---
title: Reference Table Schemas for Transactional Joins
date created: Tuesday, 23rd September 2025
date modified: Tuesday, 23rd September 2025
tags:
  - Vida
  - Database
  - Table_Schema
  - Stock_Movement
  - SQL
  - SQLite
aliases:
  - Reference Table Schema
  - Schema for Transactional Joins
---
-----

# 🧱 Reference Table Schemas for Transactional Joins

This is the foundation for making the COS logic quarriable and auditable. Here's a proposed schema blueprint for the key reference tables and how they’ll support joins, indexing, and querying by working_date across the transactional layers:

## 1. store_registry

Column Name

Type

Description

store_id

UUID

Internal unique store identifier

store_name

TEXT

Canonical store name

vid_code

TEXT

Digistics store code

gaap_code

TEXT

GAAP store code

region

TEXT

Optional grouping for reporting

status

TEXT

Active/inactive flag

Indexes: store_id (PK), vid_code, gaap_code

## 2. item_registry

Column Name

Type

Description

item_id

UUID

Internal unique item identifier

ve_code

TEXT

Digistics item code

gaap_code

TEXT

GAAP item code

plu_code

TEXT

PLU code from recipe/menu

description

TEXT

Item name

pack_size

TEXT

Unit size

supplier

TEXT

Supplier name

status

TEXT

Active/inactive flag

Indexes: item_id (PK), ve_code, gaap_code, plu_code

## 3. menu_items

Column Name

Type

Description

plu_code

TEXT

PLU code

menu_name

TEXT

Item name

category

TEXT

Menu category

price

NUMERIC

Selling price

Indexes: plu_code (PK)

4. recipe_components

Column Name

Type

Description

plu_code

TEXT

Menu item PLU

item_id

UUID

Linked stock item

quantity

NUMERIC

Quantity used

unit

TEXT

Measurement unit

yield_factor

NUMERIC

Conversion factor

Indexes: plu_code, item_id

5. working_dates

Column Name

Type

Description

report_date

DATE

Calendar date

store_id

UUID

Store reference

day_of_week

TEXT

For trend analysis

month

TEXT

For monthly joins

is_month_end

BOOLEAN

Flag for monthly rollup logic

Indexes: report_date, store_id

These reference tables will act as the backbone for joining into transactional layers like purchases, sales, transfers, wastage, and closing_stock, all of which will be keyed by store_id, item_id, and report_date.

[[Vida Stock Intelligence Landscape]]
