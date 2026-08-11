# restaurant-bar-analytics

A data analytics project for restaurants and bars. The goal is narrow and practical: turn the data a
venue already generates into decisions about marketing spend, loyalty program design, menu pricing,
and staffing.

Most hospitality analytics fails for the same reasons every time. The numbers arrive too late, they
describe what happened instead of what to do, and they are measured without a control group so every
promotion looks like a success. This project is organized around avoiding those three failures.

## What it is meant to answer

**Guests.** Who are the regulars, who is quietly lapsing, and what share of revenue rides on the top
slice of guests? Segmentation is done inside a venue, never against an industry benchmark, because a
weekly guest at a wine bar and a weekly guest at a lunch counter are both regulars with wildly
different raw numbers.

**Loyalty.** What does a proposed program actually cost, how much of the reward liability never gets
redeemed, and what visit lift is required just to break even? The simulator replays historical
transactions against a program design so the economics are known before anything is printed. Program
impact is measured against a matched control group, since enrolled-versus-not comparisons flatter
every program ever launched.

**Marketing.** Which campaigns beat their holdout, which channels earn their cost, and which offers
move behavior instead of discounting guests who were already on their way in. Every send carries a
randomized holdout, decided before the campaign runs.

**Menu and pricing.** Which items are stars, plowhorses, puzzles, or dogs, how sensitive each is to
price, and what sells together. Beverage margin gets the same treatment as food, because that is
usually where the money is.

**Demand.** Covers and sales forecast by daypart, with intervals, feeding labor and prep planning.
Weather, local events, and holiday calendars are features, not excuses after the fact.

## Repository layout

    data/           gitignored working data, plus schema and handling rules
    sql/            canonical views over POS data
    src/
      data/         POS ingestion and normalization across Toast, Square, Clover, Lightspeed, Brink, PixelPoint, Tabit
                    plus report-only ingestion, capability gating, and optional extractors
      features/     RFM and guest feature construction
      models/       customer lifetime value
      loyalty/      program simulator and reward economics
      marketing/    campaign lift, holdouts, cannibalization
      menu/         menu engineering, elasticity, basket affinity
      forecasting/  covers and sales forecasting, labor recommendations
    notebooks/      exploration, promoted into src/ once it needs to run on a schedule
    dashboards/     Streamlit app aimed at a GM with ten minutes before service
    tests/          behavior that is easy to get wrong and easy to regress
    docs/           roadmap and metric definitions

## What data this needs

The ideal input is transaction level: one row per check with a timestamp and a guest id where one
exists, one row per item sold, and plate or pour costs from a recipe sheet, since no POS knows what
an item costs to make. That unlocks everything described above.

Most independent venues cannot produce it. POS API access usually sits behind a partner tier, or
nobody on site has the back office login. What they can almost always send is canned reports: a
daily sales summary, a product mix report, hourly sales, labor, and comps. Those load through
`src/data/aggregate_ingest.py` into coarser tables, and `src/data/capabilities.py` decides what may
be computed from them. Forecasting, labor planning, menu engineering, mix shift and cost control all
survive that downgrade. Guest analytics do not: RFM, CLV, loyalty economics and campaign lift are
withheld with a reason rather than estimated, because a segment built without guest ids is not a
rougher segment, it is a fictional one. See docs/METRICS.md for the full breakdown by tier.

Worth asking before settling for reports: loyalty platforms and reservation systems often export
guest and visit history as CSV even when the POS API is shut, which recovers a real part of the
guest picture.

CSV and Excel are the supported formats. PDF report parsing is an optional addon in
`src/data/extractors/`, kept behind its own dependencies, its own confidence scoring, and a review
queue, so a parsing guess can never quietly become a reported number.

## Getting started

    git clone https://github.com/ShinDataScience/restaurant-bar-analytics.git
    cd restaurant-bar-analytics
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt

The modules are currently interface-first: signatures, docstrings, and tests that describe intended
behavior, with implementations to follow in the order laid out in docs/ROADMAP.md.

## Principles

1. **Measure against a control.** No holdout, no claimed lift.
2. **Report uncertainty.** Small venues have small samples. A model that hides that gives confident
   bad advice, which is worse than no advice.
3. **Define terms once.** Average check, covers, and net sales are defined in docs/METRICS.md and
   nowhere else.
4. **Every output implies an action.** If an analysis does not change what someone does on Monday,
   it is not finished.
5. **Guest data stays minimal.** Contact identifiers are hashed at ingestion. No raw PII in the repo.

## Status

Early scaffolding. Structure, metric definitions, and roadmap are in place; implementations are next.

## License

MIT. See LICENSE.
