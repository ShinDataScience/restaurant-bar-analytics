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
