"""Demand forecasting for covers, sales, and labor planning.

Forecasts here are deliberately at the daypart level rather than the day level. A manager does not
schedule a day, they schedule a shift, and a Saturday that is quiet at lunch and slammed at dinner
averages out to a perfectly ordinary and completely useless daily number.

Features that consistently earn their place in hospitality forecasts:

* Day of week and daypart, plus their interaction.
* Local weather: temperature, precipitation, and for patio venues, wind.
* Local event calendars: games, concerts, conventions, school schedules.
* Holidays, including the awkward ones like the Friday before a long weekend.
* Recent trend, which captures a new competitor opening or a review going viral.
* Marketing calendar, so a promotion driven spike is not learned as normal demand.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class ForecastConfig:
    horizon_days: int = 21
    granularity: str = "daypart"   # day or daypart
    include_weather: bool = True
    include_events: bool = True


def build_training_frame(checks: pd.DataFrame, config: ForecastConfig) -> pd.DataFrame:
    """Aggregate checks to the forecast grain and join external features."""
    raise NotImplementedError


def forecast_covers(training: pd.DataFrame, config: ForecastConfig) -> pd.DataFrame:
    """Forecast guest counts per daypart with prediction intervals.

    Intervals matter more than point estimates here. Scheduling to the midpoint of a wide interval
    is how venues end up either paying idle labor or wrecking service on a busy night.
    """
    raise NotImplementedError


def forecast_sales(training: pd.DataFrame, config: ForecastConfig) -> pd.DataFrame:
    """Forecast net sales per daypart, derived from covers times expected average check."""
    raise NotImplementedError


def labor_recommendation(forecast: pd.DataFrame, target_labor_pct: float = 0.28) -> pd.DataFrame:
    """Translate a sales forecast into recommended labor hours by role.

    Output is a recommendation, not a schedule. It leaves room for the judgment of whoever knows
    that a particular party of 20 always runs long.
    """
    raise NotImplementedError


def backtest(training: pd.DataFrame, config: ForecastConfig, folds: int = 4) -> pd.DataFrame:
    """Rolling-origin backtest reporting MAPE and interval coverage by daypart.

    A forecast that has never been backtested is a guess with extra steps.
    """
    raise NotImplementedError
