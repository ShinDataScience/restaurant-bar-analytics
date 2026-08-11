"""POS ingestion and normalization.

Every POS exports a slightly different shape of the same thing. Toast, Square, Clover,
Lightspeed, Brink, PixelPoint and Tabit all disagree about what a check is, where the tip
lives, whether voids appear as negative lines or as a status flag, and how modifiers are
attached to items.

The job of this module is to turn all of them into one canonical schema so nothing downstream
has to care which POS the venue uses.

Canonical tables produced here:

* checks        - one row per closed check, with venue, business date, daypart, channel, totals
* check_items   - one row per item sold, with category, modifiers, quantity, price, cost
* guests        - one row per identified guest, with hashed contact identifiers only
* venues        - venue metadata, including operating hours and daypart definitions

Two rules that save a lot of pain later:

1. Business date is not calendar date. A bar closing at 2am belongs to the previous business date,
   and getting this wrong shifts a meaningful chunk of late-night revenue to the wrong day.
2. Raw files are never edited in place. Corrections are new rows with a load timestamp.

Venues that cannot export check level data at all are handled by aggregate_ingest.py, which reads
canned reports into coarser tables. Summary rows are never routed through this module, because a
fabricated check id is worse than an honest aggregate.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

SUPPORTED_SOURCES = ("toast", "square", "clover", "lightspeed", "brink", "pixelpoint", "tabit", "generic_csv")


def load_raw(source: str, path: Path) -> pd.DataFrame:
    """Read a raw POS export without transforming it. Fails loudly on unknown sources."""
    raise NotImplementedError


def normalize_checks(raw: pd.DataFrame, source: str, venue_id: str) -> pd.DataFrame:
    """Map a POS-specific export into the canonical checks schema."""
    raise NotImplementedError


def normalize_items(raw: pd.DataFrame, source: str, venue_id: str) -> pd.DataFrame:
    """Map a POS-specific export into the canonical check_items schema."""
    raise NotImplementedError


def assign_business_date(timestamps: pd.Series, close_hour: int = 4) -> pd.Series:
    """Shift timestamps before the close hour back to the previous business date."""
    raise NotImplementedError


def assign_daypart(timestamps: pd.Series, venue_id: str) -> pd.Series:
    """Label each timestamp with the venue daypart: brunch, lunch, happy_hour, dinner, late_night.

    Dayparts are per venue. Happy hour at one place ends when dinner starts at another.
    """
    raise NotImplementedError


def validate(df: pd.DataFrame, table: str) -> None:
    """Run schema and sanity checks, raising on anything that would silently corrupt analysis.

    Checks include: no negative net sales on non-void checks, no checks without a venue, no
    duplicate check ids, and no business dates in the future.
    """
    raise NotImplementedError
