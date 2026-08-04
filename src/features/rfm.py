"""RFM scoring for restaurant and bar guests.

Recency / Frequency / Monetary scoring is the workhorse segmentation for hospitality because
it only needs what every POS already has: a guest id, a check date, and a check total.

Hospitality-specific notes baked into this module:

* Recency is measured against the last operating day of the venue, not against today, so a
  venue that is closed on Mondays does not look like every guest suddenly lapsed.
* Frequency is counted in visits, not checks. Two checks opened for the same guest on the same
  service (tab moved from bar to table) is one visit.
* Monetary uses net sales excluding tax and tips, since tips are not revenue to the venue.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class RFMConfig:
    quantiles: int = 5
    visit_gap_hours: int = 6  # checks within this window collapse into one visit
    exclude_comped_checks: bool = True


def build_visits(checks: pd.DataFrame, config: RFMConfig = RFMConfig()) -> pd.DataFrame:
    """Collapse raw checks into guest visits.

    Expects columns: guest_id, opened_at, net_sales, is_comped.
    Returns one row per guest visit with the visit start time and total net sales.
    """
    raise NotImplementedError


def score_rfm(visits: pd.DataFrame, as_of: pd.Timestamp, config: RFMConfig = RFMConfig()) -> pd.DataFrame:
    """Return per-guest R, F, M raw values plus 1-5 scores and a combined segment label.

    Scores are computed with quantile bins inside the venue, never against an industry benchmark.
    A weekly guest at a wine bar and a weekly guest at a quick-service counter are both regulars,
    but their raw frequency numbers are nowhere near each other.
    """
    raise NotImplementedError


def label_segment(r: int, f: int, m: int) -> str:
    """Map an R/F/M triple to a plain-language segment an operator can act on.

    Intended labels: regular, lapsing regular, big spender, occasional, new, one-and-done, lost.
    The point of the plain language is that the marketing decision follows from the name.
    """
    raise NotImplementedError
