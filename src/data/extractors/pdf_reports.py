"""Optional addon: pull aggregate reports out of PDF.

Not imported anywhere by default, and deliberately not a dependency of aggregate_ingest. The core
ingestion path accepts CSV and Excel only, because PDF extraction fails quietly in exactly the ways
that corrupt a sales number. A wrapped item name becomes two rows. A negative in parentheses loses
its sign. A thousands separator turns 1,234 into 1. A two page report drops the page the totals
were printed on, and the result still looks like a perfectly reasonable week.

This addon exists anyway, because some venues genuinely cannot produce anything else. Usually the
POS reporting is locked to a printer, or the reports arrive as an emailed attachment from a manager
with no back office login. For those venues a flagged, low confidence number beats no number, as
long as nothing downstream is ever allowed to forget which one it is holding.

The contract with the rest of the pipeline:

* Output frames match the aggregate_ingest schemas exactly. Nothing downstream branches on PDF.
* Every extraction carries a confidence score, and lands in ReportFile.confidence below 1.0.
* Any figure that fails an internal arithmetic check is emitted as null with a reason attached,
  never as a best guess.
* Totals printed on the report are the source of truth and are used to check the line items, not
  the other way round.
* Nothing below MIN_CONFIDENCE_TO_ACCEPT reaches the canonical tables. It goes to a review queue.

Install the optional dependencies before using this module:

    pip install -r requirements-pdf.txt
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

# Layout families seen in the wild. Each POS prints its reports differently, and one template per
# family is far more reliable than a single clever general parser.
KNOWN_LAYOUTS = (
    "toast_sales_summary",
    "square_sales_summary",
    "clover_sales_summary",
    "lightspeed_sales_summary",
    "brink_sales_summary",
    "pixelpoint_sales_summary",
    "tabit_sales_summary",
    "generic_two_column",
)

# Extractions below this score never load automatically, whatever the deadline.
MIN_CONFIDENCE_TO_ACCEPT = 0.90

# A week on week swing larger than this in a headline total gets a human look even if the parse
# looked clean, because a confident parse of the wrong column is the failure mode that hurts.
REVIEW_SWING_THRESHOLD = 0.25

ISSUE_KINDS = (
    "wrapped_row",
    "sign_ambiguous",
    "separator_ambiguous",
    "missing_total",
    "column_drift",
    "page_dropped",
    "ocr_low_confidence",
)


@dataclass(frozen=True)
class ExtractionIssue:
    """One thing the parser is not sure about, kept rather than rounded away."""

    page: int
    field: str
    kind: str        # a value from ISSUE_KINDS
    raw_text: str
    resolved: bool = False


@dataclass
class ExtractionResult:
    """Frames plus everything needed to decide whether to believe them."""

    frame: pd.DataFrame
    report_type: str
    layout: str
    confidence: float
    page_count: int
    issues: list[ExtractionIssue] = field(default_factory=list)


def is_available() -> bool:
    """Report whether the optional PDF dependencies are installed, without raising on import.

    Callers check this rather than wrapping an import in a try block, so a missing extra reads as a
    disabled feature instead of a crash halfway through a nightly load.
    """
    raise NotImplementedError


def detect_layout(path: Path) -> str:
    """Identify which known layout a PDF matches, falling back to generic_two_column."""
    raise NotImplementedError


def extract(path: Path, report_type: str, layout: str | None = None) -> ExtractionResult:
    """Pull one report out of a text based PDF into the matching aggregate_ingest schema.

    Text based PDFs only. A scanned or photographed report needs extract_scanned, which is a
    separate call so that nobody runs OCR by accident and reads the output as a clean parse.
    """
    raise NotImplementedError


def extract_scanned(path: Path, report_type: str) -> ExtractionResult:
    """OCR path for scanned or photographed reports. Always returns reduced confidence."""
    raise NotImplementedError


def check_internal_arithmetic(result: ExtractionResult) -> ExtractionResult:
    """Verify the numbers against themselves before anything believes them.

    Line items must sum to the printed subtotal, subtotals to the printed total, and any category
    breakdown to the same net sales figure. Failures become issues and null the affected fields.
    """
    raise NotImplementedError


def to_report_file(result: ExtractionResult, venue_id: str, source: str):
    """Wrap an extraction as an aggregate_ingest.ReportFile with confidence carried through."""
    raise NotImplementedError


def review_queue(
    results: list[ExtractionResult],
    history: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """List the extractions a human needs to look at before the numbers are used anywhere.

    Anything under MIN_CONFIDENCE_TO_ACCEPT, anything with an unresolved arithmetic failure, and
    anything whose headline totals move more than REVIEW_SWING_THRESHOLD against the same report a
    week earlier.
    """
    raise NotImplementedError


def add_layout_template(name: str, spec: dict) -> None:
    """Register a new layout template so a venue with an unusual report can be supported.

    This is the intended extension point. Adding a POS to the core ingestion path is a schema
    question; adding one here is only ever a layout question, and the two should not be confused.
    """
    raise NotImplementedError
