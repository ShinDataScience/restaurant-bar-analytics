# Data directory

No guest data is committed to this repository. Ever. This directory defines structure and
expectations; everything inside it except documentation is gitignored.

## Layout

    data/
      raw/         POS, reservation, loyalty and marketing exports exactly as received
      interim/     parsed but not yet conformed to the canonical schema
      processed/   canonical tables ready for analysis
      external/    weather, local events, holiday calendars, trade-area data

## Rules

1. Raw is immutable. If an export was wrong, request a new one and keep both with load timestamps.
2. No personally identifying guest data lands in processed tables. Email and phone are hashed at
   ingestion, and the salt lives in the environment, not in the repo.
3. Every raw file is paired with a metadata note: source system, venue, date range, extraction
   date, and who pulled it.
4. Processed tables are rebuildable from raw with one command. If a table can only be reproduced
   by remembering what someone did in a spreadsheet, it does not belong here.

## Canonical tables

| Table | Grain | Notes |
| --- | --- | --- |
| venues | one row per venue | hours, daypart definitions, seat count, concept type |
| checks | one row per closed check | business date, daypart, channel, net sales, margin |
| check_items | one row per item sold | category, modifiers, quantity, price, item cost |
| guests | one row per identified guest | hashed identifiers, first seen, opt-in status |
| loyalty_events | one row per earn or redeem | points, tier, reward, liability impact |
| campaigns | one row per send | audience, holdout flag, offer, cost |
| external_daily | one row per venue per day | weather, events, holiday flags |

## Aggregate tables

Not every venue can give up transaction level data. Where POS API access is not available, the
reports a venue can already export land in these coarser tables instead, built by
`src/data/aggregate_ingest.py`. They are canonical in their own right, not a staging area, and
`src/data/capabilities.py` decides which analyses are allowed to run on them.

| Table | Grain | Notes |
| --- | --- | --- |
| sales_daily | one row per venue, business date and daypart | covers, checks, net sales, comps, discounts; daypart null when only day grain is available |
| item_sales_period | one row per venue, period and item | from the product mix report; costs joined from the operator costing sheet, never inferred |
| labor_daily | one row per venue, business date, daypart and role | hours and cost, for labor percent and scheduling |

## Report drops

Venues without API access send files, usually on a schedule, usually by email. Those land under
`raw/` in a predictable shape so a load never has to guess what it is looking at.

    raw/
        <venue_id>/
            <source>/                  toast, square, clover, lightspeed, brink, pixelpoint, tabit
                daily_sales_summary/
                product_mix/
                hourly_sales/
                labor_summary/
                discount_comp/
                tender_summary/

CSV and Excel are the supported formats. PDF is handled only by the optional addon in
`src/data/extractors/`, which attaches a confidence score and routes anything doubtful to a review
queue rather than into these tables.

The metadata note rule above applies here too, and matters more: a report file carries no venue id,
no timezone and often no year, so the note is the only thing that says what the numbers describe.
Every drop is paired with source system, venue, report type, date range, extraction date, and who
pulled it. Two reports covering the same period must agree within tolerance or the load is rejected.
