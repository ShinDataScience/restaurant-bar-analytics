"""Aggregate report ingestion for venues without POS API access.

Most venues cannot hand over an API key. What they can do, on every POS in SUPPORTED_SOURCES, is
export or schedule a handful of canned reports: a daily sales summary, a product mix report, an
hourly sales report, a labor summary, and a discount and comp report. Those arrive as CSV or Excel,
aggregated to a period, with no check ids, no guest ids and no baskets.

This module is the second ingestion path. It does not force summary rows into the check level
schema in pos_ingest, because a fabricated check id is worse than an honest aggregate. It produces
its own coarser canonical tables instead, and capabilities.py decides which analyses are allowed to
run on top of them.

Canonical tables produced here:

* sales_daily       - one row per venue, business date and daypart, with covers, checks, net sales,
                      comps, discounts and estimated gross margin
* item_sales_period - one row per venue, period and item, from the product mix report
* labor_daily       - one row per venue, business date, daypart and role, with hours and cost

Three rules that save a lot of pain later:

1. Reports disagree. Product mix and the daily summary are pulled with different date boundaries
   more often than anyone expects, so reconcile() runs on every load and fails loudly rather than
   quietly publishing two versions of net sales.
2. Item cost never comes from the POS. It comes from a recipe costing sheet the operator supplies,
   and it is joined here, not invented.
3. Covers are not checks. If a report only gives check counts, covers stay null and every per
   person metric downstream is withheld rather than approximated.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

REPORT_TYPES = (
    "daily_sales_summary",
    "product_mix",
    "hourly_sales",
    "labor_summary",
    "discount_comp",
    "tender_summary",
)

# CSV and Excel only. PDF is handled by the optional extractors.pdf_reports addon, which returns
# the same frames with a confidence score attached and is never enabled by default.
SUPPORTED_FILE_FORMATS = (".csv", ".tsv", ".xlsx", ".xls")

# Half a percent of disagreement between two reports before a load is rejected.
RECONCILE_TOLERANCE = 0.005


@dataclass(frozen=True)
class ReportFile:
    """A single raw report drop, paired with the metadata note data/README.md requires."""

    path: Path
    source: str           # a value from pos_ingest.SUPPORTED_SOURCES
    report_type: str      # a value from REPORT_TYPES
    venue_id: str
    period_start: pd.Timestamp
    period_end: pd.Timestamp
    extracted_at: pd.Timestamp
    pulled_by: str
    confidence: float = 1.0   # below 1.0 only for machine extracted sources such as PDF


def discover_reports(root: Path) -> list[ReportFile]:
    """Scan data/raw for report drops and pair each file with its metadata note.

    Files without a metadata note are returned as errors rather than guessed at. Inferring the venue
    or the date range from a filename is how one venue's Tuesday ends up in another venue's week.
    """
    raise NotImplementedError


def load_report(report: ReportFile) -> pd.DataFrame:
    """Read one report into a frame without transforming it. Fails loudly on unknown types."""
    raise NotImplementedError


def normalize_sales_daily(raw: pd.DataFrame, report: ReportFile) -> pd.DataFrame:
    """Map a daily sales summary into the canonical sales_daily schema.

    Where the report is only available at day grain, daypart is null and the row is still usable for
    trend and forecasting at day level. Where an hourly sales report is present, split the day with
    dayparts_from_hourly first, since a daypart forecast is worth far more to a manager than a daily
    one.
    """
    raise NotImplementedError


def dayparts_from_hourly(hourly: pd.DataFrame, venue_id: str) -> pd.DataFrame:
    """Roll an hourly sales report into venue dayparts using that venue's daypart definitions."""
    raise NotImplementedError


def normalize_item_sales(raw: pd.DataFrame, report: ReportFile) -> pd.DataFrame:
    """Map a product mix report into the canonical item_sales_period schema.

    Product mix is the single most valuable report a venue can send without API access. It carries
    item, category, quantity and gross sales, which is enough for menu engineering, mix shift and
    elasticity once costs are attached.
    """
    raise NotImplementedError


def attach_item_costs(items: pd.DataFrame, costing_sheet: pd.DataFrame) -> pd.DataFrame:
    """Join operator supplied plate and pour costs onto item sales.

    Items with no cost are kept and flagged, never defaulted to a category average. A guessed cost
    turns straight into a guessed margin and then into a menu decision.
    """
    raise NotImplementedError


def normalize_labor_daily(raw: pd.DataFrame, report: ReportFile) -> pd.DataFrame:
    """Map a labor summary into the canonical labor_daily schema."""
    raise NotImplementedError


def reconcile(
    sales_daily: pd.DataFrame,
    item_sales: pd.DataFrame,
    tolerance: float = RECONCILE_TOLERANCE,
) -> dict:
    """Cross-check report totals against each other and report every disagreement.

    Compares product mix gross sales against the daily summary over the overlapping period, checks
    that the date ranges overlap at all, and looks for missing business dates inside a claimed
    range. A closed Monday and a dropped Monday look identical in a report, so the venue calendar
    decides which one it is.
    """
    raise NotImplementedError


def validate(df: pd.DataFrame, table: str) -> None:
    """Run schema and sanity checks on an aggregate table.

    Checks include: no duplicate venue and period rows, no negative net sales, covers never below
    check count, no periods in the future, and no silent overlap between two loads of the same
    report.
    """
    raise NotImplementedError
