"""Menu engineering, pricing, and basket analysis.

Menu engineering classifies every item on two axes: how often it sells (popularity) and how much
contribution margin it earns. The four quadrants have traditional names, and each one implies a
different action:

* Stars     - popular and profitable. Protect them. Do not touch the recipe or the price casually.
* Plowhorses- popular but thin margin. Re-cost, re-portion, or raise price slightly.
* Puzzles   - profitable but slow. Re-describe, re-position on the menu, or train staff to sell it.
* Dogs      - slow and thin. Remove, unless it exists for a reason (the one vegan entree, the
              cheap beer that anchors the price list).

Bars need the same treatment applied by pour cost, and beverage margins are usually where the
money actually is. A cocktail program with a 22 percent pour cost subsidizes a lot of kitchen.
"""

from __future__ import annotations

import pandas as pd

QUADRANTS = ("star", "plowhorse", "puzzle", "dog")


def contribution_margin(items: pd.DataFrame) -> pd.DataFrame:
    """Add contribution margin per item: menu price minus plate or pour cost.

    Expects columns: item_id, menu_price, item_cost, quantity_sold.
    """
    raise NotImplementedError


def classify(items: pd.DataFrame, popularity_threshold: float | None = None) -> pd.DataFrame:
    """Assign each item to a menu engineering quadrant.

    Popularity is compared within category, not across the whole menu. Desserts will never sell
    like entrees, and comparing them makes every dessert look like a dog.
    """
    raise NotImplementedError


def price_elasticity(items: pd.DataFrame, price_changes: pd.DataFrame) -> pd.DataFrame:
    """Estimate demand response to historical price changes, by item and daypart.

    Needs actual price variation to work. Without past price moves this returns nothing rather
    than a fabricated elasticity, which is the honest outcome.
    """
    raise NotImplementedError


def basket_affinity(check_items: pd.DataFrame, min_support: float = 0.01) -> pd.DataFrame:
    """Find items that sell together more often than chance would predict.

    Used for attachment strategy: which appetizer precedes a second round, which entree pairs with
    a high-margin bottle, which item shows up on the biggest checks.
    """
    raise NotImplementedError


def menu_mix_shift(items: pd.DataFrame, period_a: str, period_b: str) -> pd.DataFrame:
    """Compare menu mix between two periods to see whether a change moved guests toward margin.

    Useful after a menu redesign, a price move, or a server incentive push.
    """
    raise NotImplementedError
