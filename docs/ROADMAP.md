# Project Roadmap

This roadmap breaks the project into phases. Each phase produces something usable on its own, so an
operator gets value early instead of waiting for a whole platform to be finished.

## Phase 1 - Foundations

- Define the questions that actually matter to an operator: who are my best guests, which promotions
  paid for themselves, which menu items carry the margin, and when do I need more staff on the floor.
- Build connectors for common sources: POS exports (Toast, Square, Clover, Lightspeed), reservation
  systems (OpenTable, Resy, SevenRooms), delivery marketplaces, and loyalty/CRM exports.
- Land raw extracts in data/raw, keep them immutable, and version the schema contracts.
- Standardize into a shared transaction model: check header, line items, guest, employee, venue,
  daypart, tender, discount, and channel.

## Phase 2 - Core guest analytics

- RFM scoring and segmentation (regulars, lapsing regulars, weekend-only, high-spend occasional).
- Cohort retention curves by acquisition month, channel, and first-visit daypart.
- Customer lifetime value with BG/NBD plus Gamma-Gamma, and a simpler heuristic CLV for small venues.
- Lapse prediction tuned per venue type, since a neighborhood bar and a special-occasion restaurant
  have very different definitions of a normal gap between visits.

## Phase 3 - Loyalty program design and evaluation

- Program simulator: model points-per-dollar, tier thresholds, and reward costs against historical
  transactions to estimate breakage, liability, and incremental spend before launching anything.
- Incrementality measurement using matched control groups rather than enrolled-vs-not comparisons,
  which overstate program impact because heavy users self-select into loyalty.
- Margin-aware reward selection, so the comped item has high perceived value and low food cost.
- Tier migration analysis: who is close to the next tier, and what nudge moves them.

## Phase 4 - Marketing measurement and targeting

- Campaign attribution across email, SMS, push, paid social, and third-party marketplaces.
- Offer targeting: match segment to offer type (win-back, frequency builder, check-size builder,
  off-peak filler) with a holdout group baked into every send.
- Uplift modeling so discounts go to guests whose behavior actually changes, not to guests who were
  coming anyway.
- Creative and channel testing framework with proper sample sizing.

## Phase 5 - Menu, pricing, and operations

- Menu engineering matrix (popularity vs contribution margin) with plate-cost integration.
- Price elasticity by item and daypart, including anchor and decoy effects.
- Market-basket analysis to find attachment opportunities, such as which appetizer drives a second round.
- Demand forecasting for covers and sales by daypart, feeding labor scheduling and prep planning,
  with weather, local events, and holiday calendars as features.

## Phase 6 - Delivery and adoption

- Streamlit dashboard with a weekly one-page summary for operators.
- Scheduled refresh jobs and data quality checks that fail loudly.
- Playbooks in docs/ that translate each analysis into an action a manager can take Monday morning.

## Guardrails

- Guest data stays minimized and hashed where possible. No raw PII in the repository, ever.
- Every recommendation ships with an estimate of uncertainty. Small venues have small samples, and a
  model that ignores that will confidently give bad advice.
- Analyses are reproducible: same input, same output, no manual spreadsheet steps.
