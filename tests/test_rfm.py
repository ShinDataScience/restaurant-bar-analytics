"""Tests for RFM visit construction and scoring.

Written before the implementation on purpose. They encode the hospitality-specific behavior that
is easy to get wrong and easy to regress later.
"""

from __future__ import annotations

import pytest


@pytest.mark.xfail(reason="build_visits not implemented yet")
def test_checks_within_gap_collapse_into_one_visit():
    """A tab opened at the bar and a check opened at a table 90 minutes later is one visit."""
    raise NotImplementedError


@pytest.mark.xfail(reason="build_visits not implemented yet")
def test_late_night_check_belongs_to_previous_business_date():
    """A check opened at 1:40am Saturday belongs to Friday business."""
    raise NotImplementedError


@pytest.mark.xfail(reason="score_rfm not implemented yet")
def test_recency_measured_against_last_operating_day():
    """A venue closed Mondays should not show every guest gaining recency on a Monday."""
    raise NotImplementedError


@pytest.mark.xfail(reason="score_rfm not implemented yet")
def test_monetary_excludes_tax_and_tip():
    """Monetary value is net sales to the venue, not the total on the credit card slip."""
    raise NotImplementedError


@pytest.mark.xfail(reason="score_rfm not implemented yet")
def test_comped_checks_excluded_when_configured():
    """Manager comps and staff meals should not inflate a guest frequency score."""
    raise NotImplementedError


@pytest.mark.xfail(reason="label_segment not implemented yet")
def test_small_sample_degrades_gracefully():
    """With too few guests, segmentation should say so instead of inventing tiers."""
    raise NotImplementedError
