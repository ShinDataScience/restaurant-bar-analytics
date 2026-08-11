"""Tests for aggregate report ingestion, reconciliation and capability gating.

Written before the implementation, like test_rfm.py. These encode the failures that make report
only ingestion dangerous, and every one of them is a real way a venue has been given a confident
wrong answer: two reports that disagree, a report that looks complete but quietly dropped a day,
a cost that was averaged in because it was missing, and an analysis that ran when it should have
refused.
"""

from __future__ import annotations

import pytest


@pytest.mark.xfail(reason="reconcile not implemented yet")
def test_product_mix_disagreeing_with_daily_summary_fails_the_load():
    """Two reports covering the same period must agree within tolerance or nothing loads."""
    raise NotImplementedError


@pytest.mark.xfail(reason="reconcile not implemented yet")
def test_non_overlapping_date_ranges_are_rejected_not_averaged():
    """A product mix pull for a different week is a mistake, not a data point."""
    raise NotImplementedError


@pytest.mark.xfail(reason="reconcile not implemented yet")
def test_missing_business_date_is_distinguished_from_a_closed_day():
    """A venue closed on Mondays is not the same as a report that dropped Monday."""
    raise NotImplementedError


@pytest.mark.xfail(reason="normalize_sales_daily not implemented yet")
def test_day_grain_report_leaves_daypart_null_instead_of_splitting_it():
    """Without an hourly report there is no honest way to divide a day into dayparts."""
    raise NotImplementedError


@pytest.mark.xfail(reason="normalize_sales_daily not implemented yet")
def test_covers_stay_null_when_the_report_only_gives_check_counts():
    """Per person average is withheld rather than approximated from check count."""
    raise NotImplementedError


@pytest.mark.xfail(reason="normalize_sales_daily not implemented yet")
def test_late_night_sales_land_on_the_previous_business_date():
    """The same 4am rule as pos_ingest, or the two paths will disagree about Friday."""
    raise NotImplementedError


@pytest.mark.xfail(reason="attach_item_costs not implemented yet")
def test_items_without_a_costed_recipe_are_flagged_not_defaulted():
    """A category average cost produces a category average lie about margin."""
    raise NotImplementedError


@pytest.mark.xfail(reason="validate not implemented yet")
def test_reloading_the_same_report_does_not_double_count():
    """A manager sending Monday twice must not turn into two Mondays of sales."""
    raise NotImplementedError


@pytest.mark.xfail(reason="detect_tier not implemented yet")
def test_checks_with_almost_no_guest_ids_are_treated_as_anonymous():
    """A guest_id column that is 99 percent null does not unlock guest analytics."""
    raise NotImplementedError


@pytest.mark.xfail(reason="require not implemented yet")
def test_rfm_refuses_to_run_on_aggregate_data():
    """The aggregate tier raises at the boundary instead of returning an empty segment table."""
    raise NotImplementedError


@pytest.mark.xfail(reason="assess not implemented yet")
def test_withheld_analysis_explains_itself_in_plain_language():
    """The reason has to tell an operator what to go and ask their POS provider for."""
    raise NotImplementedError


@pytest.mark.xfail(reason="assess not implemented yet")
def test_short_history_blocks_the_forecast_rather_than_widening_it():
    """Six weeks of data cannot see a season, and a very wide interval implies it can."""
    raise NotImplementedError


@pytest.mark.xfail(reason="pdf addon not implemented yet")
def test_low_confidence_pdf_extraction_never_auto_loads():
    """Anything under the threshold lands in the review queue, not the canonical tables."""
    raise NotImplementedError


@pytest.mark.xfail(reason="pdf addon not implemented yet")
def test_pdf_line_items_must_sum_to_the_printed_total():
    """The printed total is the check on the parse, not something the parse can overwrite."""
    raise NotImplementedError


@pytest.mark.xfail(reason="pdf addon not implemented yet")
def test_core_ingestion_works_with_pdf_dependencies_absent():
    """The addon is optional, so a missing extra is a disabled feature and never an import error."""
    raise NotImplementedError
