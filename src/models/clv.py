"""Customer lifetime value for hospitality.

Hospitality CLV has two awkward properties compared to e-commerce:

1. Most guests are anonymous. Only loyalty members, reservation holders and card-linked repeat
   visitors can be tracked, so any CLV number describes the identified subset and must be labeled
   that way. Reporting identified-guest CLV as if it were all guests is a common and expensive error.
2. Visit patterns are strongly seasonal and weather-driven, so a naive model reads a slow February
   as churn.

Two model tiers are provided. The probabilistic tier (BG/NBD plus Gamma-Gamma) is the right answer
when there are enough repeat guests. The heuristic tier is for small venues where a 200-guest sample
cannot support a fitted model, and pretending otherwise produces confident nonsense.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class CLVResult:
    guest_id: str
    expected_visits_next_year: float
    expected_spend_per_visit: float
    expected_margin_next_year: float
    probability_alive: float
    confidence: str  # high, medium, low - driven by how much history the guest has


def fit_probabilistic(visits: pd.DataFrame, discount_rate: float = 0.10) -> pd.DataFrame:
    """Fit BG/NBD for visit frequency and Gamma-Gamma for spend, then combine into CLV.

    Requires a reasonable population of repeat guests. Returns per-guest CLV with a probability
    that the guest is still active.
    """
    raise NotImplementedError


def heuristic_clv(visits: pd.DataFrame, horizon_months: int = 12) -> pd.DataFrame:
    """Simple, transparent CLV: observed visit rate times average margin times horizon.

    Less accurate than the fitted model, but an operator can check it by hand, which matters more
    than the last few points of accuracy when the goal is a decision about a mailing list.
    """
    raise NotImplementedError


def value_tiers(clv: pd.DataFrame, tiers: int = 4) -> pd.DataFrame:
    """Bucket guests into value tiers and report what share of revenue each tier represents.

    The usual finding in hospitality is that the top 10 to 20 percent of identified guests drive
    a very large share of revenue, which is the entire argument for a loyalty program.
    """
    raise NotImplementedError


def coverage_report(checks: pd.DataFrame) -> dict:
    """Report what share of checks and sales are tied to an identified guest.

    Every CLV output should be read next to this number. If identification covers 18 percent of
    checks, CLV describes 18 percent of the business.
    """
    raise NotImplementedError
