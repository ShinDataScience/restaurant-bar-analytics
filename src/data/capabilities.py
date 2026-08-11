"""Which analyses the data on hand can honestly support.

This project can be fed anything from a full transaction level POS export with guest ids down to a
folder of emailed daily sales reports. Those are not the same product, and the difference is not a
detail to be smoothed over in a dashboard. An RFM segment built on data with no guest ids is not a
worse segment, it is a fictional one.

So the rule is: analyses declare the grain they need, this module reports the grain that is
actually present, and anything unsupported is withheld with a reason a GM can read. Withheld is a
result. Fabricated is not.

Tiers, in descending order of what they unlock:

* transaction_identified - check level data with guest ids. Everything runs.
* transaction_anonymous  - check level data, no guest ids. Menu, basket, elasticity and forecasting
                           run. Guest analytics do not exist at this tier.
* aggregate              - daily and period report data only. Forecasting, menu engineering from
                           product mix, mix shift and cost control run. Nothing guest level does.
* insufficient           - not enough history or too many gaps to say anything defensible.

Worth checking before settling for the aggregate tier: guest level data often exists outside the
POS. Loyalty platforms and reservation systems usually export guest and visit history as CSV even
when the POS API is closed, and joining that to sales_daily recovers a real share of the guest
analytics.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

TIERS = ("transaction_identified", "transaction_anonymous", "aggregate", "insufficient")

# Below this much history, seasonality is guesswork and a forecast should not be shown to anyone.
MIN_DAYS_FOR_FORECAST = 180

# Below this identified share, guest level output describes so little of the business that leading
# with it misleads more than it informs.
MIN_IDENTIFIED_SHARE = 0.05

# Below this many repeat guests, fit the heuristic CLV instead of the probabilistic model.
MIN_REPEAT_GUESTS_FOR_PROBABILISTIC_CLV = 300

# The lowest tier each analysis can run on.
ANALYSIS_REQUIREMENTS = {
    "rfm_segmentation": "transaction_identified",
    "clv": "transaction_identified",
    "retention_cohorts": "transaction_identified",
    "loyalty_simulation": "transaction_identified",
    "campaign_lift": "transaction_identified",
    "cannibalization": "transaction_identified",
    "basket_affinity": "transaction_anonymous",
    "average_check": "transaction_anonymous",
    "menu_engineering": "aggregate",
    "menu_mix_shift": "aggregate",
    "price_elasticity": "aggregate",
    "demand_forecast": "aggregate",
    "labor_recommendation": "aggregate",
    "discount_leakage": "aggregate",
}


@dataclass(frozen=True)
class Capability:
    """One verdict about one analysis, written to be shown in the dashboard as is."""

    analysis: str
    available: bool
    tier_required: str
    tier_present: str
    reason: str                 # plain language, written for an operator, not for a stack trace
    caveat: str | None = None   # shown next to results that run but are weakened


def detect_tier(tables: dict[str, pd.DataFrame]) -> str:
    """Work out which tier the loaded tables actually support.

    Presence of a table is not enough. A checks table where guest_id is null on 99 percent of rows
    is transaction_anonymous, not transaction_identified, whatever the schema says.
    """
    raise NotImplementedError


def identified_share(checks: pd.DataFrame) -> float:
    """Share of checks tied to a known guest. Every guest level output is read next to this."""
    raise NotImplementedError


def history_days(tables: dict[str, pd.DataFrame]) -> int:
    """Length of usable history in business days, counting only days the venue was open."""
    raise NotImplementedError


def assess(tables: dict[str, pd.DataFrame]) -> list[Capability]:
    """Return one Capability per known analysis, with a reason for anything withheld.

    Reasons are written for the person who can fix them. "No guest ids in this export, ask whether
    the loyalty platform can export visit history" is actionable. "Missing column guest_id" is not.
    """
    raise NotImplementedError


def degraded_alternatives(analysis: str, tier: str) -> list[str]:
    """Suggest what can be run instead when the requested analysis is out of reach.

    Campaign measurement is the useful example. With no guest ids there is no holdout and therefore
    no lift, but an interrupted time series against the demand forecast still says something,
    provided it is labelled directional and carries its interval.
    """
    raise NotImplementedError


def require(analysis: str, tables: dict[str, pd.DataFrame]) -> None:
    """Raise if an analysis is run against data that cannot support it.

    Called at the top of each analysis entry point so an unsupported combination fails at the
    boundary, rather than three joins later with a plausible looking empty frame.
    """
    raise NotImplementedError


def summary_for_operator(capabilities: list[Capability]) -> pd.DataFrame:
    """One table: what this venue can be told today, and what data would unlock the rest.

    The second column is the point. A venue that learns a product mix export would unlock menu
    engineering will usually go and get one.
    """
    raise NotImplementedError
