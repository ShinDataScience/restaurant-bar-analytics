"""Marketing campaign measurement.

The default way venues measure a promotion is to compare sales on promo days to sales on other days.
That comparison is almost always wrong: promotions run on days that were already going to be
different, and the guests who redeem are the guests who were already coming.

This module measures lift the boring, defensible way:

* Every send gets a randomized holdout group, decided before the campaign runs.
* Lift is measured on incremental net sales and incremental visits, not on redemption count.
* Results are reported with a confidence interval, and campaigns that cannot clear the noise floor
  are reported as inconclusive rather than as a win.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class Campaign:
    campaign_id: str
    channel: str            # email, sms, push, paid_social, marketplace, direct_mail
    offer_type: str         # win_back, frequency, check_size, off_peak, new_item_trial
    discount_cost: float    # expected cost per redemption to the venue
    sent_at: pd.Timestamp
    measurement_window_days: int = 30


def assign_holdout(audience: pd.DataFrame, holdout_share: float = 0.10, seed: int = 42) -> pd.DataFrame:
    """Randomly hold back part of the audience so the campaign can be measured at all.

    Stratified by RFM segment, because a simple random split on a small list can easily put most
    of the regulars on one side.
    """
    raise NotImplementedError


def measure_lift(campaign: Campaign, audience: pd.DataFrame, checks: pd.DataFrame) -> dict:
    """Compare treated vs holdout on visits and net sales over the measurement window.

    Returns incremental visits, incremental net sales, incremental margin after discount cost,
    ROI, and a confidence interval for each.
    """
    raise NotImplementedError


def cannibalization_check(campaign: Campaign, checks: pd.DataFrame) -> dict:
    """Estimate how much of the promo volume was pulled from visits that would have happened anyway.

    A Tuesday happy hour that simply moves Friday regulars to Tuesday has not created demand,
    it has discounted it.
    """
    raise NotImplementedError


def channel_summary(results: list[dict]) -> pd.DataFrame:
    """Roll campaign results up by channel and offer type to show what is worth repeating."""
    raise NotImplementedError
