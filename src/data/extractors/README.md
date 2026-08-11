# Extractors

Optional addons that turn awkward source formats into the frames `src/data/aggregate_ingest.py`
already understands. Nothing in here is imported by the core ingestion path, nothing in here is
installed by `requirements.txt`, and nothing in here is allowed to widen a schema.

## Why this is separate

The core path accepts CSV and Excel. That is a deliberate limit, not an oversight. Anything that
guesses at structure belongs behind a boundary, with its own dependencies, its own confidence
score, and its own review queue, so that a parsing decision can never quietly become a reported
number.

## Rules for anything added here

An extractor returns frames that match an existing `aggregate_ingest` schema exactly. If a new
source needs a new column, that is a change to the canonical schema and it happens there, in the
open, not as a side effect of adding a parser.

Every extractor reports a confidence score, and that score travels with the data as
`ReportFile.confidence`. Anything below the module threshold lands in a review queue instead of
the canonical tables.

Uncertain values are emitted as null with a reason attached. No extractor is permitted to fall back
to a best guess, an interpolation, or a category average, because the whole point of the boundary is
that a weak number stays visibly weak.

Optional dependencies live in their own requirements file, and each module exposes `is_available()`
so a missing extra reads as a disabled feature rather than a crash in a nightly job.

## Current addons

`pdf_reports.py` extracts daily sales summaries, product mix and labor reports from PDF, with a
template per POS layout family, an arithmetic self-check against the printed totals, and a separate
opt-in OCR path for scanned or photographed reports. Install with:

```
pip install -r requirements-pdf.txt
```

## Likely next ones

Emailed report attachments pulled straight from a mailbox, spreadsheet exports where a manager has
added their own header rows and totals, and the printer spool capture some older PixelPoint and
Brink installations are limited to.
