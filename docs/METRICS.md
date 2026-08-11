# Metric definitions

Half the arguments in a restaurant back office are definitional. Two people compare average check
and get different numbers because one included tax and the other did not. These definitions are
the contract for this project.

## Sales and check metrics

| Metric | Definition | Common mistake |
| --- | --- | --- |
| Net sales | Item revenue after discounts, excluding tax, tip, and service charges | Including tips, which are not venue revenue |
| Average check | Net sales divided by closed checks | Mixing split checks in with whole-party checks |
| Per person average | Net sales divided by covers | Using check count when parties vary in size |
| Contribution margin | Menu price minus item cost | Using gross margin percent from the P and L instead of item-level cost |
| Comp rate | Comped value divided by gross sales | Treating comps as marketing spend without tracking why |

## Guest metrics

| Metric | Definition | Note |
| --- | --- | --- |
| Visit | All checks for one guest at one venue within a 6 hour window | Handles bar-to-table tab moves |
| Recency | Days between last visit and the last operating day | Not calendar days, so closed days do not count against the guest |
| Frequency | Visits in the trailing 12 months | Venue-relative, never benchmarked across concepts |
| Identified share | Share of checks tied to a known guest | Every guest-level number should be read next to this |
| Repeat rate | Share of first-time guests who return within 90 days | The single best early health signal for a new venue |
| CLV | Expected gross margin from a guest over 12 months | Reported with a confidence label |

## Loyalty metrics

| Metric | Definition | Note |
| --- | --- | --- |
| Enrollment rate | Enrolled guests divided by identified guests | Rising enrollment with flat visits is a vanity metric |
| Breakage | Earned rewards never redeemed | Real money, but never budget as if it is guaranteed |
| Liability | Value of outstanding unredeemed rewards | Belongs on the books, not just in the dashboard |
| Incremental lift | Treated minus holdout, on visits and net sales | Without a holdout this metric does not exist |
| Program ROI | Incremental margin minus reward cost, divided by reward cost | Must use incremental margin, not total member spend |

## Marketing metrics

| Metric | Definition | Note |
| --- | --- | --- |
| Reach | Deliverable audience for a send | Not list size, which quietly rots |
| Redemption rate | Redemptions divided by delivered | Popular and nearly meaningless on its own |
| Incremental visits | Treated visits minus holdout visits, scaled | The number that decides whether to run it again |
| Cannibalization | Share of promo volume shifted from a visit that would have happened anyway | The reason discount programs disappoint |
| Cost per incremental visit | Total campaign cost divided by incremental visits | Compare against contribution margin per visit |

## Operations metrics

| Metric | Definition | Note |
| --- | --- | --- |
| Covers | Guests served | Party size from POS or reservation system, not seat turns |
| Seat turns | Covers divided by seats, per daypart | Meaningless without daypart split |
| Forecast MAPE | Mean absolute percent error on covers | Tracked by daypart, since dinner and lunch behave differently |
| Labor percent | Labor cost divided by net sales | Forecast-driven scheduling is judged on this and on service quality together |

## Metric availability by data tier

The definitions above do not change with the data source. What changes is whether a metric can be
computed at all. A venue sending emailed daily reports is not getting a slightly worse version of
guest analytics, it is getting none, and saying so plainly is the difference between a tool an
operator trusts and one they quietly stop opening. `src/data/capabilities.py` enforces this.

| Metric | Transaction with guest ids | Transaction, anonymous | Aggregate reports only |
| --- | --- | --- | --- |
| Net sales | yes | yes | yes |
| Average check | yes | yes | yes, if the report gives check counts |
| Per person average | yes | yes | only if the report gives covers |
| Covers | yes | yes | only if the report gives covers |
| Contribution margin | yes | yes | yes, with a costing sheet |
| Comp rate | yes | yes | yes, from the discount and comp report |
| Labor percent | yes | yes | yes, with a labor report |
| Forecast MAPE | yes | yes | yes |
| Seat turns | yes | yes | only at day grain without an hourly report |
| Identified share | yes | zero by definition | not applicable |
| Recency, Frequency, CLV | yes | no | no |
| Repeat rate | yes | no | no |
| Enrollment, breakage, liability | yes | no | no |
| Incremental lift and ROI | yes | no | no |
| Cannibalization | yes | no | no |

Two notes that matter more than the table.

Covers are the field most often missing from a summary report, and the temptation is to divide net
sales by an assumed average check to recover them. That produces a per person average which is a
restatement of the assumption, so covers stay null instead and the metric is withheld.

Campaign measurement has no aggregate equivalent. Incremental lift is defined against a holdout, and
a holdout requires knowing who was sent what. Where that does not exist, the honest substitute is an
interrupted time series against the demand forecast, reported as directional with its interval, and
it is never labelled lift.
