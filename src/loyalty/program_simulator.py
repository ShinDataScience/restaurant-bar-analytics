"""Loyalty program simulator.

Most loyalty programs in hospitality are designed by picking a round number (10 points per dollar,
free entree at 100 points) and hoping. This module replays a venue historical transactions against
a proposed program so the economics are known before anyone prints a punch card.

What the simulation answers:

* What would this program have cost last year in reward liability?
* How much of that liability would never be redeemed (breakage)?
* Which guests would have hit each tier, and how concentrated is the reward spend?
* What incremental visit lift is needed just to break even?

That last number is the important one. If a program needs a 12 percent visit lift to break even and
realistic programs deliver 3 to 5 percent, the design is wrong and no amount of marketing fixes it.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


@dataclass
class RewardTier:
    name: str
    threshold_points: int
    reward_description: str
    reward_retail_value: float
    reward_cost_to_venue: float  # true cost, not menu price


@dataclass
class ProgramDesign:
    points_per_dollar: float = 10.0
    points_expire_after_days: int | None = 365
    tiers: list[RewardTier] = field(default_factory=list)
    enrollment_rate: float = 0.35   # share of guests expected to join
    redemption_rate: float = 0.60   # share of earned rewards actually claimed


def simulate(checks: pd.DataFrame, design: ProgramDesign) -> dict:
    """Replay history against a program design.

    Expects columns: guest_id, business_date, net_sales, gross_margin.
    Returns a summary dict with total points issued, reward cost, breakage value, liability at
    period end, cost as a percent of sales, and the break-even incremental visit lift.
    """
    raise NotImplementedError


def tier_distribution(checks: pd.DataFrame, design: ProgramDesign) -> pd.DataFrame:
    """Show how many guests would land in each tier and what share of sales they represent.

    A healthy program has a top tier that is small in headcount but meaningful in sales. If the top
    tier holds 40 percent of guests, the thresholds are too low and rewards are being given away.
    """
    raise NotImplementedError


def breakeven_lift(summary: dict) -> float:
    """Incremental visit lift required for the program to pay for itself, as a decimal fraction."""
    raise NotImplementedError


def reward_efficiency(tiers: list[RewardTier]) -> pd.DataFrame:
    """Rank rewards by perceived value per dollar of real cost.

    A dessert with a 9 dollar menu price and 1.80 of food cost is a far better reward than 8 dollars
    off the check, even though the guest reads them as similar.
    """
    raise NotImplementedError
